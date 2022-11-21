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
        url="",  # REPLACE
        scheme="https",
    )
    token: SecretStr = Field(
        name="Personal Access Token",
        default=None,
        description="A BitBucket Personal Access Token.",
    )
    username: str = None

    @validator("username")
    def _validate_username_characters(cls, value: str) -> str:
        """Validators are by default only called on provided arguments."""
        pattern = "^[A-Za-z0-9_-]*$"
        assert bool(
            re.match(pattern, value)
        ), "username must be alpha, num, dash and/or underscore only"
        assert len(value) <= 30, "username cannot be longer than 30 chars"
        return value
