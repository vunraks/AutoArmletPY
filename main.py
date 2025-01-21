import cv2
import time
import numpy as np
import configparser
import easyocr
import keyboard
import multiprocessing as mp
from mss import mss
reader = easyocr.Reader(['en'], gpu=True)

def read_coordinates():
    config = configparser.ConfigParser()
    config.read('C:/Users/VUNRAKS/Desktop/NM/Py/settings.ini')
    coordinates = config['DEFAULT']
    x1, y1, x2, y2 = map(int, (coordinates['x1'], coordinates['y1'], coordinates['x2'], coordinates['y2']))
    return x1, y1, x2, y2

def capture_screen(sct, region):
    screen = np.array(sct.grab(region))
    return cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

def process_screen(screen):
    global min_hp
    global armlet_button
    global cooldown
    text = reader.readtext(screen, detail = 0)
    if len(text) > 0:
        hp = text[0]
        if hp.isdigit() and int(hp) <= min_hp:
            print('ABUZE!!')
            keyboard.send(armlet_button)
            keyboard.send(armlet_button)
            time.sleep(cooldown)

def screen_processing(sct, region):
    while True:
        start_time = time.time()
        screen = capture_screen(sct, region)
        process_screen(screen)
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        print(f'FPS: {round(fps)}')

def main():
    x1, y1, x2, y2 = read_coordinates()
    with mss() as sct:
        region = {'top': y1, 'left': x1, 'width': x2-x1, 'height': y2-y1}
        screen_processing(sct, region)

if __name__ == "__main__":
    min_hp = 250
    armlet_button = 'x'
    cooldown = 0.6
    mp.set_start_method('spawn')
    main()