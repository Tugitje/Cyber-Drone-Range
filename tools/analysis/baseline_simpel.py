#!/usr/bin/env python3
"""
Telt MAVLink-berichten in een tcpdump-opname (tcpdump -i any -w bestand.pcap).

Gebruik:  python3 baseline_simpel.py opname.pcap
Toont per richting (drone -> GCS en GCS -> drone) welke berichten er zijn,
hoe vaak, en hoeveel per seconde.

Alleen de verbinding met QGroundControl op de Windows-host (10.0.2.2:14550) telt mee.
"""
import collections
import struct
import sys

from pymavlink.dialects.v20 import ardupilotmega as mavlink

GCS_IP = bytes([10, 0, 2, 2])   # QGroundControl op de host
GCS_POORT = 14550

bestand = sys.argv[1]
tellingen = {"drone -> GCS": collections.Counter(), "GCS -> drone": collections.Counter()}
parser = mavlink.MAVLink(None)
parser.robust_parsing = True
eerste = laatste = None

with open(bestand, "rb") as f:
    kop = f.read(24)                                  # pcap-bestandskop
    linktype = struct.unpack("<I", kop[20:24])[0]
    linkkop = 20 if linktype == 276 else 16           # 276 = Linux cooked v2, 113 = v1

    while True:
        pakketkop = f.read(16)
        if len(pakketkop) < 16:
            break
        sec, usec, lengte, _ = struct.unpack("<IIII", pakketkop)
        data = f.read(lengte)

        ip = data[linkkop:]
        if len(ip) < 28 or ip[9] != 17:               # alleen IPv4 + UDP
            continue
        ihl = (ip[0] & 0x0F) * 4
        src_ip, dst_ip = ip[12:16], ip[16:20]
        src_poort, dst_poort = struct.unpack("!HH", ip[ihl:ihl + 4])
        payload = ip[ihl + 8:]

        if dst_ip == GCS_IP and dst_poort == GCS_POORT:
            richting = "drone -> GCS"
        elif src_ip == GCS_IP and src_poort == GCS_POORT:
            richting = "GCS -> drone"
        else:
            continue

        tijd = sec + usec / 1e6
        eerste = eerste or tijd
        laatste = tijd
        for bericht in parser.parse_buffer(payload) or []:
            naam = bericht.get_type()
            if naam == "BAD_DATA":          # bytes die pymavlink niet als bericht herkent
                naam = "(niet herkend)"
            tellingen[richting][naam] += 1

duur = (laatste - eerste) if eerste else 0
print(f"Opname: {bestand}  ({duur:.0f} seconden)\n")
for richting, teller in tellingen.items():
    print(f"{richting}: {sum(teller.values())} berichten")
    print(f"  {'Bericht':<28}{'Aantal':>8}{'Per seconde':>14}")
    for naam, aantal in teller.most_common():       # alle berichttypes
        print(f"  {naam:<28}{aantal:>8}{aantal / duur if duur else 0:>14.2f}")
    print()
