import os
import time
import cv2
import numpy as np
import pyautogui
import keyboard
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def run_debug_macro():
    print("Fishing Grind Cheat button press")
    print(" In the game, wait for a bite. If the script is silent, PRESS THE F9 KEY.")
    print("   The script will save a 'DEBUG_SCREEN.png' file — from it we'll see what's blinding the bot.")
    
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    screen_w, screen_h = 1920, 1080

    region = (int(screen_w/2 - 300), int(screen_h/2 - 300), 600, 600)
    
    while True:

        screen = pyautogui.screenshot(region=region)
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        

        if keyboard.is_pressed('f9'):
            debug_path = os.path.join(current_folder, "DEBUG_SCREEN.png")
            cv2.imwrite(debug_path, screen_gray)
            print(f"\n[Debug] DEBUG_SCREEN.png saved: {debug_path}")
            time.sleep(1.0) 
        
        files = os.listdir(current_folder)
        png_files = [f for f in files if f.endswith('.png') and not f.startswith('DEBUG')]
        
        for file_name in png_files:
            image_path = os.path.join(current_folder, file_name)
            keys_to_press = file_name[:-4]
            
            template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                continue
                
            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val >= 0.93:  # accuracy 
                print(f"[{file_name}] (accuracy: {max_val:.2f})")
                
                for char in keys_to_press:
                    keyboard.send(char)
                    print(f"Button: {char}")
                    
                time.sleep(0.5)
                break 
                
        time.sleep(0.01)

if __name__ == "__main__":
    run_debug_macro()
