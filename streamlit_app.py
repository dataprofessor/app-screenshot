import streamlit as st
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

st.set_page_config(page_title="🎈 App Screenshot")
st.title('🎈 App Screenshot')
st.write('An app for taking screenshot of a Streamlit app.')

app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').rstrip('/')
app_name = app_url.replace('https://','').replace('.streamlit.app','')

# Settings

with st.sidebar:
    st.header('⚙️ Settings')
    width = st.slider('Width', 426, 3840, 1000)
    height = st.slider('Height', 240, 2160, 540)

@st.cache_resource
def get_driver():
    #options = Options()
    options = webdriver.ChromeOptions()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    #options.add_argument(f"--window-size=1290x550")
    ## options.add_argument(f"--window-size=1100x550")
    options.add_argument(f"--window-size={width}x{height}")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    #return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return webdriver.Chrome(service=service, options=options)

if app_url:
    driver = get_driver()
    driver.get(f"{app_url}/~/+/")
    
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
    
    #st.code(driver.page_source)
    
    
    with Image.open('screenshot.png') as image:
        st.image(image)
    
    with open("screenshot.png", "rb") as file:
        btn = st.download_button(
                label="Download image",
                data=file,
                file_name=f"{app_name}.png",
                mime="image/png"
              )
