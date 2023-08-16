import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

st.title('🎈 App Screenshot')

app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').strip('/')
app_name = app_url.lstrip('https://').rstrip('.streamlit.app')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f"--window-size=1290x550")

# User agent string for Chrome on Mac OSX
#mac_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
#options.add_argument(f"user-agent={mac_user_agent}")

with webdriver.Chrome(options=options) as driver:
    driver.get(f'{app_url}/~/+/')

    time.sleep(10)
    
    # Explicitly wait for an essential element to ensure content is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Get scroll height and width
    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')

    # Set window size
    driver.set_window_size(scroll_width, scroll_height)

    # Now, capture the screenshot
    driver.save_screenshot('screenshot.png')



with open("screenshot.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"{app_name}.png",
            mime="image/png"
          )
