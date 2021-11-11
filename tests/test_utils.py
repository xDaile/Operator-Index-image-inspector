import json.decoder
from unittest.mock import MagicMock, patch
import pytest
from OIIInspector.utils import run_cmd, convert_output, setup_arg_parser


input_file_name = "./tests/data/{test_name}"
CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT = 4
CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT = 4
CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT = 9
mock_process = MagicMock()
mock_process.communicate.return_value = ["success".encode("utf-8"), 0]


def load_and_convert_file(file_name):
    test_file_name = input_file_name.format(test_name=file_name)
    with open(test_file_name, "r") as file:
        input_data = file.read()
    return convert_output(input_data)


@patch("OIIInspector.utils.subprocess.Popen")
def test_run_cmd_pass(mocked_popen):
    mock_process.returncode = 0
    mocked_popen.return_value = mock_process
    output = run_cmd("ls")
    assert output == "success"
    mocked_popen.assert_called_once_with(["ls"], stdout=-1, stderr=-1)


@patch("OIIInspector.utils.subprocess.Popen")
def test_run_cmd_fail(mocked_popen):
    mock_process.returncode = 1
    mocked_popen.return_value = mock_process
    with pytest.raises(RuntimeError):
        output = run_cmd("ls")
        assert output == "success"
    mocked_popen.assert_called_once_with(["ls"], stdout=-1, stderr=-1)


def test_convert_output_combined():

    converted_input = load_and_convert_file("convert_output_combined.json")
    assert "csvJson" in converted_input
    assert "spec" in converted_input
    assert "object" in converted_input
    assert len(converted_input["csvJson"]) == CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT
    assert len(converted_input["object"]) == CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT
    assert len(converted_input["spec"]) == CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT


def test_convert_output_csvjson():
    converted_input = load_and_convert_file("convert_output_csvjson.json")
    assert "csvJson" in converted_input
    assert len(converted_input["csvJson"]) == CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT


def test_convert_output_object_list():
    converted_input = load_and_convert_file("convert_output_object_list.json")
    assert "object" in converted_input
    assert len(converted_input["object"]) == CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT


def test_convert_output_spec():
    converted_input = load_and_convert_file("convert_output_spec.json")
    assert "spec" in converted_input
    assert len(converted_input["spec"]) == CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT


def test_convert_output_empty_input():
    with pytest.raises(RuntimeError):
        convert_output("")


def test_bad_input():
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_1.json")
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_2.json")
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_3.json")


def test_parser_arg_groups(capsys):
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": True,
            "type": str,
        },
        ("--arg2",): {
            "group": "Group 1",
            "help": "Argument 2",
            "required": True,
            "type": str,
        },
        ("--arg3",): {
            "group": "Group 2",
            "help": "Argument 3",
            "required": True,
            "type": str,
        },
        ("--arg4",): {
            "group": "Group 2",
            "help": "Argument 4",
            "required": True,
            "type": bool,
        },
    }

    parser = setup_arg_parser(args)
    parser.print_help()
    out, _ = capsys.readouterr()

    assert "Group 1:" in out
    assert "Group 2:" in out


def test_parser_arg_required():
    args = {
        ("--arg2",): {
            "group": "Group 1",
            "help": "Argument 2",
            "required": True,
            "type": str,
        }
    }

    parser = setup_arg_parser(args)
    with pytest.raises(SystemExit):
        parser.parse_args(["--arg2"])
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_arg_not_required():
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": False,
            "type": str,
        }
    }

    parser = setup_arg_parser(args)
    parser.parse_args(["--arg1", "test"])
    parser.parse_args([])
    with pytest.raises(SystemExit):
        parser.parse_args(["--arg1"])


def test_parser_help(capsys):
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": True,
            "type": str,
        },
        ("--arg2",): {
            "group": "Group 1",
            "help": "Argument 2",
            "required": True,
            "type": str,
        },
    }

    parser = setup_arg_parser(args)
    parser.print_help()
    out, _ = capsys.readouterr()
    assert "Argument 1" in out
    assert "Argument 2" in out
    assert "usage:" in out


def test_parser_type():
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": True,
            "type": int,
        }
    }

    parser = setup_arg_parser(args)
    parser.parse_args(["--arg1", "-1502"])
    with pytest.raises(SystemExit):
        parser.parse_args(["--arg1", "s"])


def test_parser_default():
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": False,
            "type": int,
            "default": "1",
        }
    }

    parser = setup_arg_parser(args)
    parser.parse_args(["--arg1", "-1502"])
    parsed_args = parser.parse_args([])
    assert parsed_args.arg1 == 1


def test_parser_action():
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": True,
            "action": "store_true",
        }
    }

    parser = setup_arg_parser(args)
    parsed_args = parser.parse_args(["--arg1"])
    assert parsed_args.arg1 is True
