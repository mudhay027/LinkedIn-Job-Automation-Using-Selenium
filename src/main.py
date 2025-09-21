import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====== Selenium Setup ======
def init_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


# ====== LinkedIn Login ======
def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.ENTER)

    try:
        WebDriverWait(driver, 20).until(
            lambda d: "/feed" in d.current_url or "/jobs" in d.current_url
        )
        print("Logged in successfully!")
    except TimeoutException:
        input("Login not detected. Please complete captcha or 2FA, then press ENTER...")

# ====== Job Search ======
def search_jobs(driver, keywords, location):
    query = keywords.replace(' ', '%20')
    loc = location.replace(' ', '%20')
    url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}&f_AL=true"
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.jobs-search__results-list"))
        )
        print("Jobs listing loaded.")
    except TimeoutException:
        input("Please solve LinkedIn security check manually, then press ENTER...")

# ====== Load More Job Cards ======
def load_job_cards(driver, pause=2, max_scrolls=30):
    prev_count = 0
    for i in range(max_scrolls):
        cards = driver.find_elements(By.XPATH, "//*[contains(@class,'job-card-container--clickable')]")
        if not cards:
            break

        driver.execute_script("arguments[0].scrollIntoView();", cards[-1])
        time.sleep(pause)

        new_count = len(cards)
        if new_count == prev_count:
            print(f" Loaded all {new_count} job cards after {i+1} scrolls.")
            break
        prev_count = new_count


# ====== Discard Application ======
def discard_application(driver):
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.artdeco-modal__dismiss"))
        )
        driver.execute_script("arguments[0].click();", close_btn)
        time.sleep(1)

        discard_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Discard')]"))
        )
        driver.execute_script("arguments[0].click();", discard_btn)
        print(" Application discarded")
    except Exception as e:
        print(" Error discarding application:", e)

# ====== Apply Easy Apply ======
def apply_easy_apply(driver, idx):
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button")
        if "Easy Apply" not in btn.text:
            print(f"[{idx}] No Easy Apply")
            return False
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)
    except NoSuchElementException:
        print(f"[{idx}] Easy Apply button not found")
        return False

    try:
        primary = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.artdeco-button--primary"))
        )
        text = primary.text.strip()
        print(f"[{idx}] Modal button: {text}")

        if text in ["Submit application", "Apply now"]:
            driver.execute_script("arguments[0].click();", primary)
            print(f"[{idx}]  Application submitted")
        else:
            print(f"[{idx}]  Not direct submit, discarding.")
            discard_application(driver)

    except TimeoutException:
        print(f"[{idx}]  No modal button found, discarding.")
        discard_application(driver)

    time.sleep(2)
    return True

# ====== Loop Through Job Cards ======
def apply_to_listings(driver, max_per_page=None):
    cards = driver.find_elements(By.XPATH, "//*[contains(@class,'job-card-container--clickable')]")
    print(f"Found {len(cards)} jobs on page")
    for idx, card in enumerate(cards if max_per_page is None else cards[:max_per_page], start=1):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", card)
            time.sleep(2)
        except (ElementClickInterceptedException, Exception) as e:
            print(f"[{idx}] Failed clicking card: {e}")
            continue
        apply_easy_apply(driver, idx)

# ====== Next Page ======
def go_next_page(driver):
    try:
        # Locate the "Next" button
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'jobs-search-pagination__button--next') and not(@disabled)]"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        print(" Moving to next page...")

        # Wait for job cards on the new page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'job-card-container--clickable')]"))
        )
        time.sleep(2)
        return True
    except TimeoutException:
        print(" No next page available.")
        return False
    except Exception as e:
        print(" Error moving to next page:", e)
        return False


def main(username, password, keywords, location):
    print(" Starting LinkedIn Job Automation Script...")
    driver = init_driver()
    try:
        print("Logging into LinkedIn...")
        linkedin_login(driver, username, password)

        print(f"Searching jobs: {keywords} in {location}")
        search_jobs(driver, keywords, location)

        page = 1
        while True:
            print(f"\n===  Processing Page {page} ===")
            load_job_cards(driver)
            apply_to_listings(driver)

            if not go_next_page(driver):
                print(" All pages processed. Job automation finished.")
                break
            page += 1

    finally:
        input("Enter to terminate the browser")
        driver.quit()
        print(" Browser closed. Program finished.")


if __name__ == "__main__":
    with open("../config.json") as config_file:
        data = json.load(config_file)
    main(data['email'],data['password'],data['keywords'],data['location'])
    
    
