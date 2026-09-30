# Network Topology and Addressing

This network contains two hosts and two routers. The goal is for Host A to communicate with Host B through both routers using static routing.

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
