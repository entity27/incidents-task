#!/usr/bin/env bash

set -e
set -x

cd src
docker compose up tests
