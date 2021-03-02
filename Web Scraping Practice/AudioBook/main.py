from selenium import webdriver
import pyautogui
import time

url = "https://ujyaaloonline.com/show/9594"
browser = webdriver.Chrome()
browser.get(url)

browser.find_element_by_css_selector(".btn-primary").click()
# browser.get("https://unncdn.prixacdn.net/media/radio_audio/2020/12/18/Shruti_Shembeg-Junkiri_ko_Sangeet-14-2020-12-18.mp3")
# browser.save_screenshot("audio.png") 


# FILE_NAME = 'C:\\path\\to\\file\\file.ext'
# Type the file path and name is Save AS dialog
# pyautogui.typewrite(FILE_NAME)

pyautogui.hotkey("ctrl", 's')
time.sleep(3)
pyautogui.hotkey('enter')