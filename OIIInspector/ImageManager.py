import logging
from retry import retry
import subprocess
import time
import shlex
from contextlib import suppress
from OIIInspector.Exceptions import AddressAlreadyInUse, OIIInspectorError
from OIIInspector.utils import run_cmd

log = logging.getLogger(__name__)


class ImageManager:
    _grpc_start_port = 50051
    _grpc_max_port_tries = 100
    _grpc_max_tries = 5
    _grpc_init_wait_time = 1000
    _base_container_name = "OIIInspector_running_image"

    def __init__(self):
        self._container_platform = self._get_container_platform()
        self._image_address = None
        self._port = self._grpc_start_port
        self._rpc_proc = None

    def start_image(self, image_address):
        self._image_address = image_address
        self._remove_old_image_if_exists()
        if self._check_if_image_already_runs() is False:
            self._pull_image()
            self._port, self._rpc_proc = self._serve_index_registry()
        else:  # pragma: no cover"
            pass

    def get_local_address_of_image(self):
        return "localhost:{port}".format(port=self._port)

    def close_image_manager(self):
        self._stop_image_registry()
        self._rpc_proc.kill()
        self._remove_image_registry()

    def _get_container_platform(self):
        docker_terminal_result = run_cmd("command -v docker")
        podman_terminal_result = run_cmd("command -v podman")
        if "/podman" in podman_terminal_result:
            return "podman"
        elif "/docker" in docker_terminal_result:
            return "docker"
        else:
            raise OIIInspectorError("Docker or Podman is needed to be installed on the platform")

    def _remove_old_image_if_exists(self):
        with suppress(Exception):
            self._stop_image_registry(tolerate_err=True)
        with suppress(RuntimeError):
            self._remove_image_registry(tolerate_err=True)

    def _stop_image_registry(self, tolerate_err=False):
        run_cmd(f"{self._container_platform} stop {self._base_container_name}_{self._port}", tolerate_err=tolerate_err)

    def _remove_image_registry(self, tolerate_err):
        run_cmd(f"{self._container_platform} rm {self._base_container_name}_{self._port}", tolerate_err=tolerate_err)

    def _check_if_image_already_runs(self):
        return False

    def _pull_image(self):
        """
        Pull needs to be done separately, because run can be interrupted with timer later (while running podman run).
        """
        run_cmd(f"{self._container_platform} pull {self._image_address}")
        pass

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
                        port, self._grpc_max_tries, self._grpc_init_wait_time),
                )
            except AddressAlreadyInUse:
                log.info('Port %d is in use, trying another.', port)

        err_msg = "No free port has been found after {number_of_ports} attempts.".format(
            number_of_ports=self._grpc_max_port_tries)
        log.error(err_msg)
        raise Exception(err_msg)


    @retry(exceptions=OIIInspectorError, tries=1, logger=log)
    def _serve_index_registry_at_port(self, port, max_tries, wait_time):
        """
        Start an image registry service at a specified port.
        :param str db_path: path to index database containing the registry data.
        :param str int port: port to start the service on.
        :param max_tries: how many times to try to start the service before giving up.
        :param wait_time: time to wait before checking if the service is initialized.
        :return: object of the running Popen process.
        :rtype: Popen
        :raises IIBError: if the process has failed to initialize too many times, or an unexpected
        error occured.
        :raises AddressAlreadyInUse: if the specified port is already being used by another service.
        """
        cmd = f"{self._container_platform} run --name={self._base_container_name}_{port} -p={port}:{port} {self._image_address}"
        for attempt in range(max_tries):

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
                       raise AddressAlreadyInUse("Port {port} is already used by a different service".format(port=port))
                   raise OIIInspectorError("Command {cmd} has failed with error {stderr}"
                                           .format(cmd="".join(cmd), stderr=stderr))

               # query the service to see if it has started
                try:
                    output = run_cmd("grpcurl -plaintext localhost:{port} list api.Registry".format(port=port))
                except OIIInspectorError:
                    output = ''

                if "api.Registry.ListBundles" in output or "api.Registry.ListPackages" in output:
                    log.debug("Started the command {cmd}".format(cmd="".join(cmd)))
                    log.info("Index registry service has been initialized.")
                    return rpc_proc

            rpc_proc.kill()

        raise OIIInspectorError("Index registry has not been initialized after {max_tries} tries"
                            .format(max_tries=max_tries))
