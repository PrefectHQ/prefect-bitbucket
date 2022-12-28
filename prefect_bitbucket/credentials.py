"""Module to enable authenticate interactions with BitBucket."""
import re
from typing import Optional, Union
from enum import Enum

from prefect.blocks.abstract import CredentialsBlock
from prefect.blocks.core import Block
from pydantic import Field, SecretStr, validator
try:
    from atlassian.bitbucket import Bitbucket, Cloud
except ImportError:
    pass

class ClientType(Enum):
    LOCAL = "local"
    CLOUD = "cloud"

class BitBucketCredentials(CredentialsBlock):
    """Store BitBucket credentials to interact with private BitBucket repositories.

    Attributes:
        token: An access token to authenticate with BitBucket.
        username: Identification name unique across entire BitBucket site.


    Examples:
        Load stored BitBucket credentials:
        ```python
        from prefect_bitbucket import BitBucketCredentials
        bitbucket_credentials_block = BitBucketCredentials.load("BLOCK_NAME")
        ```


    """

    _block_type_name = "BitBucket Credentials"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/27LMR24ewTSDW238Lks1vH/34c5028659f4007528feadc8db8cecbd/500px-Bitbucket-blue-logomark-only.svg.png?h=250"  # noqa
    token: SecretStr = Field(
        name="Personal Access Token",
        default=None,
        description="A BitBucket Personal Access Token.",
    )
    username: Optional[str] = Field(
        default=None,
        description="Identification name unique across entire BitBucket site.",
    )
    password: Optional[str] = Field(
        default=None,
        description="The password to authenticate to BitBucket."
    )
    url: Optional[str] = Field(
        default=None,
        description="The base url used for the cloud / local client",
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

    def get_client(self, client_type: Union[str, ClientType]) -> Union[Cloud, Bitbucket]:
        """
        Get an authenticated local or cloud Bitbucket client.

        Args:
            client_type: Whether to use a local or cloud client.

        Returns:
            An authenticated Bitbucket client.
        """
        # ref: https://atlassian-python-api.readthedocs.io/
        if isinstance(client_type, str):
            client_type = ClientType(client_type.lower())
        client_kwargs = dict(url=self.url, username=self.username, password=self.password)
        if client_type == ClientType.CLOUD:
            client = Cloud(cloud=True, **client_kwargs)
        else:
            client = Bitbucket(**client_kwargs)
        return client