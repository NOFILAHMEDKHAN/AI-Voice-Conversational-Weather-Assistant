import streamlit as st
from speech_weather import speak, listen, extract_city, get_weather, generate_ai_response

def process_user_input(user_input, weather_key, gemini_key):
    if any(word in user_input.lower() for word in ['quit', 'exit', 'stop', 'bye']):
        farewell = "Goodbye! Have a nice day!"
        st.session_state.conversation.append({"type": "assistant", "content": farewell})
        speak(farewell)
        st.session_state.continuous_mode = False
        st.session_state.listening = False
    else:
        city = extract_city(user_input)
        if city:
            st.session_state.conversation.append({"type": "assistant", "content": f"Getting weather for {city}..."})
            weather_data, error = get_weather(city, weather_key)
            if weather_data:
                st.session_state.last_city = {
                    'name': city,
                    'temp': weather_data['temp'],
                    'feels_like': weather_data['feels_like'],
                    'desc': weather_data['desc'],
                    'humidity': weather_data['humidity'],
                    'wind_speed': weather_data['wind_speed'],
                    'pressure': weather_data['pressure'],
                    'country': weather_data['country'],
                    'visibility': weather_data['visibility']
                }
                ai_response = generate_ai_response(city, weather_data, gemini_key)
                if st.session_state.continuous_mode:
                    follow_up = "\n\nI'm still listening... Say another city name or 'stop' to end."
                else:
                    follow_up = "\n\nWhich city would you like to check next?"
                full_response = ai_response + follow_up
                st.session_state.conversation.append({"type": "assistant", "content": full_response})
                speak(full_response)
            else:
                st.session_state.conversation.append({"type": "assistant", "content": error})
                speak(error)
        else:
            error_msg = "I couldn't detect a city name. Try saying something like 'weather in Paris' or just 'London'."
            st.session_state.conversation.append({"type": "assistant", "content": error_msg})
            speak(error_msg)

st.set_page_config(page_title="🌤️ Weather Assistant", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        color: #4A90E2;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-bubble {
        background-color: #f8f9fa;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        font-size: 1rem;
        line-height: 1.5;
        border-left: 4px solid #4A90E2;
    }
    .user-bubble {
        background-color: #e3f2fd;
        padding: 1rem 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0 0.8rem 15%;
        font-size: 1rem;
        border-right: 4px solid #2196f3;
    }
    .weather-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton button {
        border-radius: 10px;
        height: 3em;
        font-size: 1rem;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3436;
        margin: 1.5rem 0 1rem 0;
    }
    .continuous-mode {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🌤️ Weather Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Speak naturally to get weather information</div>", unsafe_allow_html=True)

try:
    with open("weather_key.txt") as f:
        weather_key = f.read().strip()
    with open("gemini_key.txt") as f:
        gemini_key = f.read().strip()
except Exception as e:
    st.error(f"Error loading API keys: {e}")
    weather_key = None
    gemini_key = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_city" not in st.session_state:
    st.session_state.last_city = None
if "continuous_mode" not in st.session_state:
    st.session_state.continuous_mode = False
if "listening" not in st.session_state:
    st.session_state.listening = False

if not st.session_state.conversation:
    greeting = "Hello! I'm your Weather Assistant! Click 'Start Continuous Mode' for hands-free operation or use single voice input."
    st.session_state.conversation.append({"type": "assistant", "content": greeting})
    speak(greeting)

for msg in st.session_state.conversation:
    bubble = "user-bubble" if msg["type"] == "user" else "chat-bubble"
    label = "You" if msg["type"] == "user" else "Assistant"
    st.markdown(f"<div class='{bubble}'><strong>{label}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

if st.session_state.last_city:
    city = st.session_state.last_city
    st.markdown(f"""
    <div class='weather-card'>
        <h3>📍 {city['name']}, {city['country']}</h3>
        <h1>{city['temp']}°C</h1>
        <p>Feels like {city['feels_like']}°C • {city['desc'].title()}</p>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;'>
            <div>💧 Humidity: {city['humidity']}%</div>
            <div>💨 Wind: {city['wind_speed']} m/s</div>
            <div>📊 Pressure: {city['pressure']} hPa</div>
            <div>👁️ Visibility: {city['visibility']}m</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.session_state.continuous_mode:
        if st.button("🛑 Stop Continuous Mode", use_container_width=True, type="primary"):
            st.session_state.continuous_mode = False
            st.session_state.listening = False
            stop_msg = "Continuous mode stopped. You can now use single voice inputs."
            st.session_state.conversation.append({"type": "assistant", "content": stop_msg})
            speak(stop_msg)
            st.rerun()
    else:
        if st.button("🔄 Start Continuous Mode", use_container_width=True, type="primary"):
            st.session_state.continuous_mode = True
            st.session_state.listening = True
            continuous_msg = "Continuous mode started! I'm listening for your commands. Say any city name or 'stop' to end."
            st.session_state.conversation.append({"type": "assistant", "content": continuous_msg})
            speak(continuous_msg)
            st.rerun()

with col2:
    if not st.session_state.continuous_mode:
        if st.button("🎤 Single Voice Input", use_container_width=True):
            with st.spinner("Listening..."):
                user_input = listen()

            if user_input:
                st.session_state.conversation.append({"type": "user", "content": user_input})
                process_user_input(user_input, weather_key, gemini_key)
            else:
                error_msg = "Sorry, I didn't catch that. Please try again."
                st.session_state.conversation.append({"type": "assistant", "content": error_msg})
                speak(error_msg)
            st.rerun()

if st.session_state.continuous_mode and st.session_state.listening:
    with st.spinner("🔊 Continuous listening... Speak now!"):
        user_input = listen()
        
        if user_input:
            st.session_state.conversation.append({"type": "user", "content": user_input})
            process_user_input(user_input, weather_key, gemini_key)
            
            if not any(word in user_input.lower() for word in ['stop', 'quit', 'exit', 'end']):
                st.session_state.listening = True
            else:
                st.session_state.continuous_mode = False
                st.session_state.listening = False
                farewell = "Continuous mode ended. Thank you!"
                st.session_state.conversation.append({"type": "assistant", "content": farewell})
                speak(farewell)
            
            st.rerun()

st.markdown("---")
st.markdown("### Quick Cities")
quick_cities = ["Karachi", "London", "Tokyo", "New York", "Paris", "Dubai"]
cols = st.columns(3)
for idx, city in enumerate(quick_cities):
    with cols[idx % 3]:
        if st.button(f"📍 {city}", key=f"quick_{city}", use_container_width=True):
            weather_data, error = get_weather(city, weather_key)
            if weather_data:
                st.session_state.last_city = {
                    'name': city,
                    'temp': weather_data['temp'],
                    'feels_like': weather_data['feels_like'],
                    'desc': weather_data['desc'],
                    'humidity': weather_data['humidity'],
                    'wind_speed': weather_data['wind_speed'],
                    'pressure': weather_data['pressure'],
                    'country': weather_data['country'],
                    'visibility': weather_data['visibility']
                }
                ai_response = generate_ai_response(city, weather_data, gemini_key)
                follow_up = "\n\nWhich city would you like to check next?"
                full_response = ai_response + follow_up
                st.session_state.conversation.append({"type": "assistant", "content": full_response})
                speak(full_response)
            else:
                st.session_state.conversation.append({"type": "assistant", "content": error})
                speak(error)
            st.rerun()

if st.button("Clear Chat", use_container_width=True):
    st.session_state.conversation = []
    st.session_state.last_city = None
    st.session_state.continuous_mode = False
    st.session_state.listening = False
    st.rerun()

st.markdown("---")
st.markdown("### How to use:")
st.markdown("""
- **Continuous Mode**: Click 'Start Continuous Mode' for hands-free operation
- **Single Input**: Click 'Single Voice Input' for one-time queries  
- **Quick Cities**: Click any city button for instant weather
- **Say 'stop'** to end continuous mode
""")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Powered by Nofil</div>", unsafe_allow_html=True)
