import os
import sys
import time
import subprocess
import requests

# Warna
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
P = "\033[95m"
C = "\033[96m"
W = "\033[97m"
E = "\033[0m"

def clear():
    os.system("clear")

def banner():
    print(f"{G}")
    print(" ██╗   ██╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗")
    print(" ╚██╗ ██╔╝██╔═══██╗╚██╗██╔╝██╔════╝╚██╗██╔╝")
    print("  ╚████╔╝ ██║   ██║ ╚███╔╝ █████╗   ╚███╔╝ ")
    print("   ╚██╔╝  ██║   ██║ ██╔██╗ ██╔══╝   ██╔██╗ ")
    print("    ██║   ╚██████╔╝██╔╝ ██╗███████╗██╔╝ ██╗")
    print("    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝")
    print(f"        {Y}100+ TOOLS HACKING FOR TERMUX{E}")
    print(f"        {C}By:RifttGG | GangenG-Bgt{E}\n")

def check_user():
    if not os.path.exists("w.txt"):
        print(f"{R}[!] File w.txt tidak ditemukan!{E}")
        print(f"{Y}Buat file w.txt berisi username Termux-mu (hasil 'whoami'){E}")
        sys.exit(1)

    with open("w.txt", "r") as f:
        allowed_users = [line.strip() for line in f if line.strip()]

    current_user = os.popen("whoami").read().strip()

    if current_user not in allowed_users:
        print(f"{R}[✗] Akses ditolak!{E}")
        print(f"{Y}User saat ini: {current_user}{E}")
        print(f"{Y}User yang diizinkan ada di w.txt{E}")
        sys.exit(1)

def install_deps():
    if os.path.exists(".installed"):
        return

    print(f"{Y}[~] Menginstal dependensi...{E}")
    os.system("pkg update -y && pkg upgrade -y")
    os.system("pkg install git python curl wget tar proot -y")
    os.system("pip install requests colorama")
    print(f"{G}[✓] Dependensi terinstal!{E}")
    with open(".installed", "w") as f:
        f.write("done")

def clone_tool(name, url, path):
    if os.path.exists(path):
        print(f"{G}   [✓] {name} sudah terinstal{E}")
    else:
        print(f"{Y}   [~] Mengunduh {name}...{E}")
        os.system(f"git clone {url} {path} 2>/dev/null")

def menu():
    clear()
    banner()
    print(f"{C}Pilih kategori:{E}")
    print(f"{G}[1]{W} Recon & OSINT")
    print(f"{G}[2]{W} Web Hacking")
    print(f"{G}[3]{W} Password Attacks")
    print(f"{G}[4]{W} Wireless & Network")
    print(f"{G}[5]{W} Exploitation")
    print(f"{G}[6]{W} Post-Exploitation")
    print(f"{G}[7]{W} Forensik & DFIR")
    print(f"{G}[8]{W} Lainnya")
    print(f"{R}[0]{W} Keluar\n")
    
    choice = input(f"{P}┌──({G}yok㉿termux{P})-[{Y}~/menu{P}]\n└─{C}$ {E}")
    return choice

def install_category(category):
    tools = {
        "1": [
            ("Sherlock", "https://github.com/sherlock-project/sherlock", "sherlock"),
            ("theHarvester", "https://github.com/laramies/theHarvester", "theHarvester"),
            ("PhoneInfoga", "https://github.com/sundowndev/PhoneInfoga", "PhoneInfoga"),
            ("OSIF", "https://github.com/ciku370/OSIF", "OSIF"),
            ("userrecon", "https://github.com/thelinuxchoice/userrecon", "userrecon"),
        ],
        "2": [
            ("sqlmap", "https://github.com/sqlmapproject/sqlmap", "sqlmap"),
            ("XSStrike", "https://github.com/s0md3v/XSStrike", "XSStrike"),
            ("WPScan", "https://github.com/wpscanteam/wpscan", "wpscan"),
            ("Nuclei", "https://github.com/projectdiscovery/nuclei", "nuclei"),
            ("ffuf", "https://github.com/ffuf/ffuf", "ffuf"),
        ],
        "3": [
            ("JohnTheRipper", "https://github.com/openwall/john", "john"),
            ("Hashcat", "https://github.com/hashcat/hashcat", "hashcat"),
            ("Hydra", "https://github.com/vanhauser-thc/thc-hydra", "hydra"),
            ("Cupp", "https://github.com/Mebus/cupp", "cupp"),
        ],
        "4": [
            ("Nmap", "https://github.com/nmap/nmap", "nmap"),
            ("Wireshark (CLI)", "https://github.com/wireshark/wireshark", "wireshark"),
            ("Bettercap", "https://github.com/bettercap/bettercap", "bettercap"),
        ],
        "5": [
            ("Metasploit", "https://github.com/rapid7/metasploit-framework", "metasploit-framework"),
            ("SearchSploit", "https://github.com/offensive-security/exploitdb", "exploitdb"),
            ("RouterSploit", "https://github.com/threat9/routersploit", "routersploit"),
        ],
        "6": [
            ("LinPEAS", "https://github.com/carlospolop/PEASS-ng", "peass-ng"),
            ("WinPEAS", "https://github.com/carlospolop/PEASS-ng", "peass-ng"),
            ("Chisel", "https://github.com/jpillora/chisel", "chisel"),
        ],
        "7": [
            ("Volatility3", "https://github.com/volatilityfoundation/volatility3", "volatility3"),
            ("Binwalk", "https://github.com/ReFirmLabs/binwalk", "binwalk"),
        ],
        "8": [
            ("LazyScript", "https://github.com/arismelachroinos/lscript", "lscript"),
            ("Tool-X", "https://github.com/rajkumardusad/Tool-X", "Tool-X"),
            ("Kali Nethunter", "https://github.com/Hax4us/Nethunter-In-Termux", "Nethunter-In-Termux"),
        ]
    }

    if category not in tools:
        print(f"{R}[!] Kategori tidak valid{E}")
        time.sleep(1)
        return

    clear()
    banner()
    print(f"{Y}Menginstal tools kategori {category}...{E}\n")
    
    for name, url, path in tools[category]:
        clone_tool(name, url, path)
    
    print(f"\n{G}[✓] Semua tools kategori {category} siap!{E}")
    input(f"\n{C}Tekan Enter untuk kembali ke menu...{E}")

def main():
    check_user()
    install_deps()

    while True:
        choice = menu()
        if choice == "1":
            install_category("1")
        elif choice == "2":
            install_category("2")
        elif choice == "3":
            install_category("3")
        elif choice == "4":
            install_category("4")
        elif choice == "5":
            install_category("5")
        elif choice == "6":
            install_category("6")
        elif choice == "7":
            install_category("7")
        elif choice == "8":
            install_category("8")
        elif choice == "0":
            print(f"{Y}[!] Keluar...{E}")
            sys.exit(0)
        else:
            print(f"{R}[!] Pilihan tidak valid{E}")
            time.sleep(1)

# Entry point
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gas":
        main()
    else:
        print(f"{Y}Jalankan dengan: {G}python yok.py gas{E}")
        print(f"{Y}atau: {G}gas{E} (jika sudah buat alias)")
