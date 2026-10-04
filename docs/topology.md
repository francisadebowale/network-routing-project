# Network Topology and Addressing

The static routing topology contains two hosts and two routers. The goal is for Host A to communicate with Host B through both routers using static routing.

There are three connections: Host A to Router 1, Router 1 to Router 2, and Router 2 to Host B.

## Interfaces

| Device | Interface | IP address | Connects to |
|---|---|---|---|
| Host A | eth1 | 192.168.10.10/24 | Router 1 |
| Router 1 | eth1 | 192.168.10.1/24 | Host A |
| Router 1 | eth2 | 10.0.0.1/30 | Router 2 |
| Router 2 | eth1 | 10.0.0.2/30 | Router 1 |
| Router 2 | eth2 | 192.168.20.1/24 | Host B |
| Host B | eth1 | 192.168.20.10/24 | Router 2 |

## Subnets

| Subnet | Purpose |
|---|---|
| 192.168.10.0/24 | Host A's local network |
| 10.0.0.0/30 | Link between the routers |
| 192.168.20.0/24 | Host B's local network |

The /30 subnet provides two usable host addresses, enough for the two router interfaces.

## Gateways and Routes

Host A will use 192.168.10.1 as its gateway. Host B will use 192.168.20.1.

Router 1 will need a static route to 192.168.20.0/24 through 10.0.0.2.

Router 2 will need a static route to 192.168.10.0/24 through 10.0.0.1. This provides the return path for replies.

## VLAN Topology

`phase2-vlans/` contains three hosts, a Linux bridge switch and an FRR router. Switch ports eth1 and eth2 are untagged access ports in VLAN 10; eth3 is an untagged access port in VLAN 20. Switch eth4 connects to router eth1 as a tagged trunk carrying both VLANs. Management eth0 stays outside the bridge.

| Device | Interface | VLAN | IP address | Gateway |
|---|---|---|---|---|
| Host A | eth1 | 10 | 192.168.10.10/24 | 192.168.10.1 |
| Host B | eth1 | 10 | 192.168.10.11/24 | 192.168.10.1 |
| Host C | eth1 | 20 | 192.168.20.10/24 | 192.168.20.1 |
| Router | eth1.10 | 10 | 192.168.10.1/24 | N/A |
| Router | eth1.20 | 20 | 192.168.20.1/24 | N/A |

Before routing was configured, temporary addresses in one subnet verified Host A and Host B could ping each other in both directions, while Host A and Host C received no replies in either direction across VLANs. The temporary addresses were then removed.

With the addresses above and router forwarding enabled, Host A could ping Host B, and both VLAN 10 hosts could ping Host C in both directions. Each test received three replies with no packet loss. Both VLAN subnets appeared as installed connected routes on the router.

These results were tested by configuring the existing containers. A fresh deployment from the completed topology has not yet been verified. Switch package installation used an alternative Alpine mirror with a temporary IPv4 host entry in the running container.

## OSPF Topology

`phase3-ospf/` contains three FRR routers connected in a line. Router 1 eth1 connects to Router 2 eth1; Router 2 eth2 connects to Router 3 eth1.

| Router | Interface | IP address |
|---|---|---|
| Router 1 | eth1 | 10.0.12.1/30 |
| Router 1 | lo | 10.255.0.1/32 |
| Router 2 | eth1 | 10.0.12.2/30 |
| Router 2 | eth2 | 10.0.23.1/30 |
| Router 2 | lo | 10.255.0.2/32 |
| Router 3 | eth1 | 10.0.23.2/30 |
| Router 3 | lo | 10.255.0.3/32 |

All project interfaces use OSPF area 0. Each router uses its loopback address as its router ID. Loopbacks are passive: their addresses are advertised without sending neighbour discovery packets. OSPF is not enabled on management eth0.

After redeployment from the saved configuration, all four neighbour entries reached Full state. Each router installed OSPF routes to the other two loopbacks. Router 1 and Router 3 could ping each other's loopback using their own loopback as the source, with three replies and no packet loss in each direction.
