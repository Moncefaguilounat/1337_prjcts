import sys  # gives you information about Python installation
import os  # gives you environment variables
import site  # shows you where packages are installed
from typing import Tuple, Optional


def detect_venv() -> Tuple[Optional[str], bool]:

    # Check if VIRTUAL_ENV is set
    # (the variable returns the virtual env path if activated and None if not)
    venv = os.getenv('VIRTUAL_ENV')

    # check sys.prefix vs sys.base_prefix
    # sys.prefix returns the current python environment
    # sys.base_prefix returns the original python environment
    in_venv = sys.prefix != sys.base_prefix

    return venv, in_venv


def show_environment_info() -> None:

    try:
        venv_path, in_venv = detect_venv()

        if in_venv:

            print("MATRIX STATUS: Welcome to the construct")
            print(f"Current Python: {sys.executable}")
            # sys.executable gives the path to the current Python interpreter

            if venv_path:

                # extracts the name of the venv out of the path
                venv_name = os.path.basename(venv_path)
                print(f"Virtual Environment: {venv_name}")
                print(f"Environment Path: {venv_path}")

            print("\nSUCCESS: You're in an isolated environment!")
            print("Safe to install packages without affecting")
            print("the global system.")

            # show where packages will be installed
            print("\nPackage installation path:")
            packages_path = site.getsitepackages()
            if packages_path:
                print(packages_path[0])

        else:
            print("MATRIX STATUS: You're still plugged in")
            print(f"\nCurrent Python: {sys.executable}")
            print("Virtual Environment: None detected")
            print("\nWARNING: You're in the global environment!")
            print("The machines can see everything you install.")
            print("\nTo enter the construct, run:")
            print("python -m venv matrix_env")
            print("source matrix_env/bin/activate   # On Unix")
            print("matrix_env\nScripts\nactivate    # On Windows")
            print("\nThen run this program again.")
    except Exception as e:
        print(f"an environment error occured : {e}")
        sys.exit(1)


def main() -> None:
    show_environment_info()


if __name__ == "__main__":
    main()
