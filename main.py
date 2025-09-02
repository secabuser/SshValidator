import socket
import threading
import concurrent.futures
import time
from pystyle import Colors, Colorate, Center
from colorama import Fore, init
from os import system, name
from tqdm import tqdm

init()

G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
RE = Fore.RESET
Y = Fore.YELLOW

class T:
    def __init__(self, fil, wrk, del_, fts, sav, inv):
        self.fil = fil
        self.wrk = wrk
        self.del_ = del_
        self.fts = fts
        self.sav = sav
        self.inv = inv
        self.tgt = []
        self.lok = threading.Lock()
        self.val = 0
        self.inv_ = 0
        self.err = 0
        self.chk = 0
        self.tot = 0

    def clr(self):
        system("cls" if name == "nt" else "clear")

    def bnr(self):
        banner = '''
 ▗▄▄▖ ▗▄▄▖▗▖ ▗▖    ▗▖  ▗▖ ▗▄▖ ▗▖   ▗▄▄▄▖▗▄▄▄   ▗▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
▐▌   ▐▌   ▐▌ ▐▌    ▐▌  ▐▌▐▌ ▐▌▐▌     █  ▐▌  █ ▐▌ ▐▌ █ ▐▌ ▐▌▐▌ ▐▌
 ▝▀▚▖ ▝▀▚▖▐▛▀▜▌    ▐▌  ▐▌▐▛▀▜▌▐▌     █  ▐▌  █ ▐▛▀▜▌ █ ▐▌ ▐▌▐▛▀▚▖
▗▄▄▞▘▗▄▄▞▘▐▌ ▐▌     ▝▚▞▘ ▐▌ ▐▌▐▙▄▄▖▗▄█▄▖▐▙▄▄▀ ▐▌ ▐▌ █ ▝▚▄▞▘▐▌ ▐▌

                           t.me/secabuser
'''
        print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(banner)))

    def lod(self):
        try:
            with open(self.fil, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or ":" not in line:
                        continue
                    try:
                        ip, port = line.split(":")
                        self.tgt.append((ip, int(port)))
                    except (ValueError, IndexError):
                        continue
            self.tot = len(self.tgt)
        except FileNotFoundError:
            print(f"{R}File not found ;]{RE}")
            exit(1)

    def vrf(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.del_)
            s.connect((ip, port))
            b = s.recv(1024)
            if b"SSH" in b:
                s.close()
                return True
            else:
                s.close()
                return False
        except socket.error:
            return False

    def prc(self, target):
        ip, port = target
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.del_)
            res = s.connect_ex((ip, port))
            if res == 0:
                is_v = False
                if self.fts:
                    is_v = self.vrf(ip, port)
                else:
                    is_v = True
                if is_v:
                    with self.lok:
                        self.val += 1
                    with self.lok:
                        with open(self.sav, "a") as o:
                            o.write(f"{ip}:{port}\n")
                    txt = f"{G}[VALID]{RE}"
                else:
                    with self.lok:
                        self.inv_ += 1
                    with self.lok:
                        with open(self.inv, "a") as o:
                            o.write(f"{ip}:{port}\n")
                    txt = f"{Y}[INVALID]{RE}"
            else:
                with self.lok:
                    self.inv_ += 1
                with self.lok:
                    with open(self.inv, "a") as o:
                        o.write(f"{ip}:{port}\n")
                txt = f"{R}[Closed]{RE}"
            s.close()
        except:
            txt = f"{Y}[Error]{RE}"
            with self.lok:
                self.err += 1
        finally:
            with self.lok:
                self.chk += 1
        return f"{txt} {ip}:{port}"

    def run(self):
        self.lod()
        self.clr()
        self.bnr()
        strt = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.wrk) as ex:
            futs = [ex.submit(self.prc, t) for t in self.tgt]
            with tqdm(total=self.tot, ncols=100, bar_format="{desc}") as p:
                for fut in concurrent.futures.as_completed(futs):
                    status = fut.result()
                    elps = time.time() - strt
                    per = round(self.chk / elps, 1) if elps > 0 else 0
                    p.set_description_str(
                        f"Valid: {self.val} | Invalid: {self.inv_} | Error: {self.err} | Per/s: {per}ip | {self.chk}/{self.tot} Ips"
                    )
                    p.update(1)

if __name__ == "__main__":
    system("cls" if name == "nt" else "clear")
    tool = T("", 0, 0, False, "valid.txt", "invalid.txt")
    tool.bnr()
    fil_in = input(f"{W}File > {RE}").strip()
    try:
        wrk_in = int(input(f"{W}Workers > {RE}").strip())
        del_in = float(input(f"{W}Timeout > {RE}").strip())
        fts_in = input(f"{W}Full Test? (y/n) > {RE}").strip().lower() == "y"
        sav_in = input(f"{W}Valid Output > {RE}").strip()
        inv_in = input(f"{W}Invalid Output > {RE}").strip()
    except:
        print(f"{R}Invalid input ;]{RE}")
        exit(1)
    
    main = T(fil_in, wrk_in, del_in, fts_in, sav_in, inv_in)
    main.run()