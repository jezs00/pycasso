#! /usr/bin/bash
# Due to the similarity in projects, a lot of this is based on TomWhitwell's install script from SlowMovie
# https://github.com/TomWhitwell/SlowMovie/blob/main/Install/install.sh

GIT_REPO=https://github.com/jezs00/pycasso
GIT_BRANCH=main
SKIP_DEPS=false

# Set the local directory
LOCAL_DIR="$HOME/$(basename $GIT_REPO)"

# File paths
SERVICE_DIR=/etc/systemd/system
SERVICE_FILE=pycasso.service
SERVICE_FILE_TEMPLATE=pycasso.service.template
KEY_SCRIPT=scripts/set_keys.py
LED_SCRIPT=scripts/pijuice_disable_leds.py

# Color code variables
RED="\e[0;91m"
YELLOW="\e[0;93m"
RESET="\e[0m"

function install_linux_packages(){
  sudo apt-get update
  sudo apt-get install -y git python3-pip libatlas-base-dev pass gnupg2
}

function install_pijuice_package(){
  # Install pijuice.
  sudo apt-get install -y pijuice-base pijuice-gui
}

function install_python_packages(){
  sudo pip3 install git+https://github.com/jezs00/pycasso
  sudo pip3 install grpcio grpcio-tools
  sudo pip3 install stability-sdk @ git+https://github.com/Stability-AI/stability-sdk.git --ignore-installed grpcio grpcio-tools
  sudo pip3 install openai @ git+https://github.com/openai/openai-python.git
}

function uninstall_python_packages(){
  sudo pip3 uninstall piblo
}

function fix_grpcio(){
  sudo pip3 uninstall grpcio grpcio-tools
  sudo pip3 install grpcio==1.44.0 --no-binary=grpcio grpcio-tools==1.44.0 --no-binary=grpcio-tools
}

function set_key(){
  sudo dbus-run-session python3 "${LOCAL_DIR}/${KEY_SCRIPT}"
}

function disable_leds(){
  sudo python3 "${LOCAL_DIR}/${LED_SCRIPT}"
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

function service_installed(){
  # return 0 if the service is installed, 1 if no
  if [ -f "$SERVICE_DIR/$SERVICE_FILE" ]; then
    return 0
  else
    return 1
  fi
}

function copy_service_file(){
  sudo mv $SERVICE_FILE $SERVICE_DIR
  sudo systemctl daemon-reload
}

function install_service(){
  if [ -d "${LOCAL_DIR}" ]; then
    cd "$LOCAL_DIR" || return

    # generate the service file
    envsubst <$SERVICE_FILE_TEMPLATE > $SERVICE_FILE

    if ! (service_installed); then
      # install the service files and enable
      copy_service_file
      sudo systemctl enable pycasso

      echo -e "pycasso service installed! Use ${YELLOW}sudo systemctl start pycasso${RESET} to test"
    else
      echo -e "${YELLOW}pycasso service is installed, checking if it needs an update${RESET}"
      if ! (cmp -s "pycasso.service" "/etc/systemd/system/pycasso.service"); then
        copy_service_file
        echo -e "Updating pycasso service file"
      else
        # remove the generated service file
        echo -e "No update needed"
        rm $SERVICE_FILE
      fi
    fi
  else
    echo -e "${RED}pycasso repo does not exist! Use option 1 - Install/Upgrade pycasso first${RESET}"
  fi

  # go back to home
  cd "$HOME" || return
}

function uninstall_service(){
  if (service_installed); then
    # stop if running and remove service files
    sudo systemctl stop pycasso
    sudo systemctl disable pycasso
    sudo rm "${SERVICE_DIR}/${SERVICE_FILE}"
    sudo systemctl daemon-reload

    echo -e "pycasso service was successfully uninstalled"
  else
    echo -e "${RED}pycasso service is already uninstalled.${RESET}"
  fi
}

function install_pycasso(){

  # check if service is currently running and stop if it is
  RESTART_SERVICE="FALSE"

  if (systemctl is-active --quiet pycasso); then
    sudo systemctl stop pycasso
    RESTART_SERVICE="TRUE"
  fi

  FIRST_TIME=1  # if this is a first time install

  if [ "${SKIP_DEPS}" = false ]; then
    # install from apt
    install_linux_packages

    # configure the hardware
    setup_hardware
  else
    echo -e "Skipping dependency installs, updating pycasso code only"
  fi

  if [ -d "${LOCAL_DIR}" ]; then
    echo -e "Existing Install Found - Updating Repo"
    cd "${LOCAL_DIR}" || exit
    git fetch
    git checkout $GIT_BRANCH
    git pull
  else
    echo -e "No Install Found - Cloning Repo"
    git clone -b "${GIT_BRANCH}" "${GIT_REPO}" "${LOCAL_DIR}"
    FIRST_TIME=0
  fi

  # generate default config files and prompts
  if [ ! -f "${LOCAL_DIR}/.config" ]; then
    cp "${LOCAL_DIR}/examples/.config-example" "${LOCAL_DIR}/.config"
  fi

  if [ ! -f "${LOCAL_DIR}/prompts" ]; then
    mkdir "${LOCAL_DIR}/prompts"
  fi

  if [ ! -f "${LOCAL_DIR}/images" ]; then
    mkdir "${LOCAL_DIR}/images"
  fi

  if [ ! -f "${LOCAL_DIR}/images/generated" ]; then
    mkdir "${LOCAL_DIR}/images/generated"
  fi

  if [ ! -f "${LOCAL_DIR}/images/external" ]; then
    mkdir "${LOCAL_DIR}/images/external"
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

  cd "${LOCAL_DIR}" || exit

  echo -e "pycasso install/update complete. To test, run ${YELLOW}'python3 ${LOCAL_DIR}/examples/review_screen.py'${RESET}"

  return $FIRST_TIME
}

INSTALL_OPTION=0

while [ $INSTALL_OPTION -ne 9 ]
do
 INSTALL_OPTION=$(whiptail --menu "\


    █ ▄▄ ▀▄    ▄ ▄█▄    ██      ▄▄▄▄▄    ▄▄▄▄▄   ████▄
    █   █  █  █  █▀ ▀▄  █ █    █     ▀▄ █     ▀▄ █   █
    █▀▀▀    ▀█   █   ▀  █▄▄█ ▄  ▀▀▀▀▄ ▄  ▀▀▀▀▄   █   █
    █       █    █▄  ▄▀ █  █  ▀▄▄▄▄▀   ▀▄▄▄▄▀    ▀████
     █    ▄▀     ▀███▀     █
      ▀                   █
                         ▀

  Repo set to '${GIT_REPO}/${GIT_BRANCH}'
  Setting up in local directory '${LOCAL_DIR}'

  Choose what you want to do." 0 0 0 \
 1 "Install/Upgrade pycasso" \
 2 "Install pycasso Service" \
 3 "Install pijuice" \
 4 "Apply GRPCIO Fix" \
 5 "Set an API key" \
 6 "Disable pijuice LEDs" \
 7 "Uninstall pycasso" \
 8 "Uninstall pycasso Service" \
 9 "Exit Setup" \
 3>&1 1>&2 2>&3)

 : "${INSTALL_OPTION:=9}"

 if [ $INSTALL_OPTION -eq 1 ]; then

   # Prompt for service install if the first time being run (whiptail 1=No)
   INSTALL_SERVICE=1
   if [ ! -d "${LOCAL_DIR}" ]; then
     if whiptail --yesno "Would you like to install the pycasso service to start on boot?" 0 0; then
       INSTALL_SERVICE=0
     else
       INSTALL_SERVICE=1
     fi
   fi

   # Install or update
   install_pycasso

   # Install service, if desired
   if [ $INSTALL_SERVICE -eq 0 ]; then
     install_service
   fi

   if whiptail --yesno "Would you like to install pijuice?" 0 0; then
     INSTALL_PIJUICE=0
   else
     INSTALL_PIJUICE=1
   fi

   if [ $INSTALL_PIJUICE -eq 0 ]; then
     install_pijuice_package
   fi

 elif [ $INSTALL_OPTION -eq 2 ]; then
   # Install the service
   install_service
 elif [ $INSTALL_OPTION -eq 3 ]; then
   # Install pijuice
   install_pijuice_package
 elif [ $INSTALL_OPTION -eq 4 ]; then
   # Fix GRPCIO with version decrement
   fix_grpcio
 elif [ $INSTALL_OPTION -eq 5 ]; then
   # Uninstall pycasso
   set_key
 elif [ $INSTALL_OPTION -eq 6 ]; then
   # Run python script to disable leds on pijuice
   disable_leds
 elif [ $INSTALL_OPTION -eq 7 ]; then
   # Uninstall pycasso
   uninstall_python_packages
   uninstall_service
 elif [ $INSTALL_OPTION -eq 8 ]; then
   # Uninstall the service
   uninstall_service
 fi
done


if [ "${RESTART_SERVICE}" = "TRUE" ] && (service_installed); then
  sudo systemctl start pycasso
fi