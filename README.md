# DS2006 final project

## About

This was my final project for the course called Introduction to data science with the code DS2006.

## Features
- Conduct and configure the training of multiple machine learning models.

## Technology stack

- Python
  - OS
  - Pandas
  - numpy
  - Scikit-learn
  - mathplotlib

## Setup

1. Create a directory called `datasets` in the project root or the directory will be created during startup to enable automatic dataset detection. If feature is not desired, go to the third step.
2. Add CSV files containing datasets to the previously created directory.
3. Dasets containing categorical features requires additional configuration, which can be accomplished through two alternatives:
    - The first alternative is to rename 'sample.dataset_configuration.json'in the directory called `configuration` to `dataset_configuration.json'. Define each feature based on the sample, which should be removed. 
    - The second alternative is to follow the instructions which are displayed if no configuration is found, while categorical features are found in the datasets.
4. Install the required dependencies by executing:

```bash
pip install -r requirements.txt
```

## Usage

1. Execute `main.py` to start the project.
2. Follow the instructions.
