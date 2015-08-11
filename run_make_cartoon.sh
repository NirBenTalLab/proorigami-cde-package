#!/bin/sh
DN="$(dirname "$(readlink -f "${0}")")"
cd $DN/cde-root/home/proorigami && $DN/cde-exec ./make_cartoon.sh "$@"
