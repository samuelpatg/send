import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
 
st.set_page_config(
    page_title="MQTT Control",
    page_icon="🎛️",
    layout="centered",
)
 
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
 
    :root {
        --ink: #12263A;
        --ink-soft: #5B6B7B;
        --paper: #F3F6F9;
        --card: #FFFFFF;
        --line: #DCE4EC;
        --signal: #0E9F8E;
        --signal-soft: #E1F5F2;
        --alert: #D64545;
    }
 
    html, body, [class*="css"], .stApp { font-family: 'Manrope', system-ui, sans-serif; }
 
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: var(--paper) !important;
        color: var(--ink) !important;
    }
    .block-container { padding-top: 2rem; max-width: 760px; }
 
    header[data-testid="stHeader"] { background: transparent !important; }
    header[data-testid="stHeader"] * { color: var(--ink) !important; fill: var(--ink) !important; }
 
    .stApp p, .stApp label, .stApp li, .stApp h2, .stApp h3,
    [data-testid="stWidgetLabel"] p { color: var(--ink) !important; }
 
    .hero {
        background: var(--ink);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
    }
    .stApp .hero h1 {
        color: #FFFFFF !important;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.3rem 0;
        padding: 0;
    }
    .stApp .hero p { color: #B9C7D5 !important; margin: 0 0 1rem 0; font-size: 0.95rem; }
    .chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .stApp .chip {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        color: #E6EEF5 !important;
        border-radius: 999px;
        padding: 0.25rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
 
    .stApp .section-title {
        color: var(--ink) !important;
        font-weight: 800;
        font-size: 1.15rem;
        margin: 1.6rem 0 0.2rem 0;
    }
    .stApp .section-sub {
        color: var(--ink-soft) !important;
        font-size: 0.88rem;
        margin: 0 0 0.8rem 0;
    }
 
    .state {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.8rem 1.1rem;
        margin-top: 0.8rem;
        font-weight: 600;
    }
    .stApp .state { color: var(--ink) !important; }
    .dot { width: 10px; height: 10px; border-radius: 50%; background: #AAB6C2; flex-shrink: 0; }
    .state.on .dot { background: var(--signal); }
    .state.off .dot { background: var(--alert); }
    .state .tag {
        margin-left: auto;
        border-radius: 999px;
        padding: 0.15rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 800;
        background: #EEF2F6;
    }
    .stApp .state.on .tag { background: var(--signal-soft); color: #0A6B5F !important; }
    .stApp .state.off .tag { background: #FBE9E9; color: #9B2C2C !important; }
 
    .valuecard {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.3rem;
        margin: 0.4rem 0 0.8rem 0;
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
    }
    .stApp .valuecard .label { color: var(--ink-soft) !important; font-weight: 600; font-size: 0.9rem; }
    .stApp .valuecard .value {
        color: var(--ink) !important;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        font-variant-numeric: tabular-nums;
        margin-left: auto;
    }
 
    .stButton > button {
        border: none;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        background: var(--signal);
        transition: filter 0.15s ease;
    }
    .stButton > button, .stButton > button p, .stButton > button span { color: #FFFFFF !important; }
    .stButton > button:hover { filter: brightness(0.92); border: none; }
    .st-key-btn_off button { background: var(--alert); }
    .st-key-btn_analog button { background: var(--ink); }
 
    [data-testid="stSlider"] [role="slider"] { background: var(--signal) !important; box-shadow: none !important; }
    [data-testid="stSliderThumbValue"], [data-testid="stSliderThumbValue"] *,
    [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] { color: var(--ink) !important; }
 
    div[data-testid="stAlert"] { background: var(--signal-soft) !important; border-radius: 12px; }
    div[data-testid="stAlert"] p { color: #0A6B5F !important; }
 
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)
 
values = 0.0
act1 = "OFF"
 
 
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass
 
 
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)
 
 
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("samuel")
client1.on_message = on_message
 
if "last_act" not in st.session_state:
    st.session_state.last_act = None
 
st.markdown(
    f"""
    <div class="hero">
        <h1>🎛️ MQTT Control</h1>
        <p>Envía órdenes y valores analógicos a tu dispositivo por MQTT.</p>
        <div class="chips">
            <span class="chip">Broker: {broker}</span>
            <span class="chip">Puerto: {port}</span>
            <span class="chip">Python {platform.python_version()}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
 
st.markdown(
    '<div class="section-title">💡 Actuador</div>'
    '<div class="section-sub">Enciende o apaga el actuador 1 (tópico: enviar1)</div>',
    unsafe_allow_html=True,
)
 
col_on, col_off = st.columns(2)
 
with col_on:
    if st.button("ON", key="btn_on", use_container_width=True):
        act1 = "ON"
        client1 = paho.Client("samuel")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("enviar1", message)
        st.session_state.last_act = "ON"
 
with col_off:
    if st.button("OFF", key="btn_off", use_container_width=True):
        act1 = "OFF"
        client1 = paho.Client("samuel")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("enviar1", message)
        st.session_state.last_act = "OFF"
 
last = st.session_state.last_act
if last:
    st.markdown(
        f"""
        <div class="state {last.lower()}">
            <span class="dot"></span>
            <span>Última orden enviada</span>
            <span class="tag">{last}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="state">
            <span class="dot"></span>
            <span>Aún no se ha enviado ninguna orden</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
st.markdown(
    '<div class="section-title">🎚️ Valor analógico</div>'
    '<div class="section-sub">Elige un valor entre 0 y 100 y envíalo (tópico: enviar)</div>',
    unsafe_allow_html=True,
)
 
values = st.slider("Selecciona el rango de valores", 0.0, 100.0)
 
st.markdown(
    f"""
    <div class="valuecard">
        <span class="label">Valor seleccionado</span>
        <span class="value">{values:.1f}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
 
if st.button("Enviar valor analógico", key="btn_analog", use_container_width=True):
    client1 = paho.Client("samuel")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("enviar", message)
    st.success(f"Valor {values:.1f} enviado correctamente", icon="✅")
 
