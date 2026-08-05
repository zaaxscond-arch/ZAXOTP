#!/usr/bin/env python3
# run.py - Main entry

import sys
import time
import os
import webbrowser
from colorama import Fore, Style
from utils import get_device_id, get_date, get_device_name, clear_screen, print_status
from banner import BANNER
from database import check_license, use_quota, activate_with_code, get_user_stats, get_user_level
from spammer import OTPSpammer
from config import TRIAL_QUOTA, WHATSAPP_CHANNEL, VERSION

def open_whatsapp_channel():
    """Buka WhatsApp Channel otomatis"""
    try:
        print_status("info", "Membuka WhatsApp Channel...")
        time.sleep(1)
        
        # Coba pake webbrowser
        webbrowser.open(WHATSAPP_CHANNEL)
        
        # Fallback buat Termux
        if os.name == 'posix':
            try:
                os.system(f"termux-open {WHATSAPP_CHANNEL}")
            except:
                pass
        
        print_status("success", f"Channel dibuka: {WHATSAPP_CHANNEL}")
        print_status("warning", "WAJIB FOLLOW channel untuk info update & kode akses!")
        print()
    except Exception as e:
        print_status("error", f"Gagal buka channel: {e}")
        print_status("info", f"Buka manual: {WHATSAPP_CHANNEL}")

def show_activation_menu(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}AKTIVASI KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}⚠️ SYARAT: Follow WhatsApp Channel dulu!{Style.RESET_ALL}")
    print()
    
    # Tanya udah follow belum
    follow = input(f"{Fore.WHITE}Udah follow channel? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if follow != 'y':
        print_status("warning", "Buka channel dulu ya!")
        open_whatsapp_channel()
        input("Tekan Enter setelah follow...")
        return
    
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
        print_status("info", "Pastikan follow channel & kode benar!")
    
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
    print(f"{Fore.CYAN}PANDUAN MENDAPATKAN KODE AKSES{Style.RESET_ALL}")
    print()
    print(f"{Fore.RED}⚠️ WAJIB FOLLOW CHANNEL DULU!{Style.RESET_ALL}")
    print()
    
    # Auto buka channel
    open_whatsapp_channel()
    print()
    
    print(f"{Fore.YELLOW}Level Akses:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• Owner  : XAZMODESAD{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}• Admin  : BLINGBLING{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• Premium: FCLOSE{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Cara Dapat Kode:{Style.RESET_ALL}")
    print(f"  1. Follow channel WhatsApp di atas")
    print(f"  2. Chat admin di channel/komentar")
    print(f"  3. Kirim Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print(f"  4. Dapatkan kode akses dari admin")
    print()
    print(f"{Fore.CYAN}Channel: {WHATSAPP_CHANNEL}{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Aktivasi Kode (WAJIB FOLLOW CHANNEL)")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Statistik")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Panduan & Channel")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Buka Channel WhatsApp")
        print(f"{Fore.GREEN}[6]{Style.RESET_ALL} Keluar")
        
        choice = input(f"\n{Fore.WHITE}Pilih: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            if status == "trial_expired" or (status == "trial" and quota <= 0):
                print_status("error", "Kuota habis! Aktivasi kode.")
                print_status("info", "Pastikan follow channel dulu!")
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
            open_whatsapp_channel()
            input("\nTekan Enter untuk kembali...")
        
        elif choice == "6":
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
