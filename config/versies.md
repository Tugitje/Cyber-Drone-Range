# Gebruikte versies

Deze versies zijn getest. Wijk je ergens van af, noteer dat dan hier en in [Documentatie/bevindingen.md](../Documentatie/bevindingen.md).

| Onderdeel | Versie | Opmerking |
|---|---|---|
| VirtualBox | 7.2.20 | Op Windows-host |
| Besturingssysteem VM | Ubuntu 26.04.1 LTS (resolute) | Desktop-ISO |
| ArduPilot | Copter-4.7.1 | Git-tag; controleren met `git tag --points-at HEAD` |
| MAVProxy | meegeleverd door installatiescript ArduPilot | Versie noteren met `mavproxy.py --version` |
| QGroundControl | nog invullen | AppImage |

## Aanbevolen VM-instellingen

| Instelling | Waarde |
|---|---|
| CPU-kernen | 4 of meer |
| Werkgeheugen | 8 GB |
| Virtuele schijf | 60 GB (25 GB is te krap) |
| Grafische controller | VBoxSVGA, 128 MB videogeheugen |
| 3D-acceleratie | Uit tijdens installatie, daarna optioneel aan |
