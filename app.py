import streamlit as st
import googletrans

from googletrans import Translator
from CohereApp import CohereApp
from apps.hackcohere import Semantic_Search

def header(url):  
    st.markdown(f'<p style="color:#0066cc;font-size:30px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def text(url):  
    st.markdown(f'<p style="font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)
    
def subtext(url):  
    st.markdown(f'<p style="font-size:20px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def main():
    
    st.set_page_config(layout="wide")    
    
    translator = Translator()    
    header_text = translator.translate('UK Ukrainian Refugee Information Search', src='en', dest='uk')
    
    header(header_text.text)
    header("UK Ukrainian Refugee Information Search 🔍")
    
    with st.form("query_form"):
        query = translator.translate("Input your question in Ukrainian", src='en', dest='uk')        
        text(query.text+ '    ' + '( ' + query.origin + ' ) ')
        subtext("приклад (Examples):" + "  " + "  " + "отримання медичної допомоги (Getting healthcare)" + ';' + '  ' + "банківський рахунок (Getting bank account)" + ';' + '  ' + "догляд за дітьми (childcare)")
                
        query_text = st.text_input(" ", " ")   
        submit_button = st.form_submit_button("Submit (Надіслати)")

    app = CohereApp()
    if query_text or submit_button:
        app.add_app("Search", Semantic_Search(query_text))
        app.run()
        

if __name__ == "__main__":
    main()