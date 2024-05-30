from setuptools import setup, find_packages

# Read requirements.txt and populate the install_requires list
install_requires = []
with open("requirements.txt", "r") as file:
    for line in file:
        requirement = line.strip()
        if requirement:
            install_requires.append(requirement)

setup(
    name="adchackathon202405t1",
    version="0.0.5",
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
