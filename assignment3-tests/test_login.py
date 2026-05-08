# test_login.py - First 3 Test Cases

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome Options (Headless for EC2)
chrome_options = Options()
chrome_options.add_argument("--headless")  # No GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# App URL (Change with your EC2 IP)
APP_URL = "http://13.61.194.93:3001"  # Ya apna EC2 IP daal do

def get_driver():
    """Chrome driver setup"""
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

# TEST CASE 1: Login Page Load Hota Hai
def test_login_page_loads():
    """TC1: Verify login page loads successfully"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/auth/login")
        assert "Login" in driver.title or "Sign In" in driver.title
        print("✅ TC1 PASSED: Login page loaded successfully")
        return True
    except Exception as e:
        print(f"❌ TC1 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TEST CASE 2: Login Page Par Elements Dikh Rahe Hain
def test_login_page_elements():
    """TC2: Verify login form elements are present"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/auth/login")
        
        # Check email field
        email_field = driver.find_element(By.NAME, "email")
        assert email_field is not None
        
        # Check password field
        password_field = driver.find_element(By.NAME, "password")
        assert password_field is not None
        
        # Check submit button
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        assert submit_btn is not None
        
        print("✅ TC2 PASSED: All login form elements present")
        return True
    except Exception as e:
        print(f"❌ TC2 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# TEST CASE 3: Invalid Login Attempt
def test_invalid_login():
    """TC3: Verify login fails with invalid credentials"""
    driver = get_driver()
    try:
        driver.get(f"{APP_URL}/auth/login")
        
        # Enter invalid credentials
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("invalid@test.com")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("wrongpassword")
        
        # Submit form
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()
        
        # Wait for error message or stay on login page
        time.sleep(2)
        
        # Check if still on login page (login failed)
        assert "/login" in driver.current_url or "Login" in driver.title
        
        print("✅ TC3 PASSED: Invalid login correctly rejected")
        return True
    except Exception as e:
        print(f"❌ TC3 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

# Run Tests
if __name__ == "__main__":
    print("=" * 60)
    print("STUDENT APP - LOGIN TEST CASES")
    print("=" * 60)
    
    results = []
    results.append(test_login_page_loads())
    results.append(test_login_page_elements())
    results.append(test_invalid_login())
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
