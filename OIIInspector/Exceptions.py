class BaseException(Exception):
    """The base class for all OIIInspector exceptions."""


class AddressAlreadyInUse(BaseException):
    """Adress is already used by other service."""


class OIIInspectorError(BaseException):
    """An error was encountered in OIIInspector"""


class MissingContainerPlatform(BaseException):
    """Docker nor Podman is not present at the current platform"""
