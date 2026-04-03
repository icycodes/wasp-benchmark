import os
import shutil
import pytest

PROJECT_DIR = "/home/user/wasp-project"

def test_wasp_binary_available():
    assert shutil.which("wasp") is not None, "wasp binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_main_wasp_file_exists():
    main_wasp_path = os.path.join(PROJECT_DIR, "main.wasp")
    assert os.path.isfile(main_wasp_path), f"main.wasp not found at {main_wasp_path}."
