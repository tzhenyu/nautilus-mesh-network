#!/bin/bash
# mesh-bridge.sh - Mesh WiFi bridge with B.A.T.M.A.N. and DHCP (dnsmasq)
# This script sets up a Raspberry Pi as a mesh bridge and DHCP server for nodes

set -e

# ==== User-configurable variables ====
WIFACE="wlan0"
MESHID="my-mesh-network"
MESH_FREQ=2412          # Channel 1 (2.412 GHz)
BATNAME="bat0"
BRIDGE="br0"
ETH="eth0"
BRIDGE_IP="192.168.199.254/24"
DHCP_RANGE_START="192.168.199.100"
DHCP_RANGE_END="192.168.199.200"
DHCP_LEASE="24h"
DNSMASQ_CONF="/etc/dnsmasq.d/mesh.conf"
# ====================================

# 1. Install dependencies if not present
sudo apt update
sudo apt install -y batctl bridge-utils iw dnsmasq

# 2. Bring down WiFi, set mesh mode, and bring up
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

# 5. Create bridge between bat0 and eth0
sudo brctl addbr $BRIDGE || true
sudo brctl addif $BRIDGE $BATNAME || true
sudo brctl addif $BRIDGE $ETH || true
sudo ip link set up dev $BRIDGE
sudo ip link set up dev $ETH

# 6. Assign static IP to the bridge
sudo ip addr flush dev $BATNAME
sudo ip addr flush dev $WIFACE
sudo ip addr add $BRIDGE_IP dev $BRIDGE

# 7. Configure dnsmasq for DHCP on the bridge
sudo bash -c "cat > $DNSMASQ_CONF" <<EOF
# dnsmasq config for mesh bat0/bridge interface
interface=$BRIDGE
dhcp-range=$DHCP_RANGE_START,$DHCP_RANGE_END,255.255.255.0,$DHCP_LEASE
bind-interfaces
domain-needed
bogus-priv
EOF

# 8. Restart dnsmasq to apply new configuration
sudo systemctl restart dnsmasq

echo "Mesh bridge setup complete."
echo "Bridge IP: $BRIDGE_IP"
echo "DHCP serving: $DHCP_RANGE_START - $DHCP_RANGE_END on $BRIDGE"
