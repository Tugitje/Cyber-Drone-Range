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

## Automatisch per vlucht

Twee manieren om opname en analyse automatisch te laten lopen. Resultaten komen in `results/vluchten/<naam>/samenvatting.txt`, de opname in `~/captures/`.

### Per SITL-sessie: `scripts/run-vlucht.sh`

Start opname en SITL met één commando. **Ctrl + C** stopt SITL én de opname, daarna volgt direct de analyse. De opname bevat de hele sessie, inclusief rustfases; geschikt voor de baselineruns.

```bash
source ~/venv-ardupilot/bin/activate
~/drone-cyber-range/scripts/run-vlucht.sh baseline -w
```

- Het eerste woord is de naam van de run (optioneel; standaard `vlucht`). Alles daarna gaat naar `sim_vehicle.py`.
- Zonder eigen `--out` voegt het script `--out=udp:10.0.2.2:14550` toe, zodat QGroundControl op de Windows-host meekijkt.
- `-w` start SITL met standaardparameters, zodat elke run gelijk begint.
- Het script start alleen opname en SITL. De vlucht zelf voer je uit met de MAVProxy-commando's uit [missions/README.md](../../missions/README.md), in dezelfde terminal.
- tcpdump draait zonder toegang tot de terminal. Anders leest `sudo` mee met het toetsenbord en komen MAVProxy-commando's verminkt aan. Meldingen van tcpdump staan in `tcpdump.log` in de resultatenmap.
- Start in het VM-venster als je `--console --map` wilt gebruiken.

### Per vlucht (arm tot disarm): `tools/analysis/auto_vlucht.py`

Luistert mee op UDP 14551 (vrije uitgang van MAVProxy). Start de opname zodra de drone **gearmd** wordt, stopt **10 seconden na disarm** en analyseert direct. Werkt voor meerdere vluchten achter elkaar in dezelfde SITL-sessie.

```bash
# Terminal 1: SITL zoals gewoonlijk
sim_vehicle.py --out=udp:10.0.2.2:14550
# Terminal 2: de automatische opname
sudo ~/venv-ardupilot/bin/python ~/drone-cyber-range/tools/analysis/auto_vlucht.py
```

Stoppen met Ctrl + C. De opname begint pas bij arming, dus de rustfase vóór de vlucht zit er niet in. Gebruik voor de baseline daarom `run-vlucht.sh`.
