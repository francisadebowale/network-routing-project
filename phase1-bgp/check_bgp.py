"""Check expected BGP neighbours and display learned routes."""

import json
import subprocess
import sys

# Expected neighbours for each router.
ROUTERS = {
    "router1": {"10.0.12.2"},
    "router2": {"10.0.12.1", "10.0.23.2"},
    "router3": {"10.0.23.1"},
}


def query(router, command):
    """Run a read-only FRR command and parse its JSON response."""
    result = subprocess.run(
        ["docker", "exec", f"clab-bgp-{router}", "vtysh", "-c", command],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return data


def main():
    failed = False

    for router, expected_peers in ROUTERS.items():
        print(f"\n{router}")

        try:
            summary = query(router, "show bgp summary json")
            routes = query(router, "show ip route bgp json")
            peers = summary["ipv4Unicast"]["peers"]
            if not isinstance(peers, dict):
                raise ValueError("Expected a peers object")

            # Include expected peers so missing configurations are detected.
            for address in sorted(expected_peers | set(peers)):
                peer = peers.get(address)
                state = peer["state"] if peer is not None else "Missing"
                healthy = address in expected_peers and state == "Established"
                label = "OK" if healthy else "FAIL"
                print(f"  [{label}] {address}: {state}")
                if not healthy:
                    failed = True

            print(f"  Learned BGP prefixes: {len(routes)}")
            for prefix, entries in sorted(routes.items()):
                next_hops = {
                    hop["ip"]
                    for entry in entries
                    for hop in entry.get("nexthops", [])
                    if "ip" in hop
                }
                via = ", ".join(sorted(next_hops)) or "unavailable"
                print(f"    {prefix} via {via}")

        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            OSError,
            ValueError,
            KeyError,
            TypeError,
            AttributeError,
        ) as error:
            failed = True
            if isinstance(error, subprocess.CalledProcessError):
                detail = error.stderr.strip() or error.stdout.strip() or str(error)
            else:
                detail = str(error)
            print(f"  [ERROR] {detail}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
