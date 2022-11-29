import pytest
from prefect.blocks.core import Block

from prefect_bitbucket.credentials import BitBucketCredentials


@pytest.mark.parametrize("token", [None, "token_value"])
def test_bitbucket_credentials(token):
    """Test credentials is Block type."""
    credentials_block = BitBucketCredentials(token=token)
    assert isinstance(credentials_block, Block)


def test_bitbucket_username_invalid_char():
    """Ensure invalid char username raises."""
    with pytest.raises(ValueError):
        BitBucketCredentials(token="token", username="invalid!username")


def test_bitbucket_username_over_max_length():
    """Ensure username of greater than max allowed length raises."""
    with pytest.raises(ValueError):
        BitBucketCredentials(
            token="token", username="usernamethatisoverthirtycharacters"
        )
