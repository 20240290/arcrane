"""
 Copyright 2024 Resurgo

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import os
import inspect
import importlib

def generate_docs(project_dir):
    """
    Generate a documentation file that list all functions in the project with their docstrings.

    Args:
        str: Directory path.

    Returns:
        None 
    """
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.relpath(os.path.join(root, file), start=project_dir)
                module_path = module_path.replace(os.sep, ".").rstrip(".py")
                try:
                    module = importlib.import_module(module_path)
                    print(f"Module: {module_name}")
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        print(f"\nFunction: {name}")
                        doc = inspect.getdoc(obj)
                        print(f"Docstring: {doc or 'No docstring available'}")
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")

# Use it
# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate upwards to the root directory (adjust the number of '..' depending on the structure)
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
#print(root_directory)

generate_docs(root_directory)
