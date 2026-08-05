
#!/usr/bin/env python3
# ZAXOTP - OTP Spammer Premium (REAL)
# Developer: zaax
# Version: 3.0

import sys
import os
import time
import json
import platform
import hashlib
import uuid
import random
import threading
import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

VERSION = "3.0"
TOOLS_NAME = "ZAXOTP"
DEVELOPER = "zaax"

# ==================== BANNER ASCII ====================
BANNER = """
..                                                 
                                                .XX.                                                
                                                x&&x.                                               
                                               :&&&&;                                               
                        ...;.                 .&&&&&&..                .;...                        
                    ..+&&&&$          :.     .&&&&&&&&.     .:         .$&&&&+..                    
                  .;&&&&&&&;        ..&+.   .$&&&&&&&&$.    ;&..        :&&&&&&&;.                  
                .;&&&&&&&&$.        .&&&;  .+&&&&&&&&&&x.  :&&&.        .$&&&&&&&&+.                
               :&&&&&&&&&&X        .$&&&&: .....X&&&..... .&&&&$.        x&&&&&&&&&&:               
             .X&&&&&&&&&&&+       .+&&&&&&.     X&&&.    .$&&&&&x.       +&&&&&&&&&&&X.             
            .&&&&&&&&&&&&&+      .;&&&&&&&X.    X&&&.   .x&&&&&&&;.      +&&&&&&&&&&&&&.            
           .&&&&&&&&&&&&&&x.     :&&&&&&&&&x    X&&&.   +&&&&&&&&&:      x&&&&&&&&&&&&&&:           
          :&&&&&&&&&&&&&&&$.    .$&&&&&&&&&&:   X&&&.  :&&&&&&&&&&&.    .X&&&&&&&&&&&&&&&:          
         .&&&&&&&&&&&&&&&&&;    .....&&&x.....  X&&&.  ....;&&&:....    :&&&&&&&&&&&&&&&&&.         
        .$&&&&&&&&&&&&&&&&&&.       .&&&x.      X&&&.      ;&&&:       .&&&&&&&&&&&&&&&&&&$.        
       .x&&&&&&&&&&&&&&&&&&&&..     .&&&x.      X&&&.      ;&&&:     ..&&&&&&&&&&&&&&&&&&&&X.       
       :&&&&&&&&&&&&&&&&&&&&&&&:.   .&&&x.      X&&&.      ;&&&:   .:&&&&&&&&&&&&&&&&&&&&&&&;       
      .$&&&&&&&&&&&&&&&&&&&&&&&&&:  .&&&x.      X&&&.      ;&&&:  :&&&&&&&&&&&&&&&&&&&&&&&&&$.      
      ;&&&&&&&&&&&&&&&&&&&&&&&&&&:  .&&&x.      X&&&.      ;&&&:  :&&&&&&&&&&&&&&&&&&&&&&&&&&+      
      $&&&&&&&&&&&&&&&&&&&&&&&&&&:  .&&&x.      X&&&.      ;&&&:  :&&&&&&&&&&&&&&&&&&&&&&&&&&&.     
     .&&&&&&&&&&&&&&&&&&&&&&&&&&&:  .&&&x.  ..;+$&&&+:..   ;&&&:  :&&&&&&&&&&&&&&&&&&&&&&&&&&&.     
    .+&&&&&&&&&&&&&&&&&&&&&&&&&&&:  .&&&$$&&&&&&&&&&&&&&&&$X&&&:  :&&&&&&&&&&&&&&&&&&&&&&&&&&&+.    
    .$&&&&&&&&&&&&&&&&&&&;....;&&:  .&&&&&&&&$+:X&&&:+$&&&&&&&&:  :&&;....;&&&&&&&&&&&&&&&&&&&&.    
    .&&&&&&&&&&&&&&&&&&:.       ;:  .&&&X:..    X&&&.    .:X&&&:  .;        :&&&&&&&&&&&&&&&&&&.    
    .&&&&&&&&X+X&&&&&&..            .+..        X&&&.       ..:.             .&&&&&&X+X&&&&&&&&.    
    .&&&&&&.    .:&&&.                          X&&&.                         .&&&:     .&&&&&&.    
    .&&&&X.       .&x.                          X&&&.                          x&.       .X&&&&.    
    .$&&$.         :.                           X&&&.                          .:         .X&&&.    
    .+&&:           .                           X&&&.                          .           :&&+.    
     .&X.                                       X&&&.                                      .X&.     
     .$+                                        X&&&.  ...::;++xxx++;;:..                   ;$      
      .:                                        X&&&&&&&&&&&&&&&&&&&&&&&&&&X..              :.      
      ..                                        X&&&&&&&&$$Xx+;;;;;+xX$&&&&&&&&+.                   
           .                                    X&X;:...                ..:x&&&&&X.                 
          .&+.                                                              ..X&&&&;.               
         .X&&+.                                                                .X&&&x.              
        .+&&&&x.    ..:;+xxx+:....                                              .x&&&;              
        .&&&&&&&:x&&&&&&&&&&&&&&&&&X+...                                         .X&&&.             
       .X&&&&&&&&&&&&&X+:.::+X&&&&&&&&&&x...                                      +&&&.             
       :&&&&&&&&&&&x.           ...+X&&&&&&&+..                                   +&&&.             
      .X&&&&&&&&&&&&&&..             ..:$&&&&&&X.                                 X&&&.             
      .&&&&&&&&&&&&&&&&&&+:..             .+&&&&&&X:.                            x&&&;              
      x&&&&&&&&&&&&&&&&&&+...               ..:&&&&&&&+..                      .$&&&x.              
     .$&&&&&&&&&&&&&X:.                         .:X&&&&&&&+:...            ..:&&&&&;                
     .&&&&&&&&&&&;.                                ..;&&&&&&&&&$Xx;:...:+x$&&&&&&+.                 
     :&&&&&&&&;.                                       ..:X&&&&&&&&&&&&&&&&&&&X.                    
    .+&&&&&x.                                               ...:;+xXX$XXx;:..                       
    .X&&&:                                                                                          
     $&:.                                                                                           
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    

                                                                                                    
                                                                                                    


 ________  ________     ___    ___ ________  _________  ________   
|\_____  \|\   __  \   |\  \  /  /|\   __  \|\___   ___\\   __  \  
 \|___/  /\ \  \|\  \  \ \  \/  / | \  \|\  \|___ \  \_\ \  \|\  \ 
     /  / /\ \   __  \  \ \    / / \ \  \\\  \   \ \  \ \ \   ____\
    /  /_/__\ \  \ \  \  /     \/   \ \  \\\  \   \ \  \ \ \  \___|
   |\________\ \__\ \__\/  /\   \    \ \_______\   \ \__\ \ \__\   
    \|_______|\|__|\|__/__/ /\ __\    \|_______|    \|__|  \|__|   
                       |__/ \|__|
"""

# ==================== UTILITY ====================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_device_id():
    try:
        if os.name == 'posix':
            import subprocess
            result = subprocess.check_output(['getprop', 'ro.serialno'], text=True).strip()
            if result:
                return result
        return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]
    except:
        return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]

def get_device_name():
    try:
        return platform.node()
    except:
        return "Unknown Device"

def get_formatted_datetime():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{days[now.weekday()]}, {now.day} {months[now.month-1]} {now.year}"

def log_info(msg):
    print(f"{Fore.CYAN}[INFO] {msg}{Style.RESET_ALL}")

def log_success(msg):
    print(f"{Fore.GREEN}[✓] {msg}{Style.RESET_ALL}")

def log_warning(msg):
    print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")

def log_error(msg):
    print(f"{Fore.RED}[✗] {msg}{Style.RESET_ALL}")

def log_input(msg):
    return input(f"{Fore.YELLOW}[>] {msg}{Style.RESET_ALL}")

def log_header():
    clear_screen()
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║  {Fore.WHITE}{TOOLS_NAME} v{VERSION} — OTP Spammer Premium{Fore.CYAN}              ║")
    print(f"{Fore.CYAN}║  {Fore.WHITE}Developer: {Fore.GREEN}{DEVELOPER}{Fore.CYAN}                                  ║")
    print(f"{Fore.CYAN}║  {Fore.WHITE}Device: {Fore.YELLOW}{get_device_name()}{Fore.CYAN}                              ║")
    print(f"{Fore.CYAN}║  {Fore.WHITE}Date: {Fore.YELLOW}{get_formatted_datetime()}{Fore.CYAN}                        ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝")
    print()

# ==================== MAIN ====================
if __name__ == "__main__":
    from core import LicenseSystem
    from engine import SpamEngine

    license = LicenseSystem()
    
    # Cek maintenance
    if license.is_maintenance():
        clear_screen()
        log_header()
        log_warning(license.get_maintenance_message())
        input("Tekan Enter untuk keluar...")
        sys.exit(0)
    
    status, quota, device_id = license.check_license()
    
    if status == "trial":
        while True:
            clear_screen()
            log_header()
            premium, trial = license.get_user_stats()
            print(f"{Fore.CYAN}Total Pengguna  : {Fore.WHITE}{premium + trial}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}├─ Premium      : {Fore.GREEN}{premium}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}└─ Trial        : {Fore.YELLOW}{trial}{Style.RESET_ALL}")
            print()
            print(f"{Fore.YELLOW}Mode Trial - Sisa Kuota: {quota}/{license.get_trial_quota()}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hanya bisa menggunakan Single Round.{Style.RESET_ALL}")
            print()
            print(f"{Fore.CYAN}Menu Trial{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Jalankan Single Round")
            print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Beli Lisensi Premium")
            print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Keluar")
            print()
            
            choice = log_input("Pilih menu (1/2/3): ").strip()
            
            if choice == "1":
                if quota <= 0:
                    log_warning("Kuota trial habis!")
                    log_info("Silakan beli lisensi premium untuk melanjutkan.")
                    input("Tekan Enter untuk melihat panduan pembelian...")
                    from core import show_buy_guide
                    show_buy_guide(license)
                    _, quota, _ = license.check_license()
                    continue
                engine = SpamEngine()
                engine.run_single_round(threads=1)
                if license.use_quota():
                    _, quota, _ = license.check_license()
                    log_info(f"Sisa kuota sekarang: {quota}/{license.get_trial_quota()}")
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "2":
                from core import show_buy_guide
                show_buy_guide(license)
                _, quota, _ = license.check_license()
            
            elif choice == "3":
                log_info("Keluar...")
                sys.exit(0)
            
            else:
                log_warning("Pilihan tidak valid")
                input()
    
    elif status == "premium":
        while True:
            clear_screen()
            log_header()
            premium, trial = license.get_user_stats()
            print(f"{Fore.CYAN}Total Pengguna  : {Fore.WHITE}{premium + trial}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}├─ Premium      : {Fore.GREEN}{premium}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}└─ Trial        : {Fore.YELLOW}{trial}{Style.RESET_ALL}")
            print()
            print(f"{Fore.GREEN}Premium Active - Full Access{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Terima kasih sudah membeli lisensi premium!{Style.RESET_ALL}")
            print()
            print(f"{Fore.CYAN}Menu Premium{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Single Round")
            print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Infinite Loop")
            print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Keluar")
            print()
            
            choice = log_input("Pilih menu (1/2/3): ").strip()
            
            if choice == "1":
                threads = int(log_input("Jumlah thread (1-10, default 5): ") or "5")
                threads = max(1, min(10, threads))
                engine = SpamEngine()
                engine.run_single_round(threads=threads)
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "2":
                engine = SpamEngine()
                engine.run_infinite_loop()
                log_info("Tekan Enter untuk kembali ke menu...")
                input()
            
            elif choice == "3":
                log_info("Keluar...")
                sys.exit(0)
            
            else:
                log_warning("Pilihan tidak valid")
                input()
