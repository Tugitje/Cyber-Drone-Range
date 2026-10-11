# Analysescripts

## baseline_simpel.py

Kort script (±65 regels) dat per richting telt welke MAVLink-berichten er in een opname zitten, hoe vaak, en hoeveel per seconde. Leest de opname van `tcpdump -i any` in de VM en telt alleen de verbinding met QGroundControl op de Windows-host (`10.0.2.2:14550`).

```bash
source ~/venv-ardupilot/bin/activate
python3 baseline_simpel.py ~/captures/baseline_20261011_1530.pcap
```

Voorbeelduitvoer:

```
drone -> GCS: 1923 berichten
  Bericht                       Aantal   Per seconde
  ATTITUDE                        1200         10.01
  GLOBAL_POSITION_INT              600          5.00
  HEARTBEAT                        120          1.00
```

Werkt alleen met `.pcap` uit tcpdump in de VM, niet met `.pcapng` uit Wireshark op Windows. Pas `GCS_IP` en `GCS_POORT` bovenin aan als de opstelling verandert.
