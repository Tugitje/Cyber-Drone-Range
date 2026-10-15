# Drone Cyber Range

Een geïsoleerde en reproduceerbare testomgeving waarin studenten en onderzoekers de beveiliging van een dronesysteem gecontroleerd kunnen onderzoeken.

## Aan de slag

- Installatie en eerste vlucht: [Documentatie/installatie-sitl.md](Documentatie/installatie-sitl.md)
- QGroundControl installeren en verbinden: [Documentatie/installatie-qgc.md](Documentatie/installatie-qgc.md)
- Normaal MAVLink-verkeer opnemen en analyseren (baseline): [Documentatie/baseline-procedure.md](Documentatie/baseline-procedure.md)
- Vlucht automatisch opnemen: zie [hieronder](#vlucht-automatisch-opnemen)
- Commando's kopiëren en plakken via SSH vanuit Windows: [Documentatie/ssh-verbinding.md](Documentatie/ssh-verbinding.md)
- Gebruikte versies: [config/versies.md](config/versies.md)
- Bevindingen en bekende problemen: [Documentatie/bevindingen.md](Documentatie/bevindingen.md)

Achtergrond en projectorganisatie:

- Keuze voor ArduPilot in plaats van PX4: [Documentatie/ontwerpbeslissing-autopilot.md](Documentatie/ontwerpbeslissing-autopilot.md)
- Hoe MAVLink en message signing werken: [Documentatie/kennisnotitie-mavlink-signing.md](Documentatie/kennisnotitie-mavlink-signing.md)
- Sprints, Scrum Master en deadlines: [Documentatie/scrum-proces.md](Documentatie/scrum-proces.md)

Snelle installatie op een schone Ubuntu 26.04-VM:

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/Tugitje/Cyber-Drone-Range.git ~/drone-cyber-range
bash ~/drone-cyber-range/scripts/install-sitl.sh
```

## Vlucht automatisch opnemen

`scripts/run-vlucht.sh` start de opname en ArduPilot SITL met één commando, en analyseert de opname na Ctrl + C:

```bash
~/drone-cyber-range/scripts/run-vlucht.sh <naam> [opties voor sim_vehicle.py]
```

Het eerste woord is de naam van de run. Zonder naam heet de run `vlucht`. Alles daarna gaat naar `sim_vehicle.py`. Bijvoorbeeld:

| Commando | Wanneer |
|---|---|
| `run-vlucht.sh baseline -w` | Baselinerun: een vaste referentievlucht. `-w` zet SITL terug op de standaardparameters, zodat elke run gelijk begint |
| `run-vlucht.sh test` | Een gewone testvlucht. `-w` is niet nodig |

De stappen voor de referentievlucht staan in [missions/README.md](missions/README.md), meer over de scripts in [tools/analysis/README.md](tools/analysis/README.md).

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
| `results/` | Resultaten per vlucht (`vluchten/`) en baselinemetingen met opnames (`baseline/`) |

De broncode van ArduPilot staat niet in deze repository. Die wordt door het installatiescript opgehaald op een vaste versie.

## Werkafspraken

- `main` bevat altijd een werkende versie.
- Werk op een eigen branch per taak, bijvoorbeeld `feature/qgc-installatie`.
- Wijzigingen gaan via een pull request met minimaal één review van een ander groepslid.
- Geen wachtwoorden, sleutels, VM-images of grote logbestanden in de repository.
