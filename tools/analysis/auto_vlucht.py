#!/usr/bin/env python3
"""
Neemt automatisch elke vlucht op: start tcpdump zodra de drone gearmd wordt,
stopt 10 seconden na disarm en analyseert de opname direct met baseline_simpel.py.

Luistert mee op UDP 14551, de vrije uitgang van MAVProxy (sim_vehicle.py stuurt
daar standaard een kopie van het MAVLink-verkeer heen).

Start (na SITL, in een eigen terminal):
  sudo ~/venv-ardupilot/bin/python ~/drone-cyber-range/tools/analysis/auto_vlucht.py
Stoppen: Ctrl + C.
"""
import datetime
import os
import signal
import subprocess
import sys
import time

from pymavlink import mavutil

NA_DISARM = 10                      # seconden doorgaan na de landing
GEBRUIKER = os.environ.get("SUDO_USER") or os.environ.get("USER")
THUIS = os.path.expanduser(f"~{GEBRUIKER}")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(REPO, "tools", "analysis", "baseline_simpel.py")

if os.geteuid() != 0:
    sys.exit("Start dit script met sudo (zie bovenaan het bestand).")


def start_opname():
    naam = "vlucht_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"{THUIS}/captures", exist_ok=True)
    pad = f"{THUIS}/captures/{naam}.pcap"
    proc = subprocess.Popen(["tcpdump", "-i", "any", "-Z", GEBRUIKER, "-w", pad,
                             "tcp port 5760 or udp portrange 14550-14551"],
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    print(f"[{naam}] gearmd: opname gestart -> {pad}")
    return naam, pad, proc


def stop_en_analyseer(naam, pad, proc):
    proc.send_signal(signal.SIGINT)
    proc.wait()
    uit = os.path.join(REPO, "results", "vluchten", naam)
    os.makedirs(uit, exist_ok=True)
    resultaat = subprocess.run([sys.executable, SCRIPT, pad], capture_output=True, text=True)
    with open(os.path.join(uit, "samenvatting.txt"), "w") as f:
        f.write(resultaat.stdout or resultaat.stderr)
    subprocess.run(["chown", "-R", GEBRUIKER, uit])
    print(f"[{naam}] opname gestopt en geanalyseerd -> {uit}/samenvatting.txt")


verbinding = mavutil.mavlink_connection("udpin:127.0.0.1:14551")
print("Wachten op de drone (UDP 14551)... Stop met Ctrl + C.")
opname = None
disarm_tijd = None

try:
    while True:
        hb = verbinding.recv_match(type="HEARTBEAT", blocking=True, timeout=1)
        if hb and hb.type != mavutil.mavlink.MAV_TYPE_GCS:
            gearmd = bool(hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
            if gearmd and opname is None:
                opname = start_opname()
            if gearmd:
                disarm_tijd = None
            elif opname and disarm_tijd is None:
                disarm_tijd = time.time()
                print(f"[{opname[0]}] gedisarmd: nog {NA_DISARM} s opnemen")
        if opname and disarm_tijd and time.time() - disarm_tijd >= NA_DISARM:
            stop_en_analyseer(*opname)
            opname, disarm_tijd = None, None
except KeyboardInterrupt:
    if opname:
        stop_en_analyseer(*opname)
    print("Gestopt.")
