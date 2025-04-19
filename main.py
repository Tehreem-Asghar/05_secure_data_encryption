import streamlit as st
from session_state import get_session, save_to_file
from utils import encrypt_data, decrypt_data, hash_passkey

# Initialize session
get_session()

# App Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 Secure Data Vault</h1>", unsafe_allow_html=True)
st.write("### Protect your sensitive text using encryption and passkeys.")

# Sidebar Navigation
menu = st.sidebar.radio("📂 Menu", ["🏠 Home", "📝 Insert Data", "🔓 Retrieve Data", "🔐 Login"])

# Home Page
if menu == "🏠 Home":
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
    st.markdown("### 👋 Welcome to your **Secure Data Vault!**")
    st.info("You can store encrypted data using a passkey and retrieve it securely.")

# Insert Data Page
elif menu == "📝 Insert Data":
    st.subheader("🔒 Store Secret Message")
    with st.expander("📥 Enter Data"):
        text = st.text_area("Enter your secret message here:")
        passkey = st.text_input("🔑 Create a passkey:", type="password")

        if st.button("📌 Store Securely"):
            if text and passkey:
                encrypted = encrypt_data(text)
                passkey_hash = hash_passkey(passkey)

                entry_id = f"data_{len(st.session_state.data_store) + 1}"
                st.session_state.data_store[entry_id] = {
                    "encrypted": encrypted,
                    "passkey_hash": passkey_hash
                }

                save_to_file()
                st.success("✅ Your data has been securely stored!")
                st.balloons()
            else:
                st.error("⚠️ Please enter both text and passkey.")

# Retrieve Data Page
elif menu == "🔓 Retrieve Data":
    st.subheader("🔍 Retrieve & Decrypt Data")
    if st.session_state.data_store:
        selected_id = st.selectbox("📁 Select data entry:", list(st.session_state.data_store.keys()))
        passkey = st.text_input("🔑 Enter your passkey:", type="password")

        if st.button("🔓 Decrypt"):
            stored = st.session_state.data_store[selected_id]
            entered_hash = hash_passkey(passkey)

            if entered_hash == stored["passkey_hash"]:
                decrypted = decrypt_data(stored["encrypted"])
                st.success("✅ Decryption Successful!")
                st.code(decrypted, language='text')
                st.session_state.attempts = 0
            else:
                st.session_state.attempts += 1
                st.error(f"❌ Incorrect passkey! Attempt {st.session_state.attempts}/3")

                if st.session_state.attempts >= 3:
                    st.session_state.authorized = False
                    st.warning("🚫 Too many failed attempts. Redirect to login.")
    else:
        st.warning("⚠️ No data found. Please insert something first.")

# Login Page
elif menu == "🔐 Login":
    st.subheader("🔑 Login to Reauthorize")
    if not st.session_state.authorized:
        username = st.text_input("👤 Username (admin)")
        password = st.text_input("🔐 Password (admin123)", type="password")

        if st.button("🔓 Login"):
            if username == "admin" and password == "admin123":
                st.session_state.authorized = True
                st.session_state.attempts = 0
                st.success("✅ Reauthorized Successfully!")
            else:
                st.error("❌ Invalid credentials.")
    else:
        st.success("✅ You are already authorized.")
