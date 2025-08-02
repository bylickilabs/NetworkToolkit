
import socket
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

class NetworkToolkitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Toolkit")
        self.geometry("800x600")
        self.configure_gui()

    def configure_gui(self):
        container = ttk.Frame(self, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        self.input_field = ttk.Entry(container, width=60)
        self.input_field.pack(pady=5)
        self.input_field.insert(0, "google.com")

        button_frame = ttk.Frame(container)
        button_frame.pack(pady=10)

        buttons = [
            ("Local IP", self.get_local_ip),
            ("Hostname", self.get_hostname),
            ("Ping", self.ping_host),
            ("Reverse DNS", self.reverse_dns),
            ("Port Scan", self.port_scan),
            ("Check Internet", self.check_internet),
            ("External IP", self.get_external_ip)
        ]

        for idx, (label, cmd) in enumerate(buttons):
            ttk.Button(button_frame, text=label, command=cmd).grid(row=0, column=idx, padx=5)

        self.output = scrolledtext.ScrolledText(container, wrap=tk.WORD, font=("Courier", 10))
        self.output.pack(fill=tk.BOTH, expand=True, pady=10)

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def get_local_ip(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            self.log(f"Local IP Address: {ip}")
        except Exception as e:
            self.log(f"[Error] Could not retrieve local IP: {e}")

    def get_hostname(self):
        try:
            hostname = socket.gethostname()
            self.log(f"Hostname: {hostname}")
        except Exception as e:
            self.log(f"[Error] Could not retrieve hostname: {e}")

    def ping_host(self):
        target = self.input_field.get()
        def run_ping():
            try:
                self.log(f"Starting ping to {target}...")
                output = subprocess.check_output(
                    ["ping", "-n", "4", target],
                    stderr=subprocess.STDOUT,
                    encoding="cp850",
                    errors="replace"
                )
                self.log(output)
            except Exception as e:
                self.log(f"[Error] Ping failed: {e}")
        threading.Thread(target=run_ping).start()

    def reverse_dns(self):
        target = self.input_field.get()
        try:
            ip = socket.gethostbyname(target)
            hostname = socket.gethostbyaddr(ip)[0]
            self.log(f"Reverse DNS for {ip}: {hostname}")
        except Exception as e:
            self.log(f"[Error] Reverse DNS lookup failed: {e}")

    def port_scan(self):
        target = self.input_field.get()
        common_ports = [21, 22, 23, 25, 53, 80, 110, 123, 135, 139, 143, 443, 445, 587, 993, 995, 1433, 3306, 3389, 8080]
        def run_scan():
            self.log(f"Scanning top ports on {target}...")
            for port in common_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(0.5)
                        result = sock.connect_ex((target, port))
                        if result == 0:
                            self.log(f"[Open] Port {port}")
                except Exception as e:
                    self.log(f"[Error] Port {port}: {e}")
            self.log("Port scan finished.")
        threading.Thread(target=run_scan).start()

    def check_internet(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            self.log("Internet Connection: ✅ Online")
        except:
            self.log("Internet Connection: ❌ Offline")

    def get_external_ip(self):
        try:
            ip = requests.get("https://api.ipify.org").text
            self.log(f"External IP Address: {ip}")
        except Exception as e:
            self.log(f"[Error] Could not retrieve external IP: {e}")

if __name__ == "__main__":
    app = NetworkToolkitApp()
    app.mainloop()
