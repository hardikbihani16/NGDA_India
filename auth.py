
import streamlit as st


def show_login() -> bool:
    """
    Return True when a demo role has been selected.
    This is role selection only, not identity verification.
    """
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    if st.session_state.user_role:
        return True

    st.markdown(
        """
        <div style="
            padding:32px;
            border-radius:18px;
            background:linear-gradient(120deg,#082b46,#008f91);
            color:white;
        ">
            <h1 style="color:white">Aqua-Net</h1>
            <p style="color:#d6f1f0">
                Community-powered groundwater intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Welcome")
    st.write("Choose the experience you want to explore.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Community member")
        st.write("Explore boreholes, submit reports and follow updates.")
        if st.button("Continue as community member", use_container_width=True):
            st.session_state.user_role = "community"
            st.rerun()

    with col2:
        st.markdown("### Government employee")
        st.write("Review borehole records, verification and repair tickets.")
        if st.button("Continue as government employee", use_container_width=True):
            st.session_state.user_role = "government"
            st.rerun()

    st.caption(
        "Demonstration mode: these buttons do not verify identity. "
        "Do not use this selector to protect real government data."
    )

    return False


def logout():
    st.session_state.user_role = None
    st.rerun()
