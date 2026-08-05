#!/usr/bin/env python3
# run.py - Main entry dengan lisensi

import sys
import time
from colorama import Fore, Style
from utils import get_device_id, get_date, get_device_name, clear_screen, print_status
from banner import BANNER
from database import check_license, use_quota, get_user, activate_premium
from spammer import OTPSpammer
from config import TRIAL_QUOTA, LICENSE_PRICE, WHATSAPP_ADMIN, TELEGRAM_USERNAME, VERSION

def show_buy_guide(device_id):
    clear_screen()
    print(BANNER)
    print(f"{Fore.CYAN}PANDUAN PEMBELIAN LISENSI PREMIUM{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Keuntungan Premium:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Akses FULL unlimited")
    print(f"  {Fore.GREEN}•{Style.RESET_ALL} Update tools terbaru")
    print()
    print(f"{Fore.CYAN}Harga: {Fore.GREEN}Rp. {LICENSE_PRICE:,}{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Cara Pembelian:{Style.RESET_ALL}")
    print(f"  1. Chat admin via WhatsApp atau Telegram")
    print(f"  2. Kirim Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
    print(f"  3. Lakukan pembayaran")
    print(f"  4. Tunggu aktivasi")
    print()
    print(f"{Fore.CYAN}Kontak Admin:{Style.RESET_ALL}")
    print(f"  WhatsApp : {Fore.GREEN}{WHATSAPP_ADMIN}{Style.RESET_ALL}")
    print(f"  Telegram : {Fore.WHITE}{TELEGRAM_USERNAME}{Style.RESET_ALL}")
    print()
    input("Tekan Enter untuk kembali...")

def main():
    device_id = get_device_id()
    
    while True:
        clear_screen()
        print(BANNER)
        print(f"{Fore.CYAN}{get_date()} | {Fore.WHITE}{get_device_name()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Device ID: {Fore.WHITE}{device_id}{Style.RESET_ALL}")
        print()
        
        status, quota, _ = check_license(device_id)
        
        if status == "trial":
            print(f"{Fore.YELLOW}📌 MODE TRIAL - Sisa: {quota}/{TRIAL_QUOTA}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📌 Premium: Rp. {LICENSE_PRICE:,} (unlimited){Style.RESET_ALL}")
            print()
            print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Jalankan Spam")
            print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Beli Premium")
            print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Keluar")
            
            choice = input(f"\n{Fore.WHITE}Pilih: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                if quota <= 0:
                    print_status("error", "Kuota habis! Beli premium.")
                    time.sleep(1)
                    continue
                
                phone = input(f"{Fore.WHITE}📞 Nomor (62xxx): {Style.RESET_ALL}").strip()
                threads = input(f"{Fore.WHITE}⚡ Thread (1-5, default 3): {Style.RESET_ALL}").strip()
                threads = int(threads) if threads.isdigit() else 3
                threads = max(1, min(threads, 5))
                
                rounds = input(f"{Fore.WHITE}🔄 Rounds (default 3): {Style.RESET_ALL}").strip()
                rounds = int(rounds) if rounds.isdigit() else 3
                
                # Kurangi kuota
                if not use_quota(device_id):
                    print_status("error", "Gagal mengurangi kuota!")
                    continue
                
                spammer = OTPSpammer(threads=threads)
                spammer.spam(phone, rounds=rounds)
                
                input("\nTekan Enter untuk kembali...")
            
            elif choice == "2":
                show_buy_guide(device_id)
            
            elif choice == "3":
                print_status("info", "Keluar...")
                sys.exit(0)
        
        elif status == "premium":
            print(f"{Fore.GREEN}⭐ MODE PREMIUM - UNLIMITED{Style.RESET_ALL}")
            print()
            print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Jalankan Spam")
            print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Keluar")
            
            choice = input(f"\n{Fore.WHITE}Pilih: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                phone = input(f"{Fore.WHITE}📞 Nomor (62xxx): {Style.RESET_ALL}").strip()
                threads = input(f"{Fore.WHITE}⚡ Thread (1-10, default 5): {Style.RESET_ALL}").strip()
                threads = int(threads) if threads.isdigit() else 5
                threads = max(1, min(threads, 10))
                
                rounds = input(f"{Fore.WHITE}🔄 Rounds (default 10): {Style.RESET_ALL}").strip()
                rounds = int(rounds) if rounds.isdigit() else 10
                
                spammer = OTPSpammer(threads=threads)
                spammer.spam(phone, rounds=rounds)
                
                input("\nTekan Enter untuk kembali...")
            
            elif choice == "2":
                print_status("info", "Keluar...")
                sys.exit(0)
        
        elif status == "trial_expired":
            print(f"{Fore.RED}❌ KUOTA HABIS!{Style.RESET_ALL}")
            print()
            input("Tekan Enter untuk melihat panduan pembelian...")
            show_buy_guide(device_id)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Keluar...")
        sys.exit(0)
