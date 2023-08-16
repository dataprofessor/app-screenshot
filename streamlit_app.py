import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

st.title('🎈 App Screenshot')

app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').rstrip('/')
app_name = app_url.replace('https://','').replace('.streamlit.app','')

st.write(app_url)
st.write(app_name)



@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument(f"--window-size=1290x550")

driver = get_driver()
driver.get("https://langchain-quickstart.streamlit.app/~/+/")

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

st.code(driver.page_source)



#with open("screenshot.png", "rb") as file:
#    btn = st.download_button(
#            label="Download image",
#            data=file,
#            file_name=f"{app_name}.png",
#            mime="image/png"
#          )
