class AddressAlreadyInUse(Exception):
    """Address is already used by other service."""


class OIIInspectorError(Exception):
    """An error was encountered in OIIInspector"""


class MissingContainerPlatform(Exception):
    """Docker nor Podman is not present at the current platform"""


class NoFreePortFound(Exception):
    """All available ports are already taken"""
