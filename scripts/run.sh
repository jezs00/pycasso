#! /usr/bin/bash

PARENT_DIR=$( dirname -- "${BASH_SOURCE[0]}")
VENV_DIR=$(realpath "${PARENT_DIR}")/venv
SCRIPT_DIR=$( cd -- "${PARENT_DIR}" &> /dev/null && pwd )

#Run from venv if available
if [ -d "${VENV_DIR}" ]; then
  source "${VENV_DIR}"/bin/activate
  echo -e "Activated virtual environment from ${VENV_DIR}/bin/activate"
else
  echo -e "${VENV_DIR}/bin/activate not found to create virtual environment"
fi

echo -n 'db' | gnome-keyring-daemon --unlock
python3 "${SCRIPT_DIR}/run.py"