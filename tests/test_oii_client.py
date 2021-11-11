from unittest.mock import patch
from OIIInspector.oii_client import (
    get_bundle,
    list_packages,
    list_bundles,
    get_package,
    get_bundle_for_channel,
    get_bundle_that_replaces,
    get_default_bundle_that_provides,
    use_container_manager
)

input_file_name = "./tests/data/{test_name}"


def load_file(file_name):
    test_file_name = input_file_name.format(test_name=file_name)
    return open(test_file_name, "r").read()


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("get_bundle.json"))
def test_get_bundle(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = get_bundle("test_address:50051", "serverless-operator", "4.3",
                        "serverless-operator.v1.2.0")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"serverless-operator\", "
                                         "\"channelName\":\"4.3\", "
                                         "\"csvName\":\"serverless-operator.v1.2.0\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundle")
    assert output["version"] == "1.2.0"
    assert output["providedApis"][0]["plural"] == "test_plural"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("list_packages.json"))
def test_list_packages(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = list_packages("test_address:50051")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext "
                                         "test_address:50051 "
                                         "api.Registry/ListPackages")
    assert output[0]["name"] == "test-operator"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("list_bundles.json"))
def test_list_bundles(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = list_bundles("test_address:50051")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext test_address:50051 api.Registry/ListBundles")
    assert output[0]["csvName"] == "test_csv_name 1"
    assert output[0]["object"][2]["apiVersion"] == "test_api_version_0"
    assert output[1]["csvName"] == "test_csv_name 2"
    assert output[2]["csvName"] == "test_csv_name 3"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("get_package.json"))
def test_get_package(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = get_package("test_address:50051", "serverless-operator")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"name\":\"serverless-operator\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetPackage")
    assert output["name"] == "test-operator"
    assert output["channels"][3]["csvName"] == "test-operator.v1.10.0"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("get_bundle_for_channel.json"))
def test_get_bundle_for_channel(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = get_bundle_for_channel("test_address:50051", "submariner", "alpha")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"submariner\", "
                                         "\"channelName\":\"alpha\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundleForChannel")
    assert output["csvName"] == "test-name.v0.8.1"
    assert output["object"][8]["kind"] == "ClusterServiceVersion"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("get_bundle_that_replaces.json"))
def test_get_bundle_that_replaces(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = get_bundle_that_replaces("test_address:50051", "submariner", "alpha",
                                      "beta")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"submariner\", "
                                         "\"channelName\":\"alpha\","
                                         "\"csvName\":\"beta\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundleThatReplaces")
    assert output["csvName"] == "test-operator.v1.3.0"
    assert output["providedApis"][0]["plural"] == "test_plural"


@patch("OIIInspector.oii_client.ContainerManager")
@patch("OIIInspector.oii_client.run_cmd", return_value=load_file("get_default_bundle_that_provides.json"))
def test_get_default_bundle_that_provides(mock_run_cmd, mock_img_manager):
    mock_img_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test_address:50051"
    output = get_default_bundle_that_provides("test_address:50051", "testGroup",
                                              "testVersion", "testKind", "testPlural")
    check_container_manager_calls(mock_img_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d \'{"
                                         "\"group\":\"testGroup\", "
                                         "\"version\":\"testVersion\","
                                         "\"kind\":\"testKind\","
                                         "\"plural\":\"testPlural\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetDefaultBundleThatProvides")
    assert output["csvName"] == "test-operator.v8.2.0"
    assert output["providedApis"][4]["plural"] == "caches"
    assert output["object"][5]["kind"] == "CustomResourceDefinition"


@patch("OIIInspector.oii_client.run_cmd", return_value="result")
@patch("OIIInspector.oii_client.ContainerManager")
def test_use_container_manager(mock_container_manager, mock_run_cmd):
    mock_container_manager.return_value.__enter__.return_value.get_local_address_of_image.return_value = "test-local-address"
    result = use_container_manager("test-address", "test-api-address")
    assert result == "result"
    mock_container_manager.return_value.__enter__.return_value.get_local_address_of_image.assert_called_once()
    mock_container_manager.assert_called_once_with("test-address")
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext "
                                         "test-local-address "
                                         "api.Registry/test-api-address")

    use_container_manager("test-address", "test-api-address", call_argument="test-call-argument")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d "
                                    "test-call-argument "
                                    "test-local-address "
                                    "api.Registry/test-api-address")


def check_container_manager_calls(mock_container_manager):
    mock_container_manager.return_value.__enter__.return_value.get_local_address_of_image.assert_called_once()
    mock_container_manager.assert_called_once_with("test_address:50051")
