from unittest import mock
from unittest.mock import patch, call
import OIIInspector.container_manager as container_manager
import pytest
import OIIInspector.exceptions as exceptions
import retry.api


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "pull-result", "api.Registry.ListPackages", "stop-result", "remove-result",
                    "/usr/bin/docker", "", "pull-result", "api.Registry.ListPackages", "stop-result", "remove-result"])
def test_platform_check(mock_run_cmd, mock_subprocess, ):
    mock_subprocess.Popen.return_value.poll.return_value = None
    with container_manager.ContainerManager("test") as image_manager_instance:
        image_manager_instance.start_container()
    assert call("command -v podman") in mock_run_cmd.call_args_list
    assert call("command -v docker") in mock_run_cmd.call_args_list
    assert image_manager_instance._container_platform == "podman"

    with container_manager.ContainerManager("test") as image_manager_instance:
        image_manager_instance.start_container()
    assert call("command -v podman") in mock_run_cmd.call_args_list
    assert call("command -v docker") in mock_run_cmd.call_args_list
    assert image_manager_instance._container_platform == "docker"


@patch("OIIInspector.container_manager.run_cmd")
def test_platform_missing(mock_run_cmd):
    mock_run_cmd.return_value = ""
    with pytest.raises(exceptions.OIIInspectorError):
        container_manager.ContainerManager("test").start_container()
    assert mock_run_cmd.call_count == 2
    assert call("command -v podman") in mock_run_cmd.call_args_list
    assert call("command -v docker") in mock_run_cmd.call_args_list


@patch("OIIInspector.container_manager.run_cmd")
def test_address_setup(mock_run_cmd):
    mock_run_cmd.return_value = "/usr/bin/podman"
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        assert image_manager_instance._image_address == "test_address"


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", ""])
def test_container_commands(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.return_value = None
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert call("podman pull test_address") in mock_run_cmd.call_args_list
        assert ["podman", "run", "--name=OIIInspector_running_container_50051", "-p=50051:50051", "test_address"] \
               == mock_subprocess.Popen.call_args.args[0]
    assert call(f"podman stop {image_manager_instance._base_container_name}_{image_manager_instance._port}",
                tolerate_err=False) in mock_run_cmd.call_args_list
    assert call(f"podman rm {image_manager_instance._base_container_name}_{image_manager_instance._port}",
                tolerate_err=False) in mock_run_cmd.call_args_list


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd", side_effect=["", "/usr/bin/podman", "", "", "", "", ""])
def test_get_address_before_running(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.return_value = None
    with pytest.raises(exceptions.OIIInspectorError):
        with container_manager.ContainerManager("test") as image_manager_instance:
            image_manager_instance.get_local_address_of_image()
    # This _image_is_running variable is set to True only if container is running
    image_manager_instance.container_status = True
    assert image_manager_instance.get_local_address_of_image() == "localhost:50051"


@patch("OIIInspector.container_manager.time")
@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", ""])
def test_time_out(mock_run_cmd, mock_subprocess, mock_time):
    mock_subprocess.Popen.return_value.poll.return_value = None
    mock_time.time.side_effect = [5, 11]

    # suspending retry functioning, also suspends catching the OIIInspectorError exception
    with mock.patch.object(retry.api, "__retry_internal", lambda f, *args: f()):
        with pytest.raises(exceptions.OIIInspectorError):
            with container_manager.ContainerManager("test_address") as image_manager_instance:
                image_manager_instance.start_container()
    mock_subprocess.Popen.return_value.kill.assert_called_once()


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       return_value="/usr/bin/podman")
def test_retry_called_twice(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.return_value = None
    with pytest.raises(exceptions.OIIInspectorError):
        with container_manager.ContainerManager("test_address") as image_manager_instance:
            image_manager_instance.start_container()
    # other ports are not used, as exception will get trough try block in _serve_index_registry
    assert mock_subprocess.Popen.return_value.kill.call_count == 2


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", ""])
def test_address_already_in_use_and_next_port_used(mock_run_cmd, mock_subprocess):
    # only two return values are needed, as the retry decorator will not be applied due to thrown exception
    mock_subprocess.Popen.return_value.poll.side_effect = ["terminated", None]
    mock_subprocess.Popen.return_value.stderr.read.return_value = "address already in use"
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert image_manager_instance._port == image_manager_instance._grpc_start_port + 1


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", ""])
def test_exception_address_used(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.side_effect = ["terminated", None]
    mock_subprocess.Popen.return_value.stderr.read.return_value = "address already in use"
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert mock_subprocess.Popen.return_value.poll.call_count == 2


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", ""])
def test_exception_name_in_use(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.side_effect = ["terminated", None]
    mock_subprocess.Popen.return_value.stderr.read.return_value = "the container name test_ is already in use by test_"
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert mock_subprocess.Popen.return_value.poll.call_count == 2


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", ""])
def test_exception_unknown(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.side_effect = ["terminated", None]
    # retry is applied
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert mock_subprocess.Popen.return_value.poll.call_count == 2
        assert image_manager_instance._port == image_manager_instance._grpc_start_port


@patch("OIIInspector.container_manager.time.sleep")
@patch("OIIInspector.container_manager.time.time", return_value=0)
@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "", "api.Registry.ListPackages", "", "", "", ""])
def test_exception_no_free_port(mock_run_cmd, mock_subprocess, mock_time, mock_sleep):
    mock_subprocess.Popen.return_value.poll.return_value = "terminated"
    mock_subprocess.Popen.return_value.stderr.read.return_value = "address already in use"
    # retry is applied
    with pytest.raises(exceptions.NoFreePortFound):
        with container_manager.ContainerManager("test_address") as image_manager_instance:
            image_manager_instance.start_container()
    assert mock_sleep.call_count == 100


@patch("OIIInspector.container_manager.subprocess")
@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "pull-result", RuntimeError,
                    "api.Registry.ListBundles", "stop-result", "remove-result"])
def test_grpcurl_query_failed_recovery(mock_run_cmd, mock_subprocess):
    mock_subprocess.Popen.return_value.poll.return_value = None
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
    assert mock_run_cmd.call_count == 7


@patch("OIIInspector.container_manager.run_cmd",
       side_effect=["", "/usr/bin/podman", "pull-result",
                    "api.Registry.ListBundles", "stop-result", "remove-result"])
def test_container_status(mock_run_cmd):
    with container_manager.ContainerManager("test_address") as image_manager_instance:
        image_manager_instance.start_container()
        assert image_manager_instance.container_status is True
        image_manager_instance.container_status = False
        assert image_manager_instance.container_status is False
        image_manager_instance.container_status = True
