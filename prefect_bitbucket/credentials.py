"""Module to enable authenticate interactions with BitBucket."""
import re
from typing import Optional

from prefect.blocks.core import Block
from pydantic import Field, SecretStr, validator


class BitBucketCredentials(Block):
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
