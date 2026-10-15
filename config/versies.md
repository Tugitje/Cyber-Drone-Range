# Gebruikte versies

Deze versies zijn getest. Vul de ontbrekende versies in vóór de volgende baselinemeting: zonder versies is een meting niet te herhalen. Wijk je ergens van af, noteer dat dan hier en in [Documentatie/bevindingen.md](../Documentatie/bevindingen.md).

| Onderdeel | Versie | Opmerking |
|---|---|---|
| VirtualBox | 7.2.20 | Op Windows-host |
| Besturingssysteem VM | Ubuntu 26.04.1 LTS (resolute) | Desktop-ISO |
| ArduPilot | Copter-4.7.1 | Git-tag; controleren met `git tag --points-at HEAD` |
| MAVProxy | nog invullen | Meegeleverd door het installatiescript van ArduPilot; versie met `mavproxy.py --version` |
| QGroundControl | nog invullen | Windows-installer op de host, via docs.qgroundcontrol.com (Stable V5.1); versie staat in het menu onder het Q-pictogram |
| tcpdump | nog invullen | In de VM; versie met `tcpdump --version` |
| tshark | nog invullen | In de VM; versie met `tshark --version \| head -1` |
| Wireshark | nog invullen | Op de Windows-host; versie in Help → About Wireshark |
| pymavlink | nog invullen | In `venv-ardupilot`; versie met `pip show pymavlink` |

## Aanbevolen VM-instellingen

| Instelling | Waarde |
|---|---|
| CPU-kernen | 4 of meer |
| Werkgeheugen | 8 GB |
| Virtuele schijf | 60 GB (25 GB is te krap) |
| Grafische controller | VBoxSVGA, 128 MB videogeheugen |
| 3D-acceleratie | Uit tijdens installatie, daarna optioneel aan |
