# Preamble

This is purely a tinkering project and was made in a flash, without any fore-thought into publication. Therefore you might encounter several issues, i did not even think of. Also, the compatability for your system is not a given, f.e. i use a 1440p Monitor, which the coordinates of the class that takes the screenshots in order to determine the enemy TemTem at hand will have to be fitted to other resolutions, if that applies to you. Also, this application provides no further customization, other than manually tweaking the code of course. 


# Temtem Overlay for Enemies (Python)

This project provides an overlay tool for the game **Temtem**. It detects enemy Temtems and displays relevant information, such as their types and a weaknesses/resistances table, on your screen. This tool is built using Python and relies on image recognition and web scraping techniques.

## Features

- **Real-time detection:** Automatically detects enemy Temtems during battles.
- **Types:** Display the icons of the TemTem's types. Also displays the weakness/resistances table for this/those type(s).
- **Web scraping:** Fetches its data from the Fandom TemTem Wiki 'https://temtem.fandom.com/wiki/', but saves the html upon encountering a new TemTem, thus saving requests.


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PredixCode/temtem-enemy-overlay-python.git

2. **Install Tesseract-OCR and alter the tesseract path, by changing the variable 'path_to_tesseract' in 'EnemyTemtemDetector.py'**

3. **Install the rest of the requirements in requirements.txt**


## Usage

1. **Run App.py and start TemTem**
2. **When in battle the overlay should display automatically and hide again when the name of the TemTem is no longer detected for longer than 15s**