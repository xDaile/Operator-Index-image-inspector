import sys
import pytest
from unittest.mock import patch
from OIIInspector import oii_inspector_calls

input_file_name = "./tests/data/{test_name}"


@patch("OIIInspector.oii_inspector_calls.get_bundle", return_value="Client-response")
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_get_bundle_main(mock_json_dump, mock_get_bundle):
    test_args = [
        "name",
        "--address",
        "test-address:1",
        "--package-name",
        "test-package-name",
        "--channel-name",
        "0.1",
        "--csv-name",
        "csv-test-name.4.1.3",
    ]

    output = oii_inspector_calls.get_bundle_main(test_args)
    mock_get_bundle.assert_called_once_with(
        "test-address:1", "test-package-name", "0.1", "csv-test-name.4.1.3"
    )
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_get_bundle_main_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.get_bundle_main()


@patch("OIIInspector.oii_inspector_calls.list_packages", return_value="Client-response")
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_list_packages_main(mock_json_dump, mock_list_packages):
    test_args = ["name", "--address", "test-address:1"]

    output = oii_inspector_calls.list_packages_main(test_args)
    mock_list_packages.assert_called_once_with("test-address:1")
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_list_packages_main_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.list_packages_main()


@patch("OIIInspector.oii_inspector_calls.list_bundles", return_value="Client-response")
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_list_bundles_main(mock_json_dump, mock_list_bundles):
    test_args = ["name", "--address", "test-address:1"]

    output = oii_inspector_calls.list_bundles_main(test_args)
    mock_list_bundles.assert_called_once_with("test-address:1")
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_list_bundles_main_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.list_bundles_main()


@patch("OIIInspector.oii_inspector_calls.get_package", return_value="Client-response")
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_get_package_main(mock_json_dump, mock_get_package):
    test_args = [
        "name",
        "--address",
        "test-address:1",
        "--package-name",
        "test-package-name",
    ]

    output = oii_inspector_calls.get_package_main(test_args)
    mock_get_package.assert_called_once_with("test-address:1", "test-package-name")
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_get_package_dump_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.get_package_main()


@patch(
    "OIIInspector.oii_inspector_calls.get_bundle_for_channel",
    return_value="Client-response",
)
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_get_bundle_for_channel_main(mock_json_dump, mock_get_bundle_for_channel):
    test_args = [
        "name",
        "--address",
        "test-address:1",
        "--package-name",
        "test-package-name",
        "--channel-name",
        "0.1",
    ]

    output = oii_inspector_calls.get_bundle_for_channel_main(test_args)
    mock_get_bundle_for_channel.assert_called_once_with(
        "test-address:1", "test-package-name", "0.1"
    )
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_get_bundle_for_channel_dump_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.get_bundle_for_channel_main()


@patch(
    "OIIInspector.oii_inspector_calls.get_bundle_that_replaces",
    return_value="Client-response",
)
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_get_bundle_that_replaces_main(mock_json_dump, mock_get_bundle_that_replaces):
    test_args = [
        "name",
        "--address",
        "test-address:1",
        "--package-name",
        "test-package-name",
        "--channel-name",
        "0.1",
        "--csv-name",
        "csv-test-name.4.1.3",
    ]

    output = oii_inspector_calls.get_bundle_that_replaces_main(test_args)
    mock_get_bundle_that_replaces.assert_called_once_with(
        "test-address:1", "test-package-name", "0.1", "csv-test-name.4.1.3"
    )
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_get_bundle_that_replaces_dump_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.get_bundle_that_replaces_main()


@patch(
    "OIIInspector.oii_inspector_calls.get_default_bundle_that_provides",
    return_value="Client-response",
)
@patch("OIIInspector.oii_inspector_calls.json.dump")
def test_get_default_bundle_that_provides_main(
    mock_json_dump, mock_get_default_bundle_that_provides
):
    test_args = [
        "name",
        "--address",
        "test-address:1",
        "--group",
        "test-group-name",
        "--version",
        "0.1",
        "--kind",
        "test-kind",
        "--plural",
        "test-plural",
    ]

    output = oii_inspector_calls.get_default_bundle_that_provides_main(test_args)
    mock_get_default_bundle_that_provides.assert_called_once_with(
        "test-address:1", "test-group-name", "0.1", "test-kind", "test-plural"
    )
    mock_json_dump.assert_called_once_with(
        "Client-response", sys.stdout, sort_keys=True, indent=4, separators=(",", ": ")
    )
    assert output == "Client-response"


def test_get_default_bundle_that_provides_dump_ends_without_args():
    with pytest.raises(SystemExit):
        oii_inspector_calls.get_default_bundle_that_provides_main()
