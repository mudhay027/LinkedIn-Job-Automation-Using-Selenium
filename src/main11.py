from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
import json
import time

class EasyApplyLinkedIn:
    def __init__(self,data):
        
    ## Parameters
        self.email = data['email']
        self.password = data['password']
        self.keyword = data['keywords']
        self.location = data['location']
        chrome_service = Service(executable_path=data['driver_path'])
        chrome_options = Options()
        #chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        
    def login_linkedIn(self):
        """"This function log into your personal LinkedIn profile"""
        # Make driver go to the LinkedIn url
        self.driver.get("https://www.linkedin.com/login")
        
        # Introduce our email and password and hit enter
        login_email = self.driver.find_element("name","session_key")
        login_email.clear()
        login_email.send_keys(self.email)
        login_password = self.driver.find_element("name","session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)
        #input("Press Enter to close browser...")
    
    def job_search(self):
        """This funtion goes to the 'Jobs' section and looks for all the jobs that matches the keywords and location"""

        # Go to the Jobs section
        jobs_link = self.driver.find_element("link text","Jobs")
        jobs_link.click()
        time.sleep(3)
        
        #Introduce our keyword and location and hit enter
        # Fill the job keyword
        search_keyword = self.driver.find_element("xpath","//input[starts-with(@id,'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keyword)
        time.sleep(1)
        
        # Fill the location
        search_location = self.driver.find_element("xpath","//input[starts-with(@id,'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(Keys.CONTROL + "a")
        search_location.send_keys(self.location)
        time.sleep(5)
        search_location.send_keys(Keys.ARROW_DOWN)
        search_location.send_keys(Keys.RETURN)
        time.sleep(2)

    
    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""

        # select all filters, click on Easy Apply and apply the filter
        wait = WebDriverWait(self.driver, 10)

        all_filters_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Show all filters')]")))
        all_filters_button.click()
        time.sleep(5)
        
        # Step 1: Wait for the scrollable modal container
        scroll_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'artdeco-modal__content')]")))

        # Step 2: Scroll it all the way down to reveal 'Easy Apply'
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(2)

        # Step 3: Locate the toggle and switch it ON
        toggle_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@role='switch' and contains(@class,'artdeco-toggle__button')]")))

        if toggle_input.get_attribute("aria-checked") == "false":
            self.driver.execute_script("arguments[0].click();", toggle_input)
            print("✅ Easy Apply toggled ON")
        else:
            print("ℹ️ Easy Apply already ON")

        time.sleep(3)
        show_results_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-reusables-filters-modal-show-results-button='true']")))
        self.driver.execute_script("arguments[0].click();", show_results_btn)
        print("✅ Clicked 'Show results' button")

        
    def find_offers(self):
        """This function finds all the offers through all the pages of the search results."""
        wait = WebDriverWait(self.driver, 10)
        
        total_results_element = self.driver.find_element(By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal")
        total_results_text = total_results_element.text.split(' ', 1)[0].replace(",", "")
        total_results_int = int(total_results_text)
        print("Total Results Found:", total_results_int)
        while True:
            job_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.jobs-search__results-list li div.job-card-container")))

            print(f"Found {len(job_cards)} job cards on this page.")

            for index, job_card in enumerate(job_cards, start=1):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
                    time.sleep(1)
                    job_card.click()
                    time.sleep(3)

                    try:
                        easy_apply_btn = self.driver.find_element(By.XPATH, "//button[contains(@class,'jobs-apply-button')]")
                        print(f"[{index}] Easy Apply available → Applying...")
                        easy_apply_btn.click()
                        time.sleep(2)

                        # Submit application
                        submit_btn = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//button[@type='submit' and contains(., 'Submit application')]")))
                        submit_btn.click()
                        print("✅ Applied successfully.")
                        time.sleep(2)

                        # Close confirmation dialog if it appears
                        try:
                            dismiss_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                            dismiss_btn.click()
                        except NoSuchElementException:
                            pass

                    except NoSuchElementException:
                        print(f"[{index}] No Easy Apply → Skipping.")

                except Exception as e:
                    print(f"⚠️ Error clicking job card {index}: {e}")

            # Try to go to the next page
            try:
                next_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                if next_btn.is_enabled():
                    next_btn.click()
                    time.sleep(3)
                else:
                    print("🚀 Reached last page.")
                    break
            except NoSuchElementException:
                print("🚀 No next button found. Ending.")
                break

        
    def apply(self):
        """Apply to job offers"""
        self.driver.maximize_window()
        self.login_linkedIn()
#        input("✅ Please complete LinkedIn's security check manually if prompted. Press Enter to continue...")
        time.sleep(8)
        self.job_search()
        time.sleep(15)
        self.filter()
        time.sleep(2)
        self.find_offers()
        input('✅ Search complete. Press Enter to close browser...')
if __name__ == "__main__":
    with open("../config.json") as config_file:
        data = json.load(config_file)
    bot = EasyApplyLinkedIn(data)
    bot.apply()
    