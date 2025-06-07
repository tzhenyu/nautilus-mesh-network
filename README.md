Yes, your idea is very much possible and quite practical! Here’s how your plan would work, step by step:

### 1. BATMAN-adv Mesh Network
- BATMAN-adv (Better Approach To Mobile Adhoc Networking - advanced) is designed for exactly this kind of scenario: creating a layer 2 mesh network over WiFi where all nodes (your Raspberry Pis) are peers.
- Each Raspberry Pi will have a WiFi interface configured to operate in mesh mode (not AP or client) and will use BATMAN-adv to create a seamless network.

### 2. Web Servers on Each Node
- Every Pi runs a web server (e.g., Flask, Node.js, or even simple Python HTTPServer).
- Each web server exposes a status endpoint (e.g., `/status`) with its own data (uptime, temperature, etc.).

### 3. Access Point for Laptop Connection
- One Pi is configured with a second WiFi interface (USB WiFi dongle) or can switch modes between mesh and AP, but **dual interfaces** is recommended for stability.
- This Pi acts as an AP (Access Point) so your laptop can join the mesh network.
- The AP Pi bridges traffic between the AP interface and the mesh network interface.

### 4. Discovering Other Pis’ Status
- Since BATMAN-adv is a layer 2 mesh, all nodes are on the same broadcast domain. The AP Pi can see all others’ IPs.
- The AP Pi (and thus your laptop) can query each Pi’s web server using its mesh IP address (e.g., 192.168.1.X).
- You can write a simple "dashboard" web app (running on the AP Pi or your laptop) to scan the mesh subnet, query `/status` on each Pi, and display a list of their statuses.

### 5. Key Points & Considerations
- **IP Addressing:** Use static IPs or a mesh-local DHCP server so each Pi has a known address.
- **Dual Interfaces:** For the AP Pi, it’s best to have one interface for mesh and another for AP mode.
- **Firewall:** Ensure iptables/ufw allows traffic between the AP and mesh interfaces.
- **Performance:** BATMAN-adv is robust for small to medium meshes; for very large networks, consider OLSR or other protocols.
- **Discovery:** You can use mDNS/Avahi, a simple broadcast, or just scan a known IP range.

---

## Example Topology

```plaintext
        (Mesh Network)
      [Pi1]---[Pi2]---[Pi3]
         \            /
          [AP Pi] (AP mode + mesh mode)
                  |
                Laptop
```

---

## Summary

- **Yes, you can use BATMAN-adv to mesh Pis.**
- **Each Pi can run a web server for status.**
- **One Pi can act as AP for your laptop to join.**
- **A dashboard can poll all Pis and show their status.**

If you need a sample configuration, script, or a network diagram, let me know!
