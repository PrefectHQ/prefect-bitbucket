"""Module to enable authenticate interactions with BitBucket."""
import re
import warnings
from enum import Enum
from typing import Optional, Union

from prefect.blocks.abstract import CredentialsBlock
from pydantic import Field, SecretStr, validator

try:
    from atlassian.bitbucket import Bitbucket, Cloud
except ImportError:
    pass


class ClientType(Enum):
    """The client type to use."""

    LOCAL = "local"
    CLOUD = "cloud"


class BitBucketCredentials(CredentialsBlock):
    """Store BitBucket credentials to interact with private BitBucket repositories.

    Attributes:
        token: An access token to authenticate with BitBucket. This is required
            for accessing private repositories.
        username: Identification name unique across entire BitBucket site.
        password: The password to authenticate to BitBucket.
        url: The base URL of your BitBucket instance.


    Examples:
        Load stored BitBucket credentials:
        ```python
        from prefect_bitbucket import BitBucketCredentials
        bitbucket_credentials_block = BitBucketCredentials.load("BLOCK_NAME")
        ```


    """

    _block_type_name = "BitBucket Credentials"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/27LMR24ewTSDW238Lks1vH/34c5028659f4007528feadc8db8cecbd/500px-Bitbucket-blue-logomark-only.svg.png?h=250"  # noqa
    token: Optional[SecretStr] = Field(
        name="Personal Access Token",
        default=None,
        description=(
            "A BitBucket Personal Access Token - required for private repositories."
        ),
        example="x-token-auth:my-token",

    )
    username: Optional[str] = Field(
        default=None,
        description="Identification name unique across entire BitBucket site.",
    )
    password: Optional[SecretStr] = Field(
        default=None, description="The password to authenticate to BitBucket."
    )
    url: str = Field(
        default="https://api.bitbucket.org/",
        description="The base URL of your BitBucket instance.",
        title="URL",
    )

    @validator("username")
    def _validate_username(cls, value: str) -> str:
        """When username provided, will validate it."""
        pattern = "^[A-Za-z0-9_-]*$"

        if not re.match(pattern, value):
            raise ValueError(
                "Username must be alpha, num, dash and/or underscore only."
            )
        if not len(value) <= 30:
            raise ValueError("Username cannot be longer than 30 chars.")
        return value

    @validator("token", pre=True, always=True)
    def _validate_token(cls, value: Optional[SecretStr]) -> Optional[SecretStr]:
        """Warns if the token is not prefixed with 'x-token-auth:'."""
        if value:
            secret_value = (
                value.get_secret_value() if isinstance(value, SecretStr) else value
            )
            if not secret_value.startswith("x-token-auth:"):
                warnings.warn(
                    "For use in git operations such as Prefect deployment steps, the token must be prefixed with 'x-token-auth:'."
                    " You can do this by setting the token to 'x-token-auth:<my-token>'.",
                    UserWarning,
                )
        return value

    def get_client(
        self, client_type: Union[str, ClientType], **client_kwargs
    ) -> Union[Cloud, Bitbucket]:
        """Get an authenticated local or cloud Bitbucket client.

        Args:
            client_type: Whether to use a local or cloud client.

        Returns:
            An authenticated Bitbucket client.

        """
        # ref: https://atlassian-python-api.readthedocs.io/
        if isinstance(client_type, str):
            client_type = ClientType(client_type.lower())

        password = self.password.get_secret_value()
        input_client_kwargs = dict(
            url=self.url, username=self.username, password=password
        )
        input_client_kwargs.update(**client_kwargs)

        if client_type == ClientType.CLOUD:
            client = Cloud(**input_client_kwargs)
        else:
            client = Bitbucket(**input_client_kwargs)
        return client
