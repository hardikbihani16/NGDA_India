
import streamlit as st

TRANSLATIONS = {
    "English": {
        "app_title": "Aqua-Net",
        "language": "Language",
        "overview": "Overview",
        "borehole_registry": "Borehole registry",
        "verification_queue": "Verification queue",
        "repair_management": "Repair management",
        "groundwater_trends": "Groundwater trends",
        "community_app": "Community app",
        "explore_boreholes": "Explore boreholes",
        "report_issue": "Report an issue",
        "my_contributions": "My contributions",
        "logout": "Log out",
        "demo_notice": "Prototype mode: all records are illustrative.",
    },
    "isiZulu": {
        "app_title": "Aqua-Net",
        "language": "Ulimi",
        "overview": "Uhlolojikelele",
        "borehole_registry": "Uhlu lwemithombo yamanzi",
        "verification_queue": "Imibiko elindele ukuqinisekiswa",
        "repair_management": "Ukuphathwa kokulungisa",
        "groundwater_trends": "Izinguquko emanzini angaphansi komhlaba",
        "community_app": "Uhlelo lomphakathi",
        "explore_boreholes": "Hlola imithombo yamanzi",
        "report_issue": "Bika inkinga",
        "my_contributions": "Iminikelo yami",
        "logout": "Phuma",
        "demo_notice": "Uhlelo lokuhlola: yonke imininingwane iyisibonelo.",
    },
}


def language_selector():
    if "language" not in st.session_state:
        st.session_state.language = "English"

    st.selectbox(
        "Language / Ulimi",
        options=list(TRANSLATIONS.keys()),
        key="language",
    )


def t(key: str) -> str:
    language = st.session_state.get("language", "English")
    return TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(
        key,
        TRANSLATIONS["English"].get(key, key),
    )
