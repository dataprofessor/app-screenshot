import streamlit as st
import time
import psutil
import os
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from os.path import exists

st.set_page_config(page_title="🎈 App Screenshot")
st.title('🎈 App Screenshot')
st.warning('An app for taking screenshot of a Streamlit app.')

#@st.cache_resource
def get_driver():
    options = webdriver.ChromeOptions()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(f"--window-size={width}x{height}")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    return webdriver.Chrome(service=service, options=options)

# Settings
with st.sidebar:
    st.header('⚙️ Settings')
    width = st.slider('Width', 426, 1920, 1000)
    height = st.slider('Height', 240, 1080, 540)

    # Getting % usage of virtual_memory ( 3rd field)
    ram_usage = psutil.virtual_memory()[2]
    st.caption(f'RAM used (%): {ram_usage}')

# Input URL
with st.form("my_form"):
    app_url = st.text_input('App URL', 'https://langchain-quickstart.streamlit.app').rstrip('/')
    app_name = app_url.replace('https://','').replace('.streamlit.app','')
    
    submitted = st.form_submit_button("Submit")
    if submitted:
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



def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    
    # Apply rounded corners only to the top
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    
    im.putalpha(alpha)
    return im



file_exists = exists('screenshot.png')
if file_exists:
    bg_img = Image.open('background/background-76.jpeg')
    app_img = Image.open('screenshot.png')

    st.write('bg_img (w/h):', bg_img.width, bg_img.height)
    st.write('app_img (w/h):', app_img.width, app_img.height)

    image_resize = 0.8
    new_width = int(app_img.width * image_resize)
    new_height = int(app_img.height * image_resize)
    resized_app_img = app_img.resize((new_width, new_height))

    resized_app_img = add_corners(resized_app_img, 50)
    bg_img.paste(resized_app_img, (0, 0), resized_app_img)
    bg_img.save('final.png')

    st.image(bg_img)

    #with Image.open('final.png') as image:
    #    st.image(image)
        
    with open("final.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"{app_name}.png",
            mime="image/png"
            )
        if btn:
            os.remove('screenshot.png')



