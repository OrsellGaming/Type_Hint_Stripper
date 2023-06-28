
#! DEVELOPER FILE
#! Purpose: To remove all type hints from python script files.
#! It is possible to specify a specific directory 
#! and have the option to either scan subdirectories or not.
#! Recommend targeting the src folder and not the whole project folder.

# TODO: Add case to exit when no python scripts could be found
# TODO: If an exception occurs with scan or strip, try to continue to next file instead of exiting

import re
import os

def find_py_scripts(subdirectories: bool, directory: str):
    """Scans for python script files in the specified directory.

    Args:
        directory (str): Directory to scan for files.
        subdirectories (bool): Specify if it should also scan and modify files in subdirectories below this script file.
    """
    
    py_scripts = []
    py_script_count = 0
    
    #TODO: Optimize this a bit so it looks less wonky
    # Scan through the specified directory and only scan subdirectories if specified
    try:
        if subdirectories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file == "type_hint_stripper.py":
                        continue
                    if file.endswith(".py"):
                        py_script_count += 1
                        py_scripts.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                if file == "type_hint_stripper.py":
                        continue
                if file.endswith(".py"):
                    py_script_count += 1
                    py_scripts.append(os.path.join(directory, file))
        
        # Report how many files were found and what files they are
        print(f"Scanned for python files and found {py_script_count}.")
        print("Found python script files:")
        for py_file in py_scripts:
            print(py_file)
        
        return py_scripts
    except Exception as e:
        print(f'An error occurred while scanning the directory:\n{str(e)}')
        print("Exiting...")
        exit()

def remove_type_hints(py_file_paths: dict):
    """Removes the type hints of every function that has a type hint in the specified python script file.

    Args:
        py_file_paths (dict): Dictionary containing paths to python script files.
    """
    try:
        for py_file_path in py_file_paths:
            # Read the contents of the inputted python script file, then remove the type hints
            # using the regular expressions module (re). Then overwrite the original python 
            # script file with the new type hint stripped one.
            with open(py_file_path, 'w+') as py_file:
                script_code = py_file.read()
                modified_code = re.sub(r'(\s*->\s*[^:\n]+)', '', script_code)
                py_file.write(modified_code)

            print(f'Type hints removed in python script file "{py_file_path}".')
    except Exception as e:
        print(f'An error occurred while scanning the directory:\n{str(e)}')
        print("Exiting...")
        exit()

def main():
    print("Welcome to the Type Hint Stripper 2000!")

    # Ask what directory to scan for python script files
    while True:
        directory = input(
            "Please specify the directory to scan for Python scripts to strip type hints out of.\n"
            "Leave blank to specify the directory where this script is located...\n"
        ).strip()

        # Continue without specifying a directory in order to target the directory where this script is in
        if len(directory) == 0:
            directory = os.path.abspath(__file__).replace("\\type_hint_stripper.py", "")
            break

        if not os.path.isdir(directory):
            print("Invalid directory! Please enter a valid directory path...\n")
            continue

        # Valid directory has been inputted so we will break out of the loop
        break
    
    # TODO: This can also be fixed to be a little less wonky
    # Ask if the script should also look inside subdirectories for python scripts too.
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
    
    py_files: dict = find_py_scripts(subdirectories, directory)
    remove_type_hints(py_files)
    print("Finished removing type hints from python script(s). Exiting...")
    exit()

if __name__ == "__main__":
    main()
else:
    print("Please run this script directly for it to work properly. Exiting...")
    exit()