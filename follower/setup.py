from setuptools import setup

setup(
    name="aspects-follower",
    python_requires=">=3.10",
    packages=["src"],
    entry_points={
        "console_scripts": ["follower-cli=src.main:main"],
    },
)
