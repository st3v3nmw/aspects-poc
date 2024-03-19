from setuptools import setup

setup(
    name="aspects-registration-agent",
    python_requires=">=3.10",
    packages=["src"],
    entry_points={
        "console_scripts": ["registration-agent-cli=src.main:main"],
    },
)
