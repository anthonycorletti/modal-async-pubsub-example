#!/bin/sh -e

pip install --upgrade pip
pip install --upgrade --no-cache-dir '.[dev,test]'
pre-commit install
