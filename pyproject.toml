[build-system]
requires = ["setuptools>=63"]
build-backend = "setuptools.build_meta"

[project]
name = "adchackathon202405t1"
version = "0.0.1"
description = "Software development assistant for the ADCHackathon202405T1"
readme = "README.md"
requires-python = ">=3.11"

license = {text = "PROPRIETARY"}
authors = [
    { name = "Patrick Schneider", email = "patrick.g.schneider@gmail.com" },
]

classifiers = [
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

dependencies = [
    "dynaconf",
    "argparse",
    "PyYAML==6.0.1",
    "pytest==7.4.3",
]

[project.scripts]
run = "src.__main__:main"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["."]  # ["."] by default
include = ["*"]  # ["*"] by default

[tool.setuptools.package-data]
random_package = ["*.yaml"]

[tool.black]

[tool.pipeline]
python_release_versions = [3.8]
python_test_versions = [3.8]
