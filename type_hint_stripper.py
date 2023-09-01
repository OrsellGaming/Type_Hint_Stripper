
#! Purpose: To remove all type hints from Python script files.
#! It is possible to specify a specific directory 
#! and have the option to either scan subdirectories or not.
#! Recommend targeting the src folder and not the whole project folder.

# TODO: If an exception occurs with scan or strip, try to continue to next file instead of exiting

import re
from pathlib import Path

def find_py_scripts(directory: str, subdirectories: bool) -> list:
    """Scans specified directory for Python scripts and returns it as a list. Has the option to also scan subdirectories.

    Args:
        directory (str): Directory to scan for Python script files.
        subdirectories (bool): Whether the user does or does not want to scan subdirectories below the specified directory.

    Returns:
        list: Returned list of paths to Python script files.
    """
    
    py_script_list = []
    py_script_count = 0

    #TODO: Optimize this a bit so it looks less wonky
    #TODO: as_posix() for Path.glob
    # Scan through the specified directory and only scan subdirectories if specified
    try:
        # Use the glob method to find Python files
        py_scripts = Path(directory).is_file(Path(directory).glob('**/*.py' if subdirectories else '*.py'))

        # Count the files using sum, for every scanned Python script file count by one
        py_script_count = sum(1 for py_file in py_scripts)

        py_scripts = [sorted(py_scripts)]

        # if subdirectories:
        #     for path in Path(directory).glob('*.py'):
        #         py_script_count += 1
        #         py_scripts.append(path)
        # else:
        #     for file in os.listdir(directory):
        #         if file.endswith(".py"):
        #             py_script_count += 1
        #             py_scripts.append(os.path.join(directory, file))
        
        # Report how many files were found and what files they are
        print(f"Scanned for Python files and found {py_script_count}.")
        print("Found Python script files:")
        print(py_scripts)
        for py_file in py_scripts:
            # py_script_list.append(py_file.parent)
            print(py_file)
        
        return py_script_list
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except PermissionError:
        print(f"Permission denied for directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred while scanning the directory:\n{str(e)}")

def remove_type_hints(py_file_paths: list):
    """Removes the type hints of every function that has a type hint in the specified Python script file.

    Args:
        py_file_paths (list): List containing paths to Python script files.
    """
    for py_file_path in py_file_paths:
        # Added exception to this script file so nothing gets messed up, ironically this has only one type hint.
        if "type_hint_stripper.py" in py_file_path:
            print("type_hint_stripper.py will not be modify itself, skipping...")
            continue
        try:
            # Read the contents of the inputted Python script file, then remove the type hints
            # using the regular expressions module (re). Then overwrite the original Python 
            # script file with the new type hint stripped one.
            with open(py_file_path, 'w+') as py_file:
                script_code = py_file.read()
                modified_code = re.sub(r'(\s*->\s*[^:\n]+)', '', script_code)
                py_file.write(modified_code)

            print(f'Type hints removed in Python script file "{py_file_path}".')
        except Exception as e:
            print(f'An error occurred while scanning the directory:\n{str(e)}')
            print("Exiting...")
            exit()

def main():
    print("Welcome to the Type Hint Stripper 2000!")

    # Ask what directory to scan for Python script files
    while True:
        directory = input(
            "Please specify the directory to scan for Python scripts to strip type hints out of.\n"
            "Leave blank to specify the directory where this script is located...\n"
        ).strip()

        # Continue without specifying a directory in order to target the directory where this script is in
        if len(directory) == 0:
            directory = Path.cwd()
            break

        if not Path(directory).isdir():
            print("Invalid directory! Please enter a valid directory path...\n")
            continue

        # Valid directory has been inputted so we will break out of the loop
        break
    
    # TODO: This can also be fixed to be a little less wonky
    # Ask if the script should also look inside subdirectories for Python scripts too.
    while True:
        subdirectories = input(
            "Do you also want to scan and modify Python scripts in subdirectories below this script file? (y/n)"
        ).lower().strip()

        if subdirectories == "y":
            subdirectories = True
            break
        
        if subdirectories == "n":
            subdirectories = False
            break
    
    py_files = find_py_scripts(directory, subdirectories)
    remove_type_hints(py_files)
    print("Finished removing type hints from Python script(s). Exiting...")
    exit()

if __name__ == "__main__":
    main()
else:
    print("Please run this script directly for it to work properly. Exiting...")
    exit()