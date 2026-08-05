#!/usr/bin/env python3
# run.py - Main dengan sistem kode akses

import sys
import time
from colorama import Fore, Style
from utils import get_device_id, get_date, get_device_name, clear_screen, print_status
from banner import BANNER
from database import (
    check_license, 
    use_quota, 
    get_user, 
    activate_with_code,
    get_user_stats,
    get_user_level,
    ACCESS_CODES,
)
from spammer import OTPSpammer
from config import TRIAL_QUOTA, WHATSAPP_ADMIN, TELEGRAM_USERNAME, VERSION

def show_activation_menu(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}AKTIVASI KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Masukkan kode akses yang Anda dapatkan:{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Level Akses:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• Owner  : XAZMODESAD{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}• Admin  : BLINGBLING{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• Premium: FCLOSE{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Device ID Anda: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print()
    
    code = input(f"{Fore.WHITE}Kode Akses: {Style.RESET_ALL}").strip().upper()
    
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
    print(f"{Fore.CYAN}📊 STATISTIK PENGGUNA{Style.RESET_ALL}")
    print(f"  {Fore.RED}👑 Owner   : {stats['owner']}{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}🛡️ Admin   : {stats['admin']}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}⭐ Premium : {stats['premium']}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}📌 Trial   : {stats['trial']}{Style.RESET_ALL}")
    print()

def show_buy_guide(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}PANDUAN MENDAPATKAN KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Level Akses:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• Owner  : XAZMODESAD{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}• Admin  : BLINGBLING{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• Premium: FCLOSE{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Cara Mendapatkan Kode:{Style.RESET_ALL}")
    print(f"  1. Chat admin via WhatsApp atau Telegram")
    print(f"  2. Kirim Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print(f"  3. Dapatkan kode akses dari admin")
    print(f"  4. Masukkan kode di menu aktivasi")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}{WHATSAPP_ADMIN}{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}{TELEGRAM_USERNAME}{Style.RESET_ALL}")
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
        level = get_user_level(device_id)
        
        print(f"  Level: {show_level_badge(status)}")
        
        if status == "trial":
            print(f"  Sisa Kuota: {quota}/{TRIAL_QUOTA}")
        elif status in ["owner", "admin", "premium"]:
            print(f"  {Fore.GREEN}♾️ Unlimited Access{Style.RESET_ALL}")
        
        print()
        
        # Menu utama
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Jalankan Spam")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Aktivasi Kode Akses")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Lihat Statistik")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Panduan / Beli")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Keluar")
        
        choice = input(f"\n{Fore.WHITE}Pilih: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Cek apakah bisa spam
            if status == "trial_expired":
                print_status("error", "Kuota habis! Aktivasi kode atau beli premium.")
                time.sleep(2)
                continue
            
            if status == "trial" and quota <= 0:
                print_status("error", "Kuota habis! Aktivasi kode atau beli premium.")
                time.sleep(2)
                continue
            
            phone = input(f"{Fore.WHITE}📞 Nomor (62xxx): {Style.RESET_ALL}").strip()
            if not phone:
                print_status("error", "Nomor tidak boleh kosong!")
                continue
            
            # Batasan thread berdasarkan level
            if status == "trial":
                max_threads = 3
                default_threads = 2
            elif status in ["premium", "admin"]:
                max_threads = 10
                default_threads = 5
            elif status == "owner":
                max_threads = 20
                default_threads = 10
            else:
                max_threads = 3
                default_threads = 2
            
            threads = input(f"{Fore.WHITE}⚡ Thread (1-{max_threads}, default {default_threads}): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads.isdigit() else default_threads
            threads = max(1, min(threads, max_threads))
            
            # Batasan rounds berdasarkan level
            if status == "trial":
                max_rounds = 5
                default_rounds = 3
            else:
                max_rounds = 999
                default_rounds = 10
            
            rounds = input(f"{Fore.WHITE}🔄 Rounds (default {default_rounds}): {Style.RESET_ALL}").strip()
            rounds = int(rounds) if rounds.isdigit() else default_rounds
            rounds = max(1, min(rounds, max_rounds))
            
            # Kurangi kuota untuk trial
            if status == "trial":
                if not use_quota(device_id):
                    print_status("error", "Gagal mengurangi kuota!")
                    continue
            
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
