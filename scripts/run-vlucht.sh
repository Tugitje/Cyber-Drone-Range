#!/usr/bin/env bash
# Start een opname en ArduPilot SITL in één keer.
# Ctrl + C stopt SITL én de opname; daarna wordt de opname direct geanalyseerd.
#
# Gebruik:  scripts/run-vlucht.sh [naam] [extra opties voor sim_vehicle.py]
# Voorbeeld: scripts/run-vlucht.sh baseline --out=udp:10.0.2.2:14550

set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
# Eerste argument is de naam, tenzij het met '-' begint (dan is het een SITL-optie)
if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then
  NAAM="$1"; shift
else
  NAAM="vlucht"
fi
NAAM="${NAAM}_$(date +%Y%m%d_%H%M%S)"
# Zonder --out: standaard ook naar QGroundControl op de Windows-host sturen
case " $* " in
  *" --out"*) ;;
  *) set -- "$@" --out=udp:10.0.2.2:14550 ;;
esac
echo "SITL-opties: $*"
OPNAME="$HOME/captures/$NAAM.pcap"
UIT="$REPO/results/vluchten/$NAAM"
mkdir -p "$HOME/captures" "$UIT"

sudo -v || exit 1                       # wachtwoord nu vragen, niet halverwege
trap ':' INT                            # dit script blijft draaien na Ctrl + C

echo "Opname start: $OPNAME"
# Geen terminal voor sudo/tcpdump: anders leest sudo mee met het toetsenbord
# en komen MAVProxy-commando's verminkt aan.
sudo -n tcpdump -i any -Z "$USER" -w "$OPNAME" 'tcp port 5760 or udp portrange 14550-14551' \
  < /dev/null > "$UIT/tcpdump.log" 2>&1 &
DUMP_PID=$!
sleep 2

cd "$HOME/ardupilot/ArduCopter"
sim_vehicle.py "$@"                     # stop met Ctrl + C

sudo pkill -INT -f "tcpdump.*$NAAM" 2>/dev/null
wait "$DUMP_PID" 2>/dev/null
cp -f mav.tlog "$UIT/$NAAM.tlog" 2>/dev/null

echo "Analyseren..."
python3 "$REPO/tools/analysis/baseline_simpel.py" "$OPNAME" | tee "$UIT/samenvatting.txt"
echo "Klaar. Opname: $OPNAME  Resultaat: $UIT/"
