# Bevindingen

Feitelijke bevindingen uit het werk aan de cyber range. Gebruik deze voor de afwegingsmatrix, de risicoanalyse en het eindverslag.

## Sprint 1: eerste installatie ArduPilot SITL

**Datum:** 9–10 oktober 2026
**Door:** [naam]
**Omgeving:** VirtualBox 7.2.20 op Windows, Ubuntu 26.04.1 LTS, ArduPilot Copter-4.7.1

### Resultaat

ArduPilot SITL is geïnstalleerd en een eerste gesimuleerde vlucht is gelukt: opstijgen naar 10 meter, rondvliegen (`mode circle`) en terugkeren en landen (`mode rtl`). Daarna is QGroundControl geïnstalleerd en automatisch verbonden met de simulatie via MAVLink over UDP 14550; de drone is zichtbaar in QGC.

### Bevindingen

| # | Bevinding | Gevolg | Status |
|---|---|---|---|
| B1 | Het installatiescript van ArduPilot Copter-4.7.1 ondersteunt Ubuntu 26.04 nog niet officieel. | Script aangepast zodat 26.04 wordt behandeld als 25.10 met SFML 3.0. Opgenomen in `scripts/install-sitl.sh`. | Opgelost |
| B2 | Op Ubuntu 26.04 is `/tmp` te klein voor het bouwen van wxPython (`Disk quota exceeded`). | `TMPDIR` instellen op een map op schijf. | Opgelost |
| B3 | Een virtuele schijf van 25 GB is te krap (na installatie ±16 GB in gebruik). | Advies: 60 GB voor nieuwe VM's. | Advies |
| B4 | De Ubuntu-installatie in VirtualBox gaf een zwart scherm. | Opgelost met "safe graphics" en VBoxSVGA. | Opgelost |
| B5 | Ubuntu 26.04 gebruikt Wayland. Het rechtsklikmenu op de MAVProxy-kaart en het gedeelde klembord van VirtualBox werken daardoor niet. | Omweg: `GDK_BACKEND=x11`, QGroundControl, of werken via SSH. | Omweg |
| B6 | De VM kan traag zijn als Hyper-V in Windows aanstaat. | Hyper-V uitschakelen (zie installatiehandleiding). | Advies |
| B7 | De totale installatietijd was ongeveer [aantal] uur, inclusief het oplossen van problemen. | Input voor afwegingsmatrix ArduPilot vs. PX4. | Te vergelijken |
| B8 | Het installatiescript van ArduPilot zet de venv en het pad alleen in `~/.profile`. Een nieuw terminalvenster leest dat niet, waardoor `sim_vehicle.py` niet gevonden wordt. | Regels toegevoegd aan `~/.bashrc`; opgenomen in `scripts/install-sitl.sh`. | Opgelost |
| B9 | QGroundControl heeft `libfuse2` nodig; op Ubuntu 26.04 heet dit pakket `libfuse2t64`. | Pakketnaam aangepast in de handleiding. | Opgelost |
| B10 | QGroundControl verbindt zonder extra configuratie met SITL via MAVLink over UDP 14550. | Basis voor verdere tests: dit is de verbinding die later wordt geanalyseerd en beveiligd. | Werkt |

### Risico's voor de risicoanalyse

- **Nieuwe Ubuntu-versie wordt nog niet ondersteund door tooling.** Kans: hoog, impact: middel. Maatregel: werkende aanpassing vastleggen in het installatiescript; Ubuntu 24.04 LTS als uitwijkoptie.
- **Prestaties van de VM op laptops van groepsleden.** Kans: middel, impact: middel. Maatregel: minimale VM-eisen vastleggen; Hyper-V uitschakelen; eventueel een gedeelde server bij het lectoraat aanvragen.
- **Verschillende hardware binnen de groep (bijvoorbeeld een Mac met Apple-chip).** Kans: onbekend, impact: hoog. Maatregel: vroeg testen op elk apparaat.

### Volgende stappen

- Eerste missie plannen en vliegen in QGroundControl, en het missiebestand opslaan in `missions/`.
- Installatie laten testen door een ander groepslid op een schone VM.
- PX4 SITL uitproberen ter vergelijking.
