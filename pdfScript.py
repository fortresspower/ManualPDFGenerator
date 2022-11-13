from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import streamlit as st
import os


#--------------------------------------------------------------------------------------------------------------------------
# Setup
#--------------------------------------------------------------------------------------------------------------------------

dictionary={} #stores all html files
counter = 0.0 #stores number of html files not in subdirectory
empty_html = '<html><head></head><body></body></html>' #append html here to merge files
num = 0 #used to provide a sortable key to the dictionary

def readHTML(html, path) :
    #Extract file number from html page
    soup = BeautifulSoup(html, features="html.parser")
    html = html.decode("utf-8")
    #fix image references if file path for them is provided
    if path != "":
        if path[-1] == '/': #Remove trailing slash
            path = path[:-1]

        for img in soup.findAll('img'):
            html = html.replace(img.get('src'), path + "/inline-images" + img.get('src').split("/inline-images", 1)[1])

    #cleanup uneccesary parsed content
    for script in soup(["script", "style"]):
        script.extract() 

    #Gets the header decimal number for each file after its been parsed and cleaned
    potentialNum = soup.get_text().replace('\n', '')[:3]
    if potentialNum.replace('.', '').isnumeric():
        num = float(soup.get_text().replace('\n', '')[:3])
    else:
        num = counter + 0.01

    #Update dictionary with appropriate key and decoded html content
    dictionary.update({num: html})


st.set_page_config(
                    page_title="Manual PDF Generator - FP",
                    page_icon=":arrow_up:"
)

# Show Fortress Logo
# header_image_html = "<img src='fortress_logo.png' class='img-fluid' width='50%'>"
# st.markdown(header_image_html, unsafe_allow_html=True)

st.title('Zoho Learn Manual PDF Generator')

# Instructions
with st.expander("Instructions"):
     st.markdown(""
     "First upload the unzipped html export folder of the manual you dowload from zoho learn.  \n"
     "Next if you want the images to be conserved in the output, input the path to the inline images folder of the manual. Note the folder needs to be in your PCs downloads folder  \n"
    "Ex for the eFlex manual download if you unzipped the following:  \n"
     "Product-Manual---eFlex-5.4-10-04-2022-09_52/eflex-5-4-manual/inline-images  \n"
     "Copy into the input the path above the inline-images folder. Here this is:  \n" 
     "Product-Manual---eFlex-5.4-10-04-2022-09_52/eflex-5-4-manual"
     "")

# path input

file_path = st.text_input("Optionally input file path for images")

# if file_path:
# file uploader
st.header('Upload folder of manual templates')
uploaded_file = st.file_uploader("Choose a file", type= ["dir", "png", "html"], accept_multiple_files=True)
if uploaded_file:
#print(uploaded_file)
    for file in uploaded_file:
        if file.type == "text/html":
            print("RUNNING")
            readHTML(file.read(), file_path)

    #Sort dictionary based on keys which are header section decimals
    #Iterate over sorted dictionary merging html
    #print(sorted(dictionary.items(), key=lambda x:x[0]))
    for key, value in sorted(dictionary.items(), key=lambda x:x[0]):
        empty_html = empty_html.replace('</body></html>', value + '</body></html>')

    # save merged html to disc
    with open('merged.html', 'w', encoding="utf-8") as f:
        f.write(empty_html)

    with open('merged.html', 'r', encoding="utf-8") as f:
        st.download_button('Download HTML Report', f, file_name="mergedReport.html")



