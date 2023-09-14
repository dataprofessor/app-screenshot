#import streamlit as st
#import time
#from PIL import Image
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.support.ui import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

import streamlit as st
import time
import psutil
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

st.set_page_config(page_title="🎈 App Screenshot")
st.title('🎈 App Screenshot')
st.warning('An app for taking screenshot of a Streamlit app.')

# Getting % usage of virtual_memory ( 3rd field)
st.caption(f'RAM memory % used: {psutil.virtual_memory()[2]}')
# Getting usage of virtual_memory in GB ( 4th field)
st.caption(f'RAM Used (GB): {psutil.virtual_memory()[3]/1000000000}')


# Input URL
app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').rstrip('/')
app_name = app_url.replace('https://','').replace('.streamlit.app','')
st.divider()

# Settings
with st.sidebar:
    st.header('⚙️ Settings')
    width = st.slider('Width', 426, 3840, 1000)
    height = st.slider('Height', 240, 2160, 540)

@st.cache_resource
def get_driver():
    options = webdriver.ChromeOptions()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(f"--window-size={width}x{height}")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    return webdriver.Chrome(service=service, options=options)

if app_url:
    driver = get_driver()
    if app_url.endswith('streamlit.app'):
        driver.get(f"{app_url}/~/+/")
    else:
        driver.get(app_url)
    
    time.sleep(2)
        
    # Explicitly wait for an essential element to ensure content is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Get scroll height and width
    #scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    #scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    
    # Set window size
    #driver.set_window_size(scroll_width, scroll_height)
    
    # Now, capture the screenshot
    driver.save_screenshot('screenshot.png')
    
    with Image.open('screenshot.png') as image:
        st.image(image)
    
    with open("screenshot.png", "rb") as file:
        btn = st.download_button(
                label="Download image",
                data=file,
                file_name=f"{app_name}.png",
                mime="image/png"
              )
        if btn:
            st.cache_resource.clear()
