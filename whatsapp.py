
import streamlit as st
from urllib.parse import quote
from config import get_secret


def show_whatsapp():
    st.subheader("Connect through WhatsApp")
    st.write(
        "Follow community announcements or start a conversation "
        "to report a borehole issue."
    )

    channel_url = get_secret("WHATSAPP_CHANNEL_URL")
    business_number = get_secret("WHATSAPP_BUSINESS_NUMBER")

    if channel_url:
        st.link_button(
            "Follow Aqua-Net Channel",
            channel_url,
            use_container_width=True,
        )
    else:
        st.info("The Aqua-Net WhatsApp Channel link has not been configured.")

    if business_number:
        message = quote("Hello Aqua-Net, I would like to report a borehole issue.")
        chat_url = (
            f"https://wa.me/{business_number}"
            f"?text={message}"
        )
        st.link_button(
            "Chat with Aqua-Net",
            chat_url,
            use_container_width=True,
        )
    else:
        st.info("The Aqua-Net WhatsApp Business number has not been configured.")
