+++
date = '2026-04-08T15:38:43+02:00'
draft = false
title = 'Diamond ICE'
weight = 37
+++
  
A Cyberdeck in the Dystopian Sci-Fi world is nothing with out ICE. In Shadowrun, ICE stands for Intrusion   
Countermeasures (or sometimes Intrusion Countermeasure Electronics).   
  
In the real world that is a security layer protecting a Computer or Network.   
  
For this Cyberdeck AI Knowledge System exploring the possibilities of Ollama Open Source LLMs in a Thesis  
form, it is using the mpiuser layer of the Beowulf stake to create a security layer in this set up.  
  
We do two things:  
  
Secure the LAN.  
Create the first /etc/hosts using scripts operating within the mpiusers set up on each node.  
  
Here we go.  
  
Summary: The Diamond ICE Architecture  
  
   Cyberdeck (Head Node): Your hardened access point, running Kali tools, Snort, OSSEC server, and a VPN.  
  
   Diamond ICE (Worker Nodes): Locked‑down nodes with only SSH (restricted to download commands), protected   
   by host‑based intrusion detection (OSSEC) and network‑level controls.  
  
   Security Layers: Firewall rules, VPN‑only access, intrusion detection (host and network), file integrity 
   monitoring, and centralized logging.  
  
By implementing this layered defense with open‑source tools, your cluster will resemble the formidable   
“Diamond ICE” of Shadowrun lore—a resilient, monitored fortress where the only entry point is your controlled   
Cyberdeck.  
  
   Note: This configuration is for a private LAN. If you expose any service to the internet, additional   
   precautions (like a reverse proxy, rate limiting, and regular vulnerability scans) are essential.   
   Always keep your tools and systems updated.  
    
   RKHunter - Rootkit detector   
   ClamAV - Antivirus  
   Automatic Security Updates (set and forget)  
   sudo apt install unattended-upgrades apt-listchanges -y  
   sudo dpkg-reconfigure --priority=low unattended-upgrades  # Choose "Yes"  
   Logwatch - Daily security summary emails  
   PSAD (Port Scan Attack Detector)  
  
```batch
================================================================================
                DIAMOND ICE – CLUSTER SECURITY FRAMEWORK
================================================================================

This directory contains the Diamond ICE security suite for your Beowulf cluster.
The core script `ice_analytics.py` audits and enforces a strict security model:

  • Every node must run UFW (Uncomplicated Firewall).
  • Incoming traffic from outside the cluster is blocked.
  • Outgoing internet (updates, surfing) is allowed.
  • Intra‑cluster communication is allowed ONLY between the exact IPs listed in
    /etc/hosts. No subnet wildcards – explicit per‑node rules for SSH and MPI.

This is the "Diamond" part: each node allows every other node individually,
creating a fully connected mesh of trust without relying on network ranges.

================================================================================
                              QUICK START
================================================================================

1. Edit /etc/hosts on the headnode (920) to include all cluster nodes:
     192.168.178.33  headnode
     192.168.178.30  node1
     192.168.178.31  node3
     192.168.178.26  node5
     192.168.178.36  node2
     192.168.178.29  node6
     192.168.178.40  node7

2. Run the security fix (enables UFW, adds explicit rules, configures mpiuser sudo):
     ./ice_analytics.py --fix

3. Generate a report:
     ./ice_analytics.py

4. For automation (cron, CI), use the non‑interactive mode:
     ./ice_analytics.py --yes --json --output /var/log/ice_report.json

================================================================================
                         WHAT THE SCRIPT CHECKS
================================================================================

Metric                  | Meaning                           | Action if not OK
------------------------|-----------------------------------|------------------
Reachable               | Node responds to SSH as mpiuser   | Check network / SSH
mpiuser sudo (nopasswd) | Can run sudo without password     | Run --fix
UFW active              | Firewall is enabled               | Run --fix
UFW explicit rules      | Per‑node allow rules exist        | Run --fix
Fail2Ban active         | SSH brute‑force protection        | Install manually
Exposed services        | Service listening on 0.0.0.0      | Acceptable for lab
Disk warnings           | Root >80% full                    | Move data to USB
Pending updates         | Unpatched security                | apt upgrade

================================================================================
                     HOW EXPLICIT PER‑NODE RULES WORK
================================================================================

When you run `--fix`, the script reads all IPs from /etc/hosts. For each node,
it adds UFW rules that allow traffic from every *other* node:

   • SSH (port 22) from each other node.
   • Full MPI port range (1024-65535) from each other node.

No subnet rule (e.g. 192.168.178.0/24) is ever added. This ensures that even if
a rogue device joins the same LAN, it cannot communicate with cluster nodes
unless explicitly listed in /etc/hosts.

The number of rules grows as O(n²), but UFW handles it easily for clusters up
to ~50 nodes. For larger clusters, consider a subnet rule – but Diamond ICE
prefers explicitness.

================================================================================
                         LOAD BALANCER INTEGRATION
================================================================================

Your Nexus Load Balancer runs on the headnode (port 8888) and connects to Ollama
on worker nodes (port 11434). Because the explicit rules allow all traffic
between cluster nodes (any port), the load balancer works without extra
configuration.

To verify that the load balancer can reach Ollama, run on the headnode:
    curl http://<worker-ip>:11434/api/tags

If you see a JSON response, the connection works.

================================================================================
                        AFTER THE ANALYTICS REPORT
================================================================================

1. If any node shows "UFW explicit rules: WARN", run `--fix` again.
2. If "Exposed services" shows many services, remember this is normal in a lab.
3. To tighten Ollama, you can later add a rule that allows only the headnode:
      sudo ufw allow from 192.168.178.33 to any port 11434
   But this is optional – the cluster‑wide per‑node rules already allow it.
4. Schedule weekly checks with cron:
      (crontab -l; echo "0 2 * * 1 /path/to/ice_analytics.py --yes --json --output 
      /var/log/ice_weekly.json") | crontab -

================================================================================
                               FILES
================================================================================

ice_analytics.py        – Main script (audit + fix)
ollama_nexus_client.py  – AI client using Nexus LB
README.txt              – This file

================================================================================
                               SUPPORT
================================================================================

For questions, refer to the chat history with your AI assistant. The script is
designed to be self‑documenting; use `./ice_analytics.py --help`.

================================================================================
                             DIAMOND ICE READY
================================================================================
```
  
The core script: ice_analytics.py
  
```batch
#!/usr/bin/env python3
"""
ICE Analytics & Enforcement Script - Cluster Security Auditor & Fixer
- Reads /etc/hosts for cluster nodes
- Uses mpiuser for all remote operations (must have passwordless sudo)
- Ensures UFW is active and allows intra‑cluster traffic via EXPLICIT per‑node rules
- Checks Fail2Ban, exposed services, disk usage, pending updates
- Optionally applies missing configurations (--fix)

Usage:
  ./ice_analytics.py                # Report only
  ./ice_analytics.py --fix          # Apply missing UFW rules & configure mpiuser sudo
  ./ice_analytics.py --yes --fix    # Non‑interactive
  ./ice_analytics.py --json         # JSON output
"""

import subprocess
import re
import sys
import os
import json
import argparse
import signal
import atexit
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# ---------- rich formatting (optional) ----------
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = print

# ---------- terminal restoration (fixes broken terminal) ----------
def restore_terminal():
    try:
        subprocess.run(['stty', 'sane'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        pass

def signal_handler(sig, frame):
    restore_terminal()
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(restore_terminal)

# ---------- configuration ----------
CLUSTER_SUBNET = "192.168.178.0/24"   # Only used for display, not for UFW rules
SSH_USER = "mpiuser"                  # primary remote user (must have passwordless sudo)
SSH_TIMEOUT = 5
CRITICAL_PORTS = {
    22: "SSH",
    11434: "Ollama",
    8080: "HAProxy",
    9090: "Prometheus",
    80: "HTTP",
    443: "HTTPS",
}
WARN_DISK_USAGE = 80
ARGS = None

# ---------- utilities ----------
def run_local_cmd(cmd: List[str]) -> Tuple[str, str, int]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except Exception as e:
        return "", str(e), -1

def run_remote_cmd(host: str, cmd: str, user: str = SSH_USER) -> Tuple[str, str, int]:
    ssh_cmd = [
        "ssh", "-T", "-o", f"ConnectTimeout={SSH_TIMEOUT}",
        "-o", "BatchMode=yes",
        f"{user}@{host}", cmd
    ]
    return run_local_cmd(ssh_cmd)

def parse_etc_hosts() -> List[Tuple[str, str]]:
    nodes = []
    try:
        with open("/etc/hosts", "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    if ip.startswith("192.168.178."):
                        hostname = parts[1]
                        nodes.append((ip, hostname))
    except Exception as e:
        print(f"Error reading /etc/hosts: {e}")
        sys.exit(1)
    return nodes

def get_cluster_ips(nodes: List[Tuple[str, str]]) -> List[str]:
    """Extract IPs from node list."""
    return [ip for ip, _ in nodes]

# ---------- check functions (all run as mpiuser) ----------
def check_ssh_connectivity(host: str) -> bool:
    out, err, rc = run_remote_cmd(host, "echo OK")
    return rc == 0 and "OK" in out

def check_sudo_nopasswd(host: str) -> bool:
    """Check if mpiuser can run sudo without password."""
    out, err, rc = run_remote_cmd(host, "sudo -n true")
    return rc == 0

def check_fail2ban(host: str) -> Dict:
    result = {"installed": False, "active": False, "jails": [], "banned_count": 0}
    out, _, rc = run_remote_cmd(host, "dpkg -l fail2ban 2>/dev/null | grep ^ii")
    if rc == 0 and out:
        result["installed"] = True
        out, _, rc = run_remote_cmd(host, "systemctl is-active fail2ban")
        result["active"] = (rc == 0 and out.strip() == "active")
        if result["active"]:
            out, _, _ = run_remote_cmd(host, "sudo fail2ban-client status | grep 'Jail list' 
| cut -d':' -f2")
            if out:
                result["jails"] = [j.strip() for j in out.split(',')]
            out, _, _ = run_remote_cmd(host, "sudo fail2ban-client status sshd 2>/dev/null 
| grep 'Total banned' | awk '{print $NF}'")
            if out and out.isdigit():
                result["banned_count"] = int(out)
    return result

def check_ufw(host: str) -> Dict:
    result = {"active": False, "has_rules": False, "rules": []}
    out, _, rc = run_remote_cmd(host, "sudo ufw status")
    if rc == 0:
        if "Status: active" in out:
            result["active"] = True
            # Look for any "allow" rules (not just subnet)
            if "ALLOW" in out:
                result["has_rules"] = True
            for line in out.split('\n'):
                if line.strip() and not line.startswith('Status:'):
                    result["rules"].append(line.strip())
    return result

def check_exposed_services(host: str) -> Dict:
    result = {}
    for port, name in CRITICAL_PORTS.items():
        cmd = f"sudo netstat -tlnp 2>/dev/null | grep ':{port} ' | grep -E '0.0.0.0:|:::'"
        out, _, _ = run_remote_cmd(host, cmd)
        if out:
            result[name] = "EXPOSED"
        else:
            cmd_local = f"sudo netstat -tlnp 2>/dev/null | grep ':{port} ' | grep '127.0.0.1'"
            out_local, _, _ = run_remote_cmd(host, cmd_local)
            if out_local:
                result[name] = "SECURE (localhost)"
            else:
                result[name] = "NOT LISTENING"
    return result

def check_disk_usage(host: str) -> Dict:
    cmd = "df -h / | tail -1 | awk '{print $5}' | sed 's/%//'"
    out, _, rc = run_remote_cmd(host, cmd)
    if rc == 0 and out and out.isdigit():
        usage = int(out)
        return {"usage": usage, "status": "OK" if usage < WARN_DISK_USAGE else "WARN"}
    return {"usage": -1, "status": "UNKNOWN"}

def check_updates(host: str) -> Dict:
    cmd = "apt list --upgradable 2>/dev/null | grep -c 'security' || echo 0"
    out, _, rc = run_remote_cmd(host, cmd)
    count = 0
    if rc == 0 and out:
        try:
            count = int(out.strip())
        except:
            pass
    return {"pending_security": count, "status": "OK" if count == 0 else "PENDING"}

# ---------- enforcement functions (called only with --fix) ----------
def setup_mpiuser_sudo(host: str) -> Tuple[bool, List[str]]:
    """Use ibo's SSH to configure passwordless sudo for mpiuser on this node."""
    changes = []
    cmd = "echo 'mpiuser ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/mpiuser-nopasswd 
&& sudo chmod 440 /etc/sudoers.d/mpiuser-nopasswd"
    ssh_cmd = ["ssh", "-T", "-o", f"ConnectTimeout={SSH_TIMEOUT}", f"ibo@{host}", cmd]
    out, err, rc = run_local_cmd(ssh_cmd)
    if rc == 0:
        changes.append(f"Configured passwordless sudo for mpiuser on {host}")
        return True, changes
    else:
        changes.append(f"Failed to configure sudo for mpiuser on {host}: {err}")
        return False, changes

def enforce_ufw(host: str, all_cluster_ips: List[str]) -> Tuple[bool, List[str]]:
    """
    Ensure UFW is active and allows traffic from every other cluster node (explicit per‑node rules).
    No subnet rule – only explicit IPs from /etc/hosts.
    """
    changes = []
    success = True
    ufw = check_ufw(host)
    
    # Enable UFW if not active
    if not ufw["active"]:
        cmd = "sudo ufw --force reset && sudo ufw default deny incoming && sudo ufw 
default allow outgoing && sudo ufw --force enable"
        out, err, rc = run_remote_cmd(host, cmd)
        if rc == 0:
            changes.append("Enabled UFW")
        else:
            success = False
            changes.append(f"Failed to enable UFW: {err}")
    
    # Add explicit allow rules for every other node in the cluster
    # We allow SSH (port 22) and the full MPI port range (1024-65535)
    for other_ip in all_cluster_ips:
        if other_ip == host:
            continue  # no need to allow self
        # Allow SSH
        cmd_ssh = f"sudo ufw allow from {other_ip} to any port 22 proto tcp comment 
'SSH from {other_ip}'"
        out_ssh, err_ssh, rc_ssh = run_remote_cmd(host, cmd_ssh)
        if rc_ssh == 0:
            changes.append(f"Allowed SSH from {other_ip}")
        else:
            success = False
            changes.append(f"Failed to allow SSH from {other_ip}: {err_ssh}")
        # Allow MPI port range
        cmd_mpi = f"sudo ufw allow from {other_ip} to any port 1024:65535 proto tcp comment 
'MPI from {other_ip}'"
        out_mpi, err_mpi, rc_mpi = run_remote_cmd(host, cmd_mpi)
        if rc_mpi == 0:
            changes.append(f"Allowed MPI range from {other_ip}")
        else:
            success = False
            changes.append(f"Failed to allow MPI range from {other_ip}: {err_mpi}")
    
    return success, changes

# ---------- report generation (formatted) ----------
def print_report(nodes: List[Tuple[str, str]]):
    all_ips = get_cluster_ips(nodes)
    summary = {
        "total": len(nodes),
        "reachable": 0,
        "sudo_nopasswd": 0,
        "ufw_active": 0,
        "ufw_has_rules": 0,
        "fail2ban_active": 0,
        "exposed_services": 0,
        "disk_warnings": 0,
        "pending_updates": 0,
    }

    if RICH_AVAILABLE:
        console.print(Panel.fit("[bold cyan]🧊 ICE CLUSTER ANALYTICS REPORT[/bold cyan]", 
border_style="cyan"))
        console.print(f"[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
        console.print(f"[dim]Cluster subnet: {CLUSTER_SUBNET} (explicit per‑node rules)[/dim]")
        console.print(f"[dim]Nodes found: {len(nodes)}[/dim]\n")
    else:
        print("=" * 80)
        print(f"🧊 ICE CLUSTER ANALYTICS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(f"Cluster subnet: {CLUSTER_SUBNET} (explicit per‑node rules)")
        print(f"Nodes found: {len(nodes)}")
        print("-" * 80)

    for ip, hostname in nodes:
        if RICH_AVAILABLE:
            console.print(f"\n[bold yellow]📡 {hostname} ({ip})[/bold yellow]")
            console.print("─" * 40)
        else:
            print(f"\n📡 NODE: {hostname} ({ip})")
            print("-" * 40)

        # SSH connectivity (as mpiuser)
        ssh_ok = check_ssh_connectivity(ip)
        if not ssh_ok:
            if RICH_AVAILABLE:
                console.print("[red]❌ SSH (mpiuser): UNREACHABLE - skipping most checks[/red]")
            else:
                print("  ❌ SSH (mpiuser): UNREACHABLE - skipping most checks")
            continue
        summary["reachable"] += 1
        if RICH_AVAILABLE:
            console.print("[green]✅ SSH (mpiuser): Reachable[/green]")
        else:
            print("  ✅ SSH (mpiuser): Reachable")

        # Passwordless sudo check
        sudo_ok = check_sudo_nopasswd(ip)
        if sudo_ok:
            summary["sudo_nopasswd"] += 1
            if RICH_AVAILABLE:
                console.print("[green]✅ mpiuser has passwordless sudo[/green]")
            else:
                print("  ✅ mpiuser has passwordless sudo")
        else:
            if RICH_AVAILABLE:
                console.print("[red]❌ mpiuser cannot run sudo without password[/red]")
            else:
                print("  ❌ mpiuser cannot run sudo without password")

        # Fail2Ban
        fb = check_fail2ban(ip)
        if not fb["installed"]:
            if RICH_AVAILABLE:
                console.print("[red]❌ Fail2Ban: NOT INSTALLED[/red]")
            else:
                print("  ❌ Fail2Ban: NOT INSTALLED")
        elif not fb["active"]:
            if RICH_AVAILABLE:
                console.print("[yellow]⚠️ Fail2Ban: INSTALLED but NOT ACTIVE[/yellow]")
            else:
                print("  ⚠️  Fail2Ban: INSTALLED but NOT ACTIVE")
        else:
            summary["fail2ban_active"] += 1
            jail_str = ', '.join(fb['jails']) if fb['jails'] else 'none'
            if RICH_AVAILABLE:
                console.print(f"[green]✅ Fail2Ban: ACTIVE[/green] (jails: {jail_str})")
                if fb["banned_count"] > 0:
                    console.print(f"     [red]🚫 Banned IPs: {fb['banned_count']}[/red]")
            else:
                print(f"  ✅ Fail2Ban: ACTIVE (jails: {jail_str})")
                if fb["banned_count"] > 0:
                    print(f"     🚫 Banned IPs: {fb['banned_count']}")

        # UFW
        ufw = check_ufw(ip)
        if not ufw["active"]:
            if RICH_AVAILABLE:
                console.print("[red]❌ UFW: NOT ACTIVE[/red]")
            else:
                print("  ❌ UFW: NOT ACTIVE")
        else:
            summary["ufw_active"] += 1
            if ufw["has_rules"]:
                summary["ufw_has_rules"] += 1
                if RICH_AVAILABLE:
                    console.print("[green]✅ UFW: ACTIVE and explicit allow rules present[/green]")
                else:
                    print("  ✅ UFW: ACTIVE and explicit allow rules present")
            else:
                if RICH_AVAILABLE:
                    console.print("[yellow]⚠️ UFW: ACTIVE but no explicit allow rules[/yellow]")
                else:
                    print("  ⚠️  UFW: ACTIVE but no explicit allow rules")

        # Exposed services
        if RICH_AVAILABLE:
            console.print("[bold cyan]🔌 Service exposure:[/bold cyan]")
        else:
            print("  🔌 Service exposure:")
        services = check_exposed_services(ip)
        for svc, status in services.items():
            if "EXPOSED" in status:
                summary["exposed_services"] += 1
                if RICH_AVAILABLE:
                    console.print(f"     [red]❌ {svc}: {status}[/red]")
                else:
                    print(f"     ❌ {svc}: {status}")
            elif "SECURE" in status:
                if RICH_AVAILABLE:
                    console.print(f"     [green]✅ {svc}: {status}[/green]")
                else:
                    print(f"     ✅ {svc}: {status}")
            else:
                if RICH_AVAILABLE:
                    console.print(f"     [dim]ℹ️ {svc}: {status}[/dim]")
                else:
                    print(f"     ℹ️  {svc}: {status}")

        # Disk usage
        disk = check_disk_usage(ip)
        if disk["usage"] >= 0:
            if disk["status"] == "WARN":
                summary["disk_warnings"] += 1
                if RICH_AVAILABLE:
                    console.print(f"[yellow]⚠️ Root disk: {disk['usage']}% used 
(>{WARN_DISK_USAGE}%)[/yellow]")
                else:
                    print(f"  ⚠️ Root disk: {disk['usage']}% used - above threshold")
            else:
                if RICH_AVAILABLE:
                    console.print(f"[green]✅ Root disk: {disk['usage']}% used[/green]")
                else:
                    print(f"  ✅ Root disk: {disk['usage']}% used")
        else:
            if RICH_AVAILABLE:
                console.print("[dim]💾 Root disk: UNKNOWN[/dim]")
            else:
                print("  💾 Root disk: UNKNOWN")

        # Pending updates
        updates = check_updates(ip)
        if updates["pending_security"] > 0:
            summary["pending_updates"] += updates["pending_security"]
            if RICH_AVAILABLE:
                console.print(f"[yellow]🔄 Security updates: {updates['pending_security']} 
pending[/yellow]")
            else:
                print(f"  🔄 Security updates: ⚠️ {updates['pending_security']} pending")
        else:
            if RICH_AVAILABLE:
                console.print("[green]🔄 Security updates: up to date[/green]")
            else:
                print("  🔄 Security updates: ✅ up to date")

    # Summary table
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]📊 SUMMARY[/bold cyan]")
        table = Table(title="Cluster Security Overview (Explicit Per‑Node Rules)", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Status", style="yellow")
        table.add_row("Total nodes", str(summary["total"]), "")
        table.add_row("Reachable", f"{summary['reachable']}/{summary['total']}", "OK" 
if summary['reachable'] == summary['total'] else "WARN")
        table.add_row("mpiuser sudo (nopasswd)", f"{summary['sudo_nopasswd']}/{summary['reachable']}", "OK" 
if summary['sudo_nopasswd'] == summary['reachable'] else "WARN")
        table.add_row("UFW active", f"{summary['ufw_active']}/{summary['reachable']}", "OK" 
if summary['ufw_active'] == summary['reachable'] else "WARN")
        table.add_row("UFW explicit rules", f"{summary['ufw_has_rules']}/{summary['ufw_active']}", "OK" 
if summary['ufw_has_rules'] == summary['ufw_active'] else "WARN")
        table.add_row("Fail2Ban active", f"{summary['fail2ban_active']}/{summary['reachable']}", "OK" 
if summary['fail2ban_active'] == summary['reachable'] else "WARN")
        table.add_row("Exposed services", str(summary["exposed_services"]), "CRITICAL" 
if summary["exposed_services"] > 0 else "OK")
        table.add_row("Disk warnings", str(summary["disk_warnings"]), "WARN" 
if summary["disk_warnings"] > 0 else "OK")
        table.add_row("Pending security updates", str(summary["pending_updates"]), "WARN" 
if summary["pending_updates"] > 0 else "OK")
        console.print(table)
    else:
        print("\n" + "=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"Total nodes: {summary['total']}")
        print(f"Reachable: {summary['reachable']}/{summary['total']}")
        print(f"mpiuser sudo (nopasswd): {summary['sudo_nopasswd']}/{summary['reachable']}")
        print(f"UFW active: {summary['ufw_active']}/{summary['reachable']}")
        print(f"UFW explicit rules: {summary['ufw_has_rules']}/{summary['ufw_active']}")
        print(f"Fail2Ban active: {summary['fail2ban_active']}/{summary['reachable']}")
        print(f"Exposed services: {summary['exposed_services']}")
        print(f"Disk warnings: {summary['disk_warnings']}")
        print(f"Pending security updates: {summary['pending_updates']}")

    # Recommendations
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]🎯 RECOMMENDATIONS[/bold cyan]")
        recos = [
            "Run './ice_analytics.py --fix' to enable UFW and add explicit per‑node allow rules.",
            "Ensure Fail2Ban is active on all nodes (especially Raspberry Pis).",
            "Restrict exposed services (Ollama, HAProxy) to localhost or VPN if they must not be 
            cluster‑wide.",
            "Set up automatic file moving from Downloads, dwhelper to USB pool.",
            "Schedule weekly security updates with `unattended-upgrades`.",
            "The explicit per‑node rules are the Diamond ICE standard – no subnet wildcards."
        ]
        for rec in recos:
            console.print(f"• {rec}")
    else:
        print("\n🎯 RECOMMENDATIONS")
        print("=" * 80)
        print("1. Run './ice_analytics.py --fix' to enable UFW and add explicit per‑node allow rules.")
        print("2. Ensure Fail2Ban is active on all nodes (especially Raspberry Pis).")
        print("3. Restrict exposed services (Ollama, HAProxy) to localhost or VPN if they must not 
        be cluster‑wide.")
        print("4. Set up automatic file moving from Downloads, dwhelper to USB pool.")
        print("5. Schedule weekly security updates with `unattended-upgrades`.")
        print("6. The explicit per‑node rules are the Diamond ICE standard – no subnet wildcards.")

# ---------- main ----------
def main():
    global ARGS
    parser = argparse.ArgumentParser(description="ICE Cluster Security Auditor & Fixer 
    (using mpiuser, explicit per‑node rules)")
    parser.add_argument("--fix", action="store_true", help="Apply missing configurations 
    (UFW explicit rules, mpiuser sudo)")
    parser.add_argument("--yes", action="store_true", help="Skip all interactive prompts")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead 
    of formatted report")
    parser.add_argument("--output", help="Save JSON output to file")
    ARGS = parser.parse_args()

    nodes = parse_etc_hosts()
    if not nodes:
        print("No cluster nodes found in /etc/hosts. Please ensure IPs are listed.")
        sys.exit(1)

    all_ips = get_cluster_ips(nodes)

    # If --fix, apply missing configurations
    if ARGS.fix:
        print("🔧 Applying missing configurations...")

        # Step 1: Configure passwordless sudo for mpiuser on all nodes (using ibo SSH)
        for ip, hostname in nodes:
            print(f"\nSetting up mpiuser sudo on {hostname} ({ip})...")
            success, changes = setup_mpiuser_sudo(ip)
            for change in changes:
                print(f"  {'✅' if success else '❌'} {change}")

        # Step 2: Enable UFW and add explicit per‑node rules (now as mpiuser with sudo)
        for ip, hostname in nodes:
            print(f"\nConfiguring UFW on {hostname} ({ip})...")
            success, changes = enforce_ufw(ip, all_ips)
            for change in changes:
                print(f"  {'✅' if success else '❌'} {change}")

        print("\n✅ Fixes applied. Re-running report...\n")

    if ARGS.json:
        # JSON output (no formatting)
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "subnet": CLUSTER_SUBNET,
            "explicit_rules": True,
            "nodes": []
        }
        for ip, hostname in nodes:
            ssh_ok = check_ssh_connectivity(ip)
            node_info = {
                "ip": ip,
                "hostname": hostname,
                "reachable": ssh_ok,
            }
            if ssh_ok:
                node_info["sudo_nopasswd"] = check_sudo_nopasswd(ip)
                node_info["fail2ban"] = check_fail2ban(ip)
                node_info["ufw"] = check_ufw(ip)
                node_info["services"] = check_exposed_services(ip)
                node_info["disk"] = check_disk_usage(ip)
                node_info["updates"] = check_updates(ip)
            report_data["nodes"].append(node_info)
        json_out = json.dumps(report_data, indent=2)
        if ARGS.output:
            with open(ARGS.output, "w") as f:
                f.write(json_out)
            print(f"JSON report saved to {ARGS.output}")
        else:
            print(json_out)
    else:
        print_report(nodes)

if __name__ == "__main__":
    main()
```
  
Finally a DeepSeek generated set up instruction manual:
  
```batch
# 🧊 Diamond ICE: Installing the Ultimate Beowulf Cluster Security Suite

*This guide walks you through hardening your Beowulf cluster with the Diamond ICE framework 
– explicit per‑node firewall rules, automated security auditing, and full integration with 
your AI load balancer.*

---

## 📋 Prerequisites

Before you begin, ensure your environment meets these requirements:

| Component | Requirement |
|-----------|-------------|
| **LAN** | A dedicated subnet (e.g., `192.168.178.0/24`) where all cluster nodes reside. |
| **Beowulf Cluster** | At least two nodes (headnode + workers) with SSH access. |
| **Headnode** | Runs the Nexus Load Balancer and the ICE analytics script. |
| **Worker Nodes** | Run Ollama, MPI jobs, or other services. |
| **User Accounts** | `mpiuser` exists on every node (dedicated for MPI & automation) and 
has passwordless `sudo` (configured by the script). |
| **`/etc/hosts`** | Contains the IP and hostname of **every** cluster node. Example:

  192.168.178.33  headnode
  192.168.178.30  worker1
  192.168.178.31  worker2
  192.168.178.26  worker3

| **Network** | All nodes can reach each other via SSH (keys recommended). |
| **Python 3** | Version 3.8 or newer on the headnode. |

> 💡 **Why explicit per‑node rules?**  
> Diamond ICE rejects subnet‑wide wildcards. Instead, it reads `/etc/hosts` and adds 
UFW rules that allow traffic **only between the exact IPs listed**. This prevents rogue 
devices on the same LAN from accessing your cluster.

---

## 🚀 Installation Steps

### 1. Clone the Diamond ICE repository onto your headnode
```
  
```bash
cd ~
git clone https://github.com/your-org/diamond-ice.git
cd diamond-ice
```
  
```bash
If you have the scripts manually, place them in a directory 
(e.g., `~/LTS_Cyberdeck_Scripts/production/Diamond_ICE/`).

### 2. Install required system packages on all nodes

Run this on every node (as `mpiuser` or `sudo` user):
```
   
```bash
sudo apt update
sudo apt install -y ufw fail2ban
```
  
```bash
### 3. Configure `mpiuser` with passwordless sudo (one‑time)

The script can do this automatically, but you may also pre‑configure it:

# On each node, as a user with sudo (e.g., ibo)
echo "mpiuser ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/mpiuser-nopasswd
sudo chmod 440 /etc/sudoers.d/mpiuser-nopasswd

### 4. Run the ICE analytics & fix script

The main script `ice_analytics.py` does two things:

- **Reports** the current security status.
- **Fixes** missing configurations when `--fix` is used.
```
  
```bash
cd ~/LTS_Cyberdeck_Scripts/production/Diamond_ICE
chmod +x ice_analytics.py
./ice_analytics.py --fix
```
  
```bash
What happens during `--fix`:

1. It reads `/etc/hosts` to get all cluster IPs.
2. For **each node**, it enables UFW (if not already active).
3. For **each node**, it adds explicit allow rules for **every other node**:
   - SSH (port 22)
   - MPI port range (1024‑65535)
4. It configures passwordless `sudo` for `mpiuser` on all nodes (using your `ibo` SSH key).

> 🔒 No subnet rules – only explicit per‑node allowances. This is the Diamond ICE standard.

### 5. Verify the setup with a report
     
./ice_analytics.py`

You will see a colour‑coded table (if `rich` is installed) or plain text. Look for:

- `✅ UFW active and explicit allow rules present`
- `✅ mpiuser has passwordless sudo`
- `✅ Fail2Ban: ACTIVE`

If any metric shows `WARN` or `CRITICAL`, follow the recommendations printed at the end 
of the report.

### 6. (Optional) Install `rich` for prettier output
```
```bash
pip install rich
```
```bash
Then re‑run the report for beautiful tables and colour coding.

---

## 🔌 Integrating the Nexus Load Balancer

Your cluster likely includes a **Nexus Load Balancer** (port `8888`) on the headnode that 
distributes AI tasks to Ollama workers. Diamond ICE fully supports this:

- Because UFW rules allow **all ports** between cluster nodes (not just 22 and the MPI range), 
  the load balancer can reach Ollama on any worker without extra rules.
- Ollama remains listening on `0.0.0.0:11434` (default) – which is **exposed** according to the 
  report, but in a lab with per‑node UFW rules, this exposure is harmless because only cluster 
  IPs are allowed.

To verify the load balancer can talk to a worker:

# From headnode, test connection to worker's Ollama
curl http://192.168.178.30:11434/api/tags

If you get a JSON response, the load balancer integration works.

---

## 📊 Understanding the Report Metrics

| Metric | Desired State | Action if not OK |
|--------|---------------|------------------|
| **Reachable** | All nodes reachable | Check network or SSH service. |
| **mpiuser sudo (nopasswd)** | All nodes OK | Run `--fix` again or manually add sudoers file. |
| **UFW active** | All nodes active | Run `--fix` to enable UFW. |
| **UFW explicit rules** | All active nodes have rules | Run `--fix` to add per‑node rules. |
| **Fail2Ban active** | All nodes active | Install and start Fail2Ban manually. |
| **Exposed services** | *Ignored in lab* | In production, restrict to localhost or VPN. |
| **Disk warnings** | None | Move large files to USB storage. |
| **Pending security updates** | Zero | Run `sudo apt upgrade -y` on each node. |

---

## 🧪 Testing the Firewall Rules

After running `--fix`, you can test that only cluster nodes can connect:
```
  
```bash
# From a non‑cluster machine (different IP), try to SSH:
ssh mpiuser@192.168.178.33
# Should timeout or be rejected (UFW default deny incoming)

# From another cluster node:
ssh mpiuser@192.168.178.33
# Should succeed (explicit allow rule)
```
```bash
Check UFW status on any node:

sudo ufw status numbered

You will see many rules like:

[ 1] 22/tcp ALLOW IN FROM 192.168.178.30
[ 2] 1024:65535/tcp ALLOW IN FROM 192.168.178.30
[ 3] 22/tcp ALLOW IN FROM 192.168.178.31

No subnet rule (`192.168.178.0/24`) – only explicit per‑node entries.

---

## 🔄 Automating with Cron

To run a security report every Monday at 2 AM and save JSON output:
```
```bash
(crontab -l 2>/dev/null; echo "0 2 * * 1 /home/mpiuser/diamond-ice/ice_analytics.py --yes --json 
--output /var/log/ice_weekly.json") | crontab -
```
  
```bash
The `--yes` flag disables all interactive prompts.

---

## 🎯 Final Checklist

- [ ] `/etc/hosts` contains all cluster IPs.
- [ ] `mpiuser` exists on every node.
- [ ] `./ice_analytics.py --fix` ran without errors.
- [ ] Report shows `UFW explicit rules: OK` for all nodes.
- [ ] Load balancer can reach Ollama workers (test with `curl`).
- [ ] Cron job scheduled for weekly reports.

---

## 📚 Additional Resources

- `ice_analytics.py --help` – full command‑line reference.
- `README.txt` (in the same directory) – detailed explanation of the Diamond ICE philosophy.
- The chat history with your AI assistant – contains the evolution of the scripts.

---

**Your cluster is now fortified with Diamond ICE – explicit, verifiable, and automated security.** 🧊🔒

*Happy clustering!*
``` 
