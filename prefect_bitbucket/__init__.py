from . import _version
from .credentials import BitBucketCredentials  # noqa

__version__ = _version.get_versions()["version"]
__all__ = ["BitBucketCredentials"]
