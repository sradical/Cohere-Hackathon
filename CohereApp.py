import streamlit as st

class CohereApp():
    def __init__(self):
        self.apps = []

    def add_app(self, title, func="nothing"):
        self.apps.append({"title":title, "function":func})

    def run(self):
        #app = st.sidebar.selectbox('', self.apps, format_func= lambda app: app['title'])
        app = self.apps
        #app["function"]