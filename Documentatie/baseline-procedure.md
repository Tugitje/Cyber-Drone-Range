# Baseline-procedure: normaal MAVLink-verkeer vastleggen

**Backlog-item:** Verkeer tussen SITL en GCS opnemen met tcpdump/Wireshark en de MAVLink-dissector laden. Een baseline vastleggen van normaal verkeer.
**Prioriteit:** Should · **Categorie:** Testing & Validation · **Deelvraag:** DV5

## Doel

Vastleggen hoe het MAVLink-verkeer tussen drone (SITL) en Ground Control Station (QGroundControl) eruitziet in een normale situatie: welke berichten, hoe vaak, in welke richting, en hoe stabiel dat is tussen herhaalde runs. Latere securitytests worden met deze baseline vergeleken.

## Opstelling

```
VM (Ubuntu 26.04)                                              Windows-host
ArduPilot SITL ──TCP 5760──► MAVProxy ──UDP 10.0.2.2:14550──► QGroundControl
                                     ├─UDP 127.0.0.1:14550
                                     └─UDP 127.0.0.1:14551
```

- ArduPilot Copter-4.7.1 SITL en MAVProxy in de VM, QGroundControl op de Windows-host.
- De VM gebruikt het NAT-netwerk van VirtualBox; de host is vanuit de VM bereikbaar op `10.0.2.2`.
- MAVLink 2, **zonder** berichtondertekening (signing). Dit is de onbeveiligde normaalsituatie.
- Opname in de VM met `tcpdump` op alle interfaces. Zo staan zowel de verbinding SITL ↔ MAVProxy als MAVProxy ↔ QGC in één bestand.

Voor de analyse telt de verbinding met QGC op de host (`10.0.2.2:14550`). MAVProxy stuurt hetzelfde verkeer ook naar twee poorten binnen de VM; die worden niet meegeteld, anders tel je alles dubbel.

## Eenmalige voorbereiding

### 1. Tools installeren in de VM

```bash
sudo apt install -y tcpdump tshark
sudo usermod -aG wireshark $USER
```

Log daarna uit en weer in.

### 2. MAVLink-dissector maken

Zie [tools/wireshark/README.md](../tools/wireshark/README.md). Kort:

```bash
cd ~/drone-cyber-range/tools/wireshark
mavgen.py --lang=WLua --wire-protocol=2.0 --output=mavlink_2_ardupilotmega \
  ~/ardupilot/modules/mavlink/message_definitions/v1.0/ardupilotmega.xml
```

Installeren voor tshark in de VM (Ubuntu 26.04 blokkeert plugins in de thuismap via AppArmor, zie [tools/wireshark/README.md](../tools/wireshark/README.md)):

```bash
sudo cp mavlink_2_ardupilotmega.lua /usr/lib/x86_64-linux-gnu/wireshark/plugins/
tshark -G protocols | grep -i mavlink    # moet MAVLINK_PROTO tonen
```

Installeren voor Wireshark op Windows: kopieer het `.lua`-bestand naar de map *Personal Lua Plugins* (Wireshark → Help → About Wireshark → Folders, meestal `%APPDATA%\Wireshark\plugins`) en herstart Wireshark.

### 3. Vaste missie

Maak in QGroundControl één referentiemissie (bijvoorbeeld: opstijgen naar 10 m, 4 waypoints, Return) en sla die op als `missions/baseline.plan`. Gebruik bij elke run precies deze missie.

## Procedure per run

Gebruik drie terminals (SSH mag) en QGroundControl op Windows. Noteer bij elke stap de kloktijd.

**Terminal 1: opname starten**

```bash
mkdir -p ~/captures && cd ~/captures
NAAM=baseline_$(date +%Y%m%d_%H%M)
echo $NAAM
sudo tcpdump -i any -w ${NAAM}.pcap 'tcp port 5760 or udp portrange 14550-14551'
```

**Terminal 2: SITL starten**

```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py --out=udp:10.0.2.2:14550
```

**Scenario**

| Stap | Actie | Duur |
|---|---|---|
| 1 | Wachten tot QGC verbonden is en de drone GPS heeft | ±1 min |
| 2 | Rustfase: niets doen | 60 s |
| 3 | `missions/baseline.plan` laden, uploaden en starten | ±2–3 min |
| 4 | Rustfase na landing en disarm | 30 s |
| 5 | SITL stoppen: Ctrl + C in terminal 2 | – |
| 6 | Opname stoppen: Ctrl + C in terminal 1 | – |

Stop altijd eerst SITL en daarna de opname.

**Bewaren per run**

- de opname: `~/captures/<NAAM>.pcap`
- de telemetrielog van MAVProxy: `~/ardupilot/ArduCopter/mav.tlog` (hernoemen naar `<NAAM>.tlog`)
- de autopilotlog: nieuwste bestand in `~/ardupilot/ArduCopter/logs/`

Voer **drie runs** uit.

## Analyse

### Berichten tellen

```bash
cd ~/drone-cyber-range/tools/analysis
python3 baseline_simpel.py ~/captures/<NAAM>.pcap
```

De venv (`venv-ardupilot`) moet actief zijn, want het script gebruikt pymavlink. Het script toont per richting de berichttypes met aantal en aantal per seconde. Genoeg voor een eerste baselinetabel.

Uitvoer bewaren: `python3 baseline_simpel.py ~/captures/<NAAM>.pcap > ~/captures/<NAAM>.txt`

### Handmatig in Wireshark

Kopieer de opname naar Windows (in PowerShell):

```powershell
scp -P 2222 "dronecyberrange@127.0.0.1:~/captures/*.pcap" "$HOME\Downloads\"
```

Handige filters:

| Filter | Toont |
|---|---|
| `mavlink_proto && ip.dst == 10.0.2.2` | Drone → GCS |
| `mavlink_proto && ip.src == 10.0.2.2` | GCS → drone |
| `mavlink_proto.msgid == 0` | Alleen HEARTBEAT |

Wordt het verkeer niet als MAVLink herkend: rechtsklik op een pakket → *Decode As…* → *MAVLINK_PROTO*. Wordt de filterbalk rood, dan is de dissector niet geladen.

Nuttige menu's: *Statistics → Conversations* (verkeer per verbinding), *Statistics → I/O Graphs* (pakketten per seconde over de tijd, interval 1 s).

## Wat de baseline moet laten zien

| Meetwaarde | Waarom |
|---|---|
| Pakketten en berichten per richting | Omvang van normaal verkeer |
| Pakketten per seconde per fase | Verschil tussen rust en vlucht |
| Berichttypes met frequentie (Hz) | Welke berichten normaal zijn en hoe vaak (bijv. HEARTBEAT ±1 Hz) |
| Heartbeat-interval per afzender | Regelmaat van de verbinding |
| Sequentiegaten | Op een lokale verbinding (bijna) 0 |
| Commando's van GCS naar drone | Wat er normaal gebeurt bij missie-upload, arming en moduswissels |
| MAVLink-versie en signing | MAVLink 2, niet ondertekend |
| Spreiding tussen runs (CV) | Of de baseline stabiel en herhaalbaar is |

## Observaties om op te nemen in het verslag

- De inhoud van MAVLink-berichten (positie, hoogte, status) is **niet versleuteld** en in Wireshark direct leesbaar.
- Zonder signing bevatten berichten **geen handtekening**; niets in het bericht bewijst wie de afzender is. Alleen het systeem- en componentnummer (sysid/compid) geven aan van wie een bericht zou komen.
- Deze observaties vormen het startpunt voor de securitytests en maatregelen in latere sprints.

## Resultaten vastleggen

Zet per baseline in `results/baseline/<datum>/`:
- de uitvoer van `baseline_simpel.py` per run (`<NAAM>.txt`);
- een korte notitie met kloktijden per fase, versies (zie [config/versies.md](../config/versies.md)) en afwijkingen van de procedure;
- screenshots (I/O-grafiek, ontlede HEARTBEAT) in `Documentatie/img/`.

Grote `.pcap`-bestanden komen niet in Git (zie `.gitignore`). Bewaar die op een gedeelde schijf.