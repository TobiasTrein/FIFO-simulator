# Introduction

This program simulates a simple queue with a given number of server processes and capacity. It uses an event-based simulation approach and allows the user to specify the arrival and running time of jobs in the memory.

##Execution Video
https://youtu.be/ntCMsJdiD6k

##Authors
+ Delmar Lucas Dorneles Quaresma (https://github.com/LucasDornelesQuaresma)
+ João Victor Zucco Marmentini (https://github.com/jvzmarmentini)
+ Tobias Trein(https://github.com/TobiasTrein)

## Prerequisites

To run this script, you will need to have Python installed on your computer. The script has been developed and tested on Python 3.

## Usage

You can run the script with the following command:

```python
python main.py -k <int> -c <int> -a <string> -r <string> -s <float> -i <int> -e <int> -d <bool>
```

Where the options are:

+ -k: an integer value for K
+ -c: an integer value for C
+ -a: arrival interval, in the format "start..end"
+ -r: running interval, in the format "start..end"
+ -s: start time
+ -e: executions
+ -d: debug

You can also provide a config.txt file with the same options as above, one option per line, in the following order:

```txt
arrival interval
running interval
K
C
start time
iterations
number of executions
debug
```

If the config.txt file is not present, the script will use default values.

# Docker

Install Docker: If you haven't already, install Docker from the official website at https://www.docker.com/get-started.

Then, you can build the Docker image with the following command:

```bash
docker build -t my-app .
```

Finally, you can run the Docker container with the following command:

```bash
docker run -it --rm my-app
```