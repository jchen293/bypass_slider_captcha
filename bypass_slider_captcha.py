import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import selenium.support.ui.WebDriverWait;
class webScraper:

    TRACKING_URL = 'Your_tracking_URL_here'
    tracking_response = requests.get(TRACKING_URL)
    html = BeautifulSoup(tracking_response.content, "html.parser") #parse the html
    textarea = html.find("textarea", attrs={"id": "your_id_here"}) #make sure your id is valid
    print(textarea) #finding a specific area in a page
    if not textarea: #if the textarea is empty which mean there is a slider captcha
        chrome_options = webdriver.ChromeOptions() #create a chrome option(setting), so we can pass in when we initilize the web driver
        chrome_options.add_argument(f'--window-position={217},{172}') #set window position, can be optional
        chrome_options.add_argument(f'--window-size={1200},{1000}') #set window size, can be optional
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #disable the user automation testing
        chrome_options.add_experimental_option("useAutomationExtension", False) #disable the user automation testing
        prefs = {"profile.managed_default_content_settings.images": 2} #remove the image in the captcha, save some load time
        chrome_options.add_argument( #add user agent so the server know we are acutally huamn
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')

        chrome_options.add_argument('--headless') #headless mode which does not open up a browser
        #chrome_options.add_argument('--no-sandbox') #in linux

        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options) #initilize the webdriver
        #the first argument can also be a path to the .exe ChromeDriverManager file

        driver.maximize_window() # For maximizing window
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {  #bypass the bot detection, preventing we are not using selenium
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        driver.get(TRACKING_URL)  #open the tracking link in webdriver
        driver.implicitly_wait(5) #wait for up to 5 seconds to load the HTML before we search the slider
        scrollBar = driver.find_element_by_id('your_slider_id') #find the slider id in the captcha page
        ActionChains(driver).click_and_hold(scrollBar).perform() #click and hold the slider button/icon
    
        ActionChains(driver).move_by_offset(xoffset=300,yoffset=0).perform() #move the slider to the right in order to access the tracking page
        time.sleep(5) #sleep 5 second before we get the html after the page redirection
        html = BeautifulSoup(driver.page_source, "html.parser") #parse the html in beautifulSoup
        textarea = html.find("textarea", attrs={"id": "your_id_here"}) #find the textarea
        print(textarea) #now we should get the page after bypassing the captcha
        driver.quit() #close the webdriver
       