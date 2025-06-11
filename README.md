## Introduction
This GitHub repository showed how real-time communication works in **NAUTILUS** by using WiFi Mesh Network.

**NAUTILUS** is a prototype created by "Great Wall of FSKTM" team for **UM Technothon 2025**.

## What is Mesh Network?

![Connecting mesh via WiFi](https://raw.githubusercontent.com/binnes/WiFiMeshRaspberryPi/refs/heads/master/images/PiMeshWiFi.png)

A mesh network is a decentralized networking architecture where each node (device) connects directly and dynamically to multiple other nodes. This creates a web-like structure that enables data to be transmitted along many possible paths, improving network reliability and coverage. In a mesh network, nodes can forward data on behalf of others, allowing communication even if some links fail or certain nodes go offline. 

Using a mesh network on NAUTILUS enables robust, self-healing, and scalable wireless communication. This allows to maintain connectivity over wide and dynamic areas, coordinate tasks without a central access point, and adapt to node mobility or failure, making them ideal for applications such as search and rescue, environmental monitoring, and swarm robotics.

## Current Implementation Overview

The current mesh network implementation utilizes the following hardware setup:
- 1 × Raspberry Pi 5 (designated as the bridge)
- 2 × Raspberry Pi 4 (functioning as mesh nodes)
- 1 × laptop

The Raspberry Pi 5 serves as a network bridge, connecting to the laptop via Ethernet. This configuration allows real-time monitoring and management of the mesh network status from the laptop. The two Raspberry Pi 4 devices act as independent nodes within the mesh.

![Insert image here](image_placeholder)

Each node operates a lightweight web server, which periodically transmits essential system information for demonstration purposes. The reported data includes:
- IP address
- CPU temperature
- System uptime

A DHCP server is deployed on the bridge (Raspberry Pi 5) to facilitate automatic IP address assignment for all connected nodes.

**Note:**  
The entire solution is based on the Linux platform. All Raspberry Pi devices run Raspbian Bookworm, while the laptop operates on Ubuntu.


## Setup

### 1. Create the SD card and perform initial setup

1. Download the latest Raspbian image from [https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/). 
2. Flash the image to an SD card suitable for your Raspberry Pi using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).  Instructions are available [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) if needed.

4. Insert the SD card into the Raspberry Pi and then power on the Raspberry Pi.
5. Login to the pi with user **pi** and password **raspberry**.  If using headerless setup then connect via [ssh](/additionalResources/COMMAND_LINE_ACCESS.md).  The hostname on first boot is **raspberrypi.local**.  
6. On the Raspberry Pi command line issue the command

    ```sudo raspi-config```

    and then go through and change the following settings:
    - Change the user password (don't forget it, as you will need it every time you remotely connect to the Pi)
    - Network Options - Hostname
    - Localisation Options - set Locale, Timezone and WiFi country to match your location
    - Network Option - WiFi.  If your pi is not connected to the internet already, use this option to setup WiFi connectivity to ensure your Pi has access to the internet
    - interfacing Options - SSH, ensure SSH server is enabled

    Exit raspi-config, don't reboot yet.
7. Issue command

    ```sudo apt-get update && sudo apt-get upgrade -y```
8. Reboot the Raspberry Pi with command

    ```sudo reboot -n```

### 2. Establish a connection between laptop to bridge node via Ethernet cable
1. Connect Raspberry Pi and laptop directly using Ethernet cable
2. Check the ethernet device on both devices:
```sh
ifconfig
```
Raspberry Pi should be eth0 while laptop should be enpXXX.

3. Assign fixed IPs
On both devices, flush and re-add the IPs:

On laptop:

```sh
sudo ip addr flush dev enpXXX
sudo ip addr add 192.168.50.1/24 dev enp4s0
sudo ip link set up dev enp4s0
```

On the Pi:

```sh
sudo ip addr flush dev eth0
sudo ip addr add 192.168.50.2/24 dev eth0
sudo ip link set up dev eth0
```

4. Ping IP to see of the connection is established:

On laptop:
```sh
> ping 192.168.50.2
PING 192.168.50.2 (192.168.50.2) 56(84) bytes of data.
64 bytes from 192.168.50.2: icmp_seq=1 ttl=64 time=0.165 ms
64 bytes from 192.168.50.2: icmp_seq=2 ttl=64 time=0.163 ms
64 bytes from 192.168.50.2: icmp_seq=3 ttl=64 time=0.192 ms
```
On Raspberry Pi:
```sh
zhenyu@raspberrypi: $ ping 192.168.50.1
PING 192.168.50.1 (192.168.50.1) 56(84) bytes of data.
64 bytes from 192.168.50.1: icmp_seq=1 ttl=64 time=0.267 ms
64 bytes from 192.168.50.1: icmp_seq=2 ttl=64 time=0.152 ms
64 bytes from 192.168.50.1: icmp_seq=3 ttl=64 time=0.134 ms
```

### 3. Git clone and implement mesh network

For bridge:
```
git clone
cd 
./mesh-bridge.sh
```

For node:
```
git clone
cd 
./mesh-node.sh
```
Check the devices in mesh network on bridge after setup
```
sudo batctl n
```
### 4. Set up web client for each Raspberry Pi
```
./web-server.sh
```


## Live Demo
## Potentials

In an ideal configuration, each Raspberry Pi and the laptop would be equipped to operate in both Access Point (AP) mode and mesh mode simultaneously. This dual-mode functionality would allow the laptop to connect directly to any Raspberry Pi to monitor network status, enhancing flexibility and accessibility.

With this setup, it would become feasible to monitor the status of each NAUTILUS node in real time. This includes the ability to observe critical information such as battery levels, camera feeds, and positional coordinates for each device in the mesh network.

## Improvements

The current implementation could be further enhanced by configuring the network bridge to support both Access Point (AP) mode and mesh mode, eliminating the reliance on Ethernet cable communication. This can be achieved by installing an external WiFi adapter, enabling wireless bridging and greater deployment flexibility.

However, due to time constraints, we were unable to procure and integrate the necessary WiFi adapters for this phase of development.

## Credits
[WiFiMeshRaspberryPi by Brian Innes and John Walicki](https://github.com/binnes/WiFiMeshRaspberryPi)

