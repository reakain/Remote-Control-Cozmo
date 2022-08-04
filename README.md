# Remote Control Cozmo

Made a little pygame setup with pycozmo for a remote controlled cozmo with camera feed and game controller control.

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


##### Adding Pycozmo from Source
If you want to do pycozmo development or use pycozmo from source, rather than through pip, it gets a little more screamy.

1. If your virtual environment is not currently active, activate it with ```source ./venv/Scripts/activate```
2. Uninstall the pip version of pycozmo we used previously with ```pip uninstall pycozmo```
2. Navigate to your pycozmo source folder (probably something like ```cd ../pycozmo```)
3. Install pycozmo with ```python setup.py install```
4. Navigate back to this project directory.

## Usage

### Running the Software
To run it with Cozmo:

1. Connect your PC to the Cozmo wireless network
2. Connect a joystick
3. Activate your virtual environment if it is not already activated
4. Call ```python main.py```
5. You should see Cozmo connect and display eyes, and a display from Cozmo's on board camera should appear on your computer

To run without Cozmo for testing, use ```python main.py nocozmo```

To get input info on the display use ```python main.py debug``` (you can include both nocozmo and debug commands)

To get help info on usage use ```python main.py -h```

### Controller Inputs
These are the mappings as tested with a PS3 controller

 - *Left Joystick:* Wheel control
    - *Up/Down:* Drive forward
    - *Left/Right:* Turn
 - *Right Joystick:* Head tilt and arm lift control
    - *Up/Down:* Head tilt
    - *Left/Right:* Arm lift
 - *Face Buttons:* Display Expressions
    - *X:* Happy
    - *Circle:* Angry
    - *Square:* Sad
    - *Triangle:* Random
 - *Left/RightBumpers:* Play sound


### Testing
The code was tested on Windows 10 Pro using git bash running git for windows. A Playstation Dualshock 3 controller was used, connected via USB with the [DsHidMini driver](https://github.com/ViGEm/DsHidMini). The Cozmo was an original Anki Cozmo using the last released firmware (which is included in the pycozmo resource install when following pycozmo setup instructions).

## Capabilities

### Completed

 - Cozmo camera feed
 - Cozmo wheel control via joystick
 - Cozmo head angle control via joystick
 - Cozmo lift arm control via joystick

### Todo
These functions all currently have placeholder logic in the code, but still require the pycozmo client call integration

 - Cozmo expressions to the Cozmo display
 - Cozmo audio out


## References
1. [PyCozmo](https://github.com/zayfod/pycozmo)
2. [DsHidMini PS3 Controller Driver](https://github.com/ViGEm/DsHidMini)