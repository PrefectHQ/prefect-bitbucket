"""Module to enable authenticate interactions with BitBucket"""
import re

from prefect.blocks.core import Block
from pydantic import Field, HttpUrl, SecretStr, validator


class BitBucketCredentials(Block):
    """
    Store a BitBucket access token to interact with private BitBucket
    repositories.

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
    _logo_url = HttpUrl(
        url="https://banner2.cleanpng.com/20180320/gcq/kisspng-symbol-font-bitbucket-5ab0b6a9021793.8467511015215305370086.jpg",  # noqa
        scheme="https",
    )
    token: SecretStr = Field(
        name="Personal Access Token",
        default=None,
        description="A BitBucket Personal Access Token.",
    )
    username: str = None

    @validator("username")
    def _validate_username(cls, value: str) -> str:
        """Validators are by default only called on provided arguments."""
        pattern = "^[A-Za-z0-9_-]*$"

        if not re.match(pattern, value):
            raise ValueError(
                "Username must be alpha, num, dash and/or underscore only."
            )
        if not len(value) <= 30:
            raise ValueError("Username cannot be longer than 30 chars.")
        return value
