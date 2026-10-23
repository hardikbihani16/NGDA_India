
import streamlit as st

APP_NAME = "Aqua-Net"
DEFAULT_LANGUAGE = "English"

LANGUAGES = {
    "English": "en",
    "isiZulu": "zu",
}

DEMO_MODE = True


def get_secret(name: str, default: str = "") -> str:
    """Read a Streamlit secret safely."""
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default
