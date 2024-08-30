import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from utils.getAllTemTems import getAllTemTems
from TemtemInfoRequester import TemtemInfoRequester
from EnemyTemtemDetector import EnemeyTemtemDetector
from Overlay import TemtemOverlay


class TemtemOverlayApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize components and state
        self.temtems = self.load_temtems()
        self.detector = EnemeyTemtemDetector(self.temtems)
        self.overlay = None
        self.previous_temtems = None
        self.last_found_temtem = 0

        # Check every second for enemies
        self.init_timer()

    def load_temtems(self):
        """Loads the list of all TemTems."""
        return getAllTemTems()

    def init_timer(self):
        """Initializes the timer for periodic updates."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_enemies)
        self.timer.start(1000)  # Check every 1 second

    def check_for_enemies(self):
        """Checks for updates on enemy TemTem detection."""
        self.reset_state_if_stale()

        enemies = self.detector.detectEnemies()
        if enemies:
            temtems = self.fetch_enemy_temtems(enemies)
            if temtems and temtems != self.previous_temtems:
                self.handle_new_temtem(temtems)

    def reset_state_if_stale(self):
        """Closes the overlay if no new TemTem detected for a while."""
        if (time.time() - self.last_found_temtem) > 15:
            self.clear_overlay()
            self.previous_temtems = None

    def fetch_enemy_temtems(self, enemies):
        """Fetches detailed information for each detected enemy TemTem."""
        temtems = []
        for enemy in enemies:
            try:
                requester = TemtemInfoRequester(enemy)
                info = requester.getAllInfo()
                if info:
                    temtems.append(info)
            except Exception as e:
                print(f"Error fetching data for enemy {enemy}: {e}")
        return temtems

    def handle_new_temtem(self, temtems):
        """Handles the new TemTem data by updating the overlay."""
        self.last_found_temtem = time.time()
        self.previous_temtems = temtems
        print([temtem['name'] for temtem in temtems])
        self.update_overlay(temtems)

    def clear_overlay(self):
        """Clears the existing overlay."""
        if self.overlay:
            self.overlay.close()
            self.overlay = None

    def update_overlay(self, temtems):
        """Updates the overlay with the new TemTem data."""
        self.clear_overlay()
        self.overlay = TemtemOverlay(temtems)
        self.overlay.show()


def main():
    app = QApplication(sys.argv)
    window = TemtemOverlayApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
