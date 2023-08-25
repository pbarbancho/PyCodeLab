# PyCodeLab

Experiment logging, backup and visualization (comming soon) tool.

## Installation

Activate your environment, cd into this repo directory and run

```
pip install .
```

## Requirements

- python >= 3.7
- click >= 8.1.7
- gitdb >= 4.0.10
- GitPython >= 3.1.32
- PyYAML >= 6.0.1

## Usage

Initialize new lab

```
pcl init
```

Add new data to lab

```
pcl data add
```

Currently supported data types are:

- `callable`: A python callable that returns all data

Run current workspace experiment

```
pcl exp run
```

## Experiment Logging

Experiment logging is as easy as

```Python
from pycodelab.experiments import ExperimentLogger

with ExperiementLogger() as logger:
    logger.log_value(
        name='test_value',
        value=42
    )
```