# prefect-bitbucket

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-bitbucket/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-bitbucket?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/PrefectHQ/prefect-bitbucket/" alt="Stars">
        <img src="https://img.shields.io/github/stars/PrefectHQ/prefect-bitbucket?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-bitbucket/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-bitbucket?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/PrefectHQ/prefect-bitbucket/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/PrefectHQ/prefect-bitbucket?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>


## Welcome!

Prefect integrations for working with Bitbucket repositories.

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-bitbucket` with `pip`:

```bash
pip install prefect-bitbucket
```

Then, register to [view the block](https://orion-docs.prefect.io/ui/blocks/) on Prefect Cloud:

```bash
prefect block register -m prefect_bitbucket.credentials
```

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).

### Write and run a flow
#### Load a pre-existing BitBucketCredentials block.

```python
from prefect import flow
from prefect_bitbucket.credentials import BitBucketCredentials

@flow
def use_stored_bitbucket_creds_flow():
    bitbucket_credentials_block = BitBucketCredentials.load("BLOCK_NAME")

    return bitbucket_credentials_block

use_stored_bitbucket_creds_flow()
```

#### Create a new BitBucketCredentials block in a flow.

```python
from prefect import flow
from prefect_bitbucket.credentials import BitBucketCredentials

@flow
def create_new_bitbucket_creds_flow():
    bitbucket_credentials_block = BitBucketCredentials(
        token="my-token",
        username="my-username"
    )

create_new_bitbucket_creds_flow()
```

## Resources

If you encounter any bugs while using `prefect-bitbucket`, feel free to open an issue in the [prefect-bitbucket](https://github.com/PrefectHQ/prefect-bitbucket) repository.

If you have any questions or issues while using `prefect-bitbucket`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

Feel free to ⭐️ or watch [`prefect-bitbucket`](https://github.com/PrefectHQ/prefect-bitbucket) for updates too!

## Development

If you'd like to install a version of `prefect-bitbucket` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-bitbucket.git

cd prefect-bitbucket/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
