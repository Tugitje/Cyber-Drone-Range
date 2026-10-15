# Baseline 14 oktober 2026

Zie [Documentatie/baseline-procedure.md](../../../Documentatie/baseline-procedure.md) voor de procedure en [Documentatie/bevindingen.md](../../../Documentatie/bevindingen.md) (B10–B13) voor de bevindingen.

## Opstelling

| Onderdeel | Versie |
|---|---|
| VirtualBox | 7.2.20 |
| VM | Ubuntu 26.04.1 LTS |
| ArduPilot | Copter-4.7.1 |
| MAVProxy | nog invullen |
| QGroundControl | nog invullen (op de Windows-host) |
| tcpdump | nog invullen |
| pymavlink | nog invullen |

Missie: `missions/baseline.txt`. Gestart met `scripts/run-vlucht.sh baseline -w`.

## Runs

| Run | Start opname | Duur | Arm | `mode auto` | Disarm |
|---|---|---|---|---|---|
| `baseline_20261014_145026` | 14:50:26 | 124 s | nog invullen | nog invullen | nog invullen |
| `baseline_20261014_145250` | 14:52:50 | 126 s | nog invullen | nog invullen | nog invullen |
| `baseline_20261014_145505` | 14:55:05 | 117 s | nog invullen | nog invullen | nog invullen |

De starttijd volgt uit de naam van de run. De duur komt uit `samenvatting.txt`. De overige kloktijden zijn niet genoteerd tijdens de runs. Ze zijn achteraf nog te halen uit de `.tlog` of de `.pcap` (arming en moduswissels).

## Afwijkingen van de procedure

- De runs zijn korter dan de procedure voorschrijft: de rustfases waren korter dan 60 s ervoor en 30 s erna (B13).
- QGroundControl is tussen de runs niet opnieuw gestart. Daardoor zijn de cijfers voor GCS → drone in `samenvatting.txt` te hoog (B11). De cijfers voor drone → GCS kloppen wel.
