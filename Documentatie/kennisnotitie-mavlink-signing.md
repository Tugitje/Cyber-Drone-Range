# Kennisnotitie: MAVLink en message signing

Drone Cyber Range · DV4 Security & Threat · 12 oktober 2026

## In het kort

- MAVLink is een protocol, geen applicatie. De autopilot (ArduPilot of PX4, in onze range als SITL) en de GCS (bijvoorbeeld QGroundControl) praten er via pakketten mee.

- MAVLink 2 voegt aan MAVLink 1 twee flag-bytes, een bericht-ID van 3 bytes en een optionele handtekening van 13 bytes toe.

- Message signing laat de ontvanger controleren dat een pakket van een houder van de gedeelde sleutel komt en onderweg niet is aangepast. Het versleutelt niets.

## Het pakket

Een MAVLink 2-pakket is 12 tot 280 bytes en bevat, in deze volgorde: start-byte (0xFD), lengte, incompat_flags, compat_flags, volgnummer, system-ID, component-ID, bericht-ID (3 bytes), payload, CRC (2 bytes) en optioneel de handtekening (13 bytes). Bit 0x01 van incompat_flags betekent: ondertekend. De payload heeft geen veldnamen; zender en ontvanger gebruiken dezelfde berichtdefinitie. De CRC beschermt tegen beschadiging, niet tegen een aanvaller.

Bron: [MAVLink Packet Serialization](https://mavlink.io/en/guide/serialization.html).

## De vier kernberichten

| **Bericht**                                                             | **ID** | **Functie**                                                                                     |
|-------------------------------------------------------------------------|--------|-------------------------------------------------------------------------------------------------|
| [HEARTBEAT](https://mavlink.io/en/messages/common.html#HEARTBEAT)       | 0      | Meldt dat een systeem aanwezig is; de GCS ontdekt zo voertuigen en ziet wanneer er een wegvalt. |
| [COMMAND_LONG](https://mavlink.io/en/messages/common.html#COMMAND_LONG) | 76     | Stuurt een commando (MAV_CMD) met maximaal 7 parameters; antwoord via COMMAND_ACK.              |
| [PARAM_SET](https://mavlink.io/en/messages/common.html#PARAM_SET)       | 23     | Zet een parameter op een nieuwe waarde; de ontvanger bevestigt met PARAM_VALUE.                 |
| [MISSION_ITEM](https://mavlink.io/en/messages/common.html#MISSION_ITEM) | 39     | Eén routepunt of actie van een missie. Deprecated: de opvolger is MISSION_ITEM_INT (73).        |

Bronnen: [Command Protocol](https://mavlink.io/en/services/command.html), [Parameter Protocol](https://mavlink.io/en/services/parameter.html), [Mission Protocol](https://mavlink.io/en/services/mission.html), [Heartbeat](https://mavlink.io/en/services/heartbeat.html).

## Hoe signing werkt

- De afzender plakt sleutel (32 bytes), header, payload, CRC, link-ID en timestamp aan elkaar en berekent daar een SHA-256-hash over. De eerste 48 bits daarvan zijn de handtekening.

- Meegestuurd worden 13 bytes: link-ID (1), timestamp (6, in eenheden van 10 microseconden sinds 1 januari 2015) en handtekening (6). De sleutel zelf wordt niet meegestuurd.

- De ontvanger rekent de handtekening met zijn eigen kopie van de sleutel opnieuw uit. Komt hij niet overeen, of is de timestamp ouder dan die van de vorige pakketten in dezelfde stream (of meer dan 1 minuut achter), dan wordt het pakket afgewezen.

- De sleutel wordt eenmalig ingesteld met SETUP_SIGNING, bij voorkeur via USB of bedraad Ethernet, en hoort niet in parameters of logbestanden.

Bron: [MAVLink Message Signing](https://mavlink.io/en/guide/message_signing.html).

## Wat signing niet beschermt

| **Dreiging**                        | **Beschermd?** | **Waarom**                                                                                                                     |
|-------------------------------------|----------------|--------------------------------------------------------------------------------------------------------------------------------|
| Aanpassen of namaken zonder sleutel | Ja             | Zonder sleutel is de handtekening niet uit te rekenen.                                                                         |
| Meelezen                            | Nee            | De payload blijft leesbaar. (Afleiding)                                                                                        |
| Opnieuw afspelen van oud pakket     | Grotendeels    | De timestamp-regel vangt dit af, behalve bij een nieuwe stream of een onderschept pakket dat de ontvanger nog niet had gezien. |
| Gelekte sleutel                     | Nee            | Wie de sleutel heeft, maakt geldige pakketten.                                                                                 |
| Pakketten zonder handtekening       | Nee            | Een systeem mag ze accepteren als dat is ingesteld. (Specificatie en afleiding)                                                |
| Verstoren van de verbinding         | Nee            | Signing controleert echtheid, niet of er iets aankomt. (Afleiding)                                                             |

## Voor de range

Voorstel (afleiding, niet getest): draai elke testcase met en zonder signing en vergelijk het resultaat. Zonder signing kan een test-station op hetzelfde netwerk HEARTBEAT, COMMAND_LONG, PARAM_SET en MISSION_ITEM_INT lezen en hergebruiken.

Niet onderzocht: hoe signing wordt aangezet in ArduPilot of PX4 SITL en QGroundControl. De rijen met "Afleiding" zijn eigen conclusies en geen bronnen.
