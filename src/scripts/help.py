"""help:    traShで独自実装されているコマンド一覧を表示します"""

import os
import importlib.util

def import_module_from_file(filepath):
    """Imports a module from a given file path and returns the module."""
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None:
        raise ImportError(f"Could not import module from {filepath}")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Could not import module from {filepath}")
    spec.loader.exec_module(module)
    return module

def get_all_python_files(directory):
    """Returns a list of all Python files in the given directory and subdirectories."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def print_docstrings(directory):
    """Finds all Python files in the given directory, imports them, and prints their docstrings."""
    python_files = get_all_python_files(directory)
    for filepath in python_files:
        module = import_module_from_file(filepath)
        print(f"\t{module.__doc__}")

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    print_docstrings(path)

