#!/usr/bin/env bash

set -o pipefail
set -e

__here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#------------------------------------------------------------------------------

cd $__here

poetry run python src/main.py "$@"
