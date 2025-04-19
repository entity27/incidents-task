#!/usr/bin/env bash

set -e
set -x

mypy --config-file pyproject.toml --explicit-package-bases src
ruff check src tests
ruff format src tests --check
