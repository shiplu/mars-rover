Description
===========

This project shows the movement of a mars-rover on plateau. The plateu is defined as a grid. After that some rovers are deployed there. Then command sequence is sent to the rovers and they move accordingly.

Assumptions
===========

1. It takes time for the rover to move from one grid to another. It involves moving it's wheel to go forward in a very carefully. Hence it's not very practical to have high performance move calculation.
2. If a rover is deployed on a grid-cell where a rover already exists, the new rover will not be deployed. It'll be in ERROR state. If it's deployed in an empty cell it'll be in OPERATIONAL state. If there is a collision to the border of the plateau or other rover happens after deployment it'll be marked as STOPPED. Only OPERATIONAL state allows rover to move forward
3. First all the rovers are deployed and then the movement sequence are sent. In real world this would be completely parallel. For this solution we didn't opt for parallel exection as there are many challenges to take care of. For exmaple, grid state syhchronization.


Input Output Specification
==========================

Input
-----

    L W
    X Y D
    MMM...

Here first line defines grid length and width. Next line is the initial postion of a rover. X and W is the length and width-wise co-ordinate. Co-ordinates stars from 1. X and Y has following constrait for the value.

    1 <= X <= L
    1 <= Y <= W

D is the direction of the rover. It can be any N, E, S, and W which mean  North, Eash, South, and West respectively.

Last line contains move sequeces of this rover. A rove can move forward, turn left, or turn right. These moves are denoted by M, L, and R respectively. 

Sample Input
------------

    3 4
    1 2 N
    MMRMM

Last 2 lines can be repeated if there are more rovers

    3 4
    1 2 N
    MMRMM
    1 1 E
    MMM

Output
------

The output contains the location, direction and state of each rover.

    X Y D S

Here S is the state of the rover. It can be any of `OPERATIONAL` or `STOPPED`. 

*Note*: Even though `ERROR` is a valid state, it doens't lead the rover to the plateau. Hence in the output it's not shown.

Sample Output
-------------

    3 4 E OPERATIONAL

For multiple rovers, there will be multiple lines

    3 4 E OPERATIONAL
    3 1 E STOPPED



Setup
=====

* The project was developed using python3.7. It may run with older python 3.x version.
* The functional tests are written in bash. It'll run on Linux. It's _not_ tested on OSX.

Recommended Configuration
-------------------------

1. Ubuntu Linux operating system
2. Python 3.7


HOWTO
=====

All the commands below assumes you are on project root directory in a terminal. If you are not in the project root folder, you need to change the paths accordingly

### Run program

If the input text is in file `input.txt` then we can get the output (as seen above) by running following python program.

    PYTHONPATH=. python3.7 ui/cli.py input.txt

### Run unit tests

The tests can be run using pythons unittest module.

    python -m unittest -v  tests.test_parser tests.test_entities

### Run functional tests

The functional test are written in `bash`. It's better we run it on Linux.

    tests/functional/run.sh
