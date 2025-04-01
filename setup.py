from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open("README.md") as f:
    long_description = f.read()

setup(
    name="SapScript",
    version="0.0.1",
    author="Jason Duncan",
    author_email="jason.matthew.duncan@gmail.com",
    description="A Framework Library for controlling the SAP GUI desktop client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jduncan8142/sap_script",
    project_urls={
        "Bug Tracker": "https://github.com/jduncan8142/sap_script/issues",
        "Documentation": "https://github.com/jduncan8142/sap_script/wiki",
    },
    packages=["SapScript"] + ["SapScript." + pkg for pkg in find_packages("SapScript")],
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={
        "Core": "SapScript/Core",
        "Gui": "SapScript/Gui",
        "Utils": "SapScript/Utils",
    },
    python_requires=">=3.13",
    install_requires=[
        "pywin32>=308",
        "pluggy>=1.5.0",
        "bigtree==0.25.1",
        "colorama==0.4.6",
        "iniconfig==2.0.0",
        "packaging==24.2",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.5",
        ]
    },
)
