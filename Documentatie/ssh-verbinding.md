# SSH-verbinding van Windows naar de VM

## Waarom

Op Ubuntu 26.04 werkt het gedeelde klembord van VirtualBox niet goed, door Wayland. Daardoor kun je commando's niet vanuit Windows (bijvoorbeeld uit de documentatie of een chat) in de terminal van de VM plakken.

Met SSH open je de terminal van de VM in een venster op Windows. Kopiëren en plakken werkt daar gewoon. SSH is later ook nodig voor Ansible.

## Eenmalig instellen

### 1. SSH-server installeren in de VM

In een terminal in het VM-venster:

```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
systemctl status ssh --no-pager
```

Bij de laatste regel hoort `active (running)` te staan.

### 2. Port forwarding instellen in VirtualBox

De VM gebruikt standaard het NAT-netwerk van VirtualBox. Je stuurt poort 2222 op Windows door naar poort 22 (SSH) in de VM.

Zet de VM **uit** (afsluiten, niet "toestand opslaan"). Open **PowerShell** op Windows.

Zoek eerst de exacte naam van je VM op:

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" list vms
```

Stel daarna de doorverwijzing in. Vervang `CyberDroneRange` door de naam uit de lijst:

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "CyberDroneRange" --natpf1 "ssh,tcp,,2222,,22"
```

Controleren:

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo "CyberDroneRange" | Select-String "Rule"
```

Je hoort een regel te zien met `name = ssh` en `host port = 2222, guest port = 22`.

Via de grafische instellingen van VirtualBox kan het ook (Netwerk → Adapter 1 → Port Forwarding), maar die knop zit niet in elke versie of weergave op dezelfde plek. Het commando werkt altijd.

## Verbinden

1. Start de VM en wacht tot Ubuntu is opgestart. Inloggen op het bureaublad is niet nodig.
2. Open **PowerShell** of **Windows Terminal** op Windows.
3. Verbind, met je Ubuntu-gebruikersnaam:

```powershell
ssh -p 2222 dronecyberrange@127.0.0.1
```

4. De eerste keer vraagt SSH of je de verbinding vertrouwt. Typ `yes` en druk op Enter.
5. Vul je Ubuntu-wachtwoord in. Je ziet tijdens het typen niets; dat is normaal.

Je zit nu in de terminal van de VM.

## Kopiëren en plakken

| Actie | Hoe |
|---|---|
| Plakken in de SSH-terminal | Rechtermuisknop, of Ctrl + Shift + V (Windows Terminal) |
| Kopiëren uit de SSH-terminal | Tekst selecteren met de muis, daarna rechtermuisknop of Ctrl + Shift + C |
| Verbinding verbreken | `exit` typen |

## Wat wel en niet via SSH werkt

| Werkt via SSH | Werkt niet via SSH (gebruik het VM-venster) |
|---|---|
| Installeren, scripts draaien, bestanden bewerken | Kaart- en consolevenster van MAVProxy (`--map`, `--console`) |
| `sim_vehicle.py` zonder vensters, ook samen met QGroundControl op Windows (zie [installatie-qgc.md](installatie-qgc.md)) | |
| Git (clonen, committen, pushen) | Gazebo en Wireshark (grafisch) |

Handige combinatie: start de simulatie in het VM-venster, en gebruik SSH voor al het andere werk.

## Problemen

| Melding | Oorzaak | Oplossing |
|---|---|---|
| `Connection refused` | SSH-server draait niet in de VM, of de VM is nog aan het opstarten | `sudo systemctl enable --now ssh` in de VM; even wachten |
| `Connection timed out` | Port forwarding ontbreekt | Stap 2 opnieuw doen, controleren met `showvminfo` |
| `ssh` wordt niet herkend in PowerShell | OpenSSH-client ontbreekt op Windows | Windows-instellingen → Systeem → Optionele onderdelen → OpenSSH-client toevoegen |
