from setuptools import setup, find_packages

setup(
    name="ZAXOTP",
    version="3.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "zaxotp=run:main",
        ],
    },
    author="ZAAX",
)
