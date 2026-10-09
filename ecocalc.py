import streamlit as st
import pandas as pd
import html

st.set_page_config(page_title="EcoCalc | Make Smart Choices Today", page_icon="🍃", layout="wide", initial_sidebar_state="collapsed")

APPS = [
    ("Air Conditioner", "❄", 1500, "Cooling"),
    ("Refrigerator", "▣", 150, "Kitchen"),
    ("Ceiling Fan", "✿", 75, "Airflow"),
    ("Television", "▭", 100, "Entertainment"),
    ("LED Bulb", "☼", 10, "Lighting"),
    ("Washing Machine", "◉", 500, "Laundry"),
]

if "screen" not in st.session_state:
    st.session_state.screen = "Home"
if "step" not in st.session_state:
    st.session_state.step = 0
if "values" not in st.session_state:
    st.session_state["values"] = {n: {"quantity": "0", "watts": str(w), "hours": "0"} for n, _, w, _ in APPS}
if "rate" not in st.session_state:
    st.session_state.rate = "8"
if "days" not in st.session_state:
    st.session_state.days = "30"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
:root {--forest:#294b35;--sage:#dce6d4;--cream:#fbf7eb;--ink:#263c2b}
html,body,[class*="css"],.stApp,button,input {font-family:'Playfair Display',Georgia,serif!important}
.stApp {background:radial-gradient(circle at 92% 13%,#e2e9d8 0,transparent 24%),linear-gradient(120deg,#faf5e8,#fffdf7 53%,#eff1e4);color:var(--ink)}
.block-container {max-width:1210px;padding-top:1.1rem;padding-bottom:1.4rem}
header[data-testid="stHeader"] {background:transparent}
#MainMenu,footer {visibility:hidden}
h1,h2,h3,p {color:var(--ink)}
.topbar {display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #d7decc;padding:0 0 12px;margin-bottom:20px}
.brand {font-family:Audrey,'Playfair Display',serif;font-size:29px;color:#24452f;font-weight:700}
.logo {font-size:30px;color:#2f623c;display:inline-block;vertical-align:middle;margin-right:10px}
.eyebrow {letter-spacing:3px;text-transform:uppercase;font-size:11px;color:#60755b}
.hero {min-height:305px;padding:28px 34px 20px;border-radius:24px;background:linear-gradient(110deg,#e4e8d9d9,#f7f4e6cc);box-shadow:0 10px 38px #3e5e4122;position:relative;overflow:hidden}
.hero:after {content:'❧';font-size:270px;position:absolute;right:15px;top:-96px;color:#6f906b33;transform:rotate(-25deg);pointer-events:none}
.hero h1 {font-family:Audrey,'Playfair Display',Georgia,serif;font-weight:500;font-size:clamp(58px,8vw,102px);line-height:1.05;margin:12px 0 0;color:#203f2d}
.tagline {font-family:Nautic,'Brush Script MT',cursive;font-style:italic;font-size:clamp(23px,3vw,35px);color:#365e43;margin:0 0 12px}
.hero-p {max-width:560px;font-size:17px;line-height:1.6}
.sticky {min-height:112px;border-radius:9px;padding:16px 15px;box-shadow:3px 8px 11px #64745726;transform:rotate(-2deg);font-size:16px;line-height:1.55;border:1px solid #56644710}
.sticky b {font-size:24px;display:block}
.sticky.green {background:#e1ead8}.sticky.yellow {background:#f6e9c5;transform:rotate(2deg)}.sticky.pink {background:#f5dfd7;transform:rotate(-1deg)}
.panel {background:#fffdf7cc;border:1px solid #e1e4d7;border-radius:20px;padding:24px;box-shadow:0 8px 25px #3f5b4014}
.page-title {font-size:38px;font-weight:600;margin:0 0 8px}
.subtle {font-size:15px;color:#617061}
.appliance-art {font-size:116px;text-align:center;padding:29px 0;background:#e2e9d9;border-radius:22px}
.metric {padding:21px;border-radius:17px;background:#e6eddf;border:1px solid #d6e1d1;min-height:123px}
.metric.gold {background:#f8ebcd;border-color:#f0e1bf}.metric.gray {background:#e8ebea;border-color:#d9dfdc}
.metric small {font-size:13px;color:#5b695b}.metric strong {display:block;font-size:30px;color:#284631;margin-top:7px}
.stTextInput input {background:#fffdf8!important;border:1px solid #d8ddce!important;border-radius:10px!important;color:#253e2b!important}
.stButton button[kind="primary"] {background:#284c35!important;color:#fff!important;border:none!important;border-radius:50px!important}
.stButton button {border-radius:40px!important;font-family:'Playfair Display',serif!important}
.stButton button:hover {border-color:#315f42!important;color:#315f42!important}
.stButton button[kind="primary"]:hover {background:#3f6b4b!important;color:#fff!important}

/* High-contrast navigation and call-to-action buttons */
div.stButton > button,
div.stButton > button[kind="secondary"],
div.stButton > button[kind="primary"] {
    background-color:#294B35 !important;
    background-image:none !important;
    border:1px solid #294B35 !important;
    color:#FFF9ED !important;
    border-radius:40px !important;
}
div.stButton > button *,
div.stButton > button p,
div.stButton > button span,
div.stButton > button[kind="primary"] *,
div.stButton > button[kind="secondary"] * {
    color:#FFF9ED !important;
    fill:#FFF9ED !important;
}
div.stButton > button:hover,
div.stButton > button:focus-visible {
    background-color:#416B4C !important;
    border-color:#416B4C !important;
    color:#FFFFFF !important;
}
div.stButton > button:hover *,
div.stButton > button:focus-visible * {color:#FFFFFF !important;}
/* Keep the download button consistent */
div.stDownloadButton > button {background:#294B35!important;color:#FFF9ED!important;border:1px solid #294B35!important;border-radius:40px!important;}
div.stDownloadButton > button * {color:#FFF9ED!important;}

div[data-testid="stDataFrame"] {border-radius:14px;overflow:hidden}
.smallnote {font-size:12px;color:#748072}
@media(max-width:700px){.hero{padding:25px 20px;min-height:240px}.hero h1{font-size:58px}.appliance-art{font-size:70px;padding:12px}.block-container{padding-top:.5rem}}
</style>
""", unsafe_allow_html=True)


def navigate(page):
    st.session_state.screen = page
    st.rerun()


def number(txt, label, lo=0, hi=None, integer=False):
    try:
        v = float(str(txt).strip())
        if not (lo <= v and (hi is None or v <= hi)) or (integer and not v.is_integer()):
            raise ValueError
        return int(v) if integer else v
    except (ValueError, TypeError):
        raise ValueError(f"{label}: enter a valid number{f' from {lo} to {hi}' if hi is not None else ''}.")


def calculate():
    days = number(st.session_state.days, "Billing days", 1, 366, True)
    rate = number(st.session_state.rate, "Tariff per unit", 0, 10000)
    rows = []
    for name, symbol, default, category in APPS:
        item = st.session_state["values"][name]
        qty = number(item['quantity'], f"{name} quantity", 0, 1000, True)
        watts = number(item['watts'], f"{name} wattage", 0, 100000)
        hours = number(item['hours'], f"{name} hours", 0, 24)
        kwh = qty * watts * hours * days / 1000
        if qty and hours and watts:
            rows.append({"Appliance":name,"Icon":symbol,"Quantity":qty,"Watts":watts,"Hours/day":hours,"kWh":round(kwh,3),"Cost (₹)":round(kwh*rate,2)})
    return pd.DataFrame(rows), days, rate


def header():
    st.markdown('<div class="topbar"><div class="brand"><span class="logo">❧⏻</span>EcoCalc</div><div class="eyebrow">Make Smart Choices Today</div></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for col,(name,label) in zip(cols,[("Home","Home"),("Calculator","Calculator"),("Results","Results"),("Tips","Tips")]):
        with col:
            if st.button(label,use_container_width=True,type="primary" if st.session_state.screen==name else "secondary",key="nav_"+name):
                navigate(name)

header()
screen=st.session_state.screen

if screen=="Home":
    st.markdown('''<div class="hero"><div class="eyebrow">A greener tomorrow starts at home</div><h1>EcoCalc</h1><div class="tagline">Make Smart Choices Today.</div><div class="hero-p">Understand your household energy use, lower your bills, and make a brighter future — one choice at a time.</div></div>''',unsafe_allow_html=True)
    st.write("")
    a,b,c=st.columns([1,1,1])
    with a: st.markdown('<div class="sticky green"><b>☼</b>Turn off appliances when they are not in use.</div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="sticky yellow"><b>❧</b>Choose energy-efficient appliances.</div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="sticky pink"><b>⚡</b>Small choices today, a greener tomorrow.</div>',unsafe_allow_html=True)
    st.write("")
    _,middle,_=st.columns([1,1.5,1])
    with middle:
        if st.button("Calculate My Bill →",use_container_width=True,type="primary"):
            st.session_state.step=0
            navigate("Calculator")

elif screen=="Calculator":
    name,symbol,default,category=APPS[st.session_state.step]
    st.markdown(f'<div class="eyebrow">Appliance {st.session_state.step+1} of {len(APPS)}</div>',unsafe_allow_html=True)
    st.progress((st.session_state.step+1)/len(APPS))
    st.markdown(f'<div class="page-title">{html.escape(name)}</div><div class="subtle">Enter the details below, or leave quantity as 0 if you do not use this appliance.</div>',unsafe_allow_html=True)
    left,right=st.columns([1,1.5],gap="large")
    with left:
        st.markdown(f'<div class="appliance-art">{symbol}</div>',unsafe_allow_html=True)
        st.caption(f"{category} · Suggested wattage: {default} W. Use the rating on your appliance if available.")
    with right:
        item = st.session_state["values"][name]
        item['quantity']=st.text_input("Number of appliances",value=item['quantity'],key="q_"+name,placeholder="e.g. 1")
        item['watts']=st.text_input("Power rating (watts)",value=item['watts'],key="w_"+name,placeholder="e.g. 1500")
        item['hours']=st.text_input("Hours used per day",value=item['hours'],key="h_"+name,placeholder="e.g. 4")
    st.write("")
    back,nextcol=st.columns(2)
    with back:
        if st.button("← Back",use_container_width=True):
            if st.session_state.step: st.session_state.step-=1;st.rerun()
            else: navigate("Home")
    with nextcol:
        if st.button("Next →" if st.session_state.step<len(APPS)-1 else "Review My Results →",use_container_width=True,type="primary"):
            try:
                number(item['quantity'],"Quantity",0,1000,True)
                number(item['watts'],"Wattage",0,100000)
                number(item['hours'],"Hours/day",0,24)
                if st.session_state.step<len(APPS)-1: st.session_state.step+=1;st.rerun()
                else: navigate("Results")
            except ValueError as exc: st.error(str(exc))


elif screen=="Results":
    st.markdown('<div class="page-title">Your Energy Summary</div><div class="subtle">Your personalised electricity estimate at a glance.</div>',unsafe_allow_html=True)
    st.write("")
    l,r=st.columns(2)
    with l: st.text_input("Electricity rate (₹ per unit)",key="rate")
    with r: st.text_input("Billing period (days)",key="days")
    try:
        df,days,rate=calculate()
        if df.empty:
            st.info("Add an appliance in Calculator to generate your energy summary.")
            if st.button("Go to Calculator →",type="primary"): navigate("Calculator")
        else:
            total=float(df['kWh'].sum());bill=total*rate
            # This transparent demonstration score is not an environmental certification.
            score=max(0,min(100,round(100-(total/days)*4)))
            a,b,c=st.columns(3)
            with a: st.markdown(f'<div class="metric"><small>⚡ Total Consumption</small><strong>{total:,.1f} kWh</strong><small>for {days} days</small></div>',unsafe_allow_html=True)
            with b: st.markdown(f'<div class="metric gold"><small>₹ Estimated Bill</small><strong>₹{bill:,.0f}</strong><small>at ₹{rate:g} per unit</small></div>',unsafe_allow_html=True)
            with c: st.markdown(f'<div class="metric gray"><small>❧ Illustrative Eco Score</small><strong>{score} / 100</strong><small>based on average daily usage</small></div>',unsafe_allow_html=True)
            st.write("")
            st.markdown('### Appliance-wise Consumption')
            st.bar_chart(df.set_index('Appliance')['kWh'],color="#537759",horizontal=True,height=270)
            with st.expander("See the detailed appliance report"):
                st.dataframe(df,hide_index=True,use_container_width=True)
                st.download_button("Download CSV Report",df.to_csv(index=False).encode('utf-8'),file_name="ecocalc_report.csv",mime="text/csv")
            high=df.sort_values('kWh',ascending=False).iloc[0]
            st.success(f"Your highest-consuming appliance is {high['Appliance']} ({high['kWh']:.1f} kWh). Visit Tips for simple ways to save.")
            st.caption("Estimates assume constant average power. Refrigerators, inverter ACs and other cycling appliances can differ in real use. Electricity bills may include slabs, fixed charges and taxes. Eco score is illustrative only.")
    except ValueError as exc: st.error(str(exc))
    if st.button("See Energy Saving Tips →",type="primary"): navigate("Tips")

else:
    st.markdown('<div class="page-title">Smart Tips for a Brighter Tomorrow</div><div class="subtle">Small changes. Real impact.</div>',unsafe_allow_html=True)
    st.write("")
    tips=[
        ("green","❄","Set your AC to a comfortable, efficient temperature and close doors while cooling."),
        ("yellow","▣","Keep your refrigerator door closed and ensure the seals are in good condition."),
        ("pink","✿","Choose ceiling fans instead of AC when the weather permits."),
        ("pink","☼","Use LED lighting and switch off unnecessary lights."),
        ("green","⏻","Turn off unused electronics and avoid needless standby use."),
        ("yellow","❧","Look for energy-efficiency labels when buying new appliances."),
    ]
    for start in (0,3):
        cols=st.columns(3)
        for col,(shade,icon,tip) in zip(cols,tips[start:start+3]):
            with col: st.markdown(f'<div class="sticky {shade}"><b>{icon}</b>{html.escape(tip)}</div>',unsafe_allow_html=True)
        st.write("")
    if st.button("← Back to Results",type="primary"): navigate("Results")
