# WAZON - BMS Infiltration & Security Auditing Framework
<img width="896" height="650" alt="gui" src="https://github.com/user-attachments/assets/396fdd5b-25f0-4cc4-b4df-7990b63b2bdf" />
<img width="683" height="309" alt="cli" src="https://github.com/user-attachments/assets/eb9b064f-f199-4c21-af5d-8a5d98d4e1b2" />

<p align="center">
  <b>Mission-Critical Offensive Security Framework for Building Management Systems (BMS / GTB)</b>
</p>

---

## 🛠️ Overview

**Wazon** is a modular, dual-interface (CLI & GUI) framework designed for cybersecurity professionals, penetration testers, and security researchers auditing Smart Buildings, data centers, hospitals, and industrial facilities. It bridges the gap between traditional IT network reconnaissance and specialized OT (Operational Technology) protocols such as **Modbus TCP** and **BACnet**.

---

## 📂 Project Architecture

```text
wazon/
├── core/
│   ├── __init__.py
│   ├── engine.py          # Base module abstraction class
│   ├── worker.py          # Asynchronous mission runner & database binder
│   ├── config.py          # Global configurations & stealth options
│   ├── database.py        # SQLite storage engine for mission results
│   └── reporter.py        # HTML audit report generation engine
├── modules/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── modbus_scanner.py  # Real Modbus TCP holding register reader
│   │   ├── bacnet_enum.py     # BACnet UDP Who-Is discovery network mapper
│   │   └── bacnet_writer.py   # Advanced BACnet WriteProperty attack module
│   ├── brand_tridium/
│   │   ├── __init__.py
│   │   └── rce_niagara.py     # Tridium Niagara web interface fingerprinting
│   ├── brand_schneider/
│   │   ├── __init__.py
│   │   └── overflow_tac.py    # Schneider TAC proprietary port probe
│   ├── brand_johnson/
│   │   ├── __init__.py
│   │   └── upload_metasys.py  # Johnson Controls Metasys endpoint enum
│   └── brand_honeywell/
│       ├── __init__.py
│       └── default_creds.py   # Factory default credential bruteforce checker
├── ui/
│   ├── __init__.py
│   ├── cli.py             # Rich-powered interactive terminal interface
│   └── gui.py             # PySide6 multi-threaded graphical control panel
├── main.py                # Central entry point
└── requirements.txt       # Project dependencies


# Wazon: Industrial Automation Security Tool

Wazon is a specialized tool for conducting authorized security audits on industrial control systems (ICS) and building management networks.

## ⚡ Core Features

*   **Dual Interface Control:**
    *   **CLI Mode:** Fast, streamlined workflow powered by `rich` and ASCII art.
    *   **GUI Mode:** Non-blocking, multi-threaded asynchronous interface built with PySide6.
*   **Real OT Protocol Handling:** Native implementation of raw sockets and protocol libraries for industrial automation networks (Modbus function codes, BACnet BVLC/NPDU/APDU framing).
*   **Automated Session Logging:** Every mission and target execution is automatically persisted into an internal SQLite vault (`wazon_vault.db`).
*   **Reporting Engine:** Compiles audit results into clean, executive-ready HTML reports.

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/wazon.git
    cd wazon
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage Guide

Wazon provides two main ways to run missions depending on your environment.

### 1. Running the Interactive CLI Mode
To launch the terminal interface with rich tables and menus:
```bash
python main.py
# (Alternatively: python main.py --cli)
```

### 2. Running the Graphical Dashboard (GUI)
To launch the PyQt/PySide6 control panel workspace:
```bash
python main.py --gui
```

## 🛡️ Modules Reference

| Module ID / Name | Category | Description |
| :--- | :--- | :--- |
| Modbus TCP Holding Registers | Recon | Connects to port 502 to extract live holding registers from controllers. |
| BACnet UDP Who-Is Mapper | Recon | Broadcasts real Who-Is packets on UDP 47808 to discover active building hardware. |
| BACnet WriteProperty Exploit | Exploit | Tests unauthenticated property modification on remote automation nodes. |
| Tridium Niagara Fingerprint | Recon | Probes web servers and checks headers/HTML responses for Niagara framework footprints. |
| Schneider TAC Port Probe | Recon | Sends raw TCP diagnostic packets to proprietary controller ports. |
| Johnson Controls Metasys Enum | Recon/Exploit | Checks login endpoints and assesses exposure level of Metasys installations. |
| Honeywell Default Creds Checker| Exploit | Tests standard factory default administrative pairs against exposed gateways. |

## ⚠️ Disclaimer

This tool is developed strictly for educational purposes, authorized security audits, and penetration testing engagements. Unauthorized access to industrial control systems or building management networks is illegal. The author assumes no liability for misuse or damage caused by this software.
