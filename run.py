#!/usr/bin/env python3
# run.py - Main entry

import sys
import time
from colorama import Fore, Style
from utils import get_device_id, get_date, get_device_name, clear_screen, print_status
from banner import BANNER
from database import check_license, use_quota, activate_with_code, get_user_stats, get_user_level
from spammer import OTPSpammer
from config import TRIAL_QUOTA, WHATSAPP_ADMIN, TELEGRAM_USERNAME, VERSION

def show_activation_menu(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}AKTIVASI KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Masukkan kode akses:{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Level Akses:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• Owner  : XAZMODESAD{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}• Admin  : BLINGBLING{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• Premium: FCLOSE{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print()
    
    code = input(f"{Fore.WHITE}Kode: {Style.RESET_ALL}").strip().upper()
    
    if not code:
        print_status("warning", "Kode tidak boleh kosong!")
        time.sleep(1)
        return False
    
    success, message = activate_with_code(device_id, code)
    
    if success:
        print_status("success", message)
    else:
        print_status("error", message)
    
    time.sleep(2)
    return success

def show_stats():
    stats = get_user_stats()
    print(f"{Fore.CYAN}📊 STATISTIK{Style.RESET_ALL}")
    print(f"  {Fore.RED}👑 Owner   : {stats['owner']}{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}🛡️ Admin   : {stats['admin']}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}⭐ Premium : {stats['premium']}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}📌 Trial   : {stats['trial']}{Style.RESET_ALL}")
    print()

def show_buy_guide(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}PANDUAN KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Level Akses:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• Owner  : XAZMODESAD{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}• Admin  : BLINGBLING{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• Premium: FCLOSE{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Cara Mendapatkan:{Style.RESET_ALL}")
    print(f"  Chat admin: {WHATSAPP_ADMIN} / {TELEGRAM_USERNAME}")
    print(f"  Kirim Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali...")

def show_level_badge(level):
    badges = {
        "owner": f"{Fore.RED}👑 OWNER{Style.RESET_ALL}",
        "admin": f"{Fore.BLUE}🛡️ ADMIN{Style.RESET_ALL}",
        "premium": f"{Fore.GREEN}⭐ PREMIUM{Style.RESET_ALL}",
        "trial": f"{Fore.YELLOW}📌 TRIAL{Style.RESET_ALL}",
        "trial_expired": f"{Fore.RED}❌ EXPIRED{Style.RESET_ALL}",
    }
    return badges.get(level, f"{Fore.YELLOW}📌 TRIAL{Style.RESET_ALL}")

def main():
    device_id = get_device_id()
    
    while True:
        clear_screen()
        print(BANNER)
        print(f"{Fore.CYAN}{get_date()} | {Fore.WHITE}{get_device_name()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
        print()
        
        status, quota, _ = check_license(device_id)
        
        print(f"  Level: {show_level_badge(status)}")
        
        if status == "trial":
            print(f"  Sisa Kuota: {quota}/{TRIAL_QUOTA}")
        elif status in ["owner", "admin", "premium"]:
            print(f"  {Fore.GREEN}♾️ Unlimited{Style.RESET_ALL}")
        
        print()
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Spam OTP")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Aktivasi Kode")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Statistik")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Panduan")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Keluar")
        
        choice = input(f"\n{Fore.WHITE}Pilih: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            if status == "trial_expired" or (status == "trial" and quota <= 0):
                print_status("error", "Kuota habis! Aktivasi kode.")
                time.sleep(2)
                continue
            
            print(f"\n{Fore.CYAN}Contoh nomor: 628123456789{Style.RESET_ALL}")
            phone = input(f"{Fore.WHITE}📞 Nomor: {Style.RESET_ALL}").strip()
            if not phone:
                print_status("error", "Nomor kosong!")
                continue
            
            if status == "trial":
                max_threads = 3
                default_threads = 2
                max_rounds = 5
                default_rounds = 3
            elif status == "owner":
                max_threads = 20
                default_threads = 10
                max_rounds = 999
                default_rounds = 20
            else:
                max_threads = 10
                default_threads = 5
                max_rounds = 999
                default_rounds = 10
            
            threads = input(f"{Fore.WHITE}⚡ Thread (1-{max_threads}, default {default_threads}): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads.isdigit() else default_threads
            threads = max(1, min(threads, max_threads))
            
            rounds = input(f"{Fore.WHITE}🔄 Rounds (default {default_rounds}): {Style.RESET_ALL}").strip()
            rounds = int(rounds) if rounds.isdigit() else default_rounds
            rounds = max(1, min(rounds, max_rounds))
            
            if status == "trial":
                use_quota(device_id)
            
            spammer = OTPSpammer(threads=threads)
            spammer.spam(phone, rounds=rounds)
            
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "2":
            show_activation_menu(device_id)
        
        elif choice == "3":
            clear_screen()
            print(BANNER)
            show_stats()
            input("Tekan Enter untuk kembali...")
        
        elif choice == "4":
            show_buy_guide(device_id)
        
        elif choice == "5":
            print_status("info", "Keluar...")
            sys.exit(0)
        
        else:
            print_status("warning", "Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Keluar...")
        sys.exit(0)
