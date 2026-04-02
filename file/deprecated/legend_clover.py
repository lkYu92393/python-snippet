import time
import random
from PIL import Image
import os
from io import BytesIO
import base64
# import pytesseract
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

DMM_LOGIN = "https://accounts.dmm.co.jp/service/login/password"
LEGEND_CLOVER = "https://pc-play.games.dmm.co.jp/play/legeclox/"

WAIT_TIME_BETWEEN_CLICK = 1.5
WAIT_TIME_BETWEEN_MENU = 2


def click_random(num):
    return (num + random.random())


def click_episode(actions, canvas, ep):
    if ep == 4:
        # ep4 boss skip
        actions.move_to_element(canvas).move_by_offset(0, -150).click()
        actions.perform()
    else:
        # ep7 boss skip
        actions.move_to_element(canvas).move_by_offset(500, 20).click()
        actions.perform()

    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    actions.move_to_element(canvas).move_by_offset(90, 250).click()
    actions.perform()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    actions.move_to_element(canvas).move_by_offset(500, 20).click()
    actions.perform()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    actions.move_to_element(canvas).move_by_offset(500, 20).click()
    actions.perform()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)

    # extra click to ensure no windows opened at quest
    actions.move_to_element(canvas).move_by_offset(500, -150).click()
    actions.perform()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    actions.move_to_element(canvas).move_by_offset(500, -150).click()
    actions.perform()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)


def legend_clover_daily():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1600, 1100)
    driver.get(DMM_LOGIN)

    account = os.getenv('ACCOUNT')
    password = os.getenv('PASSWORD')

    # login
    elem = driver.find_element(By.CSS_SELECTOR, "input#login_id")
    elem.send_keys(account)

    elem = driver.find_element(By.CSS_SELECTOR, "input#password")
    elem.send_keys(password)

    login_button = driver.find_element(
        By.CSS_SELECTOR, "input[data-e2e='login_button']")
    login_button.click()

    WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.ageCheck__link--r18")))

    # age check
    yes_button = (driver.find_element(
        By.CSS_SELECTOR, "a.ageCheck__link--r18"))
    yes_button.click()

    # reached homepage
    driver.get(LEGEND_CLOVER)

    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "iframe#game_frame")))

    # reached legend clover site
    actions = ActionChains(driver)
    header = driver.find_element(By.CSS_SELECTOR, "div.inner.clearfix")

    iframe = driver.find_element(By.CSS_SELECTOR, "iframe#game_frame")
    driver.switch_to.frame(iframe)
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe#main")
    driver.switch_to.frame(iframe)
    canvas = driver.find_element(By.CSS_SELECTOR, "canvas#unity-canvas")

    def click_location(x, y):
        actions.move_to_element(canvas).move_by_offset(
            click_random(x), click_random(y)).click()
        actions.perform()

    def click_main_page(num_of_time=1, wait=WAIT_TIME_BETWEEN_CLICK):
        for i in range(0, num_of_time):
            time.sleep(wait)
            actions.move_to_element(canvas).move_by_offset(
                click_random(-580), click_random(310)).click()
            actions.perform()
 
    time.sleep(20)

    # click yes for sound
    click_location(80, 130)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(80, 130)
    time.sleep(WAIT_TIME_BETWEEN_MENU)

    # click to skip OP
    
    click_main_page(3)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_main_page(3)

    print("REACHED CHOOSE DRAWING QUALITY")

    # choose drawing quality
    click_location(50, 20)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(0, 130)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(50, 20)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(0, 130)

    time.sleep(25)

    click_location(0, 130)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(60, 230)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(0, 130)
    time.sleep(WAIT_TIME_BETWEEN_MENU)
    click_location(60, 230)

    print("GACHA ACKNOWLEDGED")

    time.sleep(30)
    # wait to load into main menu

    # need to handle daily login bonus

    click_count = 0
    while (True):
        if click_count >= 4:
            break
        click_count += 1
        im = Image.open(BytesIO(base64.b64decode(canvas.screenshot_as_base64)))
        px = im.getpixel((25, 700))
        print(px)

        if not (px[0] == 255  and px[1] >= 180 and px[1] <= 200 and px[2] >= 82 and px[2] <= 117):
            click_main_page(5, 0.5)
        else:
            break

    # friend coins
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(-380, -230)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(420, 200)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_main_page(6)

    print("GOT FRIEND COINS")

    # get matome daily reward
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(-580, -150)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(-580, -150)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(-450, -230)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(360, 210)

    click_main_page(6)

    print("COLLECTED DAILY REWARDS")

    # click quest

    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(0, 300)
    time.sleep(5)

    # select sub quest
    click_location(150, -150)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)

    # chapter select
    chapter_location_x = 0
    chapter_location_y = 0

    click_location(chapter_location_x, chapter_location_y)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(chapter_location_x, chapter_location_y)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)

    chapter_start = 9
    chapter_end = 3

    # try:
    #     im = Image.open(BytesIO(base64.b64decode(canvas.screenshot_as_base64)))
    #     img = im.crop((595,10,700,40))

    #     custom_config = r'--oem 3 --psm 6'
    #     text = pytesseract.image_to_string(img, config=custom_config)
    #     stamina = int(text.split('/')[0])

    #     chapter_end = chapter_start - 1 - int(stamina / 150)
    # except:
    #     img.save("debug_stamina.png")
    #     print("FAILED TO READ. IGNORE STAMINA READING.")
    #     chapter_end = 3

    for i in range(chapter_start, chapter_end, -1):
        # choose normal mode

        click_location(-500, -250)
        time.sleep(WAIT_TIME_BETWEEN_CLICK)

        click_episode(actions, canvas, 4)
        click_episode(actions, canvas, 7)

        print(f"FINISH NORMAL MODE FOR CHAPTER {i}")

        # choose hard mode
        click_location(-500, -150)
        time.sleep(WAIT_TIME_BETWEEN_CLICK)

        click_episode(actions, canvas, 4)
        click_episode(actions, canvas, 7)

        print(f"FINISH HARD MODE FOR CHAPTER {i}")

        # previous chapter
        click_location(-580, -40)
        time.sleep(WAIT_TIME_BETWEEN_CLICK)

    print("END CHAPTER RUN")

    # go to my page
    click_main_page()
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    # get remaining daily quest reward
    click_location(-450, -230)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)
    click_location(360, 210)
    time.sleep(WAIT_TIME_BETWEEN_CLICK)

    # click_main_page(5)

    time.sleep(60)

    driver.quit()
