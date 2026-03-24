# Enterprise-Grade SIEM Homelab with Wazuh, VirusTotal, and Telegram CTI

## Project Overview
This project is an enterprise-scale Security Information and Event Management (SIEM) implementation using Wazuh deployed on Docker. The primary goal is to build comprehensive Security Operations Center (SOC) capabilities, ranging from endpoint monitoring and custom detection rules to Threat Intelligence integration and real-time alerting systems.

## Tools and Technologies Used
* **SIEM Engine:** Wazuh (Manager and Indexer) via Docker Single-Node.
* **Endpoints Monitored:** Windows 11 (Native Agent) and Kali Linux (WSL).
* **Threat Intelligence:** VirusTotal API.
* **Automation and Alerting:** Python 3, Telegram Bot API.
* **Visualization:** OpenSearch Dashboards.

## Key Features and Implementation Steps

### 1. Endpoint Detection and Response (EDR) Deployment
* Configured Wazuh Manager within a Docker container.
* Installed the Wazuh Agent on a Windows 11 environment to monitor Event Logs and File Integrity.

### 2. Custom Threat Detection (Active Monitoring)
* **Account Manipulation Detection:** Monitored the creation of backdoor accounts on Windows (`net user /add`), successfully triggering an instant Level 8 alert.
* **Linux Privilege Escalation:** Configured custom rules to detect the execution of Network Scanning Tools (Nmap) and unauthorized access to credential files (`/etc/shadow`).

### 3. Real-Time Alerting System (DzaskyBot)
* Developed a custom Python script that continuously reads the `alerts.json` log output from the Wazuh Manager.
* Integrated the script with the Telegram API to send alert notifications based on Severity Level, enabling immediate incident response from a mobile device.

### 4. Threat Intelligence Integration (VirusTotal)
* Configured File Integrity Monitoring (FIM) on designated Windows directories.
* Integrated the Wazuh Manager with the VirusTotal API.
* **Result:** When simulated malware (EICAR test file) was introduced into the system, the agent automatically extracted the SHA-256 Hash, sent it to the Manager, and triggered a Level 12 (Critical) alert after validation by global Antivirus engines.

### 5. Custom SOC Dashboard Visualization
* Utilized OpenSearch Dashboards to design threat intelligence visualizations.
* Created a Pie Chart to identify the "Top 10 Attacks" and a Vertical Bar Chart (Time Series) to monitor attack spikes based on rule severity levels.

## Technical Challenges Overcome
* **Docker Ephemeral Storage:** Resolved the automatic configuration reset issue caused by Docker Wazuh's Volume Mount architecture. Bypassed the container restart cycle by applying permission injection (`chown`) and utilizing the internal `/var/ossec/bin/wazuh-control restart` command to ensure persistent API configurations.
* **WSL Auditd Limitations:** Identified the limitations of the Windows Subsystem for Linux (WSL2) kernel, which does not fully support the Linux Audit Framework, and successfully pivoted monitoring tactics to the native Windows endpoint.
