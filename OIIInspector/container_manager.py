import logging
from retry import retry
import subprocess
import time
import shlex
import OIIInspector.exceptions as exceptions
from OIIInspector.utils import run_cmd

log = logging.getLogger(__name__)


class ContainerManager:
    """
    Class used as context manager for container operations.
    """
    _grpc_start_port = 50051
    _grpc_max_port_tries = 100
    _grpc_init_wait_time = 3
    _base_container_name = "OIIInspector_running_container"

    @property
    def local_address_of_image(self):
        return self._get_local_address_of_image()

    def __init__(self, image_address):
        """
        Initialize the ContainerManager

        :param image_address: address of the image, to which queries will be done
        :type image_address: str
        """
        self._port = self._grpc_start_port
        self._rpc_proc = None
        self._image_address = image_address
        self._container_platform = None
        self._container_running = False
        self._container_pulled = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close_container_manager()

    def start_container(self):
        """
        Start desired container at first available port
        in range _grpc_start_port : _grpc_start_port + _grpc_max_port_tries
        """
        # pull is done separately, instead of running just {platform} run command (which can pull image too),
        # because of better container control
        if self._container_running is True:
            return
        if self._container_platform is None:
            self._get_container_platform()
        if self._container_pulled is False:
            self._pull_image()
            self._container_pulled = True
        self._port, self._rpc_proc = self._serve_index_registry()
        self._container_running = True

    def _get_local_address_of_image(self) -> str:
        """
        Get local address of the running image

        :return: Returns local address where image is running in format localhost:PORT
        :rtype: str
        """
        if self._container_running is False:
            raise (exceptions.OIIInspectorError("Image is not running"))
        return f"localhost:{self._port}"

    def close_container_manager(self):
        """
        Close running container and remove used image
        """
        if self._container_running is True:
            self._rpc_proc.kill()
            self._stop_container()
            self._container_running = False
        if self._container_pulled is True:
            self._remove_container()
            self._container_pulled = False

    def _get_container_platform(self):
        """
        Search for available container platform
        """
        if self._container_platform is None:
            docker_terminal_result = run_cmd("command -v docker")
            podman_terminal_result = run_cmd("command -v podman")
            if "/podman" in podman_terminal_result:
                self._container_platform = "podman"
            elif "/docker" in docker_terminal_result:
                self._container_platform = "docker"
            else:
                raise exceptions.OIIInspectorError("Docker or Podman is needed to be installed on the platform")

    def _stop_container(self, tolerate_err=False):
        """
        Stop running container using available container platform

        :param tolerate_err: Parameter for set up handling of the exceptions
        :type tolerate_err: bool
        """
        run_cmd(f"{self._container_platform} stop {self._base_container_name}_{self._port}", tolerate_err=tolerate_err)

    def _remove_container(self, tolerate_err=False):
        """
        Remove container using available container platform

        :param tolerate_err: Parameter for set up handling of the exceptions
        :type tolerate_err: bool
        """
        run_cmd(f"{self._container_platform} rm {self._base_container_name}_{self._port}", tolerate_err=tolerate_err)

    def _pull_image(self):
        """
        Pull the image with available container platform
        """
        run_cmd(f"{self._container_platform} pull {self._image_address}")

    def _serve_index_registry(self):
        """
        Locally start podman/docker image service, which can be communicated with using gRPC queries.
        Resolution of port conflicts is handled in this function.

        :return: tuple containing port number of the running service and the running Popen object.
        :rtype: (int, Popen)
        :raises OIIInspectorError: if all tried ports are in use, or the command failed for another reason.
        """
        port_start = self._grpc_start_port
        port_end = port_start + self._grpc_max_port_tries

        for port in range(port_start, port_end):
            try:
                return (
                    port,
                    self._serve_index_registry_at_port(
                        port, self._grpc_init_wait_time),
                )
            except exceptions.AddressAlreadyInUse:
                log.info('Port %d is in use, trying another.', port)

        err_msg = f"No free port has been found after {self._grpc_max_port_tries} attempts."
        raise exceptions.NoFreePortFound(err_msg)

    @retry(exceptions=exceptions.OIIInspectorError, tries=2, logger=log)
    def _serve_index_registry_at_port(self, port, wait_time):
        """
        Start an image registry service at a specified port.

        :param str int port: port to start the service on.
        :param wait_time: time to wait before checking if the service is initialized.
        :return: object of the running Popen process.
        :rtype: Popen
        :raises OIIInspectorError: if the process has failed to initialize too many times, or an unexpected
        error occurred.
        :raises AddressAlreadyInUse: if the specified port is already being used by another service.
        """
        cmd = f"{self._container_platform} run --name={self._base_container_name}_{port} " \
              f"-p={port}:{port} {self._image_address}"

        rpc_proc = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        start_time = time.time()
        while time.time() - start_time < wait_time:
            time.sleep(1)
            ret = rpc_proc.poll()
            # process has terminated
            if ret is not None:
                stderr = rpc_proc.stderr.read()
                if "address already in use" in stderr:
                    raise exceptions.AddressAlreadyInUse(
                        f"Port {port} is already used by a different service")
                elif "the container name" in stderr and "is already in use by" in stderr:
                    raise exceptions.AddressAlreadyInUse(
                        f"Port {port} is already used by service with name: {self._base_container_name}_{port}")
                else:
                    raise exceptions.OIIInspectorError(f"Command {cmd} has failed with error {stderr}"
                                                       .format(cmd="".join(cmd), stderr=stderr))

            # query the service to see if it has started
            try:
                output = run_cmd(f"grpcurl -plaintext localhost:{port} list api.Registry")
            except RuntimeError:
                output = ''

            if "api.Registry.ListBundles" in output or "api.Registry.ListPackages" in output:
                log.debug("Started the command {cmd}".format(cmd="".join(cmd)))
                log.info("Index registry service has been initialized.")
                return rpc_proc

        rpc_proc.kill()
        raise exceptions.OIIInspectorError("Index registry has not been initialized")
