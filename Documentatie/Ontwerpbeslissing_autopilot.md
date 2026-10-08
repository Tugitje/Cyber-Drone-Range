# Ontwerpbeslissing: keuze autopilot (ArduPilot of PX4)

| | |
|---|---|
| **Trello-kaart** | S1-07 – Keuze autopilot |
| **Deelvraag** | DV1 |
| **Auteurs** | Dila Karatas, Samuel Veefkind |
| **Datum** | 07-10-2026 |
| **Status** | Voorstel – nog te bespreken met de groep |

## 1. Context

De Drone Cyber Range draait in de eerste versie volledig in simulatie (Software-in-the-Loop). Hiervoor is een autopilot-firmware nodig die als SITL op een Linux-machine kan draaien en via MAVLink met een Ground Control Station (QGroundControl) communiceert. De twee meest gebruikte open-source opties zijn ArduPilot en PX4.

Belangrijk voor dit project is dat we MAVLink-verkeer kunnen analyseren en de werking van MAVLink 2-berichtondertekening kunnen testen. Gazebo is een Could-taak; de omgeving moet dus ook zonder 3D-simulatie werken.

## 2. Vergelijking

| Criterium | ArduPilot | PX4 |
| --- | --- | --- |
| **MAVLink 2 signing** | Wordt ondersteund en is gedocumenteerd. Signing kan worden ingesteld via MAVProxy (`module load signing`) of Mission Planner. Signing zorgt voor authenticatie, niet voor encryptie. [1][2] | Beschreven in de nieuwste (main) documentatie. PX4 voegt dan een signature toe aan elk uitgaand MAVLink 2-bericht. Signing staat niet in de documentatie van de stabiele versie die wij bekeken; nog nagaan in welke release het zit. [3] |
| **Documentatie** | Uitgebreide documentatie voor SITL op Linux, met eigen pagina's voor signing en Gazebo. [1][4] | Uitgebreide documentatie voor SITL en simulatie. [5] |
| **Gazebo-koppeling** | Officiële plugin `ardupilot_gazebo` voor Gazebo Garden en Harmonic; werkt zonder ROS. SITL draait ook zonder Gazebo met de ingebouwde simulator. [4][6] | Gazebo wordt direct ondersteund. PX4 heeft ook lichtere simulatoren zonder 3D-weergave. [5] |
| **Community** | Grote community, veel voorbeelden en handleidingen voor SITL. | Grote community, veel gebruikt in onderzoek en bedrijfsleven. |
| **Geschiktheid voor latere HIL** | Draait op dezelfde soort flight controllers (bijv. Pixhawk); HIL-mogelijkheden nog uitzoeken bij het advies in sprint 8. | Heeft een eigen HITL-handleiding: de normale PX4-firmware draait dan op een echte flight controller. Let op: HITL wordt door de community onderhouden en werkt mogelijk niet met de nieuwste PX4-versies; ondersteund voor multicopters met jMAVSim of Gazebo Classic. [8] |

## 3. Argumenten voor PX4

PX4 is een serieuze optie. De sterkste argumenten zijn:

1. **Gazebo is direct ingebouwd.** PX4 koppelt rechtstreeks met Gazebo via de Gazebo-API, zonder aparte plugin. Wie de 3D-simulatie als kern ziet, heeft met PX4 minder losse onderdelen. [5]

2. **Lichte simulatie zonder 3D.** Met SIH kan PX4 ook zonder Gazebo draaien, net als ArduPilot met zijn eigen simulator. [5]

3. **Kant-en-klare pakketten en containers.** PX4 SITL kan draaien zonder eerst een eigen build-omgeving op te zetten. Dat past bij onze eis van reproduceerbare installatie met Docker. [5]

4. **Documentatie voor Hardware-in-the-Loop.** PX4 beschrijft HITL met een echte flight controller. Dit is relevant voor het advies over uitbreiding naar echte hardware (M9). [8]

5. **Nieuwe signing-implementatie.** De signing van PX4 werkt met het standaard SETUP_SIGNING-bericht uit de MAVLink-specificatie en beschermt ook tegen replay-aanvallen via een timestamp. [3][7]

6. **Licentie (BSD).** De BSD-licentie van PX4 is ruimer dan de GPLv3 van ArduPilot. Dit kan voor het lectoraat schelen als de omgeving later wordt gedeeld of uitgebreid met eigen code.

### Waarom PX4 voor ons nu niet de beste keuze is

1. Signing staat (nog) alleen in de nieuwste documentatie; bij ArduPilot is het al jaren beschikbaar en beproefd.

2. In bepaalde versies accepteert PX4 de signing-sleutel alleen via USB. In een simulatie zonder USB maakt dat het testen lastiger. [3]

3. HITL wordt door de community onderhouden en werkt mogelijk niet met de nieuwste versies, waardoor dit voordeel kleiner is dan het lijkt. [8]

4. Gazebo is bij ons een Could-taak, dus het voordeel van de ingebouwde Gazebo-koppeling weegt minder zwaar.

## 4. Besluit

Wij kiezen voor **ArduPilot (ArduCopter) SITL**.

## 5. Onderbouwing

1. **MAVLink 2 signing** is bij ArduPilot al lang beschikbaar en eenvoudig in te stellen via MAVProxy. Dit is een kernonderdeel van onze securitytests (vergelijking met en zonder ondertekening).

2. **Werkt zonder Gazebo.** Gazebo is een Could-taak. ArduPilot SITL heeft een eigen simulator, zodat de omgeving ook werkt als Gazebo te zwaar blijkt voor onze machines.

3. **Gazebo kan later alsnog** via de officiële plugin, zonder dat de autopilot gewisseld hoeft te worden.

4. **Werkt met QGroundControl**, dat wij als Ground Control Station gebruiken. Dus dat is mooi meegenomen.

PX4 is een goed alternatief, vooral voor Hardware-in-the-Loop. Dit nemen we mee in het advies voor toekomstige uitbreiding (M9).

## 6. Gevolgen en aandachtspunten

1. S1-09 (SITL laten draaien en koppelen aan QGroundControl) gaat uit van ArduCopter SITL.

2. Bij ArduPilot geldt signing niet voor USB-verbindingen. In SITL lopen verbindingen via UDP/TCP; we moeten testen hoe signing zich daar gedraagt.

3. Signing geeft authenticatie en integriteit, maar **geen encryptie**: berichten blijven leesbaar in Wireshark.

## 7. Besproken met de groep

- Datum: _____

- Akkoord: _____

- Opmerkingen: _____

## Bronnen

1. ArduPilot. MAVLink2 Signing. https://ardupilot.org/dev/docs/common-MAVLink2-signing.html

2. ArduPilot. MAVProxy – Packet Signing. https://ardupilot.org/mavproxy/docs/modules/signing.html

3. PX4. MAVLink Message Signing. https://docs.px4.io/main/en/mavlink/message_signing

4. ArduPilot. Using SITL with Gazebo. https://ardupilot.org/dev/docs/sitl-with-gazebo.html

5. PX4. Simulation. https://docs.px4.io/main/en/simulation/index

6. ArduPilot. ardupilot_gazebo (GitHub). https://github.com/ArduPilot/ardupilot_gazebo

7. MAVLink. Message Signing (Authentication). https://mavlink.io/en/guide/message_signing.html
