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

        time.sleep(1)
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
        
        time.sleep(2)
        # Wait for at least one job card to appear
        results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")))

        # Small scroll to trigger lazy load if needed
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(1)

        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")

        print(f"Found {len(job_cards)} jobs")
        if not results:
            print("⚠️ No jobs found — LinkedIn layout may have changed.")
        return

        for result in results:
            try:
                title_element = result.find_element(By.CSS_SELECTOR, "a.job-card-list__title")
                self.submit_apply(title_element)
            except NoSuchElementException:
                print("⚠️ No title found for a job card, skipping...")
        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=',1)[1])

            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+'&start='+str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements_by_class_name("occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements_by_class_name('job-card-search__title.artdeco-entity-lockup__title.ember-view')
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
        else:
            self.close_session()
        
    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""

        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(2)
        
        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element_by_xpath("//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass
        time.sleep(1)
        
        # try to submit if submit application is available...
        try:
            submit = self.driver.find_element_by_xpath("//button[@data-control-name='submit_unify']")
            submit.send_keys(Keys.RETURN)
        
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element_by_xpath("//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(1)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()
        
    def apply(self):
        """Apply to job offers"""
        self.driver.maximize_window()
        self.login_linkedIn()
        input("✅ Please complete LinkedIn's security check manually if prompted. Press Enter to continue...")
        time.sleep(10)
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
    