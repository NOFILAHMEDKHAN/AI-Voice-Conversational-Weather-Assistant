# 🌤️ AI Conversational Weather Assistant

**AI Conversational Weather Assistant** is not your ordinary weather app —  
it’s a **human-like weather companion** that listens to your voice, understands your questions intelligently, responds in speech, and displays interactive text conversations — all in real time.  

 This assistant redefines how users interact with weather data — making weather insights **intuitive, conversational, and intelligent**.  
 It combines natural interaction, live data fetching, and stunning UI responsiveness into one smooth experience.

---

## 🚀 Key Features

### 🎙️ **Conversational Voice Interaction**
Talk naturally — the AI *listens* to your voice, processes your query, and responds back in **clear speech**.  
You can ask questions like:
> “What’s the temperature in Karachi?”  
> “Do I need an umbrella today?”  
> “How’s the weather in Islamabad right now?”

It’s like having your personal weather expert — available anytime.

---

### 💬 **Dual-Mode Chat (Voice + Text)**
Each interaction appears beautifully in the UI — showing both user and agent messages.  
Even though the communication happens through voice, every response is logged visually for clarity and style.  
A seamless experience of **talk + see**.

---

### 🌆 **Quick City Access**
No need to type or speak every time!  
Just **tap a city name**, and it will instantly fetch and speak the live weather conditions for that city.  
A perfect touch for effortless exploration.

---

### 🌡️ **Real-Time Weather Insights**
- Live temperature, humidity, wind speed, and weather conditions  
- Data fetched from **OpenWeather API**  
- Adaptive responses that change with the situation — from sunny smiles to stormy alerts 🌩️

---

### 🧠 **Gemini-Powered Intelligence**
Integrated with **Google Gemini AI**, the assistant doesn’t just report numbers — it understands **context**.  
Ask “Is it good to go jogging today?” or “Should I carry a jacket?” — and it’ll respond smartly, not mechanically.

---

### 🎨 **Modern Streamlit Interface**
- Smooth, responsive, and beautifully aligned UI  
- Clean color palette and conversational layout  
- Text transitions for each response  
- Voice integration embedded directly in the interface

---

### 🔊 **Natural Text-to-Speech Output**
The agent speaks every response naturally — creating a real conversation experience.  
Combines **speech synthesis** with intelligent phrasing for realistic tone and flow.

---

### ⚡ **Robust Error Handling**
- Detects invalid cities gracefully  
- Handles missing network connections  
- Provides fallback prompts for re-inputs  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| 💻 Frontend/UI | Streamlit |
| 🧠 AI Model | Google Gemini API |
| 🌍 Weather Data | OpenWeather API |
| 🔊 Voice Output | pyttsx3 / gTTS |
| 🐍 Language | Python |
| 🎯 Mode | Real-time Voice + Text |

---

## 🔑 API Key Sources
To use the project, you’ll need two API keys:

| API | Source |
|------|---------|
| 🌤️ OpenWeather | [https://openweathermap.org/api](https://openweathermap.org/api) |
| 🤖 Google Gemini | [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

> Store both keys in **separate Python files in same folder** (for example: `weather_key.py` and `gemini_key.py`) for clean and secure integration.

---

## ⚙️ Installation & Setup

bash
# 1️⃣ Clone the Repository
```
git clone https://github.com/yourusername/AI-Weather-Assistant.git
cd AI-Weather-Assistant
```
# 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

# 3️⃣ Run the App
```
streamlit run app.py
Open your browser and navigate to:
👉 http://localhost:8501
```
---
## 💡 How It Works
The user speaks or types a weather-related query.

The assistant captures the voice input and converts it to text.

It fetches live weather data from the OpenWeather API.

Gemini AI interprets the question context and formulates an intelligent response.

The assistant speaks the answer and displays it as a chat message.

The user’s and agent’s dialogue is stored in the Streamlit chat window.

You can also click any preset city button for instant weather updates.

---
## 📊 Example Queries
User Query	Assistant Reply (Example)
“What’s the temperature in Lahore?”	“It’s currently 31°C in Lahore with light clouds and a gentle breeze.”
“Do I need an umbrella today?”	“Yes, expect some rain later today. Better keep one handy!”
“How’s Karachi right now?”	“It’s sunny and 29°C in Karachi — perfect beach weather.”
---
## 🔐 Notes & Limitations
❌ This project is for educational and research purposes.
🌍 Weather accuracy depends on the OpenWeather API.
🎤 Background noise can slightly affect speech recognition accuracy.
---
## 📈 Future Enhancements
🗓️ Add 3-day forecast support

🗺️ Integrate live maps and radar layers

🔊 Switch between male/female AI voices

🌐 Add multilingual voice support

💬 Enable memory-based conversation history
---
## 🤝 Contributing
Contributions are welcome!
If you want to improve the assistant, enhance the UI, or add new AI integrations:
---

bash
```
Copy code
# Fork → Create Branch → Commit → Push → Pull Request
```
---
## 👨‍💻 Author
Developed by: Nofil Ahmed Khan
📧 Email: nofil2012@gmail.com
🌐 LinkedIn: linkedin.com/in/khannofil
💬 Building practical AI projects that merge intelligence, interaction, and innovation.
---
## 📜 License
This project is open-source under the MIT License.

Created with 💙 by Nofil Ahmed Khan — where AI meets real human experience.
