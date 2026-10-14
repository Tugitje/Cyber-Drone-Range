# Missies

| Bestand | Beschrijving |
|---|---|
| `baseline.txt` | Referentiemissie voor de baseline: opstijgen naar 20 m, vierkant van 50 × 50 m rond de startplek, terug naar start en landen (RTL). Formaat: QGC WPL 110, te laden in MAVProxy en QGroundControl |

De missie gaat uit van de standaard startlocatie van ArduPilot SITL (vliegveld CMAC bij Canberra, -35.363262, 149.165237).

## Referentievlucht uitvoeren

Start de run met `scripts/run-vlucht.sh baseline -w` (zie [tools/analysis/README.md](../tools/analysis/README.md)). Typ daarna in dezelfde terminal, bij de MAVProxy-prompt, één commando per regel:

| Stap | Commando | Daarna |
|---|---|---|
| 1 | *(niets)* | Wacht tot `EKF3 IMU0 is using GPS` verschijnt |
| 2 | `wp load /home/<gebruiker>/drone-cyber-range/missions/baseline.txt` | Melding dat 7 waypoints geladen zijn |
| 3 | *(niets: rustfase)* | 60 seconden wachten |
| 4 | `mode guided` | – |
| 5 | `arm throttle` | Direct door naar stap 6, anders schakelen de motoren na enkele seconden uit |
| 6 | `takeoff 20` | Wachten tot de hoogte ±20 m is |
| 7 | `mode auto` | Drone vliegt het vierkant, keert terug en landt zelf |
| 8 | *(niets)* | Wachten op `DISARMED`, daarna nog 30 seconden |
| 9 | Ctrl + C | SITL en opname stoppen; de analyse draait automatisch |

Noteer de kloktijden van stap 3, 4, 7 en 8 per run. Breek een vlucht alleen af met `mode rtl` of `mode land` als er iets misgaat; zo'n run telt dan niet mee voor de baseline.

## Bekende problemen

| Wat je ziet | Oorzaak | Oplossing |
|---|---|---|
| `PreArm: ...` (bijv. "Need 3D Fix", "EKF not ready") | Drone nog niet klaar | Wachten tot `EKF3 IMU0 is using GPS`, opnieuw `arm throttle` |
| `ARMED` en kort daarna `Disarming motors` | `takeoff` te laat gegeven | `arm throttle` en direct `takeoff 20` |
| `Usage: takeoff ALTITUDE_IN_METERS` | Commando verkeerd getypt (bijv. aanhalingsteken erachter) | Commando zonder extra tekens typen |
| Commando's komen verminkt aan (`Unknown command 'atle'`) | Oude versie van `run-vlucht.sh`, waarin `sudo` meeleest met het toetsenbord | Nieuwste `scripts/run-vlucht.sh` gebruiken |
