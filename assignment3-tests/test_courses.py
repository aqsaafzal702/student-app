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
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def login(driver):
    driver.get(f"{APP_URL}/auth/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASS)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/students") or EC.url_contains("/courses"))

# TC1: Courses page loads after login
def test_courses_page_loads():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/courses")
        assert "Course" in driver.title or "Course" in driver.page_source
        print("✅ TC1 PASSED: Courses page loaded successfully")
        return True
    except Exception as e:
        print(f"❌ TC1 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC2: Add Course button exists
def test_add_course_button_exists():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/courses")
        add_btn = driver.find_element(By.XPATH, "//a[contains(@href, '/courses/add')]")
        assert add_btn is not None and ("Add" in add_btn.text or "+" in add_btn.text)
        print("✅ TC2 PASSED: Add Course button visible")
        return True
    except Exception as e:
        print(f"❌ TC2 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC6: Unauthorized user cannot view courses (redirect to login)
def test_courses_unauthenticated_redirect():
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/courses")
        WebDriverWait(driver, 10).until(EC.url_contains("/auth/login"))
        print("✅ TC3 PASSED: Unauthorized access redirected to login")
        return True
    except Exception as e:
        print(f"❌ TC6 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC7: Courses list shows table with expected columns
def test_courses_list_columns():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/courses")
        # Table columns like: ID, Name, (maybe others)
        page = driver.page_source.lower()
        assert "id" in page and ("name" in page or "title" in page)
        print("✅ TC4 PASSED: Courses list shows expected columns")
        return True
    except Exception as e:
        print(f"❌ TC7 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    tests = [
        test_courses_page_loads,
        test_add_course_button_exists,
        test_courses_unauthenticated_redirect,
        test_courses_list_columns
    ]
    results = []
    for t in tests:
        results.append(t())
    print(f"\nRESULTS: {sum(results)}/4 course test cases passed")
