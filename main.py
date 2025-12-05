import os

# Create directory
os.makedirs('boss_weather', exist_ok=True)

# Write index.html
with open('boss_weather/index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boss Weather</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <h1>Boss Weather 🌟</h1>
        <p class="quirky">Your quirky, neon-powered weather pal for Aussie adventures! No data selling, all fun! 😎</p>
    </header>
    <section id="locations">
        <h2>Add Your Spots</h2>
        <input type="text" id="locationInput" placeholder="Enter postcode or city, NSW">
        <button onclick="addLocation()">Add Vibes</button>
        <ul id="locationsList"></ul>
    </section>
    <section id="controls">
        <button onclick="getWeatherForAll()">Fetch the Magic ✨</button>
        <button onclick="toggleTheme()">Switch Mood</button>
    </section>
    <div id="weatherDisplay"></div>
    <footer>
        <p>Powered by BOM Australia via Open-Meteo. Privacy first! Custom for you, boss lady. 💜</p>
    </footer>
    <script src="script.js"></script>
</body>
</html>''')

# Write style.css (unchanged, expanded previously)
with open('boss_weather/style.css', 'w') as f:
    f.write('''@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

body {
    font-family: 'Fredoka One', cursive;
    background-color: #f3e5f5; /* Light purple */
    color: #4a148c; /* Deep purple */
    text-align: center;
    padding: 20px;
    transition: background-color 0.5s;
}
body.neon {
    background-color: #12005e; /* Dark for neon contrast */
    color: #e040fb;
}
h1 {
    color: #ab47bc;
    text-shadow: 0 0 10px #e040fb; /* Neon glow */
    font-size: 3em;
    animation: glow 1.5s infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 5px #e040fb; }
    to { text-shadow: 0 0 20px #e040fb, 0 0 30px #aa00ff; }
}
.quirky {
    font-style: italic;
    color: #7b1fa2;
    animation: bounce 2s infinite;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
input, button {
    margin: 10px;
    padding: 12px;
    font-size: 18px;
    border: 2px solid #ba68c8;
    border-radius: 20px; /* Cartoon round */
    background-color: #ede7f6;
    color: #6a1b9a;
    box-shadow: 0 0 10px #e040fb; /* Neon */
    transition: transform 0.2s;
}
button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #aa00ff;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    background: #e1bee7;
    margin: 10px auto;
    padding: 15px;
    border: 1px solid #9c27b0;
    border-radius: 15px;
    width: 80%;
    max-width: 400px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.weather-card {
    background: #f3e5f5;
    margin: 20px auto;
    padding: 25px;
    border: 2px dashed #7b1fa2; /* Quirky dashed */
    border-radius: 25px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 8px rgba(106,27,154,0.2);
    animation: fadeIn 1s;
}
.weather-card h2 {
    color: #8e24aa;
    text-shadow: 0 0 5px #e040fb;
}
.weather-card p {
    font-size: 1.2em;
}
.forecast {
    margin-top: 20px;
    border-top: 1px solid #ba68c8;
    padding-top: 10px;
}
.fun-fact {
    font-style: italic;
    color: #6a1b9a;
    margin-top: 15px;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
footer {
    margin-top: 30px;
    font-size: 0.8em;
    color: #4a148c;
}''')

# Write script.js with BOM reference
with open('boss_weather/script.js', 'w') as f:
    f.write('''let locations = JSON.parse(localStorage.getItem('locations')) || ['Coffs Harbour, NSW', 'Urunga, NSW', 'Bateau Bay, NSW']; // Preloaded: 2450, 2457 (assuming Urunga nearby), 2261

function updateLocationsList() {
    const list = document.getElementById('locationsList');
    list.innerHTML = '';
    locations.forEach((loc, index) => {
        const li = document.createElement('li');
        li.textContent = loc;
        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Bye!';
        removeBtn.onclick = () => removeLocation(index);
        li.appendChild(removeBtn);
        list.appendChild(li);
    });
}

function addLocation() {
    const input = document.getElementById('locationInput');
    const loc = input.value.trim();
    if (loc && !locations.includes(loc)) {
        locations.push(loc);
        localStorage.setItem('locations', JSON.stringify(locations));
        updateLocationsList();
    }
    input.value = '';
}

function removeLocation(index) {
    locations.splice(index, 1);
    localStorage.setItem('locations', JSON.stringify(locations));
    updateLocationsList();
}

function toggleTheme() {
    document.body.classList.toggle('neon');
}

async function getWeatherForAll() {
    const display = document.getElementById('weatherDisplay');
    display.innerHTML = '';
    const funFacts = [
        "Did you know? In Australia, it can rain fish! 🐟",
        "Weather tip: Always carry sunnies, mate! 😎",
        "Quirky fact: Penguins in Antarctica check weather too! 🐧",
        "Boss advice: Dance in the rain! 💃",
        "Unique vibe: Neon skies incoming! 🌌"
    ];
    for (const loc of locations) {
        try {
            const geoUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(loc + ', Australia')}&format=json&limit=1`;
            const geoResponse = await fetch(geoUrl);
            const geoData = await geoResponse.json();
            if (geoData.length === 0) throw new Error('Spot not found, boss!');
            const { lat, lon } = geoData[0];

            const weatherUrl = `https://api.open-meteo.com/v1/bom?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Australia%2FSydney`;
            const weatherResponse = await fetch(weatherUrl);
            const weatherData = await weatherResponse.json();
            const hourly = weatherData.hourly;
            const daily = weatherData.daily;

            // Get current weather: find closest hour
            const now = new Date();
            const currentHour = now.toISOString().slice(0, 13) + ':00';
            let currentIndex = hourly.time.findIndex(t => t >= currentHour);
            if (currentIndex === -1) currentIndex = hourly.time.length - 1; // Fallback
            if (currentIndex < 0) throw new Error('No current data');

            const current = {
                temperature_2m: hourly.temperature_2m[currentIndex],
                relative_humidity_2m: hourly.relative_humidity_2m[currentIndex],
                apparent_temperature: hourly.apparent_temperature[currentIndex],
                precipitation: hourly.precipitation[currentIndex],
                weather_code: hourly.weather_code[currentIndex],
                cloud_cover: hourly.cloud_cover[currentIndex],
                wind_speed_10m: hourly.wind_speed_10m[currentIndex],
                wind_direction_10m: hourly.wind_direction_10m[currentIndex],
                wind_gusts_10m: hourly.wind_gusts_10m[currentIndex]
            };

            const weatherCodes = {
                0: 'Clear sky ☀️ - Perfect for beach vibes!',
                1: 'Mainly clear 🌤️ - Light and breezy!',
                2: 'Partly cloudy ⛅ - A bit quirky today!',
                3: 'Overcast ☁️ - Cozy up time!',
                45: 'Fog 🌫️ - Mysterious neon mist!',
                51: 'Light drizzle 🌦️ - Sparkly drops!',
                61: 'Slight rain 🌧️ - Dance party!',
                71: 'Light snow ❄️ - Rare Aussie treat!',
                80: 'Showers 🚿 - Freshen up!',
                95: 'Thunderstorm ⚡ - Electric neon show!',
                // Expanded codes
            };
            const desc = weatherCodes[current.weather_code] || 'Mystery weather! 🕵️';

            const card = document.createElement('div');
            card.className = 'weather-card';
            card.innerHTML = `<h2>${loc} Vibes</h2>
                <p>${desc}</p>
                <p>Temp: ${current.temperature_2m}°C (Feels: ${current.apparent_temperature}°C)</p>
                <p>Humidity: ${current.relative_humidity_2m}% 💧</p>
                <p>Wind: ${current.wind_speed_10m} km/h 🌬️ from ${current.wind_direction_10m}°</p>
                <p>Precip: ${current.precipitation} mm ☔</p>
                <div class="forecast">
                    <h3>Next Days Forecast 📅</h3>`;
            for (let i = 1; i < 3; i++) { // Next 2 days
                const dayDesc = weatherCodes[daily.weather_code[i]] || 'Unknown';
                card.innerHTML += `<p>Day ${i}: ${dayDesc} High: ${daily.temperature_2m_max[i]}°C Low: ${daily.temperature_2m_min[i]}°C</p>`;
            }
            card.innerHTML += `</div>
                <p class="fun-fact">${funFacts[Math.floor(Math.random() * funFacts.length)]}</p>`;
            display.appendChild(card);
        } catch (error) {
            console.error(error);
            const card = document.createElement('div');
            card.className = 'weather-card';
            card.innerHTML = `<h2>${loc}</h2><p>Oops! Weather gremlins: ${error.message} 🤪</p>`;
            display.appendChild(card);
        }
    }
}

updateLocationsList();''')

print("Expanded Boss Weather folder created with BOM Australia reference via Open-Meteo API.")
