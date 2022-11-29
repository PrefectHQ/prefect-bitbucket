"""Allows for interaction with a BitBucket repository."""
import io
from distutils.dir_util import copy_tree
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Tuple, Union
from urllib.parse import urlparse, urlunparse

from prefect.exceptions import InvalidRepositoryUrlError
from prefect.filesystems import ReadableDeploymentStorage
from prefect.utilities.asyncutils import sync_compatible
from prefect.utilities.processutils import run_process
from pydantic import Field, HttpUrl, validator

from prefect_bitbucket.credentials import BitBucketCredentials


class BitBucketRepository(ReadableDeploymentStorage):
    """
    Interact with files stored in BitBucket repositories.

    An accessible installation of git is required for this block to function
    properly.
    """
    
    _block_type_name = "BitBucket Repository"
    _logo_url = HttpUrl(
        url="",
        scheme="https",
    )
    _description = "Interact with files stored in BitBucket repositories."

    repository: str = Field(
        default=...,
        description=(
            'The URL of a BitBucket repository to read from in HTTPS format'
        ),
    )
    reference: Optional[str] = Field(
        default=None,
        description=("An optional reference to pin to; can be a branch or tag."
        ),
    )
    credentials: Optional[BitBucketCredentials] = Field(
        default=None,
        description=(
            "An optional BitBucket Credentials block for authenticating with "
        "private BitBucket repos.",
        )
    )

    @validator("credentials")
    def _ensure_credentials_go_with_https(cls, v: str, values: dict) -> str:
        """Ensure that credentials are not provided with 'SSH' formatted BitBucket URLs.
        Note: validates `access_token` specifically so that it only fires when private
        repositories are used.
        """

        if v is not None:
            if urlparse(values["repository"]).scheme != "https":
                raise InvalidRepositoryUrlError(
                    (
                        "Credentials can only be used with BitBucket repositories "
                        "using the 'HTTPS' format. You must either remove the "
                        "credential if you wish to use the 'SSH' format and are not "
                        "using a private repository, or you must change the repository "
                        "URL to the 'HTTPS' format."
                    )
                )

        return v

    def _create_repo_url(self) -> str:
        """Format the URL provided to the `git clone` command.
        For private repos: https://x-token-auth:<access-token>@bitbucket.org/<user>/<repo>.git
        All other repos should be the same as `self.repository`.
        """
        url_components = urlparse(self.repository)
        if url_components.scheme == "https" and self.credentials is not None:
            token = self.credentials.token.get_secret_value()
            updated_components = url_components._replace(
                netloc=f"x-token-auth:{token}@{url_components.netloc}"
            )
            full_url = urlunparse(updated_components)
        else:
            full_url = self.repository
        
        return full_url

    @staticmethod
    def _get_paths(
        dst_dir: Union[str, None], src_dir: str, sub_directory: Optional[str]
    ) -> Tuple[str, str]:
        """Returns the fully formed paths for BitBucketRepository contents in the form
        (content_source, content_destination).
        """
        if dst_dir is None:
            content_destination = Path(".").absolute()
        else:
            content_destination = Path(dst_dir)
        
        content_source = Path(src_dir)

        if sub_directory:
            content_destination = content_destination.joinpath(sub_directory)
            content_source = content_source.joinpath(sub_directory)

        return str(content_source), str(content_destination)

    @sync_compatible
    async def get_directory(
        self, from_path: Optional[str] = None, local_path: Optional[str] = None
    ) -> None:
        """
        Clones a BitBucket project specified in `from_path` to the provided `local_path`;
        defaults to cloning the repository reference configured on the Block to the
        present working directory.
        
        Args:
            from_path: If provided, interpreted as a subdirectory of the underlying
                repository that will be copied to the provided local path.
            local_path: A local path to clone to; defaults to present working directory.
        """
        # Construct command
        cmd = ["git", "clone", self._create_repo_url()]
        if self.reference:
            cmd += ["-b", self.reference]
        
        # Limit git history
        cmd += ["--depth", "1"]

        # Clone to a temporary directory and move the subdirectory over
        with TemporaryDirectory(suffix="prefect") as tmp_dir:
            cmd.append(tmp_dir)

            err_stream = io.StringIO()
            out_stream = io.StringIO()
            process = await run_process(cmd, stream_ouput=(out_stream, err_stream))
            if process.returncode != 0:
                err_stream.seek(0)
                raise OSError(f"Failed to pull from remote:\n {err_stream.read()}")

            content_source, content_destination = self._get_paths(
                dst_dir=local_path, src_dir=tmp_dir, sub_directory=from_path
            )

            copy_tree(src=content_source, dst=content_destination)