# OpenClaw + Wazuh + Catalyst Command Reference

A complete command reference for managing the **OpenClaw + Wazuh + Catalyst** environment.

---

# OpenClaw (Ubuntu WSL)

## Gateway

```bash
# Start / Stop / Restart Gateway
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status
openclaw gateway install
openclaw gateway uninstall
```

## Logs

```bash
openclaw logs
openclaw logs --follow
openclaw logs --follow --local-time
```

## Chat

```bash
openclaw chat
openclaw chat --session wazuh
openclaw chat --message "your message here"
```

## Dashboard

```bash
openclaw dashboard
openclaw dashboard --no-open
```

## MCP Servers

```bash
openclaw mcp add wazuh --url http://192.168.159.134:9090/mcp --transport streamable-http --no-probe
openclaw mcp list
openclaw mcp remove wazuh
```

## Doctor / Repair

```bash
openclaw doctor
openclaw doctor --fix
openclaw doctor --repair
openclaw doctor --generate-gateway-token
```

## Configuration

```bash
nano ~/.openclaw/.env
nano ~/.openclaw/openclaw.json
nano ~/.openclaw/agents/wazuh-analyst.md
```

---

# Wazuh Manager (Kali VM)

## Manager Service

```bash
sudo systemctl start wazuh-manager
sudo systemctl stop wazuh-manager
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager
```

## Indexer Service

```bash
sudo systemctl start wazuh-indexer
sudo systemctl stop wazuh-indexer
sudo systemctl restart wazuh-indexer
sudo systemctl status wazuh-indexer
```

## Dashboard Service

```bash
sudo systemctl start wazuh-dashboard
sudo systemctl stop wazuh-dashboard
sudo systemctl restart wazuh-dashboard
sudo systemctl status wazuh-dashboard
```

## Configuration

```bash
sudo nano /var/ossec/etc/ossec.conf
```

## Logs

```bash
sudo tail -f /var/ossec/logs/ossec.log
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

## Find Credentials

```bash
sudo tar -O -xf ~/wazuh-install-files.tar wazuh-install-files/wazuh-passwords.txt
```

---

# Wazuh Agent (Ubuntu WSL)

## Agent Service

```bash
sudo systemctl start wazuh-agent
sudo systemctl stop wazuh-agent
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

## Configuration

```bash
sudo nano /var/ossec/etc/ossec.conf
```

## Logs

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

# Wazuh Indexer Direct Query (Kali VM)

## Check Indices

```bash
curl -sk -u admin:"YOUR_INDEXER_PASSWORD" \
"https://localhost:9200/_cat/indices?v" | grep wazuh
```

## Search Alerts

```bash
curl -sk -u admin:"YOUR_INDEXER_PASSWORD" \
"https://localhost:9200/wazuh-alerts-*/_search?pretty&size=5"
```

---

# Custom Wazuh MCP Server (Kali VM)

## Navigate to Project

```bash
cd ~/wazuh-mcp
```

## Activate Virtual Environment

```bash
source venv/bin/activate
```

## Start Server (Foreground)

```bash
python3 server.py
```

## Start Server (Background)

```bash
nohup python3 server.py > ~/wazuh-mcp.log 2>&1 &
```

## Stop Server

```bash
pkill -f "python3 server.py"
```

## Check if Running

```bash
ss -tlnp | grep 9090
```

## Edit Server Code

```bash
nano ~/wazuh-mcp/server.py
```

## Test Endpoints

```bash
curl http://127.0.0.1:9090/health
curl http://127.0.0.1:9090/alerts
curl http://127.0.0.1:9090/summary
curl http://127.0.0.1:9090/agents
```

---

# Catalyst (Kali VM)

## Navigate to Installation

```bash
cd ~/Downloads
```

## Start (Foreground)

```bash
./catalyst serve --http :8090
```

## Start (Background)

```bash
nohup ./catalyst serve --http :8090 > ~/catalyst.log 2>&1 &
```

## Stop

```bash
pkill -f "catalyst serve"
```

## Check if Running

```bash
ss -tlnp | grep 8090
```

## Admin User Management

```bash
./catalyst admin create admin@catalyst.local Admin1234!
./catalyst admin set-password admin@catalyst.local NewPassword!
./catalyst admin delete admin@catalyst.local
```

## Test API

```bash
curl http://127.0.0.1:8090/api/tickets \
-H "Authorization: Bearer YOUR_TOKEN"
```

## Logs

```bash
tail -f ~/catalyst.log
```

---

# Network / Connectivity Checks

## Get IP Address

```bash
hostname -I
```

## Test Connectivity

```bash
# From WSL to Kali
ping 192.168.159.134

curl http://192.168.159.134:9090/health
curl http://192.168.159.134:8090
```

## Check Open Ports

```bash
ss -tlnp | grep -E "9090|8090|55000|9200|22"
```

## Firewall (Kali)

```bash
sudo ufw allow 9090
sudo ufw allow 8090
sudo ufw status
```

---

# SSH (Optional)

## Start SSH Server

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
sudo systemctl status ssh
```

## Passwordless SSH Setup

```bash
ssh-keygen -t rsa -b 4096
ssh-copy-id kali@192.168.159.134
ssh kali@192.168.159.134
```

---

# Quick Health Check (After Every Reboot)

## On Kali VM

```bash
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard

ss -tlnp | grep -E "9090|8090|55000|9200"

cd ~/wazuh-mcp
source venv/bin/activate
nohup python3 server.py > ~/wazuh-mcp.log 2>&1 &

cd ~/Downloads
nohup ./catalyst serve --http :8090 > ~/catalyst.log 2>&1 &
```

## On Ubuntu WSL

```bash
sudo systemctl status wazuh-agent

openclaw gateway status

curl http://192.168.159.134:9090/health
curl http://192.168.159.134:8090
```
