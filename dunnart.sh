#!/bin/sh
DN="$(dirname "$(readlink -f "${0}")")"
cd $DN/cde-root/local/munk/proorigami-prod/dunnart/trunk && $DN/cde-exec ./dunnart "$@"
