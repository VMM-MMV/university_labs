import streamlit as st
import sys
import os
import random

# Add the directory containing the original script to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the DES encryption functions
from main import encrypt, decrypt, getBs

def pretty_bits(binary_string, group_size=8):
    padded_binary = binary_string.ljust((len(binary_string) + group_size - 1) // group_size * group_size, '0')
    spaced_binary = ' '.join(padded_binary[i:i+group_size] for i in range(0, len(padded_binary), group_size))
    return spaced_binary

# Function to generate fake input with 1's and 0's
def generate_fake_input():
    # Generate random string of 32 characters (only '1' or '0') for R
    R = ''.join(random.choices('01', k=32))
    # Generate random string of 48 characters (only '1' or '0') for K
    K = ''.join(random.choices('01', k=48))
    return R, K

# Streamlit app UI
def app():
    # Title
    st.title("DES Encryption, Decryption & Generate B's")

    # Create tabs for "Analysis" and "Decryption"
    tabs = st.tabs(["DES Encryption & Decryption", "Generate B's"])

    # Encryption & Decryption Tab
    with tabs[0]:
        st.header("DES Encryption and Decryption Tool")

        # Encryption Section
        st.subheader("Encryption")
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
        st.subheader("Decryption")
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

    # Generate B's Tab
    with tabs[1]:
        st.header("Generate B's")

        # Check if session state exists for R and K, otherwise initialize
        if 'fake_R' not in st.session_state:
            st.session_state.fake_R = ""
        if 'fake_K' not in st.session_state:
            st.session_state.fake_K = ""

        # Button to generate fake input
        if st.button("Generate Fake Inputs"):
            # Generate fake input for R and K and store in session state
            st.session_state.fake_R, st.session_state.fake_K = generate_fake_input()

        # Input boxes for R and K with session state values
        R = st.text_input("Enter 32 characters for R:", max_chars=32, value=st.session_state.fake_R)
        K = st.text_input("Enter 48 characters for K:", max_chars=48, value=st.session_state.fake_K)

        # Button to generate B
        if st.button("Generate B's"):
            if len(R) == 32 and len(K) == 48:
                # Placeholder for the logic to generate B's, for example:
                B = getBs(R, K)  # Here you can add your specific logic
                pretty_B = pretty_bits(B)
                st.write(f"Generated B's: {pretty_B}")
            else:
                st.error("R must be 32 characters and K must be 48 characters, containing only '1' and '0'.")

# Run the app
if __name__ == "__main__":
    app()
