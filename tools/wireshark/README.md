# MAVLink-dissector voor Wireshark en tshark

Wireshark herkent MAVLink niet standaard. Met `mavgen` uit pymavlink maak je een Lua-dissector op basis van de berichtdefinities van ArduPilot (inclusief de ArduPilot-specifieke berichten).

## Maken

In de VM, met de venv actief:

```bash
cd ~/drone-cyber-range/tools/wireshark
mavgen.py --lang=WLua --wire-protocol=2.0 --output=mavlink_2_ardupilotmega \
  ~/ardupilot/modules/mavlink/message_definitions/v1.0/ardupilotmega.xml
```

Resultaat: `mavlink_2_ardupilotmega.lua` (±3,7 MB). Het bestand staat niet in Git (zie `.gitignore`): maak het na elke nieuwe clone zelf aan met het commando hierboven, en opnieuw na een update van ArduPilot, zodat nieuwe berichten herkend worden.

## Installeren in de VM (tshark)

Ubuntu 26.04 heeft een AppArmor-profiel voor tshark dat lezen uit de thuismap blokkeert, ook uit de eigen pluginmap `~/.local/lib/wireshark/plugins`. Gebruik daarom de systeembrede pluginmap:

```bash
sudo cp mavlink_2_ardupilotmega.lua /usr/lib/x86_64-linux-gnu/wireshark/plugins/
tshark -G protocols | grep -i mavlink
```

Verwachte uitvoer: `MAVLink protocol  MAVLINK_PROTO  mavlink_proto ...`

Alternatief (alleen de eigen pluginmap toestaan, rest van AppArmor blijft actief), als `/etc/apparmor.d/tshark` een regel `include if exists <local/tshark>` bevat:

```bash
mkdir -p ~/.local/lib/wireshark/plugins
cp mavlink_2_ardupilotmega.lua ~/.local/lib/wireshark/plugins/
sudo tee -a /etc/apparmor.d/local/tshark > /dev/null << 'EOF'
owner @{HOME}/.local/lib/wireshark/plugins/ r,
owner @{HOME}/.local/lib/wireshark/plugins/** r,
EOF
sudo apparmor_parser -r /etc/apparmor.d/tshark
```

Zet AppArmor voor tshark niet uit (`aa-complain`): dat schakelt de bescherming helemaal uit.

## Installeren op Windows (Wireshark)

1. Kopieer het bestand naar Windows (in PowerShell):
   ```powershell
   scp -P 2222 dronecyberrange@127.0.0.1:~/drone-cyber-range/tools/wireshark/mavlink_2_ardupilotmega.lua "$HOME\Downloads\"
   ```
2. Open Wireshark → **Help → About Wireshark → Folders** en zoek **Personal Lua Plugins** (meestal `%APPDATA%\Wireshark\plugins`). Maak de map aan als die niet bestaat.
3. Zet het `.lua`-bestand in die map en herstart Wireshark.
4. Controleer onder **Help → About Wireshark → Plugins** of het bestand in de lijst staat.

## Gebruik

- Filter `mavlink_proto` toont alle MAVLink-berichten. Een rode filterbalk betekent dat de dissector niet geladen is.
- Wordt verkeer niet herkend (bijvoorbeeld TCP 5760): rechtsklik op een pakket → **Decode As…** → **MAVLINK_PROTO**.
- In tshark: `-d udp.port==14550,mavlink_proto` of `-d tcp.port==5760,mavlink_proto`.
