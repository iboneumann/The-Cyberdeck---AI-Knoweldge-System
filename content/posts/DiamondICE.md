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
The core class to use the mpiuser from my main user ibo:
```batch
#!/usr/bin/env python3
"""
cluster_ssh.py – Reusable SSH wrapper for split‑privilege clusters.
- On the headnode, 'ibo' runs scripts.
- All remote commands are executed as 'mpiuser' via 'sudo -u mpiuser ssh'.
- Automatically accepts new host keys (no interactive prompts).
- Includes timeout and error handling.

Usage:
    from cluster_ssh import ClusterSSH
    ssh = ClusterSSH(timeout=5)
    out, err, rc = ssh.run("192.168.178.31", "echo OK")
    if rc == 0:
        print("Success:", out)
"""

import subprocess
from typing import Tuple

class ClusterSSH:
    """
    Runs SSH commands as mpiuser using 'sudo -u mpiuser ssh'.
    Assumes:
        - ibo has passwordless sudo to mpiuser (sudoers rule)
        - mpiuser has passwordless sudo on remote nodes (optional, but needed for ufw etc.)
        - mpiuser's SSH key is deployed to all remote nodes' authorized_keys
    """
    def __init__(self, timeout: int = 5, ssh_user: str = "mpiuser"):
        """
        Args:
            timeout: Connection timeout in seconds (also used for command execution +2s).
            ssh_user: Remote user (default 'mpiuser').
        """
        self.timeout = timeout
        self.ssh_user = ssh_user

    def run(self, host: str, cmd: str) -> Tuple[str, str, int]:
        """
        Execute a command on a remote host.

        Returns:
            (stdout, stderr, returncode)
        """
        ssh_cmd = [
            "sudo", "-u", self.ssh_user,
            "ssh", "-T",
            "-o", f"ConnectTimeout={self.timeout}",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "BatchMode=yes",
            f"{self.ssh_user}@{host}", cmd
        ]
        try:
            proc = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=self.timeout + 2)
            return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
        except subprocess.TimeoutExpired:
            return "", f"Timeout after {self.timeout+2}s", -1
        except Exception as e:
            return "", str(e), -1

    def check_connectivity(self, host: str) -> bool:
        """Quick test if the host is reachable and the SSH key works."""
        out, err, rc = self.run(host, "echo OK")
        return rc == 0 and "OK" in out

    def sudo_check(self, host: str) -> bool:
        """Check if mpiuser can run sudo without password on the remote host."""
        out, err, rc = self.run(host, "sudo -n true")
        return rc == 0


# ---------- Example usage ----------
if __name__ == "__main__":
    ssh = ClusterSSH(timeout=3)
    test_host = "192.168.178.31"

    if ssh.check_connectivity(test_host):
        print(f"✅ {test_host} reachable as mpiuser")
        if ssh.sudo_check(test_host):
            print(f"✅ {test_host}: mpiuser has passwordless sudo")
        else:
            print(f"❌ {test_host}: mpiuser cannot run sudo without password")
    else:
        print(f"❌ {test_host} unreachable (SSH key or hostname problem)")
The core script: ice_analytics.py
```

```batch
def enforce_ufw(host: str, all_cluster_ips: List[str]) -> Tuple[bool, List[str]]:
    changes = []
    success = True

    # First, add missing allow rules for all other cluster IPs
    # (these rules are stored even if UFW is inactive)
    for other_ip in all_cluster_ips:
        if other_ip == host:
            continue
        # Check if rule already exists
        check_cmd = f"sudo ufw status | grep -q 'ALLOW.*{other_ip}'"
        out, _, rc_check = ssh.run(host, check_cmd)
        if rc_check == 0:
            changes.append(f"Rule for {other_ip} already exists, skipping")
            continue
        # Add SSH rule
        cmd_ssh = f"sudo ufw allow from {other_ip} to any port 22 proto tcp comment 'SSH from {other_ip}'"
        out_ssh, err_ssh, rc_ssh = ssh.run(host, cmd_ssh)
        if rc_ssh == 0:
            changes.append(f"Added SSH allow for {other_ip}")
        else:
            success = False
            changes.append(f"Failed to add SSH allow for {other_ip}: {err_ssh}")
        # Add MPI rule
        cmd_mpi = f"sudo ufw allow from {other_ip} to any port 1024:65535 proto tcp comment 'MPI from {other_ip}'"
        out_mpi, err_mpi, rc_mpi = ssh.run(host, cmd_mpi)
        if rc_mpi == 0:
            changes.append(f"Added MPI allow for {other_ip}")
        else:
            success = False
            changes.append(f"Failed to add MPI allow for {other_ip}: {err_mpi}")

    # Now enable UFW if it's not already active
    ufw = check_ufw(host)
    if not ufw["active"]:
        cmd = "sudo ufw --force enable"
        out, err, rc = ssh.run(host, cmd)
        if rc == 0:
            changes.append("Enabled UFW")
        else:
            success = False
            changes.append(f"Failed to enable UFW: {err}")
    else:
        changes.append("UFW already active")

    return success, changes

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
  as soon as I have the project completed until there:  
    
  
```bash
If you have the scripts manually, place them in a directory 
(e.g., `~/LTS_Cyberdeck_Scripts/production/Diamond_ICE/`).

### 2. Install required system packages on all nodes
```
Run this on the Headnode (as `mpiuser` or `sudo` user):  
   
```bash
sudo apt update
# Update everything first
sudo apt update && sudo apt upgrade -y

# 1. RKHunter - Rootkit detector (runs weekly by default)
sudo apt install rkhunter -y
sudo rkhunter --propupd  # Update database

# 2. ClamAV - Antivirus (quiet background scans)
sudo apt install clamav clamav-daemon -y
sudo freshclam  # Update virus definitions
sudo systemctl enable clamav-freshclam

# 3. Automatic Security Updates (set and forget)
sudo apt install unattended-upgrades apt-listchanges -y
sudo dpkg-reconfigure --priority=low unattended-upgrades  # Choose "Yes"

# 4. Logwatch - Daily security summary emails
sudo apt install logwatch -y
# Configure minimal daily reports
sudo logwatch --output mail --mailto your@email.com --detail low --service all --range yesterday

# 5. PSAD (Port Scan Attack Detector) - Silent watcher
sudo apt install psad -y
sudo psad --sig-update  # Update attack signatures
sudo systemctl enable psad
```
 What these do automatically:  
    RKHunter: Weekly rootkit scan (emails you if issues)  
    ClamAV: Daily virus scan (low CPU, runs at 2AM)  
    Automatic updates: Security patches install themselves  
    Logwatch: Daily email with suspicious activity  
    PSAD: Blocks port scanners automatically   
  
For worker Nodes:
```bash
# Run on ALL workers
sudo apt update && sudo apt upgrade -y
sudo apt install rkhunter clamav clamav-daemon unattended-upgrades psad -y

# Initialize each
sudo rkhunter --propupd
sudo freshclam
sudo psad --sig-update

# Enable all services
sudo systemctl enable clamav-freshclam
sudo systemctl enable psad
sudo dpkg-reconfigure --priority=low unattended-upgrades
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
