# Introduction

This program is a queue simulator that works based on kendall's notation. It supports simple queues, tandem queues and probability queues. There's no limitation, besides cpu and memory consuption, on the size or ammounts of queues. 

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
# how much iterations a rep will have
iterations: 1000
# how much repetitions the code will generate 
reps: 5

# array of queues
queues:
  # queue #1. the value will correspond to the id of the object
  q1:
    # REQUIRED ONLY AT THE FIRST QUEUE
    # min-max arrival time of a process. this must be a tuple of ints
    arrival: [1,2]

    # REQUIRED FIELDS
    # how many servers/workers are available in this queue
    workers: 1
    # min-max run time of a process. this must be a tuple of ints
    run: [1,2]

    # OPTIONALS FIELDS
    # queue capacity. if not setted, it will be infinity
    capacity: 2
    # next_idx will be explained bellow...
    next_idx: 
  q2:
    ...
  ...

# first proccess arrival time
first_proc: 2.5
```

The `next_idx` queue variable should assume one of the following three configurations:

- Empty: If there's no next queue, you shouldn't set this field
- String: If there's only one next queue with 100% prob., this field should be just a string variable like `next_idx: q2`
- List: If there's more than one cases, you must create a list with the key being the queue id and the value beeing the probability. If there's a chance of the proccess to go out, you don't need to set anything, the program will calculate based on the missing ammount. ex: next queue must be 30% to q2, 30% to q3 and 40% to leave, then:

```yml
...
queues:
  q1:
    ...
    next_idx:
      q2: 0.3
      q3: 0.3
  q2:
    ...
  q3:
    ...
...
```


If the config.yml file is not present, the script will use default values.

Then, run:

```bash
python3 main.py -c config.yml
```

If you need help, run:

```bash
python3 main.py --help
```

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