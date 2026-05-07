from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

APP_URL = "http://13.61.194.93:3001"
TEST_EMAIL = "aqsaafzal670@gmail.com"
TEST_PASS = "123"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

def get_driver():
    from selenium.webdriver.chrome.service import Service
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.binary_location = "/usr/bin/chromium"
    
    #  DIRECT SYSTEM CHROMEDRIVER 
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login(driver):
    driver.get(f"{APP_URL}/auth/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASS)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/students"))

# TC11: Empty form validation (Add Student)
def test_empty_form_validation():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students/add")
        driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'Add Student')]").click()
        # Should stay on same page and show error/validation
        time.sleep(1)
        alert = driver.find_elements(By.CLASS_NAME, "alert-danger")
        assert len(alert) > 0 or "required" in driver.page_source or "Error" in driver.page_source
        print("✅ TC11 PASSED: Empty student form shows validation error")
        return True
    except Exception as e:
        print(f"❌ TC11 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC12: Courses page loads
def test_courses_page():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/courses")
        assert "Course" in driver.title or "Courses" in driver.page_source
        print("✅ TC12 PASSED: Courses page loads")
        return True
    except Exception as e:
        print(f"❌ TC12 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC13: Page titles
def test_page_titles():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students/add")
        assert "Add Student" in driver.title
        driver.get(f"{APP_URL}/students")
        assert "Student" in driver.title or "Student" in driver.page_source
        print("✅ TC13 PASSED: Page titles verified")
        return True
    except Exception as e:
        print(f"❌ TC13 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC14: Flash messages after actions
def test_flash_messages():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students/add")
        # Submit empty for error (should show alert)
        driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'Add Student')]").click()
        time.sleep(1)
        error_flash = driver.find_elements(By.CLASS_NAME, "alert-danger")
        assert len(error_flash) > 0
        # Now submit with valid to get success alert
        driver.find_element(By.NAME, "name").send_keys("Flash Test Student")
        driver.find_element(By.NAME, "email").send_keys("flashtest@example.com")
        driver.find_element(By.NAME, "phone").send_keys("03121231234")
        driver.find_element(By.NAME, "address").send_keys("Flash Address")
        driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'Add Student')]").click()
        time.sleep(1)
        success_flash = driver.find_elements(By.CLASS_NAME, "alert-success")
        assert len(success_flash) > 0
        print("✅ TC14 PASSED: Flash messages work")
        return True
    except Exception as e:
        print(f"❌ TC14 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC15: Back button works on student add/edit
def test_back_button():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students/add")
        # There should be a "Back to Students" button (← Back to Students)
        back = driver.find_element(By.XPATH, "//a[contains(text(),'Back to Students')]")
        back.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/students"))
        print("✅ TC15 PASSED: Back button on add student works")
        return True
    except Exception as e:
        print(f"❌ TC15 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    results = []
    results.append(test_empty_form_validation())
    results.append(test_courses_page())
    results.append(test_page_titles())
    results.append(test_flash_messages())
    results.append(test_back_button())
    print(f"\nRESULTS: {sum(results)}/5 additional test cases passed")
