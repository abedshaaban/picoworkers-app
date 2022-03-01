import pyautogui
import time


# import subprocess
# subprocess.Popen('C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')


# pyautogui.moveTo(85, 55, duration = 1)

# pyautogui.click(100, 100)

# print(pyautogui.size())

# print(pyautogui.position())




def go_to_refresh_btn():
    pyautogui.moveTo(85, 55, duration = 1)


while True:
    if pyautogui.position().x == 85 and pyautogui.position().y ==55:
        pyautogui.moveTo(1100, 1100, duration = 1)
        pyautogui.moveTo(85, 55, duration = 5)
        pyautogui.click(85, 55)
        print('good')
        time.sleep(300)
    else:
        go_to_refresh_btn()
    