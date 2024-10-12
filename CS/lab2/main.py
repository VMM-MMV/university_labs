import streamlit as st
import pandas as pd
from collections import Counter

def count_characters(text):
    # Convert text to lowercase and count characters
    char_counts = Counter(text.lower())
    
    # Create a dictionary with all letters from a to z
    all_chars = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}
    
    # Update the dictionary with the actual counts
    all_chars.update(char_counts)
    
    # Remove non-alphabetic characters
    all_chars = {k: v for k, v in all_chars.items() if k.isalpha()}
    
    return all_chars

def main():
    st.title("Character Frequency Counter")
    
    user_input = st.text_area("Enter your text here:", height=200)
    
    if st.button("Analyze"):
        if user_input:
            with st.spinner("Loading..."):
                char_counts = count_characters(user_input)
                
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
