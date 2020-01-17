#!/bin/bash
cd $(git rev-parse --show-toplevel)
set -e

./bin/test.sh

python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload dist/*
