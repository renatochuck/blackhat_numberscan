#!/usr/bin/env python3
"""
▓█████▄ ▓█████  ██▓     ██▓ ███▄ ▄███▓ ▄▄▄       ███▄    █ 
▒██▀ ██▌▓█   ▀ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ 
░██   █▌▒███   ▒██░    ▒██▒▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒
░▓█▄   ▌▒▓█  ▄ ▒██░    ░██░▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒
░▒████▓ ░▒████▒░██████▒░██░▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░
 ▒▒▓  ▒ ░░ ▒░ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
 ░ ▒  ▒  ░ ░  ░░ ░ ▒  ░ ▒ ░░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░
 ░ ░  ░    ░     ░ ░    ▒ ░░      ░     ░   ▒      ░   ░ ░ 
   ░       ░  ░    ░  ░ ░         ░         ░  ░         ░ 
 ░                                                          
"""

import os
import sys
import time
import json
import random
import socket
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from pyfiglet import Figlet
    from rich import print
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress
    from rich.text import Text
    from colorama import init, Fore, Back, Style
except ImportError:
    print("Error: Required packages not found. Install with:")
    print("pip install pyfiglet rich colorama")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Constants
HISTORY_FILE = "scan_history.json"
CONFIG_FILE = "config.json"
TEMP_DATA_FILE = ".temp_scan_data"

# Cyberpunk color scheme
CYBER_RED = "#ff073a"
CYBER_GREEN = "#0afc06"
CYBER_BLUE = "#05f7ff"
CYBER_PURPLE = "#9467fd"
CYBER_YELLOW = "#f5e642"

# Initialize console
console = Console()

# Pre-defined profiles with enhanced cyber data
PREDEFINED_PROFILES = {
    "+14155552671": {
        "metadata": {
            "threat_level": "CRITICAL",
            "classification": "CLASSIFIED",
            "timestamp": datetime.now().isoformat(),
            "case_id": "NX-9-"+hashlib.sha256(b"johnwick").hexdigest()[:8].upper()
        },
        "identity": {
            "name": "John Wick",
            "aliases": ["The Boogeyman", "Baba Yaga"],
            "gender": "male",
            "nationality": "US/Russian",
            "dob": "1964-09-02",
            "face_id": "JW-"+hashlib.md5(b"continental").hexdigest()[:6]
        },
        "communications": {
            "phones": [
                {
                    "number": "+14155552671",
                    "type": "burner",
                    "carrier": "T-Mobile (Prepaid)",
                    "imei": "35-"+''.join(random.choices('0123456789', k=8))+"-1",
                    "sim_swaps": 3,
                    "last_swap": "2023-03-15"
                }
            ],
            "emails": [
                "john.wick@continental.com",
                "baba_yaga@onionmail.org"
            ],
            "messaging": [
                {"app": "Signal", "id": "JW_1964", "encrypted": True},
                {"app": "Telegram", "id": "@boogeyman", "last_seen": "2023-04-15"}
            ]
        },
        "digital_footprint": {
            "ips": ["192.168.1."+str(random.randint(100, 200))],
            "macs": [":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])],
            "vpn": True,
            "tor": True,
            "device_fingerprint": hashlib.sha256(b"johnwick_phone").hexdigest()
        },
        "network": {
            "known_associates": [
                {"name": "Winston", "relation": "Handler", "codename": "Charon"},
                {"name": "The Director", "relation": "High Table", "status": "Active"}
            ],
            "organization": "The Continental",
            "last_known_location": "New York"
        },
        "threat_indicators": {
            "weapons": ["Firearms", "Melee", "Tactical"],
            "skills": ["Close Combat", "Precision Shooting", "Infiltration"],
            "warning": "EXTREME RISK - DO NOT APPROACH"
        }
    },
    "+919538299331": {
        "metadata": {
            "threat_level": "HIGH",
            "classification": "RESTRICTED",
            "timestamp": datetime.now().isoformat(),
            "case_id": "IN-7-"+hashlib.sha256(b"ghostprotocol").hexdigest()[:8].upper()
        },
        "identity": {
            "name": "Rajesh Khan",
            "aliases": ["The Ghost", "RK"],
            "gender": "male",
            "nationality": "Indian",
            "dob": "1985-11-17",
            "face_id": "RK-"+hashlib.md5(b"mumbai").hexdigest()[:6]
        },
        "communications": {
            "phones": [
                {
                    "number": "+919538299331",
                    "type": "burner",
                    "carrier": "Jio (Disposable)",
                    "imei": "86-"+''.join(random.choices('0123456789', k=8))+"-9",
                    "sim_swaps": 2,
                    "last_swap": "2023-05-15"
                }
            ],
            "emails": [
                "ghost@secmail.pro",
                "rk_1985@protonmail.ch"
            ],
            "messaging": [
                {"app": "Wire", "id": "ghostprotocol", "encrypted": True},
                {"app": "Wickr", "id": "rk_secured", "last_seen": "2023-11-20"}
            ]
        },
        "digital_footprint": {
            "ips": ["176.45."+str(random.randint(100, 200))+"."+str(random.randint(1, 254))],
            "macs": [":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])],
            "vpn": True,
            "tor": False,
            "device_fingerprint": hashlib.sha256(b"ghost_phone").hexdigest()
        },
        "network": {
            "known_associates": [
                {"name": "[REDACTED]", "relation": "Handler", "codename": "Viper"},
                {"name": "[REDACTED]", "relation": "Tech", "status": "Active"}
            ],
            "organization": "Unknown",
            "last_known_location": "Mumbai"
        },
        "threat_indicators": {
            "weapons": ["Cyber", "Surveillance"],
            "skills": ["Infiltration", "Social Engineering", "Counter-Surveillance"],
            "warning": "HIGH RISK - TECH SAVVY"
        }
    }
}

def generate_cyber_banner():
    """Generate an intense cyberpunk banner"""
    f = Figlet(font='doom')
    banner = f.renderText('NUMBERSCAN PRO')
    
    console.print(f"[{CYBER_RED}]{banner}[/{CYBER_RED}]")
    
    tagline = Text("ADVANCED TARGET ACQUISITION SYSTEM", style=f"bold {CYBER_GREEN} blink")
    console.print(tagline, justify="center")
    
    warning = Text("UNAUTHORIZED ACCESS WILL BE PROSECUTED", style=f"bold {CYBER_RED}")
    console.print(warning, justify="center")
    print()

def show_scan_header(phone):
    """Display target acquisition header"""
    console.print(f"[{CYBER_RED}]┌─────────────────────────────────────────────────────────┐")
    console.print(f"[{CYBER_RED}]│[{CYBER_GREEN}] TARGET ACQUIRED: [{CYBER_BLUE}]{phone}[/{CYBER_BLUE}]                  [{CYBER_RED}]│")
    console.print(f"[{CYBER_RED}]│[{CYBER_PURPLE}] INITIATING DEEP SCAN PROTOCOL...                   [{CYBER_RED}]│")
    console.print(f"[{CYBER_RED}]│[{CYBER_PURPLE}] BYPASSING CARRIER FIREWALLS...                   [{CYBER_RED}]│")
    console.print(f"[{CYBER_RED}]│[{CYBER_PURPLE}] ACCESSING DARKNET DATABASES...                   [{CYBER_RED}]│")
    console.print(f"[{CYBER_RED}]└─────────────────────────────────────────────────────────┘")

def simulate_scan():
    """Show cyber scanning animation"""
    with Progress() as progress:
        tasks = [
            progress.add_task(f"[{CYBER_BLUE}]Carrier Trace...", total=100),
            progress.add_task(f"[{CYBER_PURPLE}]Dark Web Scan...", total=100),
            progress.add_task(f"[{CYBER_RED}]Threat Analysis...", total=100)
        ]
        
        while not all(task.completed for task in progress.tasks):
            for task in tasks:
                progress.update(task, advance=random.uniform(0.5, 5))
            time.sleep(0.03)

def display_threat_profile(profile):
    """Display the full threat profile"""
    # Metadata Panel
    meta_table = Table(show_header=False, box=None)
    meta_table.add_column("Key", style=CYBER_YELLOW)
    meta_table.add_column("Value", style=CYBER_BLUE)
    
    meta_table.add_row("THREAT LEVEL:", f"[bold {CYBER_RED}]{profile['metadata']['threat_level']}[/bold {CYBER_RED}]")
    meta_table.add_row("CASE ID:", profile['metadata']['case_id'])
    meta_table.add_row("TIMESTAMP:", profile['metadata']['timestamp'])
    
    console.print(Panel(meta_table, title=f"[{CYBER_GREEN}]THREAT PROFILE", border_style=CYBER_PURPLE))

    # Identity Section
    id_table = Table(show_header=True, header_style=f"bold {CYBER_GREEN}")
    id_table.add_column("Field", style=CYBER_YELLOW)
    id_table.add_column("Value", style=CYBER_BLUE)
    
    id_table.add_row("Full Name", profile['identity']['name'])
    id_table.add_row("Aliases", ", ".join(profile['identity']['aliases']))
    id_table.add_row("Nationality", profile['identity']['nationality'])
    id_table.add_row("Face ID", profile['identity']['face_id'])
    
    console.print(Panel(id_table, title=f"[{CYBER_GREEN}]IDENTITY", border_style=CYBER_PURPLE))

    # Communications Section
    comm_table = Table(show_header=True, header_style=f"bold {CYBER_GREEN}")
    comm_table.add_column("Type", style=CYBER_YELLOW)
    comm_table.add_column("Details", style=CYBER_BLUE)
    
    for phone in profile['communications']['phones']:
        comm_table.add_row("PHONE", 
            f"{phone['number']} ({phone['type']})\n"
            f"Carrier: {phone['carrier']}\n"
            f"IMEI: {phone['imei']}\n"
            f"SIM Swaps: {phone['sim_swaps']} (Last: {phone['last_swap']})"
        )
    
    for email in profile['communications']['emails']:
        comm_table.add_row("EMAIL", email)
    
    for msg in profile['communications']['messaging']:
        comm_table.add_row(msg['app'].upper(), 
            f"ID: {msg['id']}\n"
            f"{'ENCRYPTED: YES' if msg.get('encrypted') else ''}\n"
            f"{'Last Seen: '+msg['last_seen'] if msg.get('last_seen') else ''}"
        )
    
    console.print(Panel(comm_table, title=f"[{CYBER_GREEN}]COMMUNICATIONS", border_style=CYBER_PURPLE))

    # Digital Footprint
    digi_table = Table(show_header=True, header_style=f"bold {CYBER_GREEN}")
    digi_table.add_column("Field", style=CYBER_YELLOW)
    digi_table.add_column("Value", style=CYBER_BLUE)
    
    digi_table.add_row("IP Addresses", "\n".join(profile['digital_footprint']['ips']))
    digi_table.add_row("MAC Addresses", "\n".join(profile['digital_footprint']['macs']))
    digi_table.add_row("VPN Usage", "ACTIVE" if profile['digital_footprint']['vpn'] else "INACTIVE")
    digi_table.add_row("TOR Usage", "ACTIVE" if profile['digital_footprint']['tor'] else "INACTIVE")
    digi_table.add_row("Device Fingerprint", profile['digital_footprint']['device_fingerprint'])
    
    console.print(Panel(digi_table, title=f"[{CYBER_GREEN}]DIGITAL FOOTPRINT", border_style=CYBER_PURPLE))

    # Threat Warning
    warn_panel = Panel.fit(
        f"[bold {CYBER_RED}]{profile['threat_indicators']['warning']}[/bold {CYBER_RED}]\n\n"
        f"Skills: {', '.join(profile['threat_indicators']['skills'])}\n"
        f"Weapons: {', '.join(profile['threat_indicators']['weapons'])}",
        title=f"[{CYBER_RED}]THREAT ASSESSMENT",
        border_style=CYBER_RED
    )
    console.print(warn_panel)

def scan_number(number):
    """Execute full scan protocol"""
    show_scan_header(number)
    simulate_scan()
    
    if number in PREDEFINED_PROFILES:
        display_threat_profile(PREDEFINED_PROFILES[number])
    else:
        console.print(f"[{CYBER_RED}]TARGET NOT IN DATABASE - NO KNOWN THREAT PROFILE")

def main_menu():
    """Main interface"""
    while True:
        console.print(f"\n[{CYBER_PURPLE}]MAIN MENU[/{CYBER_PURPLE}]")
        console.print(f"[{CYBER_BLUE}][1][/{CYBER_BLUE}] Scan Phone Number")
        console.print(f"[{CYBER_BLUE}][2][/{CYBER_BLUE}] View Threat Database")
        console.print(f"[{CYBER_BLUE}][3][/{CYBER_BLUE}] Generate Random Profile")
        console.print(f"[{CYBER_BLUE}][4][/{CYBER_BLUE}] Export Data")
        console.print(f"[{CYBER_RED}][5][/{CYBER_RED}] Exit System")
        
        choice = input(f"\n[{CYBER_GREEN}]OPERATION> [/]")
        
        if choice == "1":
            num = input(f"[{CYBER_BLUE}]ENTER TARGET NUMBER (+XX...): [/]")
            scan_number(num)
        elif choice == "2":
            console.print(f"\n[{CYBER_PURPLE}]KNOWN THREATS:")
            for num in PREDEFINED_PROFILES:
                console.print(f"[{CYBER_BLUE}]{num}[/{CYBER_BLUE}] - {PREDEFINED_PROFILES[num]['identity']['name']}")
        elif choice == "3":
            fake_num = f"+{random.randint(1,99)}{random.randint(100000000,999999999)}"
            scan_number(fake_num)
        elif choice == "4":
            console.print(f"[{CYBER_GREEN}]DATA EXPORTED TO /var/log/numberscan/")
        elif choice == "5":
            console.print(f"[{CYBER_RED}]TERMINATING SYSTEM...")
            break
        else:
            console.print(f"[{CYBER_RED}]INVALID COMMAND")

if __name__ == "__main__":
    generate_cyber_banner()
    console.print(f"[{CYBER_RED}]WARNING: THIS TOOL IS FOR AUTHORIZED USE ONLY")
    console.print(f"[{CYBER_YELLOW}]By continuing you agree to the Cyber Security Act 2023\n")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n[{CYBER_RED}]SYSTEM SHUTDOWN INITIATED")
    except Exception as e:
        console.print(f"[{CYBER_RED}]CRITICAL FAILURE: {str(e)}")