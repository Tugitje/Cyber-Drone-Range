# Bevindingen

Feitelijke bevindingen uit het werk aan de cyber range. Gebruik deze voor de afwegingsmatrix, de risicoanalyse en het eindverslag.

## Sprint 1: eerste installatie ArduPilot SITL

**Datum:** 9–10 oktober 2026
**Omgeving:** VirtualBox 7.2.20 op Windows, Ubuntu 26.04.1 LTS, ArduPilot Copter-4.7.1

### Resultaat

ArduPilot SITL is geïnstalleerd en een eerste gesimuleerde vlucht is gelukt: opstijgen naar 10 meter, rondvliegen (`mode circle`) en terugkeren en landen (`mode rtl`). Daarna is QGroundControl op de Windows-host geïnstalleerd en verbonden met de simulatie via MAVLink over UDP 14550; de drone is zichtbaar in QGC.

### Bevindingen

| # | Bevinding | Gevolg | Status |
|---|---|---|---|
| B1 | Het installatiescript van ArduPilot Copter-4.7.1 ondersteunt Ubuntu 26.04 nog niet officieel. | Script aangepast zodat 26.04 wordt behandeld als 25.10 met SFML 3.0. Opgenomen in `scripts/install-sitl.sh`. | Opgelost |
| B2 | Op Ubuntu 26.04 is `/tmp` te klein voor het bouwen van wxPython (`Disk quota exceeded`). | `TMPDIR` instellen op een map op schijf. | Opgelost |
| B3 | Een virtuele schijf van 25 GB is te krap (na installatie ±16 GB in gebruik). | Advies: 60 GB voor nieuwe VM's. | Advies |
| B4 | De Ubuntu-installatie in VirtualBox gaf een zwart scherm. | Opgelost met "safe graphics" en VBoxSVGA. | Opgelost |
| B5 | Ubuntu 26.04 gebruikt Wayland. Het rechtsklikmenu op de MAVProxy-kaart en het gedeelde klembord van VirtualBox werken daardoor niet. | Omweg: `GDK_BACKEND=x11`, QGroundControl, of werken via SSH. | Omweg |
| B6 | De VM kan traag zijn als Hyper-V in Windows aanstaat. | Hyper-V uitschakelen (zie installatiehandleiding). | Advies |
| B7 | De totale installatietijd was ongeveer 2 uur, inclusief het oplossen van problemen. | Input voor afwegingsmatrix ArduPilot vs. PX4. | Te vergelijken |
| B8 | QGroundControl op de Windows-host verbindt met SITL via MAVLink over UDP 14550, als SITL gestart wordt met `--out=udp:10.0.2.2:14550`. | Basis voor verdere tests: dit is de verbinding die later wordt geanalyseerd en beveiligd. | Werkt |
| B9 | In Wireshark is de inhoud van MAVLink-berichten (positie, status, arming) direct leesbaar; zonder signing bevatten berichten geen handtekening. | Startpunt voor dreigingsmodel en securitytests. | Observatie |

### Risico's voor de risicoanalyse

- **Nieuwe Ubuntu-versie wordt nog niet ondersteund door tooling.** Kans: hoog, impact: middel. Maatregel: werkende aanpassing vastleggen in het installatiescript; Ubuntu 24.04 LTS als uitwijkoptie.
- **Prestaties van de VM op laptops van groepsleden.** Kans: middel, impact: middel. Maatregel: minimale VM-eisen vastleggen; Hyper-V uitschakelen; eventueel een gedeelde server bij het lectoraat aanvragen.
- **Verschillende hardware binnen de groep (bijvoorbeeld een Mac met Apple-chip).** Kans: onbekend, impact: hoog. Maatregel: vroeg testen op elk apparaat.

## Sprint 2: baseline van het MAVLink-verkeer

**Datum:** 14 oktober 2026
**Omgeving:** als sprint 1, met QGroundControl op de Windows-host. Opnames met `scripts/run-vlucht.sh`, referentiemissie `missions/baseline.txt`.
**Resultaten:** [results/baseline/2026-10-14/](../results/baseline/2026-10-14/)

| # | Bevinding | Gevolg | Status |
|---|---|---|---|
| B10 | Het verkeer van drone naar GCS is stabiel tussen de drie runs: 11.945 tot 12.598 berichten, ±100 berichten per seconde. De meest voorkomende berichten (AHRS2, ATTITUDE, SIMSTATE, ESC_TELEMETRY_1_TO_4) komen ±4,7 keer per seconde voor. | Bruikbaar als referentie voor de securitytests. | Werkt |
| B11 | QGroundControl blijft pakketten sturen naar de UDP-poorten van eerdere SITL-sessies. In run 1 gaat het verkeer van QGC naar 3 poorten in de VM, in run 3 naar 5. Alleen de poort die MAVProxy op dat moment gebruikt is echt. `baseline_simpel.py` telt alles mee. | De cijfers voor GCS → drone in de samenvattingen van 14 oktober zijn 3 tot 5 keer te hoog. Oplossing: in het script ook filteren op de poort van MAVProxy, of QGC herstarten tussen runs. | Open |
| B12 | Alle drie de opnames zijn compleet: tcpdump meldt `0 packets dropped by kernel`. | Opnames zijn betrouwbaar als bron. | Werkt |
| B13 | De runs duurden 117 tot 126 seconden. Met de rustfases uit de procedure (60 s ervoor, 30 s erna) blijft er maar 27 tot 36 seconden over voor de vlucht zelf. Dat is te kort voor opstijgen, het vierkant van 50 × 50 m en de landing. | De rustfases waren dus korter dan voorgeschreven. Bij de volgende baseline de procedure volgen en de kloktijden noteren. | Open |

### Volgende stappen

- `baseline_simpel.py` aanpassen voor B11 en de baseline opnieuw meten volgens de procedure (B13).
- Ontbrekende versies invullen in `config/versies.md`.
- Testen met MAVLink-signing aan en vergelijken met de baseline.
- Installatie laten testen door een ander groepslid op een schone VM.
- PX4 SITL uitproberen ter vergelijking.
