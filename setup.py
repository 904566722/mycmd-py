from setuptools import setup, find_packages

setup(
    name="mycmd",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0.0",
        "colorama>=0.4.6",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "mycmd=mycmd.cli:cli",
        ],
    },
) 