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

Run the following command to download all the dependencies
```bash
pip install -r requirements.txt
```

## Usage

You can run the script providing a config.yml file with the same options as above, one option per line, as the example:

```yml
ch:
  # name
  - "ch"
  # arrival
  - [2, 3]
  # running
  - [2, 5]
  # capacity
  - 3
  # workers
  - 2
p:
  # name
  - "p"
  # arrival
  - [2, 5]
  # running
  - [3, 5]
  # capacity
  - 3
  # workers
  - 1
start_time: 2.5
iterations: 100000
reps: 5
```

If the config.yml file is not present, the script will use default values.

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