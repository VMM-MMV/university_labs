import streamlit as st
import pandas as pd
import plotly.express as px
from freq_manager import get_alphabetically_counted
from decrypter import decrypt
import time

def load_css():
    st.markdown("""
        <style>
        .stAlert > div {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        .stSpinner > div {
            text-align: center;
            color: #0066cc;
        }
        .decryption-area {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background-color: #f9f9f9;
            font-family: monospace;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            border-radius: 4px 4px 0px 0px;
            border-right: 1px solid #f0f2f6;
            border-left: 1px solid #f0f2f6;
            border-top: 1px solid #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)

def display_frequency_analysis(char_counts):
    # Convert character counts to a DataFrame
    df = pd.DataFrame.from_dict(char_counts, orient='index', columns=['Frequency'])
    df.index.name = 'Character'
    df = df.reset_index()
    
    # Transpose the dataframe for better table display
    df_transposed = df.set_index('Character').transpose()
    st.subheader("Frequency Table")
    st.table(df_transposed)
    
    # Plotting the character frequency distribution
    fig = px.bar(df, x='Character', y='Frequency', title='Character Frequency Distribution')
    st.plotly_chart(fig)

def decrypt_text_real_time(user_input, progress_bar):
    decryption_area = st.empty()
    status_text = st.empty()
    
    decryption_generator = decrypt(user_input)
    total_steps = 26  # Assuming 26 steps for 26 letters
    
    for i, text in enumerate(decryption_generator):
        progress = min((i + 1) / total_steps, 1.0)
        progress_bar.progress(progress)
        
        decryption_area.markdown(f"<div class='decryption-area'>{text}</div>", unsafe_allow_html=True)
    
    status_text.empty()
    st.toast("Decryption complete!", icon="🎉")

def analysis_tab():
    st.header("Text Analysis")
    user_input = st.text_area("Enter your text here:", height=200, key="analysis_input")
    
    if st.button("Analyze Frequency"):
        if user_input:
            with st.spinner("Analyzing..."):
                try:
                    progress_bar = st.progress(0)
                    char_counts = get_alphabetically_counted(user_input)
                    progress_bar.progress(50)
                    display_frequency_analysis(char_counts)
                    st.session_state.analysis_result = char_counts
                    progress_bar.progress(100)
                    time.sleep(0.2)
                    st.toast("Analysis complete!", icon="📊")
                except Exception as e:
                    st.toast(f"An error occurred during analysis: {str(e)}", icon="❌")
                finally:
                    progress_bar.empty()
        else:
            st.toast("Please enter some text to analyze.", icon="ℹ️")

def decryption_tab():
    st.header("Text Decryption")
    user_input = st.text_area("Enter your text here:", height=200, key="decryption_input")
    
    if st.button("Decrypt"):
        if user_input:
            try:
                progress_bar = st.progress(0)
                st.subheader("Decryption Progress:")
                decrypt_text_real_time(user_input, progress_bar)
                st.session_state.decryption_complete = True

            except Exception as e:
                st.toast(f"An error occurred during decryption: {str(e)}", icon="❌")
            finally:
                progress_bar.empty()
        else:
            st.toast("Please enter some text to decrypt.", icon="ℹ️")

def main():
    st.set_page_config(page_title="Text Analyzer", layout="wide")
    load_css()
    
    st.title("Text Analyzer: Frequency Counter and Decrypter")
    
    tabs = st.tabs(["Analysis", "Decryption"])
    
    with tabs[0]:
        analysis_tab()
    
    with tabs[1]:
        decryption_tab()

if __name__ == "__main__":
    main()