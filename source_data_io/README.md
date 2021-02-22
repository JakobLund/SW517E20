# Source Data IO
This module collects the fucntionality to convert a Python object to a JSON file and back. The module builds on defined JSOn schemas that are used to generalize the files that should be written and read using the module. 

## Add new data type
Additional schemas and associated Python objects can be added to the module. This can be done by defining a JSON schema and a Python object that extends the ``Model`` class. This ensures that the object can be converted to and from a JSON file using the module.

By extending the ``Model`` class, the resulting JSON file will contain meta-data about the genration of itself, as well as the object converted.

## Using
First add the custom index url to your pip.conf run `pip3.8 config list -v` to find the approperiate config file. Insert the following:

```
[global]
extra-index-url = https://repos.knox.cs.aau.dk/
```

### Install via pip
```
pip install knox-source-data-io
```

## Build
```
python3.8 setup.py sdist bdist_wheel
```

## requirements.txt
All requirements stored in the _requirements.txt_ file can be install using the command:
```
pip install -r requirements.txt
```
This is all that is needed to install all modules and packages needed to run the module.

If additions are made to the list of requirements, i.e. new dependencies are added to the module, the _requirements.txt_ file can be updated to include all modules and packages installed in the current virtual environment by running the command:
```
pip freeze -l > requirements.txt
```

>:warning: ``pip freeze -l > requirements.txt`` will overwrite the file and include ALL moduels and packages installed in the current virtual environment, not only the ones used.

## Python installation Linux
```
// Install latest python (replace version)
sudo apt install build-essential libssl-dev
sudo apt install python3.9 python3.9-dev python3.9-distutils python3.9-venv

// Install pip
python3.9 -m pip install pip

// Generate virtual environment
cd /project/folder
python3.9 -m venv venv

// Activate virtual environment
cd /project/folder
source venv/bin/activate
pip3.9 install wheel

// Deactivate virtual environment
deactivate
```
