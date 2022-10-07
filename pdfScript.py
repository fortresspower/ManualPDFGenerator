# Plotly, Pandas, and Steamlight Imports
#--------------------------------------------------------------------------------------------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from pandas.io.pytables import Table
import streamlit as st

#--------------------------------------------------------------------------------------------------------------------------
# Setup
#--------------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame() # dataframe for the Panda CSV import

# Main
#--------------------------------------------------------------------------------------------------------------------------
#icon emojis https://webfx.com/tools/emoji-cheat-sheet
st.set_page_config(
                    page_title="BMS File Combiner - FP",
                    page_icon=":arrow_down:"
)

# Show Fortress Logo
# header_image_html = "<img src='fortress_logo.png' class='img-fluid' width='50%'>"
# st.markdown(header_image_html, unsafe_allow_html=True)

st.title('BMS Data File Combiner')

# Instructions
with st.expander("Instructions"):
     st.markdown("""First upload a CSV file containing individul recorded data files from the BMS software, then provide a title and sampling rate (default is to keep all rows)
     """)

# file uploader
st.header('Upload folder of manual templates')
uploaded_files = st.file_uploader("Choose a file", type= ["dir"], accept_multiple_files=False)

uploaded_files = None
#If battery isn't eflex ask for serial number before allowing file upload
if batt_type != 'eFlex':
    serial_num = st.text_input("Enter your battery serial number: ")
    software_version = st.text_input("Enter your battery software version: ")
    if serial_num and software_version: #make sure serial num and software version are filled
        if batt_type == 'eVault Max': #if eVault Max accept single csv upload
            uploaded_files = st.file_uploader("Choose a file", type= ["csv"], accept_multiple_files=False)
        else: #if eVault Classic accept single xls upload
            uploaded_files = st.file_uploader("Choose a file", type = ["xls","xlsx"], accept_multiple_files=False)
else: #if eflex accept multiple csv files
    uploaded_files = st.file_uploader("Choose a file", type= ["csv"], accept_multiple_files=True)