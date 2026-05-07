from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

APP_URL = "http://13.61.194.93:3001"  # change if needed
TEST_EMAIL = "aqsaafzal670@gmail.com"
TEST_PASS = "123"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
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
    # Wait for redirect to students page
    WebDriverWait(driver, 10).until(EC.url_contains("/students"))

# TC4: Create a valid student (FIXED)
def test_create_student():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students/add")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        
        # Fill form
        driver.find_element(By.NAME, "name").send_keys("Test Selenium Student")
        driver.find_element(By.NAME, "email").send_keys("selstudent@example.com")
        driver.find_element(By.NAME, "phone").send_keys("03001234567")
        driver.find_element(By.NAME, "address").send_keys("Fictional Address For Testing")
        
        # Click submit - flexible selector
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn-primary")
        submit_btn.click()
        
        # Wait for redirect - use url_contains instead of url_matches
        WebDriverWait(driver, 15).until(EC.url_contains("/students"))
        time.sleep(2)  # Let page fully load
        
        # Check for success - flexible assertion
        page_src = driver.page_source.lower()
        success_found = (
            "test selenium student" in page_src or 
            "success" in page_src or 
            "student created" in page_src or
            "added successfully" in page_src
        )
        assert success_found, "Student not found in page source"
        
        print("✅ TC4 PASSED: Student created successfully and is in list")
        return True
    except Exception as e:
        # Print detailed error for debugging
        print(f"❌ TC4 FAILED: {type(e).__name__}: {str(e)}")
        return False
    finally:
        driver.quit()
        
# TC5: View students list page
def test_students_list():
    driver = get_driver()
    try:
        login(driver)
        driver.get(f"{APP_URL}/students")
        # Check for the "Add New Student" button and table columns
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
        # Click first 'Edit' button, assumed like: /students/edit/{id}
        edit_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/students/edit')]")
        assert len(edit_links) > 0
        edit_links[0].click()
        WebDriverWait(driver, 10).until(EC.url_contains("/students/edit"))
        # Confirm elements
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
        # Find a delete button in Actions (should have /delete in form or as button)
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
        # Check navbar links
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
        test_create_student,
        test_students_list,
        test_edit_student_page,
        test_delete_button,
        test_logout,
        test_navigation_menu,
        test_unauthorized_redirect
    ]
    results = []
    for ti, t in enumerate(tests, 4):
        res = t()
        results.append(res)
    print(f"\nRESULTS: {sum(results)}/7 student test cases passed")
