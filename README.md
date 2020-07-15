![test](https://github.com/greenbird/p360-contact-manager/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/greenbird/p360-contact-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/p360-contact-manager)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# P360 Contact Manager

## Why

While there are built in methods to syncronize against for example brønnøysundregisteret, to enrich data or update data they are slow and point and click oriented.
There are also cases where duplicates are created by external programs.
This program tries to fix some of those issues.


## How

P360 exposes an API for dealing with contacts. It is through this api that we find, update, and fix enterprises in p360.


## Setup

easier setup will be available if the package goes to pypi. Then it would be as simple as doing pip install p360-contact-manager and use it directly like:

```sh
$ python p360_contact_manager args args action
```

But for now we install it from source. so clone the repo first. then:

### Get poetry

get poetry - dependency management:
```sh
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Make poetry create virtualenv in project folder. This makes it easier for IDE's to run correct virtualenv while debuging/running linters etc.
```sh
$ poetry config settings.virtualenvs.in-project true
```

### Get Pyenv - optional

pyenv is a nice tool that lets you 'activate' a version of python either globally, locally or for one shell instance. its really nice and i reccomend getting it and using it now but it is not needed for this program to work.

with brew:
```sh
$ brew update
$ brew install pyenv
```

Put this command into the of `~/.bash_profile` or run `pyenv init` to make sure where to put it for for example zsh.
```
$ eval "$(pyenv init -)"
```

install a version of python 3.7.2+: This installs a clean python to pyenvs folders and lets us reference that as a 'base' in our virtualenvs.
```sh
$ pyenv install 3.7.4
```

## Usage

if you did install pyenv activate pyenv for the current shell
```sh
$ pyenv shell 3.7.4
```

Run this to install required packages and a virtualenv
- if you do not plan on developing on this, add the flag: --no-dev
```sh
$ poetry install
```

### Test

```sh
$ poetry run python p360_contact_manager --authkey the_key test
```

### Create a 'Cache'(json file) of all enterprises in p360
```sh
poetry run python p360_contact_manager --authkey the_key cache_enterprises
```
add -c or --cached argument to use local cached json file.


### Create duplicate worklist
```sh
poetry run python p360_contact_manager --authkey the_key duplicates -c
```

### Update with worklist
tip: use --dry to check if everything looks good before continuing
```sh
$ poetry run python p360_contact_manager --authkey the_key update --worklist json_worklist_file.json
```

### Create Brreg data syncronize worklist
for now just add the key even though its not needed its flagged as required... will fix.
```sh
$ poetry run python p360_contact_manager --authkey the_key brreg_syncronize
```

### Call synchronize with brreg data worklist
```sh
$ poetry run python p360_contact_manager --authkey the_key synchronize --worklist brreg_synchronize_worklist.json
```
