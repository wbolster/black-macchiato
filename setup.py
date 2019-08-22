import ast
from pathlib import Path
import re
from setuptools import setup


CURRENT_DIR = Path(__file__).parent


# This function is borrowed from the setup.py at https://github.com/psf/black
def get_version() -> str:
    macchiato_py = CURRENT_DIR / "macchiato.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(macchiato_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))

setup(
    name="black-macchiato",
    description="Partial black formatting",
    url="https://github.com/wbolster/black-macchiato",
    author="wouter bolsterlee",
    author_email="wouter@bolsterl.ee",
    license="BSD License",
    version=get_version(),
    py_modules=["macchiato"],
    install_requires=["black"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["black-macchiato = macchiato:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
