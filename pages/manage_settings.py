import os
import streamlit as st
from support.settings import gemini_api_key_value, openai_api_key_value
from support.config_manager import ConfigManager

st.set_page_config(page_title="Manage Settings", layout="wide")

# Initialize config manager
config_manager = ConfigManager()

st.title("⚙️ Manage Settings")
st.markdown("Configure your API keys and model preferences.")

# Load saved configuration
saved_config = config_manager.load_config()
saved_openai_key = saved_config.get("openai_api_key", openai_api_key_value)
saved_gemini_key = saved_config.get("gemini_api_key", gemini_api_key_value)
saved_model = saved_config.get("selected_model", "openai")

# Auto-load saved configuration to session state if not present
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = saved_openai_key
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = saved_gemini_key
if "selected_model" not in st.session_state:
    st.session_state.selected_model = saved_model

# API Key Management
st.subheader("🔑 API Key Management")

# Create two columns for API keys
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🤖 OpenAI API Key**")
    openai_api_key = st.text_input(
        "Enter your OpenAI API key", 
        value=st.session_state.openai_api_key, 
        type="password",
        key="openai_key_input"
    )
    
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        st.success("✅ OpenAI API key configured")

with col2:
    st.markdown("**🌟 Gemini API Key**")
    gemini_api_key = st.text_input(
        "Enter your Gemini API key", 
        value=st.session_state.gemini_api_key, 
        type="password",
        key="gemini_key_input"
    )
    
    if gemini_api_key:
        os.environ["GOOGLE_API_KEY"] = gemini_api_key
        st.success("✅ Gemini API key configured")

# Model Selection
st.subheader("🤖 Model Selection")
st.markdown("Choose which AI model to use for CV processing:")

# Use a key that changes when the model changes to force re-render
model_choice = st.radio(
    "Select your preferred model:",
    options=["openai", "gemini"],
    format_func=lambda x: "OpenAI GPT-4" if x == "openai" else "Google Gemini",
    index=0 if st.session_state.selected_model == "openai" else 1,
    key=f"model_radio_{st.session_state.selected_model}"  # Force re-render
)

# Update session state immediately when selection changes
if model_choice != st.session_state.selected_model:
    st.session_state.selected_model = model_choice
    st.rerun()  # Force page refresh to update the radio button state

# Display current configuration
st.subheader("📋 Current Configuration")
config_col1, config_col2 = st.columns(2)

with config_col1:
    st.info(f"**Selected Model:** {model_choice.upper()}")
    
with col2:
    if model_choice == "openai" and openai_api_key:
        st.success("✅ OpenAI is ready to use")
    elif model_choice == "gemini" and gemini_api_key:
        st.success("✅ Gemini is ready to use")
    else:
        st.warning("⚠️ Please configure the selected model's API key")

# Save configuration
if st.button("💾 Save Configuration"):
    # Store in session state for other pages to use
    st.session_state.openai_api_key = openai_api_key
    st.session_state.gemini_api_key = gemini_api_key
    st.session_state.selected_model = model_choice
    
    # Save to persistent storage
    config_data = {
        "openai_api_key": openai_api_key,
        "gemini_api_key": gemini_api_key,
        "selected_model": model_choice
    }
    
    if config_manager.save_config(config_data):
        st.success("✅ Configuration saved! You can now use other features.")
        st.success("💾 Settings will be automatically loaded next time you start the app.")
    else:
        st.error("❌ Failed to save configuration. Please try again.")

# Configuration Status
st.markdown("---")
st.subheader("📁 Configuration Status")

if config_manager.has_config():
    st.success("✅ Configuration file found")
    st.info("Your settings are automatically loaded when the app starts.")
    
    # Show last saved configuration
    last_config = config_manager.load_config()
    if last_config:
        st.markdown("**Last saved configuration:**")
        st.json(last_config)
    
    # Option to clear configuration
    if st.button("🗑️ Clear All Settings", type="secondary"):
        if config_manager.clear_config():
            st.success("✅ Configuration cleared!")
            st.rerun()
        else:
            st.error("❌ Failed to clear configuration.")
else:
    st.warning("⚠️ No saved configuration found")
    st.info("Save your configuration to enable automatic loading.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("home.py", label="Back to Home", icon="🏠")
with col2:
    st.page_link("pages/portfolio.py", label="Portfolio", icon="📁")
with col3:
    st.page_link("pages/new_submission.py", label="New Submission", icon="📝")
