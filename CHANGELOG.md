# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Adds a `UserWarning` to notify user of possibly invalid token field in `BitBucketCredentials` - [#22](https://github.com/PrefectHQ/prefect-bitbucket/pull/22/)

- Adds placeholder text to the `BitBucketCredentials` block description for the Prefect UI - [#22](https://github.com/PrefectHQ/prefect-bitbucket/pull/22/)
- Adds `filterwarnings` section to the `setup.cfg` - [#22](https://github.com/PrefectHQ/prefect-bitbucket/pull/22/)

### Changed

### Deprecated

### Removed
- Removes reference to registering the `prefect-bitbucket`` blocks to view them in the UI, as they should already be there by default - [#22](https://github.com/PrefectHQ/prefect-bitbucket/pull/22/)
### Fixed
- Treatment of `BitBucketCredentials` token when using `BitBucketRepository` to access private repos - [#16](https://github.com/PrefectHQ/prefect-bitbucket/pull/16/)

### Security

## 0.1.1

Released on February 16th, 2023.

### Added
- `get_client` method and `url` field in `BitbucketCredentials` - [#7](https://github.com/PrefectHQ/prefect-bitbucket/pull/7/)
- support to log into Bitbucket Server with `token` and `username` - [#11](https://github.com/PrefectHQ/prefect-bitbucket/pull/11/)

## 0.1.0

Released on December 6th, 2022.

### Added
- `BitBucketCredentials` block - [#3](https://github.com/PrefectHQ/prefect-bitbucket/pull/3/)
- `BitBucketRepository` block - [#5](https://github.com/PrefectHQ/prefect-bitbucket/pull/5/)
