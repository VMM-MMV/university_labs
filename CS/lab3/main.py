import streamlit as st
import time
from vigenere import (
    romanian_alphabet,
    yield_encrypt,
    yield_decrypt,
    validate_romanian_text,
    format_string
)

st.set_page_config(
    page_title="Cifrul românesc",
    page_icon="🔒"
)

st.title("Cifrul românesc")
st.write("Criptare și decriptare în timp real folosind alfabetul românesc")

# Session state initialization
if 'animation_speed' not in st.session_state:
    st.session_state.animation_speed = 0.1

# Input fields
col1, col2 = st.columns(2)
with col1:
    operation = st.radio(
        "Selectați operația:",
        ["Criptare", "Decriptare"]
)

with col2:
    animation_speed = st.slider(
        "Viteza animației (secunde):",
        min_value=0.0,
        max_value=0.5,
        value=0.1,
        step=0.1
    )

message = st.text_area(
    "Introduceți textul:",
    help="Folosiți doar caractere din alfabetul românesc"
)

key = st.text_input(
    "Introduceți cheia:",
    help="Cheia trebuie să aibă minimum 7 caractere și să conțină doar caractere din alfabetul românesc"
)

# Create a placeholder for the animation
result_placeholder = st.empty()
status_placeholder = st.empty()

if st.button("Procesează"):
    if not message or not key:
        st.error("Vă rugăm să completați toate câmpurile!")
    elif len(format_string(key)) < 7:
        st.error("Cheia trebuie să aibă minimum 7 caractere!")
    elif not validate_romanian_text(message):
        st.error(f"Textul conține caractere invalide! Folosiți doar următoarele caractere: {' '.join(romanian_alphabet)}")
    elif not validate_romanian_text(key):
        st.error(f"Cheia conține caractere invalide! Folosiți doar următoarele caractere: {' '.join(romanian_alphabet)}")
    else:
        try:
            # Initialize progress bar
            progress_bar = st.progress(0)
            formatted_message = format_string(message)
            total_steps = len(formatted_message)
            
            if operation == "Criptare":
                generator = yield_encrypt(message, key)
                operation_text = "criptat"
            else:
                generator = yield_decrypt(message, key)
                operation_text = "decriptat"
            
            # Show the animation
            for i, result in enumerate(generator, 1):
                # Update progress
                progress = i / total_steps
                progress_bar.progress(progress)
                
                # Display current state
                result_placeholder.markdown(f"""
                ### Rezultat în timp real:
                ```
                {result}
                ```
                """)
                
                # Display status
                status_placeholder.write(f"Caractere procesate: {i}/{total_steps}")
                
                # Add delay for animation
                time.sleep(animation_speed)
            
            # Final success message
            st.success(f"Text {operation_text} cu succes!")
            
        except Exception as e:
            st.error(f"A apărut o eroare: {str(e)}")

# Display help information
with st.expander("Informații despre utilizare"):
    st.write("""
    ### Instrucțiuni:
    1. Selectați operația dorită (criptare sau decriptare)
    2. Introduceți textul de procesat
    3. Introduceți cheia (minimum 7 caractere)
    4. Ajustați viteza animației după preferință
    5. Apăsați butonul 'Procesează'
    
    ### Cerințe:
    - Textul și cheia trebuie să conțină doar caractere din alfabetul românesc
    - Cheia trebuie să aibă minimum 7 caractere
    - Spațiile și caracterele speciale vor fi eliminate
    - Toate literele vor fi convertite la majuscule
    """)
    
    st.write("### Alfabetul românesc disponibil:")
    st.write(" ".join(romanian_alphabet))