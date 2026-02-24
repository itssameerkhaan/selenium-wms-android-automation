from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time

caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "host.docker.internal:5555",
    "appium:app": "/apk/app-release.apk",
    "appium:autoGrantPermissions": True
}


options = UiAutomator2Options().load_capabilities(caps)

# Appium 2.x server endpoint
driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)
print("App Launched Successfully!")

# Your test flow
wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Username']"))).send_keys("asis")
wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Password']"))).send_keys("asis")
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Connect']"))).click()

wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Repacking']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Create prod. container']"))).click()

wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Folder ID ?']"))).send_keys('2660027')
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='ENTER']"))).click()

wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()

wait.until(EC.visibility_of_element_located((By.XPATH,"//android.widget.EditText[@text='Container']"))).send_keys('039999900987654326')
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()

wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.TextView[@text='Enter']"))).click()

driver.quit()
print("Driver quit successfully!")
