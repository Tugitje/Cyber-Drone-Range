# Drone Cyber Range

Een geïsoleerde en reproduceerbare testomgeving waarin studenten en onderzoekers de beveiliging van een dronesysteem gecontroleerd kunnen onderzoeken.

## Aan de slag

- Installatie en eerste vlucht: [Documentatie/installatie-sitl.md](Documentatie/installatie-sitl.md)
- QGroundControl installeren en verbinden: [Documentatie/installatie-qgc.md](Documentatie/installatie-qgc.md)
- Normaal MAVLink-verkeer opnemen en analyseren (baseline): [Documentatie/baseline-procedure.md](Documentatie/baseline-procedure.md)
- Referentievlucht automatisch opnemen: `scripts/run-vlucht.sh`, zie [missions/README.md](missions/README.md)
- Commando's kopiëren en plakken via SSH vanuit Windows: [Documentatie/ssh-verbinding.md](Documentatie/ssh-verbinding.md)
- Gebruikte versies: [config/versies.md](config/versies.md)
- Bevindingen en bekende problemen: [Documentatie/bevindingen.md](Documentatie/bevindingen.md)

Snelle installatie op een schone Ubuntu 26.04-VM:

```bash
git clone <url van deze repository> ~/drone-cyber-range
bash ~/drone-cyber-range/scripts/install-sitl.sh
```

## Mappen

| Map | Inhoud |
|---|---|
| `Documentatie/` | Handleidingen, ontwerp en bevindingen |
| `config/` | Versies en (later) parameterbestanden |
| `scripts/` | Installatie-, hulp en run-scripts |
| `patches/` | Aanpassingen op externe software (indien nodig) |
| `missions/` | Missiebestanden, zoals de referentiemissie `baseline.txt` |
| `tools/wireshark/` | MAVLink-dissector voor Wireshark en tshark |
| `tools/analysis/` | Analysescripts voor opnames, zoals `baseline_simpel.py` |
| `results/` | Resultaten per vlucht (`vluchten/`) en samenvattingen van metingen (`baseline/`); geen grote pcap-bestanden |

De broncode van ArduPilot staat niet in deze repository. Die wordt door het installatiescript opgehaald op een vaste versie.

## Werkafspraken

- `main` bevat altijd een werkende versie.
- Werk op een eigen branch per taak, bijvoorbeeld `feature/qgc-installatie`.
- Wijzigingen gaan via een pull request met minimaal één review van een ander groepslid.
- Geen wachtwoorden, sleutels, VM-images of grote logbestanden in de repository.
