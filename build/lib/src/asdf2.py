from setuptools import setup, find_packages
import os

# Establish the base path relative to the location of this file
base_path = os.path.abspath(os.path.dirname(__file__))

# Read requirements.txt and populate the install_requires list
install_requires = []
requirements_path = os.path.join(base_path, "requirements.txt")
with open(requirements_path, "r") as file:
    install_requires = [line.strip() for line in file if line.strip()]

setup(
    name="adchackathon202405t1",
    version="0.0.7",
    packages=find_packages(),
    install_requires=install_requires,
    author=["Patrick", "Andi"],
    author_email="your@email.com",
    description="Some chatGPT package",
    url="https://github.com/WZHPASJ/adc-hackathon-2024-05-t1",
    classifiers=[
        "Programming Language :: Python :: 3",
        # Add more classifiers as needed
    ],
    entry_points={
        "console_scripts": ["adchackathon202405t1=src.__main__:main"],
    },
)
