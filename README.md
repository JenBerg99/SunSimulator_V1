
# ☀️ Sun Simulator API

A FastAPI-based backend that simulates **sunlight properties** based on **location, time, and weather conditions**. The API calculates solar elevation, brightness, color temperature, and RGB color representations to mimic real-world lighting scenarios.

---

## 🚀 Features

- 🌤️ Simulate sunlight based on:
  - Sun elevation and azimuth
  - Cloud coverage and weather
  - Time of day (sunrise/sunset)
- 🔁 Dynamically update or fetch simulation state
- 🧠 Internal caching for current global model
- 📊 Outputs realistic brightness (0–100%), color temperature (Kelvin), and RGB values
- 📘 Auto-generated documentation via FastAPI (`/docs`)

---

## 📦 Tech Stack

- **Python 3.11+**
- **FastAPI** – REST framework
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server

---

## 📂 Project Structure

```bash
.
├── main.py                   # Entry point
├── api.py                    # API routes
├── cache.py                  # Global cache state (thread-safe)
├── services.py               # Sunlight calculation logic
├── models/                   # Pydantic data models
│   ├── CompleteModel.py
│   ├── SunLightProperties.py
│   ├── SunPosition.py
│   ├── TimeSettings.py
│   └── WeatherInfo.py
├── rpi/                      # Services used for communicate with Raspberry Pi
│   ├── led_service.py        # Service to controll the LED Strip
│   ├── rotary_service.py     # Service to controll the rotary and the menu 
│   ├── lcd/                  # Services for the LCD Screen 
│     ├── Adafruit_LCD1602.py # Default file from manufacturer
│     ├── PCF8574.py          # Default file from manufacturer
│     ├── I2CLCD1602.py       # File to set Text to LCD Screen
```

---

## 🔌 API Endpoints

### 🌞 `/sunlight-properties`

- `GET` – Get current calculated sunlight properties
- `PUT` – Manually set sunlight properties

### 📦 `/complete-model`

- `GET` – Get the full model (weather, time, position, sunlight)
- `PUT` – Submit minimal input to recalculate sunlight values

---

## 🧠 Sunlight Calculation Overview

Implemented in `services.py`:

- **Brightness** is calculated based on:
  - `sin(elevation)` – simulates the physical intensity of sunlight
  - Cloud attenuation:  
    ```python
    cloud_factor = (1 - cloud_coverage / 100) ** 2
    ```
    This non-linear formula reflects that:
    - Thin clouds reduce light only slightly
    - Heavy overcast blocks most sunlight
    - It better matches how brightness is perceived by humans

- **Color Temperature (Kelvin)**:
  - Ranges from `2000K` (sunrise/sunset) to `6500K` (midday)
  - Linearly interpolated based on solar elevation

- **RGB Conversion**:
  - Converts the calculated Kelvin temperature to an RGB color
  - Clamp-safe conversion based on well-known formulas

---

## ▶️ Run Locally

### 1. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access docs

- [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Example Input (PUT `/complete-model`)

```json
{
  "weatherinfo": {
    "visibility": 10000,
    "rain_mm": 0,
    "cloud_coverage_percent": 75
  },
  "timesettings": {
    "current_time": "15:30:00",
    "sunrise": "06:00:00",
    "sunset": "20:30:00"
  },
  "sunposition": {
    "elevation": 45.0,
    "azimuth": 180.0
  }
}
```

---

## 📘 Notes

- This app uses a **global in-memory cache**. No persistence layer is included.
- The root path `/` currently redirects to `/docs` for developer convenience.
- Designed as a simulation core – can be extended with geolocation, astronomical models, or UI.

---

## 📄 License

MIT – Use, modify, and integrate freely.
