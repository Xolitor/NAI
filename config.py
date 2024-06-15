import streamlit as st

def set_page_config():
    st.set_page_config(page_title="NAI", page_icon=":books:", layout="wide")

def set_custom_styles():
    st.markdown("""
        <style>
            .main {
                background-color: #f0f2f6;
                color: #333;
            }
            .title {
                text-align: center;
                color: #4a90e2;
                margin-bottom: 20px;
            }
            .stTabs [data-baseweb="tab-list"] button {
                font-size: 18px;
                background-color: #f0f2f6;
                border: none;
                color: #4a90e2;
                border-bottom: 2px solid transparent;
                padding: 10px 20px;
                margin: 0;
            }
            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                border-bottom: 2px solid #4a90e2;
            }
            .stTabs [data-baseweb="tab-list"] button:hover {
                background-color: #e0e4e8;
            }
            .stTextInput div {
                margin-top: 10px;
                margin-bottom: 20px;
            }
            .stTextInput input {
                border: 2px solid #4a90e2;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            .stButton button {
                background-color: #4a90e2;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                margin-top: 10px;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #357ab7;
            }
            .stAlert div {
                border-radius: 5px;
            }
            .card {
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .card h4 {
                margin: 0 0 10px 0;
                color: #4a90e2;
            }
            .card p {
                margin: 0;
                color: #333;
            }
            @keyframes slideIn {
                from { transform: translateY(-20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            .slide-in {
                animation: slideIn 1s ease-out;
            }
        </style>
        """, unsafe_allow_html=True)
