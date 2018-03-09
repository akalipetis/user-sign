"""
Utilities for loading secrets from either the environment or files.
"""
import os


def load_secret(name, fallback=None):
    """
    Loads a secret, in the following way:
    * Checks if name_FILE is defined in the environment and the file exists
    * Falls back to name, if it is defined in the environment
    * Falls back to the given value
    """
    file_name = os.getenv(f'{name}_FILE')
    if file_name and os.path.isfile(file_name):
        with open(file_name, 'r') as fin:
            return fin.read().strip()
    return os.getenv(name, fallback)
