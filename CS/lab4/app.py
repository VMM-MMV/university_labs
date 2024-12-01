import streamlit as st
import sys
import os

# Add the directory containing the original script to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the DES encryption functions
from main import encrypt, decrypt

def main():
    st.title("DES Encryption and Decryption Tool")
    
    # Encryption Section
    st.header("Encryption")
    message = st.text_area("Enter message to encrypt:", height=100)
    encryption_key = st.text_input("Enter encryption key:")
    
    if st.button("Encrypt"):
        if message and encryption_key:
            try:
                encrypted_message = encrypt(message, encryption_key)
                st.success("Encryption successful!")
                st.text_area("Encrypted Message (Binary):", value=encrypted_message, height=100)
            except Exception as e:
                st.error(f"Encryption failed: {str(e)}")
        else:
            st.warning("Please enter both message and key")
    
    # Decryption Section
    st.header("Decryption")
    encrypted_input = st.text_area("Enter encrypted message (binary):", height=100)
    decryption_key = st.text_input("Enter decryption key:")
    
    if st.button("Decrypt"):
        if encrypted_input and decryption_key:
            try:
                decrypted_message = decrypt(encrypted_input, decryption_key)
                st.success("Decryption successful!")
                st.text_area("Decrypted Message:", value=decrypted_message, height=100)
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")
        else:
            st.warning("Please enter both encrypted message and key")
    
    # Additional Information
    st.sidebar.header("About DES Encryption")
    st.sidebar.info("""
    DES (Data Encryption Standard) is a symmetric-key block cipher 
    that uses a 64-bit key to encrypt 64-bit blocks of data.
    
    Key Features:
    - Symmetric encryption (same key for encryption and decryption)
    - Block cipher with 64-bit block size
    - Involves multiple rounds of permutation and substitution
    """)

if __name__ == "__main__":
    main()
