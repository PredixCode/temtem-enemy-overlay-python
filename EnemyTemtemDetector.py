import os
import keyboard
import mss.tools
from PIL import Image
from pytesseract import pytesseract

from TemtemInfoRequester import TemtemInfoRequester
from utils.getAllTemTems import getAllTemTems





class EnemeyTemtemDetector:
    def __init__(self,temtems):
        self.temtems = temtems
        self.initPytesseract()        

    def detectEnemies(self):
        for i in range(0,2):
            self.sreenshotEnemyTitleBar(i)
        self.cleanImages()
        detected_temtems = self.getEnemyTemtemFromImage()
        if len(detected_temtems) > 0:
            return detected_temtems
        else:
            return None

    def initPytesseract(self):
        path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.tesseract_cmd = path_to_tesseract

    def sreenshotEnemyTitleBar(self,i):
        img_path = f"scrn_out/enemy{i}.png"
        with mss.mss() as sct:  
            monitor = {"top": 38+i*70, "left": 1560+i*530, "width": 300, "height": 50}
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=img_path)

    def cleanImages(self):
        for image_name in os.listdir('scrn_out'):
            img_path = os.path.join('scrn_out', image_name)
            img = Image.open(img_path)
            img = img.convert('RGB')  # Ensure the image is in RGB mode
            
            # Process the image pixel by pixel
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b = pixels[x, y]
                    if r != 255 or g != 255 or b != 255:
                        pixels[x, y] = (0, 0, 0)  # Turn non-white pixels black

            # Save the cleaned image
            img.save(img_path)

    def getEnemyTemtemFromImage(self):
        detected_temtems = []
        for image in os.listdir('scrn_out'):
            temtem_soup = str(pytesseract.image_to_string('scrn_out/'+image, config='--psm 11  --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')).strip().replace('\n', ' ')

            for element in temtem_soup.split(' '):
                if element in self.temtems:
                    detected_temtems.append(element)

        return detected_temtems
    

if __name__ == "__main__":
    temtems = getAllTemTems()
    detector = EnemeyTemtemDetector(temtems)
    
    # Function to detect enemies
    def detect_on_keypress():
        enemies = detector.detectEnemies()
        if enemies is not None:
            for enemy in enemies:
                print(enemy)
                requester = TemtemInfoRequester(enemy)
                data = requester.getAllInfo()
                
    
    # Listen for 'l' key press and trigger the detection
    keyboard.add_hotkey('l', detect_on_keypress)

    print("Press 'l' to detect enemies. Press 'esc' to exit.")
    keyboard.wait('esc')  # Keep the program running until 'esc' is pressed

