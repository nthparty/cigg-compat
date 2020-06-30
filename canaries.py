"""Library for loading dynamic library files.

Python library for choosing and loading dynamic library
files compatible with the operating environment.
"""

import doctest
import sys
import platform
import ctypes

class canaries():
    """
    Wrapper class for static methods.
    """

    @staticmethod
    def canary(system, path):
        """
        Single-path wrapper method for convenience.
        """
        paths = {}
        paths[system] = [path]
        obj = canaries(paths)
        return obj.lib if hasattr(obj, 'lib') else None

    @staticmethod
    def load(paths):
        """
        Wrapper method for backwards compatibility.
        """
        obj = canaries(paths)
        return obj.lib if hasattr(obj, 'lib') else None

    def __init__(self, paths):
        """
        Attempt to load a library at one of the supplied
        paths based on the platform. Retains state in order
        to record all exceptions and incorrect outputs.
        """
        if not isinstance(paths, (str, list, dict)):
            raise ValueError(
                "input must be a string, list, or dictionary"
            )

        if isinstance(paths, dict) and\
           not all(isinstance(p, (str, list)) for p in paths.values()):
            raise ValueError(
                "path values in dictionary must be strings or lists"
            )

        self.lib = None
        self.exceptions = []
        self.outputs = []

        system = platform.system()
        if isinstance(paths, str):
            self.lib = self._canary(system, paths)

        elif isinstance(paths, list):
            for path in paths:
                self.lib = self._canary(system, path)
                if self.lib is not None:
                    break

        elif isinstance(paths, dict):
            if system in paths:
                ps = paths[system]
                for path in [ps] if isinstance(ps, str) else ps:
                    self.lib = self._canary(system, path)
                    if self.lib is not None:
                        break

    def _canary(self, system, path):
        """
        Attempt to load a library file at the supplied path
        and verify that its exported functions work.
        """
        lib = None

        # Only attempt to load object files that exist.
        if os.path.exists(path):
            try:
                # Load the library.
                if system == 'Windows':
                    lib = ctypes.windll.LoadLibrary(path)
                else:
                    lib = ctypes.cdll.LoadLibrary(path)

                if lib is not None:
                    # Confirm that the library's exported functions work.
                    try:
                        # Build input parameters.
                        treat = ctypes.create_string_buffer(5)
                        for (i, c) in enumerate('treat'):
                            try:
                                treat[i] = c
                            except:
                                treat[i] = ord(c)
                        chirp = ctypes.create_string_buffer(5)

                        # Invoke compatibility validation method.
                        r = lib.canary(chirp, treat)

                        # Decode results.
                        chirp = chirp.raw
                        if isinstance(chirp, bytes):
                            chirp = chirp.decode()

                        # Record the outputs.
                        self.outputs.append((
                            (system, path),
                            (r, type(chirp), chirp)
                        ))

                        # Check that results are correct.
                        if r != 0 or chirp != 'chirp':
                            lib = None

                    except:
                        lib = None
                        self.exceptions.append((
                            (system, path),
                            (
                                sys.exc_info()[0], sys.exc_info()[1],
                                sys.exc_info()[2].tb_lineno
                            )
                        ))

            except:
                self.exceptions.append((
                    (system, path),
                    (
                        sys.exc_info()[0], sys.exc_info()[1],
                        sys.exc_info()[2].tb_lineno
                    )
                ))

        return lib

# Provide direct access to static methods.
canary = canaries.canary
load = canaries.load

if __name__ == "__main__":
    doctest.testmod()
