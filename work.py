from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
import time
import requests
import json
from translator import remove_diacritics
from utility import choose_random_word
from pynput.keyboard import Key, Controller
from prints import *


class google_work:

    def __init__(self,data_path="data.json") -> None:



        with open(data_path,'r',encoding="utf-8") as f:
            self.DATA = json.load(f)

        self.DATA['Text'] = remove_diacritics(self.DATA['Text'])

        self.first,self.second,self.third = choose_random_word(self.DATA['Text']).lower(), choose_random_word(self.DATA['Text']).lower(), choose_random_word(self.DATA['Text']).lower()


        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                 'X-Octo-Api-Token': self.DATA['X-Octo-Api-Token']
                }

        url = f"https://app.octobrowser.net/api/v2/automation/profiles?search_tags={self.DATA['title']}"



        response_octo = requests.request("GET", url, headers=headers)
        data_uuid = response_octo.json()
        uuid = data_uuid.get('data')
        newuuid = dict()
        for ud in uuid:
            newuuid[ud.pop('uuid')] = ud

        octo = str(newuuid)
        octo_str = octo.replace("}", '')
        octo_str = octo_str.replace("{", '')
        octo_str = octo_str.replace(" ", '')
        octo_str = octo_str.replace(":", '')
        octo_str = octo_str.replace("'", '')

        octo_id = octo_str.split(",")

        self.PROFILE_ID = octo_id.pop(0)
        self.PROFILE_ID = octo_id.pop(0)
        self.PROFILE_ID = octo_id.pop(0)

        self.LOCAL_API = f'http://localhost:{self.DATA.get("port")}/api/profiles'

        port = self.get_debug_port(self.PROFILE_ID)
        self.driver = self.get_webdriver(port)        


    def get_webdriver(self,port):
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
    
        # Change chrome driver path accordingly
        driver = webdriver.Chrome(options=chrome_options)
        return driver


    def get_debug_port(self,profile_id):
        data = requests.post(
            f'{self.LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
        ).json()
        return data['debug_port']

    def create_site(self):
        action = ActionChains(self.driver)       
        self.driver.get('https://sites.google.com/u/0/new?pli=1&authuser=0')

        try:
            self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[3]/div').click()    
        except:
            self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div[1]/img').click()  
        
        printOk('Sleep for 15 seconds')
        time.sleep(15)
        
        self.url_google_site = self.driver.current_url

        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[5]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[2]/div[2]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[2]/div[1]/div').click()

        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[2]/span[2]').click()

        #change home name
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div[3]').click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div[2]/div/div/span[2]').click()

        time.sleep(3)
        for _ in range(20):
            action.send_keys(Keys.BACKSPACE).perform()
            
        time.sleep(3)
        action.send_keys(self.first).perform()
        time.sleep(3)
        action.send_keys(Keys.ENTER).perform()


        # action.send_keys(Keys.DELETE).perform()
        wait_time = 2
        for name in self.second,self.third:
            time.sleep(wait_time)
            button_plus=self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[3]/div/div[1]')
            action.move_to_element(button_plus).perform()
            button_plus.click()
            time.sleep(wait_time)
            action.send_keys(name).perform()
            time.sleep(wait_time)
            action.send_keys(Keys.ENTER).perform()
        
        time.sleep(3)
        #second Window
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[1]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[1]/div[1]').click()
        time.sleep(3)
        action.send_keys(self.DATA['Text']).perform()
       
        textPart =self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[6]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[2]/div[1]/div[1]/p/span')
        textPart.click()
        time.sleep(3)
        textPart.send_keys(Keys.CONTROL,'a')
        time.sleep(3)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[6]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[4]/div/div/div[3]/div/div/div[1]/label/input').click()
        action.send_keys(Keys.DELETE).perform()
        action.send_keys('18').perform()
        time.sleep(3)
        textPart.click()


        time.sleep(3)
        # third window 
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[2]/span[2]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div/div[3]/div[3]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[1]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[1]/div[1]').click()

        time.sleep(3)
        action.send_keys(self.DATA['Text']).perform()

        textPart = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[6]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[2]/div[1]/div[1]/p/span')
        textPart.click()
        time.sleep(3)
        textPart.send_keys(Keys.CONTROL,'a')
        time.sleep(3)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section/div[7]/div[6]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[4]/div/div/div[3]/div/div/div[1]/label/input').click()
        action.send_keys(Keys.DELETE).perform()
        action.send_keys('24').perform()
        time.sleep(3)
        textPart.click()

        # first window 
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[2]/span[2]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div/div[3]/div[1]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[1]').click()
        # take photo
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[1]/div[2]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[1]/div[2]/div/div[2]/div/ul/li[1]').click()
        time.sleep(3)
        keyboard = Controller()

        keyboard.type(self.DATA['photo'])
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        #if bug perfomes
        time.sleep(7)
        action.send_keys(Keys.ESCAPE).perform()

        # type text
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[1]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[1]/div[1]').click()

        action.send_keys(self.DATA['Text']).perform()

        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[1]').click()

        #work with button creation
        button_button = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[2]/span/div/div[3]/div[4]')
        
        button_button.click()
        # action.double_click(button_button).perform()


        action.send_keys(choose_random_word(self.DATA['Text'])+" "+ choose_random_word(self.DATA['Text'])+" "+choose_random_word(self.DATA['Text'])).perform()
        time.sleep(3)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[2]/span/div/div[2]/div[1]/div[1]/div[1]/input').click()
        except:
            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/span/div/div[2]/div[1]/div[1]/div[1]/input').click()
        time.sleep(1)
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.ENTER).perform()

        # self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[2]/span/div/div[2]/div[1]/div[1]/div[1]/input').click()

        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[2]/div[3]/div[2]').click()

        time.sleep(5)        
        #blending button
        circle = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[3]/span/div/div[2]/div[2]/div/div/span/div/div[4]/div/div[1]/div/div/article/section[3]/div[7]/div[6]/div/group/div[2]/div/row/div/div[2]/tile/div[2]/div/div[4]/div[2]/div[2]')
        
        action.click_and_hold(circle).move_by_offset(1000,0).release(circle).perform()
        
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[1]/div/div/span/button[2]').click()
        #hide   
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div[3]').click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div[2]/div/div/span[5]').click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div/div[3]/div[3]/div[2]/div[1]/div[3]').click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[4]/span/div/div[1]/div[3]/span/div/div/div/div[2]/div[2]/div/div/span[5]').click()


        time.sleep(1)
        #publish
        self.site_name = choose_random_word(self.DATA['Text'])+"-"+choose_random_word(self.DATA['Text']).lower()
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[12]/div[1]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[2]/span/div/div[1]/div[1]/div[1]').click()
        action.send_keys(self.site_name).perform()
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[2]/div[4]/div[2]/span/span').click()

        # time.sleep(15)
        # #get posted url
        # self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[12]/div[2]/span').click()
        # time.sleep(5)
        # self.driver.find_element(By.XPATH,'/html/body/div[7]/div/div/span[3]/div[2]/div').click()
        # time.sleep(5)
        self.url = str('https://sites.google.com/view/'+self.site_name+"/"+self.first)
        printOk(self.url)
        # time.sleep(200)

    def perform_analytics(self):
        action = ActionChains(self.driver)       

        self.driver.get('https://analytics.google.com/analytics/web/provision/#/provision')

        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-new-promo/div/div[1]/div/div[2]/button').click()
        time.sleep(15)

        #input acc name
        name = self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[1]/ga-create-firebase-account/form/xap-card[1]/xap-card-content/div/div/div[2]/mat-form-field/div[1]/div/div[2]/input')
        time.sleep(5)
        name.click()
        time.sleep(3)
        name.send_keys(self.DATA['acc_name'])
        
        #tick check box
        time.sleep(4)
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[1]/ga-create-firebase-account/form/xap-card[2]/xap-card-content/ga-data-sharing/div/div/div[1]/div/section[1]/div[1]/div[1]/div/mat-checkbox/div/div/input').click()

        #press next
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[1]/button').click()

        time.sleep(5)
        #property
        property = self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[2]/div[2]/div/property-setup/xap-card/div[2]/mat-form-field/div[1]/div/div[2]/input')
        property.click()
        property.send_keys(self.DATA['property_name'])
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[2]/div[2]/div/button[2]').click()

        #describe your business
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[3]/div[2]/div/ga-business-info/xap-card/xap-card-content/industry-selector/searchable-select/button').click()
        time.sleep(5)
        bus_inp = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div/mat-form-field/div[1]/div[2]/div[2]/input')
        bus_inp.click()
        bus_inp.send_keys(self.DATA['desc'])
        time.sleep(1)
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.ENTER).perform()


        time.sleep(5)
        #business size
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[3]/div[2]/div/ga-business-info/xap-card/xap-card-content/business-size-selector/mat-radio-group/mat-radio-button[1]/div/div/input').click()
        time.sleep(5)
        #NEXT
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[3]/div[2]/div/button[2]').click()

        time.sleep(5)
        #business objectives
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[4]/div[2]/div/ga-business-objective-selector/div/slat[1]/div[2]/div/mat-checkbox/div/div/input').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[4]/div[2]/div/ga-business-objective-selector/div/slat[2]/div[2]/div/mat-checkbox/div/div/input').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[4]/div[2]/div/ga-business-objective-selector/div/slat[3]/div[2]/div/mat-checkbox/div/div/input').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[4]/div[2]/div/ga-business-objective-selector/div/slat[4]/div[2]/div/mat-checkbox/div/div/input').click()
        time.sleep(5)
        #NEXT
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[4]/div[2]/div/button[2]').click()

        time.sleep(15)
        #Accept Google Analytics Terms of Service Agreemen 
        self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mat-dialog-container/div/div/xap-deferred-loader-outlet/ga-tos-dialog/mat-dialog-content/ga-tos-content/section[2]/div/mat-checkbox/div/div/input').click()
        self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mat-dialog-container/div/div/xap-deferred-loader-outlet/ga-tos-dialog/mat-dialog-content/ga-tos-content/section[3]/div[3]/mat-checkbox/div/div/input').click()
        #Agree
        self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mat-dialog-container/div/div/xap-deferred-loader-outlet/ga-tos-dialog/mat-dialog-actions/ga-tos-buttons/button[1]').click()

        time.sleep(15)
        #Start collecting data
        self.driver.find_element(By.XPATH,'/html/body/ga-hybrid-app-root/ui-view-wrapper/div/ga-provision/div/ui-view-wrapper/div/ga-create-account/div/div/mat-stepper/div/div[2]/div[5]/ga-admin-streams-setting/ga-admin-streams-promo/ga-admin-stream-type-selector/div/mat-card/mat-card-content/button[1]').click()
        time.sleep(15)
        site_name_input = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mdx-slider-container/ga-admin-web-stream-editor/div/div/mat-card/mat-card-content/form/mat-form-field[2]')
        small_url = self.url.replace("https://","")
        site_name_input.click()
        time.sleep(2)
        action.send_keys(small_url).perform()
        
        time.sleep(5)

        all_site_name_input = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mdx-slider-container/ga-admin-web-stream-editor/div/div/mat-card/mat-card-content/form/mat-form-field[3]/div[1]/div/div[2]/input')
        all_site_name_input.click()
        time.sleep(2)
        action.send_keys(self.url).perform()
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mdx-slider-container/ga-admin-web-stream-editor/div/div/mat-card/mat-card-content/form/div/button').click()

        time.sleep(15)  
        action.send_keys(Keys.ESCAPE).perform()          
        # self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/gtm-container-install-page/gtm-admin-page/div/div[1]/i').click()
        #                                  /html/body/div[1]/div[2]/gtm-container-install-page/gtm-admin-page/div/div[1]/i
        time.sleep(5)
        #get MEASUREMENT ID
        self.MEASUREMENT_ID = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/mdx-slider-container/web-stream-details/div/div/web-stream-settings/xap-card/div[2]/div[4]/div[2]/span').text   
                                                  #/html/body/div[6]/div[2]/div/mdx-slider-container/web-stream-details/div/div/web-stream-settings/xap-card/div[2]/div[4]/div[2]/span


    def add_statistics(self):
        self.driver.get(self.url_google_site)
        time.sleep(10)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[10]/span/span/span/span/button').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/span/div/div/div[1]/div[5]').click()
        time.sleep(5)

        id_input = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/span/div/div/div[2]/span[5]/div/div/div/div[3]/div[1]/div[1]/input')
        id_input.click()
        id_input.send_keys(self.MEASUREMENT_ID)
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/div[2]/div[3]/div').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[12]/div[1]/span/span').click()
        time.sleep(2)
        #PUBLISH
        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/div[4]/div[2]').click()
        time.sleep(10)

    def google_console(self):
        action = ActionChains(self.driver)       

        self.driver.get('https://search.google.com/search-console/about')

        time.sleep(15)

        #push first button
        self.driver.find_element(By.XPATH,'/html/body/div/c-wiz/div/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/a').click()
        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[2]/div/div[1]/span/div[3]/div[1]/div[3]/div[4]/div/div[1]/div/div[1]/input').click()
            time.sleep(1)
            url = str('https://sites.google.com/view/'+self.site_name)
            action.send_keys(url).perform()
            time.sleep(2)
            self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[2]/div/div[1]/span/div[3]/div[1]/div[3]/div[5]').click()
            time.sleep(15)


            #Verify
            self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[3]/div[2]').click()
            time.sleep(10)
            self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[2]/div/div').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[2]/div[2]/div/div[3]/div[2]/div/div').click()
        except:
            printError('is verified before. Current url will not work')
            # return
        #find our site
        time.sleep(5)
        self.driver.find_element(By.XPATH,'/html/body/div[7]/div[2]/header/div[2]/div[2]/div[2]/form/div/div/div/div/div/div[1]/input[2]').click()
        time.sleep(3)
        action.send_keys(self.url).perform()
        time.sleep(5)
        action.send_keys(Keys.ENTER).perform()
        time.sleep(30)
        #Test Live URL
        self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[3]/div/div[2]/div[1]/div/div[2]/c-wiz/div/div').click()
        time.sleep(60)

        #Request indexing (Live test)
        for _ in range(5):
            try:
                self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[4]/div/div[2]/span/div/div[2]/span/div[2]/div/div/div[1]/span/div[2]/div/c-wiz[2]/div[3]/span/div').click() 
                
                time.sleep(15)

                self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[2]/div[1]/div/span').text
                self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[3]/div').click()
                break
            except:
                action.send_keys(Keys.ESCAPE).perform()
                printError("Oops can't request indexing\n Next attempt in 30 seconds")
                time.sleep(30)
        # Google index
        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[2]/div/div[2]/span/div/div[2]/span/div[1]/div/div[2]/c-wiz/div/div[1]').click()
        except:
            time.sleep(5)
            self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[4]/div[1]/div[2]/span/div/div[2]/span/div[1]/div/div[2]/c-wiz/div/div[1]').click() #portugal

        time.sleep(10)

        #Request indexing (Google index)
        for _ in range(5):
            try:
                try:
                    self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[3]/div/div[2]/div[2]/div/div/div[1]/span/div[2]/div/c-wiz[2]/div[3]/span/div').click()
                except:
                    self.driver.find_element(By.XPATH,'/html/body/div[7]/c-wiz[5]/div[1]/div[2]/div[2]/div/div/div[1]/span/div[2]/div/c-wiz[2]/div[3]/span/div').click() #portugal
                time.sleep(15)

                self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[2]/div[1]/div/span').text
                self.driver.find_element(By.XPATH,'/html/body/div[7]/div[6]/div/div[2]/div[3]/div').click()
                break
            except:
                action.send_keys(Keys.ESCAPE).perform()
                printError("Oops can't request indexing\n Next attempt in 30 seconds")
                time.sleep(30)





def work():
    gw = google_work()
    printOk("Start working")
    
    # gw.create_site()
    # printOk("Site was created")

    # # gw.url = 'https://sites.google.com/view/stejna-Naopak/Ceska'
    # gw.perform_analytics()
    # printOk(str("MEASUREMENT ID = " + gw.MEASUREMENT_ID + "\nAnalytics performed"))
    # gw.add_statistics()
    # printOk("Site with MEASUREMENT ID was published")
    gw.url = 'https://sites.google.com/view/CSSZ-variantou/call'

    gw.google_console()
    printOk("Verifird")




if __name__ == "__main__":
    work()
    
