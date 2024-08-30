import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from io import BytesIO

class TemtemOverlay(QWidget):
    def __init__(self, temtem_data):
        super().__init__()

        # Set up the window to be transparent and stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set a semi-transparent black background for the whole window
        self.setStyleSheet("background-color: rgba(20, 20, 20, 210);")  # Semi-transparent black

        # Set up main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add some padding around the edges
        main_layout.setSpacing(5)  # Adjust spacing between elements
        
        for temtem in temtem_data:
            temtem_layout = self.create_temtem_layout(temtem)
            main_layout.addLayout(temtem_layout)

        self.setLayout(main_layout)
        self.setGeometry(0, 10, 450, 100)  # Adjust the size and position as needed
        self.show()

    def create_temtem_layout(self, temtem):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 0, 0)  # Minimal margins for tighter layout
        layout.setSpacing(5)  # Space between the image and the text

        # Temtem image
        image_label = QLabel()
        pixmap = self.get_pixmap_from_url(temtem['image_url'])
        if pixmap:
            image_label.setPixmap(pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setFixedSize(75, 75)
        layout.addWidget(image_label)

        # Temtem name and type matchup
        name_layout = QVBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(2)

        # Name layout includes icons for each type
        name_row_layout = QHBoxLayout()
        name_row_layout.setContentsMargins(0, 0, 0, 0)
        name_row_layout.setSpacing(0)  # Reduce space between type icons and name

        # Name label
        name_label = QLabel(f"{temtem['name']} (")
        name_label.setStyleSheet("color: white; font-weight: bold;")
        name_label.setFont(QFont("Arial", 12))
        name_row_layout.addWidget(name_label)

        # Type icons next to the name
        for idx, type_ in enumerate(temtem['type']):
            type_icon_label = QLabel()
            type_icon_pixmap = QPixmap(f"type_icons/{type_}.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            type_icon_label.setPixmap(type_icon_pixmap)
            type_icon_label.setFixedSize(24, 24)
            name_row_layout.addWidget(type_icon_label)

        # Closing bracket after the types
        closing_bracket_label = QLabel(")")
        closing_bracket_label.setStyleSheet("color: white; font-weight: bold;")
        closing_bracket_label.setFont(QFont("Arial", 12))
        name_row_layout.addWidget(closing_bracket_label)

        name_layout.addLayout(name_row_layout)

        # Type matchup layout
        types_layout = QHBoxLayout()
        for type_, value in temtem['type_matchup'].items():
            type_icon_label = QLabel()
            icon_pixmap = QPixmap(f"type_icons/{type_}.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            type_icon_label.setPixmap(icon_pixmap)
            type_icon_label.setFixedSize(24, 24)
            
            if value != '4' and len(value) == 1:
                value_label = QLabel("  "+value)
            else:
                value_label = QLabel(value)
            value_label.setStyleSheet("color: white; font-weight: bold;")
            if value == "1/4":
                value_label.setStyleSheet("color: red; font-weight: bold; text-decoration: underline;")
            elif value == "1/2":
                value_label.setStyleSheet("color: yellow; font-weight: bold;")                
            elif value == "2":
                value_label.setStyleSheet("color: green; font-weight: bold;")
            elif value == "4":
                value_label.setStyleSheet("color: turquoise; font-weight: bold; text-decoration: underline;")
            value_label.setFont(QFont("Arial", 10))
            
            type_layout = QVBoxLayout()
            type_layout.setSpacing(0)  # No spacing between icon and value
            type_layout.addWidget(type_icon_label)
            type_layout.addWidget(value_label)
            type_layout.setAlignment(Qt.AlignCenter)

            types_layout.addLayout(type_layout)

        name_layout.addLayout(types_layout)

        # Add the name/type layout to the main layout
        layout.addLayout(name_layout)

        return layout

    def get_pixmap_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            return image
        except requests.exceptions.RequestException as e:
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = TemtemOverlay([
        {
            "name": "Bunbun",
            "type": ['Earth', 'Crystal'],
            "image_url": "https://static.wikia.nocookie.net/temtem_gamepedia_en/images/3/38/Bunbun.png/revision/latest/scale-to-width-down/250?cb=20220422055404",
            "type_matchup": {
                'Neutral': '-', 'Wind': '-', 'Earth': '2', 'Water': '2', 'Fire': '-', 'Nature': '2', 
                'Electric': '1/4', 'Mental': '1/2', 'Digital': '-', 'Melee': '4', 'Crystal': '1/2', 'Toxic': '1/4'
            }
        }
    ])
    sys.exit(app.exec_())
