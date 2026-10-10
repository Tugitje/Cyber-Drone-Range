# Installatie QGroundControl

QGroundControl (QGC) is het Ground Control Station van de cyber range: de "afstandsbediening" en missieplanner voor de operator. QGC verstuurt commando's en missies via MAVLink naar ArduPilot SITL en toont de telemetrie die de drone terugstuurt. De autopilot (SITL) voert de commando's zelf uit.

Voorwaarde: ArduPilot SITL is geïnstalleerd volgens [installatie-sitl.md](installatie-sitl.md).

## 1. Benodigde pakketten

Dit kan via SSH. De venv mag daarbij actief zijn.

```bash
sudo usermod -aG dialout $USER
sudo apt remove -y modemmanager
sudo apt install -y gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl \
  libfuse2t64 libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0
```

| Pakket of stap | Waarom |
|---|---|
| `dialout`-groep | Toegang tot seriële poorten, nodig zodra er later een echte flight controller (Pixhawk) wordt aangesloten |
| `modemmanager` verwijderen | Dit programma claimt seriële poorten en verstoort de verbinding met een flight controller |
| GStreamer-pakketten | Videoweergave in QGC |
| `libfuse2t64` | Nodig om een AppImage te starten. Op oudere Ubuntu-versies heet dit pakket `libfuse2` |
| `libxcb-*`, `libxkbcommon-x11-0` | Grafische bibliotheken voor QGC |

Log daarna uit en weer in, zodat de groepswijziging actief wordt.

## 2. Downloaden

Open Firefox in de VM en ga naar de officiële documentatie: **docs.qgroundcontrol.com** → *Getting Started* → *Download and Install* → *Ubuntu Linux*. Download de **AppImage**.

Maak het bestand uitvoerbaar (één keer):

```bash
chmod +x ~/Downloads/QGroundControl*.AppImage
```

Let op de hoofdletter: de map heet `Downloads`. Weet je niet waar het bestand staat:

```bash
find ~ -iname "QGroundControl*.AppImage" 2>/dev/null
```

Noteer de versie van QGC in [config/versies.md](../config/versies.md).

## 3. Verbinden met de simulatie

Doe dit in het VM-venster zelf. QGC en de kaart van MAVProxy werken niet via SSH.

**Terminal 1: SITL starten**

```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py --console --map
```

Wacht tot de drone GPS heeft (`EKF3 IMU0 is using GPS` in de console).

**Terminal 2: QGroundControl starten**

```bash
~/Downloads/QGroundControl*.AppImage
```

Start QGC niet, of zie je een leeg venster:

```bash
QT_QPA_PLATFORM=xcb ~/Downloads/QGroundControl*.AppImage
```

QGC verbindt automatisch. Je ziet de drone op de kaart bij het vliegveld in Canberra, en bovenin staat de status van de drone.

Volgorde: start eerst SITL en daarna QGC. Andersom werkt meestal ook, maar dan duurt het verbinden soms langer.

## 4. Hoe de verbinding werkt

```
ArduPilot SITL ──TCP 5760──► MAVProxy ──UDP 14550──► QGroundControl
                                      └─UDP 14551──► (vrij voor scripts)
```

- ArduPilot SITL wacht op TCP-poort 5760.
- MAVProxy, gestart door `sim_vehicle.py`, verbindt met SITL en stuurt het MAVLink-verkeer door naar UDP-poort 14550 en 14551 op `127.0.0.1`.
- QGC luistert standaard op UDP-poort 14550 en verbindt zodra daar MAVLink-berichten binnenkomen.
- Poort 14551 is vrij voor bijvoorbeeld testscripts (pymavlink).

Berichten die over deze verbinding gaan:

| Richting | Voorbeelden |
|---|---|
| Drone → QGC | `HEARTBEAT` (elke seconde), positie (`GLOBAL_POSITION_INT`), hoogte, batterij, status |
| QGC → drone | Commando's zoals opstijgen en landen (`COMMAND_LONG`), moduswissels, missie-waypoints (`MISSION_ITEM_INT`) |

Je kunt dit verkeer bekijken met Wireshark op de loopback-interface (`lo`), met het filter `udp.port == 14550`.

## 5. Eerste missie

1. Klik linksboven op **Plan**.
2. Kies **Takeoff** en klik daarna een paar punten op de kaart als waypoints.
3. Voeg aan het eind **Return** toe (terug naar de startplek en landen).
4. Klik op **Upload** om de missie naar de drone te sturen.
5. Ga terug naar **Fly**, en start de missie met de schuifknop onderin.
6. Kijk hoe de drone de route vliegt, in QGC en op de kaart van MAVProxy.
7. Sla de missie op via **File → Save** en zet het `.plan`-bestand in de map `missions/` van deze repository.

## 6. Afsluiten

1. Laat de drone landen (`mode rtl` in de SITL-terminal, of via QGC).
2. Sluit QGC.
3. Druk op **Ctrl + C** in de SITL-terminal.

## 7. Bekende problemen

| Probleem | Oorzaak | Oplossing |
|---|---|---|
| `No such file or directory` bij de AppImage | Map heet `Downloads` met hoofdletter | `~/Downloads/...` gebruiken |
| `Permission denied` bij de AppImage | Bestand niet uitvoerbaar | `chmod +x ~/Downloads/QGroundControl*.AppImage` |
| `Unable to locate package libfuse2` | Pakket heet anders op Ubuntu 26.04 | `libfuse2t64` installeren |
| QGC start niet of venster blijft leeg | Wayland | `QT_QPA_PLATFORM=xcb` voor het commando zetten |
| QGC blijft "Disconnected" | SITL draait niet, of MAVProxy stuurt niet naar 14550 | Controleer in de SITL-terminal of er regels met `udp:127.0.0.1:14550` staan; start SITL opnieuw |
