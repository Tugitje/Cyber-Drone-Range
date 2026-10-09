# Patches

Aanpassingen op externe software die nodig zijn om de cyber range te laten werken.

## ubuntu-26.04-fix.patch

Past `Tools/environment_install/install-prereqs-ubuntu.sh` van ArduPilot **Copter-4.7.1** aan, zodat het werkt op Ubuntu 26.04 ("resolute"):

- resolute wordt behandeld als Ubuntu 25.10 ("questing"), inclusief het aanmaken van een Python-venv;
- het niet-bestaande pakket `python3-argparse` wordt niet meer geïnstalleerd;
- SFML 3.0 wordt gebruikt, de versie die Ubuntu 26.04 meelevert.

[`scripts/install-sitl.sh`](../scripts/install-sitl.sh) voert dezelfde aanpassing automatisch uit. Je hebt deze patch alleen nodig als je handmatig installeert.

Toepassen op een schone checkout van Copter-4.7.1:

```bash
cd ~/ardupilot
git apply ~/drone-cyber-range/patches/ubuntu-26.04-fix.patch
```

Controleren of de patch al is toegepast:

```bash
git apply --check ~/drone-cyber-range/patches/ubuntu-26.04-fix.patch
```

Geeft dit een foutmelding, dan is de patch waarschijnlijk al toegepast.
