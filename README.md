# Remote Control Cozmo

Made a little pygame setup with pycozmo for a remote controlled cozmo. It still needs to add in the expressions and sounds.

## Environment Setup
This application uses Python 3, and these instructions assume python3 is set as your default python command. You can check your version with ```python --version```

Additionally, all of my instructions are based on using git bash through git for Windows and generic Python 3. If you're on Linux, Mac, or using pycharm or conda your mileage will vary.

- *Note:* If your Python 3 is called with ```python3``` then you use that for all python command instances, and your pip commands will be ```pip3```

#### Virtual Environment

1. In bash (or git bash on Windows) navigate to this respository folder, then create your virtual environment with ```python -m venv ./venv```
2. Once complete activate your environment with ```source ./venv/Scripts/activate```
3. Update pip with ```python -m pip install --upgrade pip```
3. Install the requirements once activated with ```pip install -r requirements.txt```
4. If you install any additional libraries, update the requirements with ```pip freeze > requirements.txt```
5. Exit the virtual environment with ```deactivate```

##### Adding Pycozmo Via Pip
If you just want to use pycozmo as on pip.

1. If your virtual environment is not currently active, activate it with ```source ./venv/Scripts/activate```
2. Install pycozmo through pip with ```pip install pycozmo==0.8.0```

##### Adding Pycozmo from Source
If you want to do pycozmo development it can get a bit more screamy.

1. If your virtual environment is not currently active, activate it with ```source ./venv/Scripts/activate```
2. Navigate to your pycozmo source folder (probably something like ```cd ../pycozmo```)
3. Install pycozmo with ```python setup.py install```
4. Navigate back to this project directory.

## Usage
List all functions:

``` python main.py -h```

## Capabilities


## References
1. [PyCozmo](https://github.com/zayfod/pycozmo)