import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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

driver = get_driver()
driver.get("https://langchain-quickstart.streamlit.app/~/+/")

st.code(driver.page_source)



#with open("screenshot.png", "rb") as file:
#    btn = st.download_button(
#            label="Download image",
#            data=file,
#            file_name=f"{app_name}.png",
#            mime="image/png"
#          )
