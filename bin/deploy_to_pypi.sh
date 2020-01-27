#!/bin/bash
cd $(git rev-parse --show-toplevel)
set -e

./bin/test.sh

rm -rf dist
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
echo 'to prod? (press enter)'; read;
twine upload dist/*
