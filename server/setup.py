from setuptools import setup

setup(
    name="aspects-server",
    python_requires=">=3.10",
    packages=["src"],
    entry_points={
        "console_scripts": ["server-cli=src.main:main"],
    },
)
