import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta, datetime

st.set_page_config(page_title="Aqua-Net | Groundwater Intelligence", page_icon="💧", layout="wide", initial_sidebar_state="expanded")

# Design tokens: clean civic-tech product, inspired by the supplied references
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --navy:#082b46; --navy2:#0d3b59; --teal:#00a6a0; --mint:#dff5ef; --blue:#1678c8; --sky:#eaf4fb; --ink:#152f45; --muted:#64798a; --line:#dce6ec; --bg:#f4f7fa; --orange:#ee9b42; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:var(--bg); color:var(--ink); }
.block-container { padding-top:1.1rem; padding-bottom:2.2rem; max-width:1600px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#082b46 0%,#0b3854 100%); }
[data-testid="stSidebar"] * { color:#edf7fb !important; }
[data-testid="stSidebar"] hr { border-color:#2b5068; }
h1,h2,h3,h4 { font-family:'Manrope',sans-serif !important; color:var(--ink); letter-spacing:-.025em; }
h1 { font-size:2rem !important; font-weight:800 !important; }
h2 { font-size:1.35rem !important; font-weight:800 !important; }
h3 { font-size:1.05rem !important; font-weight:800 !important; }
p, label { color:var(--ink); }
div[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:15px; padding:15px 17px; box-shadow:0 2px 8px rgba(8,43,70,.025); }
div[data-testid="stMetric"] label { color:var(--muted) !important; font-size:.82rem; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--navy); font-family:'Manrope',sans-serif; font-weight:800; }
.stButton>button { border-radius:10px; font-weight:700; border:1px solid #cbdce5; min-height:2.55rem; }
.stButton>button[kind="primary"] { background:#008f91; border-color:#008f91; color:white; }
.stButton>button:hover { border-color:#008f91; color:#008f91; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
[data-testid="stForm"] { background:white; border:1px solid var(--line); border-radius:15px; padding:16px; }
div[data-baseweb="tab-list"] { gap:8px; }
button[data-baseweb="tab"] { border-radius:10px 10px 0 0; font-weight:700; }
.brand { font-family:'Manrope',sans-serif; font-size:1.45rem; font-weight:800; letter-spacing:-.04em; color:white; }
.brand span { color:#54d7cb; }
.brand-sub { color:#a9c1d0; font-size:.68rem; letter-spacing:.15em; font-weight:700; margin-top:2px; }
.eyebrow { color:#008f91; font-size:.72rem; letter-spacing:.15em; font-weight:800; text-transform:uppercase; }
.hero { border-radius:20px; padding:28px 32px; background:linear-gradient(115deg,#082b46 0%,#0e4b66 58%,#008f91 100%); color:white; position:relative; overflow:hidden; }
.hero h1 { color:white !important; font-size:2.15rem !important; margin:.4rem 0 .5rem; max-width:850px; }
.hero p { color:#d6f1f0; margin:0; font-size:1rem; max-width:780px; }
.hero-tag { color:#62e0d0; text-transform:uppercase; letter-spacing:.14em; font-size:.7rem; font-weight:800; }
.hero-side { position:absolute; right:4%; top:18%; font-size:5rem; opacity:.18; }
.panel { background:white; border:1px solid var(--line); border-radius:16px; padding:17px 19px; box-shadow:0 2px 8px rgba(8,43,70,.025); }
.panel-title { font-family:'Manrope',sans-serif; font-weight:800; font-size:1.02rem; color:var(--navy); }
.muted { color:var(--muted); font-size:.82rem; }
.demo { background:#fff6df; color:#79520a; border:1px solid #f1d48d; border-radius:10px; padding:9px 13px; font-size:.78rem; margin:12px 0 17px; }
.chip { display:inline-block; padding:4px 9px; border-radius:30px; font-size:.72rem; font-weight:800; }
.good { background:#dff5e9; color:#146b4a; }
.watch { background:#fff0d0; color:#895800; }
.alert { background:#ffe5df; color:#9b3a22; }
.blue { background:#e4f1ff; color:#165da0; }
.nav-card { background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.11); border-radius:12px; padding:12px 13px; margin:6px 0; }
.nav-card b { color:white; }
.step { display:flex; gap:12px; padding:12px 0; border-bottom:1px solid #e7eef2; }
.stepnum { background:#dff5ef; color:#008f91; font-weight:800; border-radius:10px; min-width:34px; height:34px; display:flex; align-items:center; justify-content:center; }
.phone { border:7px solid #102b40; border-radius:28px; padding:15px 13px; background:#fff; min-height:390px; box-shadow:0 12px 30px rgba(8,43,70,.14); }
.phone-top { text-align:center; color:#7c8c99; font-size:.72rem; margin-bottom:12px; }
.phone-logo { text-align:center; font-family:'Manrope',sans-serif; font-weight:800; color:#0c4563; font-size:1.15rem; margin:12px 0; }
.phone-button { border-radius:10px; background:#008f91; color:white; text-align:center; padding:11px; font-weight:700; margin:9px 0; }
.phone-option { background:#f1f7fa; border:1px solid #e0ebf0; padding:10px; border-radius:10px; margin:7px 0; font-weight:600; font-size:.84rem; }
.kpi-note { color:#6b7f8f; font-size:.72rem; }
hr { border-color:var(--line); }
</style>
""", unsafe_allow_html=True)

# -------------------- Sample data (explicitly illustrative) --------------------
if "reports" not in st.session_state:
    st.session_state.reports = [
        {"id":"AN-104","borehole":"BH-17","issue":"No water","source":"Resident · SMS","reported":"08:42 today","status":"Awaiting confirmation","confirmations":1,"priority":"High"},
        {"id":"AN-103","borehole":"BH-04","issue":"Flow lower than usual","source":"Aqua Fellow","reported":"07:15 today","status":"Under review","confirmations":2,"priority":"Medium"},
        {"id":"AN-102","borehole":"BH-12","issue":"Pump noise","source":"Resident · Voice","reported":"Yesterday","status":"Ticket opened","confirmations":3,"priority":"Medium"},
    ]
if "tickets" not in st.session_state:
    st.session_state.tickets = [
        {"ticket":"T-208","borehole":"BH-12","issue":"Pump noise","owner":"Local maintenance team","priority":"Medium","status":"In progress","updated":"Today"},
        {"ticket":"T-207","borehole":"BH-03","issue":"No water","owner":"Municipal water team","priority":"High","status":"Awaiting verification","updated":"Yesterday"},
    ]
if "readings" not in st.session_state:
    st.session_state.readings = [
        {"date":date.today()-timedelta(days=6),"borehole":"BH-17","depth":31.8,"ph":7.2,"tds":410,"observer":"Aqua Fellow 01"},
        {"date":date.today()-timedelta(days=5),"borehole":"BH-17","depth":31.9,"ph":7.1,"tds":415,"observer":"Aqua Fellow 01"},
        {"date":date.today()-timedelta(days=4),"borehole":"BH-17","depth":32.0,"ph":7.2,"tds":416,"observer":"Aqua Fellow 01"},
        {"date":date.today()-timedelta(days=3),"borehole":"BH-17","depth":32.2,"ph":7.2,"tds":420,"observer":"Aqua Fellow 01"},
        {"date":date.today()-timedelta(days=2),"borehole":"BH-17","depth":32.1,"ph":7.1,"tds":418,"observer":"Aqua Fellow 01"},
        {"date":date.today()-timedelta(days=1),"borehole":"BH-17","depth":32.4,"ph":7.2,"tds":423,"observer":"Aqua Fellow 01"},
        {"date":date.today(),"borehole":"BH-17","depth":32.6,"ph":7.2,"tds":426,"observer":"Aqua Fellow 01"},
    ]

bh = pd.DataFrame([
    ["BH-01","Thabeng East","Working","Verified","Stable","Today",-26.204,28.047,180],
    ["BH-03","Thabeng East","Needs maintenance","Verified","Watch","22 Oct",-26.211,28.059,240],
    ["BH-04","Thabeng Central","Under review","Verified","Watch","Today",-26.197,28.061,310],
    ["BH-08","Thabeng West","Working","Verified","Stable","Yesterday",-26.188,28.035,125],
    ["BH-12","Thabeng Central","Repair in progress","Verified","Stable","Yesterday",-26.202,28.072,205],
    ["BH-17","Thabeng South","Report received","Verified","Watch","Today",-26.222,28.053,390],
    ["BH-21","Thabeng South","Working","Needs verification","Unknown","Not checked",-26.229,28.067,90],
    ["BH-24","Thabeng West","Working","Verified","Stable","21 Oct",-26.181,28.052,145],
], columns=["Borehole","Community","Status","Verification","Water trend","Last checked","lat","lon","People served"])
status_color={"Working":"#15966A","Needs maintenance":"#E76F51","Under review":"#E9A23B","Repair in progress":"#247BA0","Report received":"#E9A23B"}
level_color={"Stable":"#15966A","Watch":"#E9A23B","Unknown":"#8798A7","Stress":"#E76F51"}

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="brand">💧 AQUA<span>-NET</span></div><div class="brand-sub">GROUNDWATER INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    mode = st.radio("EXPERIENCE", ["Government dashboard", "Community app", "Aqua Fellow", "Basic phone access"], label_visibility="visible")
    st.markdown("---")
    if mode == "Government dashboard":
        page = st.radio("GOVERNMENT WORKSPACE", ["Overview", "Borehole registry", "Verification queue", "Repair management", "Groundwater trends"], label_visibility="visible")
    elif mode == "Community app":
        page = st.radio("COMMUNITY APP", ["Home", "Explore boreholes", "Report an issue", "My contributions"], label_visibility="visible")
    elif mode == "Aqua Fellow":
        page = st.radio("FIELD TOOLS", ["Field dashboard", "Log a reading", "Reading history"], label_visibility="visible")
    else:
        page = st.radio("BASIC PHONE", ["USSD simulator", "SMS simulator", "Voice reporting"], label_visibility="visible")
    st.markdown("---")
    st.markdown('<div class="nav-card"><div class="muted">DEMO COMMUNITY</div><b>📍 Thabeng · South Africa</b><br><span class="muted">Illustrative pilot environment</span></div>', unsafe_allow_html=True)
    st.markdown('<span class="chip watch">PROTOTYPE · SAMPLE DATA</span>', unsafe_allow_html=True)

st.markdown('<div class="demo">⚠️ <b>Prototype mode:</b> all records, locations, readings and people are illustrative. No live government records, sensors, SMS gateway or field deployment is connected.</div>', unsafe_allow_html=True)

def page_header(eyebrow, title, sub=None):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    if sub: st.markdown(f'<div class="muted" style="font-size:.94rem;margin-top:-8px;margin-bottom:18px">{sub}</div>', unsafe_allow_html=True)

def panel_title(title, sub=None):
    st.markdown(f'<div class="panel"><div class="panel-title">{title}</div>{f"<div class=muted>{sub}</div>" if sub else ""}</div>', unsafe_allow_html=True)

# -------------------- Government dashboard --------------------
if mode == "Government dashboard":
    if page == "Overview":
        st.markdown("""
        <div class="hero">
          <div class="hero-tag">DEPARTMENT / MUNICIPAL OPERATIONS · DEMO</div>
          <h1>Groundwater intelligence, in one view.</h1>
          <p>See what is mapped, what needs verification, and which borehole issues still need an accountable response.</p>
          <div class="hero-side">⌁</div>
        </div>""", unsafe_allow_html=True)
        m1,m2,m3,m4,m5=st.columns(5)
        m1.metric("Boreholes mapped", "283,030", "+2.1% in sample")
        m2.metric("Verified records", "162,430", "57% of sample registry")
        m3.metric("Community verified", "89,240", "32% of sample registry")
        m4.metric("Needs verification", "31,360", "11% of sample registry")
        m5.metric("Open reports", len(st.session_state.reports), "Demo queue")
        st.caption("The national figures above are illustrative UI placeholders inspired by your reference image; they are not verified South African statistics.")
        left,right=st.columns([1.55,1])
        with left:
            st.markdown('<div class="panel"><div class="panel-title">Borehole registry · Thabeng pilot view</div><div class="muted">Status markers are illustrative and geographically approximate.</div></div>',unsafe_allow_html=True)
            fig = px.scatter_map(
    bh,
    lat="lat",
    lon="lon",
    color="Status",
    size="People served",
    hover_name="Borehole",
    hover_data=["Community", "Verification", "Water trend"],
    color_discrete_map=status_color,
    zoom=10.7,
    height=420,
    size_max=20,
    map_style="carto-positron",
)
            fig.update_layout(
    margin=dict(l=0, r=0, t=8, b=0),
    paper_bgcolor="white",
    legend_title_text="",
    font=dict(color="#152f45"),
)
            st.plotly_chart(fig,use_container_width=True)
        with right:
            st.markdown('<div class="panel-title">Verification & maintenance queue</div><div class="muted">Prioritise issues that need a human decision.</div><br>',unsafe_allow_html=True)
            for code, issue, status, kind in [
                ("BH-17","No water reported","1 confirmation","watch"),
                ("BH-04","Flow lower than usual","2 confirmations","watch"),
                ("BH-12","Pump noise","Ticket in progress","alert"),
                ("BH-21","Registry record incomplete","Needs verification","blue")]:
                st.markdown(f'<div class="panel" style="padding:12px 14px;margin-bottom:9px"><div style="display:flex;justify-content:space-between"><b>{code}</b><span class="chip {kind}">{status}</span></div><div style="margin-top:5px">{issue}</div></div>',unsafe_allow_html=True)
            st.button("Open verification queue →",on_click=lambda: st.session_state.update({"_jump":"Verification queue"}))
        st.markdown("### Community activity")
        activity=pd.DataFrame([
            ["08:42","BH-17","No water reported by resident","Awaiting confirmation"],
            ["07:15","BH-04","Second lower-flow observation","Under review"],
            ["Yesterday","BH-12","Pump-noise report corroborated","Ticket opened"],
            ["22 Oct","BH-03","Maintenance visit recorded","Awaiting verification"],
        ],columns=["Time","Borehole","Activity","Stage"])
        st.dataframe(activity,use_container_width=True,hide_index=True)
    elif page == "Borehole registry":
        page_header("DATA & REGISTRY","Borehole registry","A shared register with explicit verification status—not a map that treats every record as confirmed.")
        c1,c2=st.columns(2)
        with c1: comm=st.selectbox("Community",["All"]+sorted(bh.Community.unique()))
        with c2: ver=st.selectbox("Verification status",["All","Verified","Needs verification"])
        data=bh.copy()
        if comm!="All": data=data[data.Community==comm]
        if ver!="All": data=data[data.Verification==ver]
        st.dataframe(data[["Borehole","Community","Status","Verification","Water trend","Last checked","People served"]],use_container_width=True,hide_index=True)
        with st.expander("Propose a new borehole record"):
            with st.form("new_bh"):
                new_id=st.text_input("Borehole code",placeholder="BH-29")
                new_com=st.selectbox("Community",sorted(bh.Community.unique()))
                source=st.selectbox("Source",["Resident report","Aqua Fellow visit","Existing register"])
                ok=st.form_submit_button("Add as unverified")
                if ok:
                    st.success(f"{new_id.upper()} staged as UNVERIFIED ({new_com}; source: {source}). Demo only—no persistent record is created.")
    elif page == "Verification queue":
        page_header("TRUST & DATA QUALITY","Verification queue","Every new record and community signal needs an explicit path to confidence.")
        reports=pd.DataFrame(st.session_state.reports)
        st.dataframe(reports[["id","borehole","issue","source","reported","status","confirmations","priority"]],use_container_width=True,hide_index=True)
        st.markdown("### Review a signal")
        a,b,c=st.columns([1,1,1])
        with a: rid=st.selectbox("Report", [r["id"] for r in st.session_state.reports])
        with b: action=st.selectbox("Action",["Add independent confirmation","Mark under review","Open repair ticket"])
        with c:
            if st.button("Apply review",type="primary",use_container_width=True):
                item=next(r for r in st.session_state.reports if r["id"]==rid)
                if action=="Add independent confirmation":
                    item["confirmations"]+=1
                    item["status"]="Verified signal" if item["confirmations"]>=3 else "Under review"
                    st.success(f"{rid}: {item['confirmations']} confirmations.")
                elif action=="Mark under review":
                    item["status"]="Under review"; st.success("Marked under review.")
                else:
                    st.session_state.tickets.insert(0,{"ticket":f"T-{209+len(st.session_state.tickets)}","borehole":item["borehole"],"issue":item["issue"],"owner":"Demo municipal water team","priority":item["priority"],"status":"Open","updated":"Just now"})
                    item["status"]="Ticket opened"; st.success("Demo ticket created.")
                st.rerun()
        st.info("The three-confirmation concept is proposed in the project materials. A real pilot must define independence, duplicates, audit trails and exception handling.")
    elif page == "Repair management":
        page_header("OPERATIONS","Repair management","The report is not complete until someone owns the response and the fix is checked.")
        tickets=pd.DataFrame(st.session_state.tickets)
        st.dataframe(tickets,use_container_width=True,hide_index=True)
        a,b,c=st.columns([1,1,1])
        with a: tid=st.selectbox("Ticket",tickets.ticket.tolist())
        with b: status=st.selectbox("Update status",["Open","In progress","Awaiting verification","Closed"])
        with c:
            if st.button("Save status",type="primary",use_container_width=True):
                item=next(t for t in st.session_state.tickets if t["ticket"]==tid); item["status"]=status; item["updated"]="Just now"; st.success(f"{tid} → {status}"); st.rerun()
        st.markdown("### Closure protocol")
        cc1,cc2,cc3=st.columns(3)
        with cc1: st.checkbox("Repair visit recorded",key="govc1")
        with cc2: st.checkbox("Fix independently checked",key="govc2")
        with cc3: st.checkbox("Reporters notified",key="govc3")
        if st.button("Check closure readiness"):
            if all(st.session_state.get(k,False) for k in ["govc1","govc2","govc3"]): st.success("Checklist complete in this demo. Real closure authority must be agreed with the pilot operator.")
            else: st.warning("Keep the ticket open until all checks are complete.")
    elif page == "Groundwater trends":
        page_header("MONITORING & INSIGHT","Groundwater trends","Repeat readings can surface changes worth investigating; they do not by themselves diagnose aquifer health.")
        readings=pd.DataFrame(st.session_state.readings); readings["date"]=pd.to_datetime(readings["date"])
        a,b=st.columns([1.2,1])
        with a:
            fig=px.line(readings[readings.borehole=="BH-17"],x="date",y="depth",markers=True,title="BH-17 · depth to water")
            fig.update_traces(line_color="#008f91",line_width=3,marker_size=8)
            fig.update_layout(height=340,margin=dict(l=0,r=0,t=50,b=0),paper_bgcolor="white",plot_bgcolor="white",xaxis_title="",yaxis_title="Depth to water (m)")
            st.plotly_chart(fig,use_container_width=True)
        with b:
            st.markdown('<div class="panel"><div class="panel-title">Interpretation guardrails</div><br><span class="chip watch">TREND TO REVIEW</span><br><br>Depth readings are meaningful only when the measuring point and method are consistent.<br><br>Combine repeat measurements with pumping context, local geology and expert review before drawing conclusions.</div>',unsafe_allow_html=True)
        st.dataframe(readings.sort_values("date",ascending=False),use_container_width=True,hide_index=True)

# -------------------- Community app --------------------
elif mode == "Community app":
    if page == "Home":
        st.markdown("""
        <div class="hero">
          <div class="hero-tag">AQUAMAP · COMMUNITY VIEW</div>
          <h1>Your water points. Your community. One shared picture.</h1>
          <p>Find a borehole, check the latest verified status, report a change and see what happens next.</p>
        </div>""",unsafe_allow_html=True)
        st.markdown("### Welcome to Thabeng")
        c1,c2,c3=st.columns(3)
        c1.metric("Nearby boreholes","8","Demo community")
        c2.metric("Verified this week","6","Sample records")
        c3.metric("Reports you can follow",len(st.session_state.reports),"Demo queue")
        st.markdown("### What would you like to do?")
        x,y,z=st.columns(3)
        with x:
            st.markdown('<div class="panel"><div style="font-size:1.8rem">📍</div><div class="panel-title">Explore boreholes</div><div class="muted">Find a water point and check its status.</div></div>',unsafe_allow_html=True)
            if st.button("Explore map →",key="home_map",use_container_width=True): st.session_state["_community_page"]="Explore boreholes"; st.rerun()
        with y:
            st.markdown('<div class="panel"><div style="font-size:1.8rem">📣</div><div class="panel-title">Report an issue</div><div class="muted">Tell the community when something changes.</div></div>',unsafe_allow_html=True)
            if st.button("Make a report →",key="home_report",use_container_width=True): st.session_state["_community_page"]="Report an issue"; st.rerun()
        with z:
            st.markdown('<div class="panel"><div style="font-size:1.8rem">🏆</div><div class="panel-title">My contributions</div><div class="muted">See verified reports and demo points.</div></div>',unsafe_allow_html=True)
            if st.button("View contributions →",key="home_rewards",use_container_width=True): st.session_state["_community_page"]="My contributions"; st.rerun()
        st.markdown("### Latest community updates")
        for code,txt,sub in [("BH-04","A second report confirms lower flow","Under review · Today"),("BH-12","Pump issue has a maintenance ticket","In progress · Today"),("BH-08","Routine check completed","Verified · Yesterday")]:
            st.markdown(f'<div class="panel" style="margin-bottom:8px;padding:12px 16px"><b>{code}</b> &nbsp; {txt}<div class="muted">{sub}</div></div>',unsafe_allow_html=True)
    elif page == "Explore boreholes":
        page_header("AQUAMAP","Explore boreholes","Check a water point's latest status before you travel. Demo locations are approximate.")
        fig=px.scatter_mapbox(bh,lat="lat",lon="lon",color="Status",size="People served",hover_name="Borehole",hover_data=["Community","Verification","Water trend"],color_discrete_map=status_color,zoom=10.8,height=440,size_max=18)
        fig.update_layout(mapbox_style="carto-positron",margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="white",legend_title_text="")
        st.plotly_chart(fig,use_container_width=True)
        code=st.selectbox("View a borehole",bh.Borehole.tolist(),index=bh.Borehole.tolist().index("BH-17"))
        record=bh[bh.Borehole==code].iloc[0]
        c1,c2,c3=st.columns(3)
        c1.metric("Current status",record["Status"])
        c2.metric("Verification",record["Verification"])
        c3.metric("Water trend",record["Water trend"])
        st.markdown(f'<div class="panel"><div class="panel-title">{code} · {record["Community"]}</div><div class="muted">Last checked: {record["Last checked"]}</div><br>Use “Report an issue” if the on-the-ground situation differs from this record. The displayed status is sample data.</div>',unsafe_allow_html=True)
    elif page == "Report an issue":
        page_header("COMMUNITY REPORT","Report a change","A short report helps start a verification process; it does not automatically diagnose the cause.")
        left,right=st.columns([1,1])
        with left:
            st.markdown('<div class="panel-title">Tell us what you noticed</div><br>',unsafe_allow_html=True)
            with st.form("community_report"):
                code=st.selectbox("Borehole code",bh.Borehole.tolist(),index=bh.Borehole.tolist().index("BH-17"))
                issue=st.radio("What changed?",["No water","Less water than usual","Pump sounds different","Water looks different","Other"],)
                contact=st.selectbox("How are you reporting?",["App / website","SMS","Voice call","Aqua Fellow"])
                detail=st.text_area("Anything else? (optional)",placeholder="When did you notice the change?")
                sent=st.form_submit_button("Submit report",type="primary",use_container_width=True)
            if sent:
                rid=f"AN-{105+len(st.session_state.reports)}"
                st.session_state.reports.insert(0,{"id":rid,"borehole":code,"issue":issue,"source":contact,"reported":"Just now","status":"Awaiting confirmation","confirmations":1,"priority":"High" if issue=="No water" else "Medium"})
                st.success(f"Report {rid} received for {code}. Next step: independent confirmation.")
        with right:
            st.markdown('<div class="panel-title">What happens after you report?</div>',unsafe_allow_html=True)
            for n,title,desc in [("1","We record it","Your report is linked to a borehole code."),("2","The signal is checked","A neighbour or trained fellow can confirm independently."),("3","A responsible team is contacted","A ticket can be assigned once the issue is confirmed."),("4","You get an update","The ticket should remain open until the repair is checked.")]:
                st.markdown(f'<div class="step"><div class="stepnum">{n}</div><div><b>{title}</b><div class="muted">{desc}</div></div></div>',unsafe_allow_html=True)
    elif page == "My contributions":
        page_header("COMMUNITY CONTRIBUTIONS","Your reports make the picture stronger","Rewards are a proposal to test, not a confirmed programme.")
        a,b,c=st.columns(3)
        a.metric("Demo points","320","Illustrative")
        b.metric("Verified contributions","7","Sample profile")
        c.metric("Community level","Level 3","Illustrative")
        st.progress(0.72,text="72% to next demo level")
        st.markdown("### Recent contributions")
        st.dataframe(pd.DataFrame([["Verified BH-08","+50","Verified"],["Reported lower flow at BH-04","+30","Under review"],["Helped confirm BH-12","+20","Verified"],["Added BH-21 record","+0","Needs verification"]],columns=["Contribution","Demo points","Status"]),use_container_width=True,hide_index=True)
        st.info("In a real pilot, any rewards would need clear verification and fraud safeguards. Never reward people for reducing necessary water use.")

# -------------------- Aqua Fellow --------------------
elif mode == "Aqua Fellow":
    readings=pd.DataFrame(st.session_state.readings)
    if page == "Field dashboard":
        page_header("AQUA FELLOW","Field dashboard","A simple field workflow for repeat readings and community observations.")
        a,b,c,d=st.columns(4)
        a.metric("Assigned points","6","Demo route")
        b.metric("Checks this week","4","Sample activity")
        c.metric("Readings needing review","1","Illustrative")
        d.metric("Kit status","Ready","Sample device")
        st.markdown("### Today's route")
        st.dataframe(pd.DataFrame([["BH-17","Water-level reading","Due today","Watch"],["BH-04","Repeat flow observation","Due today","Watch"],["BH-08","Routine screening","Completed","Stable"],["BH-21","Verify registry record","Pending","Unknown"]],columns=["Borehole","Task","Status","Signal"]),use_container_width=True,hide_index=True)
        st.info("Use the same measuring point and method each time. A screening reading is not a drinking-water safety certification.")
    elif page == "Log a reading":
        page_header("FIELD DATA","Log a reading","Record the method and context consistently so readings can be compared over time.")
        with st.form("field_log"):
            a,b,c=st.columns(3)
            with a: code=st.selectbox("Borehole",bh.Borehole.tolist(),index=bh.Borehole.tolist().index("BH-17")); rd=date.today()
            with b: depth=st.number_input("Depth to water (m)",0.0,500.0,32.6,0.1); ph=st.number_input("pH screening",0.0,14.0,7.2,0.1)
            with c: tds=st.number_input("TDS screening (ppm)",0,10000,426,5); observer=st.selectbox("Observer",["Aqua Fellow 01","Aqua Fellow 02","Pump operator"])
            method=st.selectbox("Measurement method",["Dip meter","Manual field test","Other approved method"])
            note=st.text_area("Observation / context",placeholder="Pump active? Recent rainfall? Unusual appearance?")
            save=st.form_submit_button("Save reading",type="primary")
        if save:
            st.session_state.readings.append({"date":rd,"borehole":code,"depth":depth,"ph":ph,"tds":tds,"observer":observer,"method":method,"notes":note})
            st.success(f"Reading saved for {code} in this demo session.")
    elif page == "Reading history":
        page_header("FIELD DATA","Reading history","Review trends, not single values in isolation.")
        readings["date"]=pd.to_datetime(readings["date"])
        code=st.selectbox("Borehole",bh.Borehole.tolist(),index=bh.Borehole.tolist().index("BH-17"))
        data=readings[readings.borehole==code].sort_values("date")
        if data.empty: st.info("No readings for this point yet.")
        else:
            fig=px.line(data,x="date",y="depth",markers=True,title=f"{code} · depth to water")
            fig.update_traces(line_color="#008f91",line_width=3,marker_size=8)
            fig.update_layout(height=320,paper_bgcolor="white",plot_bgcolor="white",margin=dict(l=0,r=0,t=50,b=0),xaxis_title="",yaxis_title="Depth to water (m)")
            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(data,use_container_width=True,hide_index=True)

# -------------------- Basic phone simulator --------------------
elif mode == "Basic phone access":
    if page == "USSD simulator":
        page_header("INCLUSIVE ACCESS","USSD menu simulator","Demonstrates a low-bandwidth menu for a basic phone. This does not dial a live USSD code.")
        a,b=st.columns([.8,1.2])
        with a:
            st.markdown('<div class="phone"><div class="phone-top">9:41 · SIMULATED SESSION</div><div class="phone-logo">💧 Aqua-Net</div><div style="background:#f1f6f8;border-radius:9px;padding:12px;font-size:.88rem">Welcome to Aqua-Net<br><br>1. Check a borehole<br>2. Report a problem<br>3. Verify a borehole<br>4. My points<br>5. Help<br><br>Reply with a number</div></div>',unsafe_allow_html=True)
        with b:
            choice=st.radio("Choose a menu option",["1 · Check a borehole","2 · Report a problem","3 · Verify a borehole","4 · My points","5 · Help"])
            if choice.startswith("1"):
                code=st.selectbox("Borehole code",bh.Borehole.tolist(),index=bh.Borehole.tolist().index("BH-17")); rec=bh[bh.Borehole==code].iloc[0]
                st.success(f"{code}: {rec['Status']} · Record {rec['Verification'].lower()}. Last checked: {rec['Last checked']}.")
            elif choice.startswith("2"):
                code=st.selectbox("Borehole code",bh.Borehole.tolist(),key="ussdcode")
                issue=st.selectbox("Problem",["No water","Less water than usual","Pump noise","Water looks different"])
                if st.button("Send report",type="primary"): 
                    st.session_state.reports.insert(0,{"id":f"AN-{105+len(st.session_state.reports)}","borehole":code,"issue":issue,"source":"USSD simulator","reported":"Just now","status":"Awaiting confirmation","confirmations":1,"priority":"High" if issue=="No water" else "Medium"})
                    st.success("Demo report sent. It will appear in the verification queue.")
            elif choice.startswith("3"):
                st.info("In a real flow, the user would receive a short description and confirm whether the borehole is present and working.")
            elif choice.startswith("4"):
                st.metric("Demo points","320")
            else:
                st.info("Aqua-Net records community observations and routes verified issues to an agreed responsible actor.")
    elif page == "SMS simulator":
        page_header("INCLUSIVE ACCESS","SMS reporting simulator","A simple format designed around short codes and low-bandwidth phones.")
        st.markdown('<div class="panel"><div class="muted">EXAMPLE MESSAGE</div><h3>BH-17 NO WATER</h3><div class="muted">Send to the proposed Aqua-Net short code (not connected in this prototype).</div></div>',unsafe_allow_html=True)
        with st.form("sms"):
            sender=st.text_input("Sender label (demo)",value="Resident 014")
            msg=st.text_input("Message",placeholder="BH-17 NO WATER")
            send=st.form_submit_button("Simulate SMS",type="primary")
        if send:
            parts=msg.upper().split()
            if len(parts)>=2 and parts[0] in bh.Borehole.tolist():
                issue=" ".join(parts[1:]).title()
                st.session_state.reports.insert(0,{"id":f"AN-{105+len(st.session_state.reports)}","borehole":parts[0],"issue":issue,"source":f"SMS simulator · {sender}","reported":"Just now","status":"Awaiting confirmation","confirmations":1,"priority":"High" if "NO WATER" in msg.upper() else "Medium"})
                st.success("SMS parsed into a demo report. No message was actually sent.")
            else: st.error("Try a format such as BH-17 NO WATER.")
    else:
        page_header("INCLUSIVE ACCESS","Voice reporting concept","A guided call or voice note can capture a report without requiring a smartphone.")
        st.markdown('<div class="panel"><div class="panel-title">Proposed voice flow</div><br>1. Choose language<br><br>2. Enter or speak the borehole code<br><br>3. Select the issue or record a short voice note<br><br>4. Hear a report reference number<br><br>5. Receive a follow-up when the issue is verified</div>',unsafe_allow_html=True)
        st.caption("Voice calling and WhatsApp integration are not connected in this prototype.")

st.markdown("<hr>",unsafe_allow_html=True)
st.markdown('<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;color:#708391;font-size:.75rem"><span>💧 AQUA-NET · Community-powered groundwater intelligence</span><span>Stakeholder prototype · Simulated records only</span></div>',unsafe_allow_html=True)
