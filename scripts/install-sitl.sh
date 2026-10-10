#!/usr/bin/env bash
# Installeert ArduPilot SITL op een vaste versie.
# Getest op Ubuntu 26.04.1 LTS (resolute) met ArduPilot Copter-4.7.1.
# Gebruik: bash scripts/install-sitl.sh

set -euo pipefail

ARDUPILOT_VERSION="Copter-4.7.1"
ARDUPILOT_DIR="$HOME/ardupilot"
PREREQS="Tools/environment_install/install-prereqs-ubuntu.sh"

stap() { echo; echo "=== $1 ==="; }

stap "Systeempakketten bijwerken"
sudo apt update
sudo apt install -y git lsb-release

stap "ArduPilot ophalen ($ARDUPILOT_VERSION)"
if [ ! -d "$ARDUPILOT_DIR/.git" ]; then
  git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git "$ARDUPILOT_DIR"
fi
cd "$ARDUPILOT_DIR"
git fetch --tags
git checkout "$ARDUPILOT_VERSION"
git submodule update --init --recursive

if ! git tag --points-at HEAD | grep -qx "$ARDUPILOT_VERSION"; then
  echo "FOUT: ArduPilot staat niet op $ARDUPILOT_VERSION." >&2
  exit 1
fi

CODENAME="$(lsb_release -c -s)"
if [ "$CODENAME" = "resolute" ]; then
  stap "Installatiescript aanpassen voor Ubuntu 26.04 (resolute)"
  if grep -q "resolute" "$PREREQS"; then
    echo "Aanpassing is al toegepast, wordt overgeslagen."
  else
    # Behandel resolute als questing (Ubuntu 25.10)
    sed -i "s/== 'questing' \]/== 'questing' ] || [ \${RELEASE_CODENAME} == 'resolute' ]/g" "$PREREQS"
    # Geen python3-argparse voor resolute
    sed -i "s/!= 'questing' \]/!= 'questing' ] \&\& [ \${RELEASE_CODENAME} != 'resolute' ]/" "$PREREQS"
    # Ubuntu 26.04 heeft SFML 3.0
    sed -i "/'resolute' \]; then/,/PIP=/ s/\"2.6\"/\"3.0\"/" "$PREREQS"
  fi
  echo "Aantal regels met 'resolute': $(grep -c resolute "$PREREQS")"
fi

stap "Tijdelijke map op schijf instellen (wxPython past niet in /tmp op 26.04)"
mkdir -p "$HOME/tmp"
export TMPDIR="$HOME/tmp"

stap "Benodigde software installeren (duurt 30 tot 60 minuten)"
"$PREREQS" -y

rm -rf "$HOME/tmp"

stap "Venv en pad instellen voor elke nieuwe terminal (~/.bashrc)"
VENV_LINE='source $HOME/venv-ardupilot/bin/activate'
PATH_LINE='export PATH=$HOME/ardupilot/Tools/autotest:$PATH'
grep -qxF "$VENV_LINE" "$HOME/.bashrc" || echo "$VENV_LINE" >> "$HOME/.bashrc"
grep -qxF "$PATH_LINE" "$HOME/.bashrc" || echo "$PATH_LINE" >> "$HOME/.bashrc"

stap "Klaar"
echo "Open een nieuwe terminal (of log uit en weer in), en start daarna:"
echo "  cd ~/ardupilot/ArduCopter"
echo "  sim_vehicle.py --console --map"
