from setuptools import setup

setup(
    name="black-macchiato",
    description="Partial black formatting",
    url="https://github.com/wbolster/black-macchiato",
    author="wouter bolsterlee",
    author_email="wouter@bolsterl.ee",
    license="BSD License",
    version="1.1.0",
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
