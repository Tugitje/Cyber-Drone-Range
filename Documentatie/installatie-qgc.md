# Installatie QGroundControl

QGroundControl (QGC) is het Ground Control Station van de cyber range: de "afstandsbediening" en missieplanner voor de operator. QGC verstuurt commando's en missies via MAVLink naar ArduPilot SITL en toont de telemetrie die de drone terugstuurt. De autopilot (SITL) voert de commando's zelf uit.

QGC draait op de **Windows-host**, niet in de VM. ArduPilot SITL draait in de VM en stuurt het MAVLink-verkeer naar Windows. Zo blijft de VM lichter en heb je geen last van Wayland of ontbrekende pakketten in Ubuntu.

Voorwaarde: ArduPilot SITL is geïnstalleerd volgens [installatie-sitl.md](installatie-sitl.md), en de VM gebruikt het standaard NAT-netwerk van VirtualBox.

## 1. Downloaden en installeren op Windows

Download QGC voor Windows via de officiële documentatie:

https://docs.qgroundcontrol.com/Stable_V5.1/en/qgc-user-guide/getting_started/download_and_install.html

Kies daar **Windows** en voer de installer uit.

Bij de eerste keer starten vraagt Windows Firewall of QGC het netwerk mag gebruiken. Sta dit toe, anders komen de MAVLink-berichten uit de VM niet binnen.

Noteer de versie van QGC in [config/versies.md](../config/versies.md).

## 2. SITL starten in de VM

MAVProxy stuurt het MAVLink-verkeer standaard alleen naar `127.0.0.1` in de VM zelf. Met `--out` stuur je het ook naar Windows. Binnen het NAT-netwerk van VirtualBox heeft de Windows-host altijd het adres `10.0.2.2`.

**Via SSH** (zie [ssh-verbinding.md](ssh-verbinding.md)):

```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py --out=udp:10.0.2.2:14550
```

**In het VM-venster**, met de console en de kaart van MAVProxy erbij:

```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py --console --map --out=udp:10.0.2.2:14550
```

Wacht tot de drone GPS heeft (`EKF3 IMU0 is using GPS`).

Draait SITL al zonder `--out`? Typ dan in de MAVProxy-terminal:

```
output add 10.0.2.2:14550
```

## 3. QGroundControl verbinden

Start QGC op Windows. QGC luistert standaard op UDP-poort 14550 en verbindt automatisch zodra er MAVLink-berichten binnenkomen. Je ziet de drone op de kaart bij het vliegveld in Canberra, en bovenin staat de status van de drone.

Volgorde maakt niet uit: QGC kan al openstaan voordat SITL start.

## 4. Hoe de verbinding werkt

```
               VM (Ubuntu)                         │   Windows-host
                                                   │
ArduPilot SITL ──TCP 5760──► MAVProxy ──UDP 14550──┼──► QGroundControl
                                │   (via NAT naar 10.0.2.2)
                                └─UDP 14551──► 127.0.0.1 (vrij voor scripts in de VM)
```

- ArduPilot SITL wacht op TCP-poort 5760.
- MAVProxy, gestart door `sim_vehicle.py`, verbindt met SITL en stuurt het MAVLink-verkeer door naar de adressen die met `--out` zijn opgegeven, en standaard naar UDP 14550 en 14551 op `127.0.0.1` in de VM.
- VirtualBox geeft verkeer naar `10.0.2.2` door aan Windows. QGC ontvangt het op UDP-poort 14550 en stuurt zijn commando's via dezelfde weg terug.
- Poort 14551 in de VM is vrij voor bijvoorbeeld testscripts (pymavlink).

Berichten die over deze verbinding gaan:

| Richting | Voorbeelden |
|---|---|
| Drone → QGC | `HEARTBEAT` (elke seconde), positie (`GLOBAL_POSITION_INT`), hoogte, batterij, status |
| QGC → drone | Commando's zoals opstijgen en landen (`COMMAND_LONG`), moduswissels, missie-waypoints (`MISSION_ITEM_INT`) |

Dit verkeer bekijk je met Wireshark in de VM, op de netwerkinterface van de VM (meestal `enp0s3`, controleren met `ip a`), met het filter `udp.port == 14550`.

## 5. Eerste missie

1. Klik linksboven op **Plan**.
2. Kies **Takeoff** en klik daarna een paar punten op de kaart als waypoints.
3. Voeg aan het eind **Return** toe (terug naar de startplek en landen).
4. Klik op **Upload** om de missie naar de drone te sturen.
5. Ga terug naar **Fly**, en start de missie met de schuifknop onderin.
6. Kijk hoe de drone de route vliegt in QGC.
7. Sla de missie op via **File → Save** en zet het `.plan`-bestand in de map `missions/` van deze repository.

## 6. Afsluiten

1. Laat de drone landen (`mode rtl` in de SITL-terminal, of via QGC).
2. Sluit QGC.
3. Druk op **Ctrl + C** in de SITL-terminal.

## 7. Bekende problemen

| Probleem | Oorzaak | Oplossing |
|---|---|---|
| QGC blijft "Disconnected" | SITL is gestart zonder `--out` | SITL opnieuw starten met `--out=udp:10.0.2.2:14550`, of `output add 10.0.2.2:14550` typen in MAVProxy |
| QGC blijft "Disconnected", `--out` staat goed | Windows Firewall blokkeert QGC | Windows-beveiliging → Firewall → Een app toestaan via de firewall → QGroundControl aanvinken |
| QGC blijft "Disconnected", VM gebruikt geen NAT | `10.0.2.2` bestaat alleen in het NAT-netwerk van VirtualBox | Netwerkadapter van de VM op NAT zetten |
