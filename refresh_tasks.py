from selenium.webdriver.common.by import By
import time

async def refresh_tasks(browser):
    steps_a = browser.find_element(By.CLASS_NAME, 'player-topbar__step-pins').find_elements(By.XPATH, ".//div[contains(@class, 'm-step-pin ember-view player__step-pin')]")
    for step in steps_a:
        try:
            svg = step.find_element(By.TAG_NAME, 'svg')
            step.click()
            time.sleep(1)
            browser.find_element(By.CLASS_NAME, 'again-btn white').click()
            print(browser.current_url)
        except:
            continue
    time.sleep(1000)
            

