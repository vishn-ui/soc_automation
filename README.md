# soc_automationtin
![work flow](image.png)

## Move to point 14 to view MCP server details

- **Automated SOC Pipeline:** Built using Wazuh to detect real-time threats and trigger workflows automatically.
- **Workflow Automation 1:** n8n processes alerts and forwards them to Catalyst via REST API.
- **Workflow Automation 2:** openclaw processes alerts, summarizes, and forwards them to Catalyst.
- **Incident Management:** Automatically creates and manages tickets for detected attacks.

## -----------Move to point 14 to view MCP server details--------------

##  Tech Stack

- **Kali Linux (VMware Workstation)** — Wazuh Manager + Catalyst
- **Windows 11 Host** — Wazuh Agent + n8n (Docker)
- **Python 3** — Integration script
- **Bun + Vue.js** — Frontend
- **Go** — Backend

## Workflow

1. Wazuh detects a security event on the Windows agent  
2. Custom Python script sends alert data (JSON)  
3. n8n receives data via webhook  
4. n8n transforms and sends data to Catalyst API  
5. Catalyst creates an incident ticket  
6. Analyst reviews and manages the alert
7. In place of 3 and 4, we created automation via OpenClaw, which reads and analyzes the logs and summarizes via MCP server and REST API 
## Screenshots

### 1. Wazuh Manager Running
![Wazuh Manager](wazuh_manager_running.png)

### 2. Wazuh Agent status
![Wazuh agent](wazhu_agent_status.png)

### 3. Catalyst Running
![Catalyst Server](catalyst_backend_server.png)
![Catalyst Server](catalyst_ui.png)

### 4. Custom Integration Script
![Integration Script](ossec_integration.png)
![Integration Script](custom_catalyst.png)

### 5. n8n Running in Docker Desktop
![Docker n8n](n8n_docker_server.png)

### 6. Nmap Attack Simulation
![Nmap Attack](nmap_attack.png)
![Nmap Attack](nmap_attacks_json.png)

### 7. n8n Workflow 
![n8n Executions](n8n_workflow.png)


### 8. Catalyst — Auto-Created Alert Tickets
![Catalyst Alerts](catalyst_alerts.png)

### 9. Exporting Alerts to Excel
![Excel Export](json_log_to_excel.png)
![python script](pythonscript_json_excel.png)

### 10. HTTP Server Serving Files
![HTTP Server](kali_to_win_server.png)
![Diectory listing](file_server.png)

### 11. Excel files
![log files](excel_file1.png)
![log files](excel_file2.png)


### 12. OpenClaw setup and running to replace n8n for automation
![log files](Screenshot-0.png)
![log files](Screenshot-0.1.png)

### 13. OpenClaw Dashboard
![log files](Screenshot-0.2.png)
![log files](Screenshot-0.3.png)
![log files](Screenshot-0.4.png)

### 14. MCP server
MCP server connects with Wazuh manager and indexer
- Refer to [wazuh-mcp-server.py](wazuh-mcp-server.py) for MCP server details.
![log files](openclaw_MCP_List.png)

### 15. Communicating with a Telegram bot
![log files](Screenshot-0.5.png)
![log files](Screenshot-0.6.png)


