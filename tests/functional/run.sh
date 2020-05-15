#!/bin/bash

set -e

TEST_CASE_DIR=$(dirname $(realpath $0))
PROJECT_ROOT="$(dirname $(dirname ${TEST_CASE_DIR}))"

export PYTHONPATH=${PYTHONPATH:-$PROJECT_ROOT}

for input in "${TEST_CASE_DIR}"/*.in
do
    testname=${input:0:-3}
    output=${testname}.out

    echo -n "${testname:$((${#TEST_CASE_DIR} + 1))} ... "

    SECONDS=0

    if cmp -s <(python3.7 "${PROJECT_ROOT}/ui/cli.py" -f text "${input}") < "${output}"
    then
        echo ${SECONDS}s PASSED
    else
        echo ${SECONDS}s FAILED
    fi
done | column -t
