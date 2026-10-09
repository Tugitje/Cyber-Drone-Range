# Installatie ArduPilot SITL

Deze handleiding beschrijft hoe je ArduPilot SITL (Software-in-the-Loop) installeert op een Ubuntu 26.04-VM en een eerste gesimuleerde vlucht uitvoert.

## 1. Vereisten

- VirtualBox 7.2 of nieuwer (andere hypervisors zijn niet getest)
- Ubuntu 26.04.1 LTS Desktop-ISO
- VM-instellingen: zie [config/versies.md](../config/versies.md)

Maak na de installatie van Ubuntu direct een snapshot ("Schone Ubuntu 26.04.1"). Die gebruik je voor installatietests.

### Problemen bij het installeren van Ubuntu

- **Zwart scherm na het opstartmenu:** kies "Ubuntu (safe graphics)" en wacht 2 à 3 minuten.
- **Rode `vmwgfx`-meldingen:** zet de grafische controller op VBoxSVGA in plaats van VMSVGA.
- **VM erg traag (groen schildpadje in de statusbalk):** Hyper-V in Windows staat aan. Zet Hyper-V, Virtual Machine Platform, Windows Hypervisor Platform en Geheugenintegriteit uit, en voer als administrator `bcdedit /set hypervisorlaunchtype off` uit. Herstart daarna Windows.

## 2. Snelle installatie met het script

```bash
sudo apt update && sudo apt install -y git
git clone <url van onze repository> ~/drone-cyber-range
bash ~/drone-cyber-range/scripts/install-sitl.sh
```

Het script duurt 30 à 60 minuten, vooral door het bouwen van wxPython. Log daarna uit en weer in, en ga verder met [stap 4](#4-eerste-vlucht).

## 3. Handmatige installatie

Gebruik dit als het script niet werkt, of om te begrijpen wat het script doet.

### 3.1 Systeem bijwerken

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git
```

### 3.2 ArduPilot ophalen op een vaste versie

```bash
cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git checkout Copter-4.7.1
git submodule update --init --recursive
git tag --points-at HEAD    # moet Copter-4.7.1 tonen
```

Na de checkout meldt git een "detached HEAD". Dat is normaal.

Gebruik `git tag --points-at HEAD` om de versie te controleren, niet `git describe`. `git describe` kan een andere tag tonen die op hetzelfde punt staat.

### 3.3 Installatiescript aanpassen voor Ubuntu 26.04

Het installatiescript van ArduPilot Copter-4.7.1 kent Ubuntu 26.04 ("resolute") nog niet. Zonder aanpassing probeert het een niet-bestaand pakket (`python3-argparse`) te installeren en maakt het geen Python-venv aan. De volgende commando's laten het script resolute behandelen als Ubuntu 25.10 ("questing"), met SFML 3.0:

```bash
cd ~/ardupilot
F=Tools/environment_install/install-prereqs-ubuntu.sh
sed -i "s/== 'questing' \]/== 'questing' ] || [ \${RELEASE_CODENAME} == 'resolute' ]/g" $F
sed -i "s/!= 'questing' \]/!= 'questing' ] \&\& [ \${RELEASE_CODENAME} != 'resolute' ]/" $F
sed -i "/'resolute' \]; then/,/PIP=/ s/\"2.6\"/\"3.0\"/" $F
grep -c "resolute" $F    # moet 9 tonen
```

### 3.4 Tijdelijke map op schijf instellen

Op Ubuntu 26.04 staat `/tmp` in het werkgeheugen en heeft het een limiet per gebruiker. Het bouwen van wxPython past daar niet in ("Disk quota exceeded"). Gebruik daarom een tijdelijke map op schijf:

```bash
mkdir -p ~/tmp
export TMPDIR=~/tmp
```

### 3.5 Installatiescript uitvoeren

Voer dit uit in dezelfde terminal als stap 3.4:

```bash
cd ~/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
rm -rf ~/tmp
```

Het script is klaar als je `Done!` en `install-prereqs-ubuntu.sh end` ziet.

### 3.6 Nieuwe instellingen laden

Log uit en weer in, of voer `. ~/.profile` uit. Controleer daarna:

```bash
which sim_vehicle.py
which mavproxy.py
```

Bij beide hoort een pad terug te komen.

## 4. Eerste vlucht

Start de simulatie in een terminal in het VM-venster zelf. Via SSH openen de kaart en de console niet.

```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py --console --map
```

De eerste keer wordt SITL gebouwd (5 à 15 minuten). Daarna openen een console-venster en een kaart. De drone start standaard op een vliegveld bij Canberra (Australië).

Wacht tot in de console `EKF3 IMU0 is using GPS` of `Pre-arm good` staat. Typ dan in de terminal (prompt `STABILIZE>`):

| Commando | Wat het doet |
|---|---|
| `mode guided` | De drone volgt commando's van buitenaf |
| `arm throttle` | Motoren aan; geef binnen ±10 seconden het volgende commando |
| `takeoff 10` | Opstijgen naar 10 meter |
| `mode circle` | Rondjes vliegen rond de huidige positie |
| `guided -35.3625 149.1660 10` | Naar een punt vliegen (breedtegraad lengtegraad hoogte, met punten) |
| `mode rtl` | Terugkeren naar de startplek en landen |
| `mode land` | Direct op de huidige plek landen |

Stoppen: druk op **Ctrl + C** in de terminal. Blijven er processen hangen:

```bash
pkill -f arducopter
pkill -f mavproxy
```

## 5. Hoe de onderdelen communiceren

```
ArduPilot SITL ──TCP 5760──► MAVProxy ──UDP 14550──► QGroundControl
                                      └─UDP 14551──► (vrij voor scripts)
```

ArduPilot SITL wacht op TCP-poort 5760. `sim_vehicle.py` start MAVProxy, dat het MAVLink-verkeer doorstuurt naar UDP-poort 14550 (en 14551). QGroundControl luistert standaard op 14550 en verbindt automatisch.

## 6. Bekende problemen

| Probleem | Oorzaak | Oplossing |
|---|---|---|
| Zwart scherm bij opstarten ISO | Grafische driver in de VM | "Ubuntu (safe graphics)" kiezen; VBoxSVGA gebruiken |
| `Unable to locate package python3-argparse` | Script kent Ubuntu 26.04 niet | Stap 3.3 |
| `Disk quota exceeded` bij wxPython | `/tmp` te klein op Ubuntu 26.04 | Stap 3.4 |
| `sim_vehicle.py: command not found` | Pad nog niet geladen | `. ~/.profile` of opnieuw inloggen |
| Rechtsklikmenu op de kaart werkt niet | Wayland | Start met `GDK_BACKEND=x11 sim_vehicle.py --console --map`, of gebruik QGroundControl |
| `could not convert string` bij `guided` | Getal verkeerd getypt | Punten gebruiken (`-35.3625`), spaties tussen de getallen |
| Gedeeld klembord VirtualBox werkt niet | Wayland | Via SSH werken, zie hieronder |

### Werken via SSH vanuit Windows

In de VM:

```bash
sudo apt install -y openssh-server
```

In PowerShell op Windows, met de VM uit:

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "CyberDroneRange" --natpf1 "ssh,tcp,,2222,,22"
```

Start de VM en verbind met:

```powershell
ssh -p 2222 <gebruikersnaam>@127.0.0.1
```

Vervang `CyberDroneRange` door de naam van je VM.

## 7. Volgende stap

QGroundControl installeren en verbinden met SITL, en een eerste missie plannen. Deze handleiding wordt dan aangevuld.
