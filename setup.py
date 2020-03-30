import os
from pathlib import Path
import shutil
import subprocess
import sys

from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension


MIN_GDAL_VERSION = (2, 4, 0)


# Get GDAL config from gdal-config command
def read_response(cmd):
    return subprocess.check_output(cmd).decode("utf").strip()


ext_options = {
    # GDAL 2.4.x requires C++11
    # "language": ["c++"],
    # "extra_compile_args": ["-std=c++11"],
    "include_dirs": [],
    "library_dirs": [],
    "libraries": [],
    "extra_link_args": [],
}


# setuptools clean does not cleanup Cython artifacts
if "clean" in sys.argv:
    if os.path.exists("build"):
        shutil.rmtree("build")

    root = Path(".")
    for ext in ["*.so", "*.pyc", "*.c", "*.cpp"]:
        for entry in root.rglob(ext):
            entry.unlink()

else:
    # Get libraries, etc from gdal-config
    flags = ["cflags", "libs", "version"]
    gdal_config = os.environ.get("GDAL_CONFIG", "gdal-config")
    config = {flag: read_response([gdal_config, f"--{flag}"]) for flag in flags}

    GDAL_VERSION = tuple(int(i) for i in config["version"].split("."))

    if not GDAL_VERSION > MIN_GDAL_VERSION:
        sys.exit("GDAL must be >= 2.4.x")

    ext_options["include_dirs"] = [entry[2:] for entry in config["cflags"].split(" ")]

    for entry in config["libs"].split(" "):
        if entry.startswith("-L"):
            ext_options["library_dirs"].append(entry[2:])
        elif entry.startswith("-l"):
            ext_options["libraries"].append(entry[2:])
        else:
            ext_options["extra_link_args"].append(entry)


setup(
    name="pyogrio",
    version="0.1.0",
    packages=["pyogrio"],
    url="https://github.com/brendan-ward/pyogrio",
    license="MIT",
    author="Brendan C. Ward",
    author_email="bcward@astutespruce.com",
    description="Vectorized vector I/O using GDAL",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    install_requires=[numpy],
    tests_require=["pytest", "pytest-cov", "pytest-benchmark"],
    include_package_data=True,
    ext_modules=cythonize(
        [
            Extension("pyogrio._err", ["pyogrio/_err.pyx"], **ext_options),
            Extension("pyogrio._io", ["pyogrio/_io.pyx"], **ext_options),
            Extension("pyogrio._ogr", ["pyogrio/_ogr.pyx"], **ext_options),
        ],
        compiler_directives={"language_level": "3"},
    ),
)