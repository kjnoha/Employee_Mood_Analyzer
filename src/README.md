# Zidio Task Optimizer ⚡

> **Mood-driven productivity intelligence for teams.**
> Analyze employee emotions, get personalized task recommendations, and track team wellness trends — all powered by NLP sentiment analysis.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🧠 Mood Analysis** | VADER-powered sentiment analysis with 10 granular emotion categories |
| **📋 Task Optimization** | Mood-based task priority, focus area, and time-block recommendations |
| **📈 Trend Dashboard** | Interactive Plotly charts showing mood trends over time |
| **🍩 Emotion Distribution** | Donut chart visualization of team emotion breakdown |
| **📝 Activity Feed** | Real-time feed of recent mood entries across the team |
| **👥 Team Analytics** | Aggregated statistics: avg score, active members, dominant mood |
| **🖥️ Web Dashboard** | Beautiful glassmorphic dark-mode UI built with Flask |
| **⌨️ CLI Mode** | Traditional command-line interface for quick logging |

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask** — Web framework
- **VADER Sentiment** — NLP sentiment analysis
- **Plotly.js** — Interactive charting
- **Pandas** — Data handling & CSV storage
- **NLTK** — Natural Language Toolkit

## 🚀 Quick Start

### 1. Clone & enter the project

```bash
cd zidio_task_optimizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the web dashboard

```bash
python app.py
```

Open your browser at **http://localhost:5000** 🎉

### 5. Or use CLI mode

```bash
python main.py
```

## 📁 Project Structure

```
zidio_task_optimizer/
├── app.py                  # Flask web application
├── main.py                 # CLI interface (backward compat)
├── requirements.txt
├── data/
│   └── employee_mood_logs.csv
├── src/
│   ├── __init__.py
│   ├── emotion_analyzer.py  # VADER + keyword emotion detection
│   ├── suggestion_engine.py # Mood-based task suggestions
│   ├── data_logger.py       # CSV data logging & analytics
│   └── README.md
├── static/
│   ├── css/style.css        # Glassmorphic dark-mode design
│   └── js/app.js            # Dashboard client logic
└── templates/
    └── dashboard.html       # Main dashboard template
```

## 🎨 Emotion Categories

| Emotion | Category | Icon | Task Priority |
|---------|----------|------|---------------|
| Happy | Positive | 😊 | High — creative & challenging |
| Motivated | Positive | 🔥 | High — complex & strategic |
| Confident | Positive | 💪 | High — leadership tasks |
| Calm | Neutral | 😌 | Medium — routine & planning |
| Stressed | Negative | 😰 | Low — break into small pieces |
| Frustrated | Negative | 😤 | Low — switch context |
| Anxious | Negative | 😟 | Low — small achievable wins |
| Sad | Negative | 😢 | Low — gentle tasks |
| Angry | Negative | 😡 | Low — physical/mechanical |
| Tired | Negative | 😴 | Low — admin & light tasks |

## 📄 License

MIT License — built for the Zidio internship program.