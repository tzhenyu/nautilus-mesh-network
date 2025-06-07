#!/bin/bash
# mesh-node.sh
# For a mesh-only Raspberry Pi node using DHCP (compatible with mesh bridge)

set -e

# ==== User-configurable variables ====
WIFACE="wlan0"
MESHID="my-mesh-network"
MESH_FREQ=2412          # Channel 1 (2.412 GHz)
BATNAME="bat0"
# ====================================

# 1. Install dependencies if not present
sudo apt update
sudo apt install -y batctl iw

# 2. Bring down the WiFi interface and set mesh mode
sudo ip link set $WIFACE down
sudo iw dev $WIFACE set type mp
sudo ip link set $WIFACE up

# 3. Join 802.11s mesh
sudo iw dev $WIFACE mesh join $MESHID freq $MESH_FREQ

# 4. Load batman-adv and add wlan0 to batman
sudo modprobe batman-adv
sudo batctl if add $WIFACE
sudo ip link set up dev $BATNAME
sudo ip link set up dev $WIFACE

# 5. Use DHCP to get IP for bat0 (compatible with mesh bridge running dnsmasq)
sudo ip addr flush dev $BATNAME
sudo ip addr flush dev $WIFACE
sudo dhclient -v $BATNAME

echo "Mesh node setup complete. DHCP request sent on $BATNAME."
