import pytest
from prefect.blocks.core import Block

from prefect_bitbucket import BitBucketCredentials


@pytest.mark.parametrize("token", [None, "token_value"])
def test_bitbucket_credentials_get_endpoint(token):
    credentials_block = BitBucketCredentials(token=token)
    assert isinstance(credentials_block, Block)
