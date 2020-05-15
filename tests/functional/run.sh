#!/bin/bash

set -e

TEST_CASE_DIR=$(dirname $(realpath $0))
PROJECT_ROOT="$(dirname $(dirname ${TEST_CASE_DIR}))"

export PYTHONPATH=${PYTHONPATH:-$PROJECT_ROOT}

for input in "${TEST_CASE_DIR}"/input*.txt
do
    output=$(echo "${input}" | sed -r 's/input(.*)\.txt/output\1.txt/')
    echo -n "${input:$((${#TEST_CASE_DIR} + 1))} ... "
    if cmp -s <(python3.7 "${PROJECT_ROOT}/ui/cli.py" -f text "${input}") <"${output}"
    then
        echo PASSED
    else
        echo FAILED
    fi
done | column -t
