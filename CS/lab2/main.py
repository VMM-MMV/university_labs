import streamlit as st
import pandas as pd
from freq_manager import get_alphabetically_counted

def main():
    st.title("Character Frequency Counter")
    
    user_input = st.text_area("Enter your text here:", height=200)
    
    if st.button("Analyze"):
        if user_input:
            with st.spinner("Loading..."):
                char_counts = get_alphabetically_counted(user_input)
                
                df = pd.DataFrame.from_dict(char_counts, orient='index', columns=['Frequency'])
                df.index.name = 'Character'
                df = df.reset_index()
                
                # Transpose the dataframe for table display
                df_transposed = df.set_index('Character').transpose()
                
                # Display the table
                st.table(df_transposed)
                
                # Plot the frequencies
                st.bar_chart(df.set_index('Character'))
            
if __name__ == "__main__":
    main()
