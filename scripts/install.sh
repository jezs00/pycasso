#! /usr/bin/bash
# Due to the similarity in projects, a lot of this is based on TomWhitwell's install script from SlowMovie
# https://github.com/TomWhitwell/SlowMovie/blob/main/Install/install.sh

GIT_REPO=https://github.com/jezs00/pycasso
GIT_BRANCH=main
SKIP_DEPS=false

RC_DIR=/etc/rc.local

function install_linux_packages(){
  sudo apt-get update
  sudo apt-get install -y git python3-pip libatlas-base-dev pass gnupg2
}

function install_python_packages(){
  pip3 install -r "$LOCAL_DIR/Install/requirements.txt" -U
  # Uninstall and reinstall grpcio manually until we can confirm another fix
  pip3 uninstall grpcio grpcio-tools
  pip3 install grpcio==1.44.0 --no-binary=grpcio grpcio-tools==1.44.0 --no-binary=grpcio-tools
}

function setup_hardware(){
  echo "Setting up SPI"
  if ls /dev/spi* &> /dev/null; then
      echo -e "SPI already enabled"
  else
      if command -v raspi-config > /dev/null && sudo raspi-config nonint get_spi | grep -q "1"; then
          sudo raspi-config nonint do_spi 0
          echo -e "SPI is now enabled"
      else
          echo -e "${RED}There was an error enabling SPI, enable manually with sudo raspi-config${RESET}"
      fi
  fi
}

function install_pycasso(){

  FIRST_TIME=1  # if this is a first time install

  if [ "$SKIP_DEPS" = false ]; then
    # install from apt
    install_linux_packages

    # configure the hardware
    setup_hardware
  else
    echo -e "Skipping dependency installs, updating pycasso code only"
  fi

  if [ -d "${LOCAL_DIR}" ]; then
    echo -e "Existing Install Found - Updating Repo"
    cd "$LOCAL_DIR" || exit
    git fetch
    git checkout $GIT_BRANCH
    git pull
  else
    echo -e "No Install Found - Cloning Repo"
    git clone -b ${GIT_BRANCH} ${GIT_REPO} "${LOCAL_DIR}"
    FIRST_TIME=0
  fi

  # generate default config files and prompts
  if [ ! -f "${LOCAL_DIR}/.config" ]; then
    cp "${LOCAL_DIR}/examples/.config-example" "${LOCAL_DIR}/.config"
  fi

  if [ ! -f "${LOCAL_DIR}/prompts/artists.txt" ]; then
    cp "${LOCAL_DIR}/examples/prompts/artists-example.txt" "${LOCAL_DIR}/prompts/artists.txt"
  fi

  if [ ! -f "${LOCAL_DIR}/prompts/subjects.txt" ]; then
    cp "${LOCAL_DIR}/examples/prompts/subjects-example.txt" "${LOCAL_DIR}/prompts/subjects.txt"
  fi

  if [ ! -f "${LOCAL_DIR}/prompts/prompts.txt" ]; then
    cp "${LOCAL_DIR}/examples/prompts/prompts-example.txt" "${LOCAL_DIR}/prompts/prompts.txt"
  fi

  if [ "$SKIP_DEPS" = false ]; then
    # install any needed python packages
    install_python_packages

  fi

  cd "$LOCAL_DIR" || exit

  echo -e "pycasso install/update complete. To test, run 'python3 ${LOCAL_DIR}/examples/review_screen.py'"

  return $FIRST_TIME
}

install_pycasso