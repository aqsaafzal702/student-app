from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

APP_URL = "http://13.61.194.93:3001"
TEST_EMAIL = "aqsaafzal670@gmail.com"
TEST_PASS = "123"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = "/usr/bin/chromium"

def get_driver():
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
    
def login(driver):
    driver.get(f"{APP_URL}/auth/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASS)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, 15).until(EC.url_contains("/students"))
    time.sleep(2)

# TC5: View students list page
def test_students_list():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        assert "+ Add New Student" in driver.page_source
        assert "Student Name" in driver.page_source or "Name" in driver.page_source
        print("✅ TC5 PASSED: Students list loaded and visible")
        return True
    except Exception as e:
        print(f"❌ TC5 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC6: Edit student page loads
def test_edit_student_page():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        time.sleep(1)
        edit_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/students/edit')]")
        assert len(edit_links) > 0
        edit_links[0].click()
        WebDriverWait(driver, 10).until(EC.url_contains("/students/edit"))
        assert "Edit Student" in driver.page_source
        print("✅ TC6 PASSED: Edit student page loads with form")
        return True
    except Exception as e:
        print(f"❌ TC6 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC7: Delete button exists
def test_delete_button():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        delete_buttons = driver.find_elements(By.XPATH, "//form[contains(@action, '/delete') or contains(@action, '/students/delete')]//button")
        assert len(delete_buttons) > 0
        print("✅ TC7 PASSED: Delete button found for at least one student")
        return True
    except Exception as e:
        print(f"❌ TC7 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC8: Logout functionality
def test_logout():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        logout_link = driver.find_element(By.XPATH, "//a[contains(@href, '/auth/logout')]")
        logout_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/auth/login"))
        print("✅ TC8 PASSED: Logout redirects to login page")
        return True
    except Exception as e:
        print(f"❌ TC8 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC9: Navigation menu
def test_navigation_menu():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        nav = driver.find_element(By.TAG_NAME, "nav")
        assert "Logout" in nav.text and "Students" in nav.text
        print("✅ TC9 PASSED: Navigation menu shows correct links after login")
        return True
    except Exception as e:
        print(f"❌ TC9 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TC10: Unauthorized users are redirected to login
def test_unauthorized_redirect():
    driver = get_driver()
    try:
        driver.delete_all_cookies()
        driver.get(f"{APP_URL}/students")
        WebDriverWait(driver, 10).until(EC.url_contains("/auth/login"))
        print("✅ TC10 PASSED: Unauthorized access redirected to login page")
        return True
    except Exception as e:
        print(f"❌ TC10 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    tests = [
        test_students_list,
        test_edit_student_page,
        test_delete_button,
        test_logout,
        test_navigation_menu,
        test_unauthorized_redirect
    ]
    results = []
    for t in tests:
        res = t()
        results.append(res)
    
    passed = sum(results)
    total = len(results)
    print(f"\nRESULTS: {passed}/{total} student test cases passed")
    
    # ✅ EXIT CODE FOR JENKINS
    if passed < total:
        print(f"❌ {total - passed} test(s) FAILED - Exiting with error code 1")
        sys.exit(1)
    else:
        print("✅ All student tests PASSED")
        sys.exit(0)
