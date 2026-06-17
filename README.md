# Employee Mood Analyzer

A Flask-based web application that analyzes employee mood/sentiment data and visualizes the results through charts and dashboards.

## Project Overview

This project provides a way to track and analyze employee mood data, presenting the results through a web interface with interactive charts. It is built with Python (Flask) on the backend and HTML/CSS/JavaScript on the frontend.

## Project Structure

```
├── data/                   # Mood/sentiment dataset(s)
├── presentation_charts/     # Pre-generated charts for presentations/reports
├── src/                      # Core source code/logic
├── static/                    # CSS, JS, and other static assets
├── templates/                  # HTML templates rendered by Flask
├── app.py                       # Main Flask application
├── main.py                       # Entry point / orchestration script
├── export_charts.py               # Script to generate and export mood analysis charts
├── requirements.txt                # Python dependencies
└── .gitignore
```

## How It Works

1. Mood-related data is stored/loaded from the `data/` folder.
2. `main.py` and `src/` handle the core analysis logic.
3. `export_charts.py` generates visualizations, which are saved to `presentation_charts/`.
4. `app.py` serves the Flask web app, rendering results via `templates/` and `static/` assets.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/kjnoha/Employee_Mood_Analyzer.git
   cd Employee_Mood_Analyzer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser at `http://localhost:5000` (default Flask port) to view the dashboard.

## Generating Charts

To regenerate presentation-ready charts from the mood data:
```bash
python export_charts.py
```
Output charts will be saved in the `presentation_charts/` folder.

## Tech Stack

- **Python / Flask** — backend and app logic
- **HTML, CSS, JavaScript** — frontend templates and interactivity
- **Data visualization libraries** (e.g., Matplotlib/Plotly — see `requirements.txt` for specifics)

## Author

**kjnoha**
GitHub: [github.com/kjnoha](https://github.com/kjnoha)
