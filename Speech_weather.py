import speech_recognition as sr
import pyttsx3
import requests
import re
import google.generativeai as genai

def speak(text):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    """Listen for voice input and convert to text"""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except sr.WaitTimeoutError:
            return None
    except Exception as e:
        print(f"Listening error: {e}")
        return None

def extract_city(text):
    """Extract city name from user input with flexible patterns"""
    if not text:
        return None
    
    text = text.lower().strip()
    
    # Remove common weather-related words and filler words
    remove_words = [
        'weather', 'today', 'now', 'please', 'forecast', 'right', 'currently', 
        'outside', 'temperature', 'climate', 'what\'s', 'what', 'is', 'the',
        'in', 'for', 'at', 'of', 'like', 'how', 'about', 'tell', 'me',
        'can', 'you', 'give', 'get', 'show', 'display', 'information'
    ]
    
    for word in remove_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text)
    
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    
    # Common city patterns
    patterns = [
        r'weather\s+(?:in|for|at)\s+([a-zA-Z\s]+)',
        r'(?:in|for|at)\s+([a-zA-Z\s]+)(?:\s+weather)?',
        r'how\s+(?:is|are)\s+(?:the\s+)?weather\s+(?:in|at)\s+([a-zA-Z\s]+)',
        r'tell\s+me\s+(?:about|the\s+weather\s+in)\s+([a-zA-Z\s]+)',
        r'what\s+(?:\'s|is)\s+(?:the\s+)?weather\s+(?:like\s+)?(?:in|at)?\s*([a-zA-Z\s]+)',
        r'([a-zA-Z\s]+)(?:\s+weather|\s+forecast|\s+temperature)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            if city and len(city) > 1:  # Ensure it's a valid city name
                return city.title()
    
    # If no pattern matches, try to extract the last meaningful word
    words = [word for word in text.split() if word and len(word) > 1]
    
    # Common city names to prioritize
    common_cities = [
        'karachi', 'london', 'tokyo', 'paris', 'dubai', 'new york', 'mumbai',
        'delhi', 'istanbul', 'moscow', 'beijing', 'shanghai', 'sydney',
        'melbourne', 'toronto', 'vancouver', 'berlin', 'rome', 'madrid',
        'barcelona', 'los angeles', 'chicago', 'miami', 'boston', 'seattle'
    ]
    
    # Check for multi-word city names first
    for i in range(len(words) - 1):
        two_word_city = f"{words[i]} {words[i+1]}"
        if two_word_city.lower() in common_cities:
            return two_word_city.title()
    
    # Check for single word city names
    for word in words[::-1]:  # Start from the end
        if any(city.startswith(word.lower()) for city in common_cities):
            # Find the full city name
            for city in common_cities:
                if city.startswith(word.lower()):
                    return city.title()
        elif len(word) > 2:  # Only consider words with more than 2 characters
            return word.title()
    
    return None

def get_weather(city, api_key):
    """Get weather data from OpenWeatherMap API"""
    if not api_key:
        return None, "❌ Weather API key not found. Please check your weather_key.txt file."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 404 or data.get("cod") == "404":
            return None, f"❌ City '{city}' not found. Please check the spelling and try again."
        
        if response.status_code == 401:
            return None, "❌ Invalid API key. Please check your weather_key.txt file."
        
        if response.status_code == 200:
            return {
                'temp': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'desc': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'country': data['sys']['country'],
                'visibility': data.get('visibility', 0)
            }, None
        
        return None, f"⚠️ API Error: {data.get('message', 'Unknown error occurred')}"
    
    except requests.exceptions.Timeout:
        return None, "❌ Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "❌ Connection error. Please check your internet connection."
    except Exception as e:
        return None, f"❌ Error fetching weather: {str(e)}"

def generate_ai_response(city, weather_data, gemini_key):
    """Generate AI response using Gemini API"""
    if not gemini_key:
        # Fallback response if Gemini API key is not available
        return f"The weather in {city} is {weather_data['desc']} with a temperature of {weather_data['temp']}°C (feels like {weather_data['feels_like']}°C). Humidity is {weather_data['humidity']}% with wind speed of {weather_data['wind_speed']} m/s."
    
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        
        prompt = f"""
        You're a cheerful and friendly weather assistant. Create a short, natural weather update for {city} based on this data:
        
        - Temperature: {weather_data['temp']}°C
        - Feels like: {weather_data['feels_like']}°C
        - Condition: {weather_data['desc']}
        - Humidity: {weather_data['humidity']}%
        - Wind Speed: {weather_data['wind_speed']} m/s
        - Pressure: {weather_data['pressure']} hPa
        
        Keep it conversational and friendly (1-2 sentences). Include a brief practical suggestion based on the weather.
        Don't mention that you're an AI or assistant in the response.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback response
        return f"In {city}, it's {weather_data['desc']} with {weather_data['temp']}°C. Perfect weather for going out!"
