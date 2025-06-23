[![Continuous Integration](https://github.com/casework/CASE-Mapping-Template-Python/actions/workflows/cicd.yml/badge.svg)](https://github.com/casework/CASE-Mapping-Template-Python/actions/workflows/cicd.yml)
![CASE Version](https://img.shields.io/badge/CASE%20Version-1.4.0-green)

# CASE Mapping Template Python
A template repository for adopters to create CASE mappings utilizing Python.

This repository is a basic example that generates a simple CASE-compliant RDF graph utilizing two different approaches.
1. Utilizing serialized Python dictionaries that are converted to JSON
2. Utilizing [`rdflib`](https://rdflib.readthedocs.io/en/stable/index.html) to build triple stores


## Continuous Integration

**Syntax Validation**

This repository utilizes [`pre-commit`](https://pre-commit.com/) with hooks for the following utilities to maintain consistency across the repository:
- [`black`](https://github.com/psf/black)
- [`flake8`](https://github.com/pycqa/flake8)
- [`isort`](https://github.com/pycqa/isort)
- [`mypy`](https://github.com/pre-commit/mirrors-mypy)

**Graph Validation**

These two output graphs are tested using [`pytest`](https://docs.pytest.org/en/7.1.x/) and [`rdflib`](https://rdflib.readthedocs.io/en/stable/index.html) to ensure the graphs were properly created and contain at least one triple.

The graphs are then tested for conformance with the CASE ontology using a [GitHub Action](https://github.com/kchason/case-validation-action).
