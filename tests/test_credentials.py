import pytest
from prefect.blocks.core import Block

from prefect_bitbucket.credentials import BitBucketCredentials


@pytest.mark.parametrize("token", [None, "token_value"])
def test_bitbucket_credentials_get_endpoint(token):
    credentials_block = BitBucketCredentials(token=token)
    assert isinstance(credentials_block, Block)


def test_bitbucket_username_invalid_char():
    with pytest.raises(ValueError):
        BitBucketCredentials(token="token", username="invalid!username")


def test_bitbucket_username_over_max_length():
    with pytest.raises(ValueError):
        BitBucketCredentials(
            token="token", username="usernamethatisoverthirtycharacters"
        )
