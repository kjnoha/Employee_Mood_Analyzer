import os
import pandas as pd
from datetime import datetime, timedelta


DATA_FILE_NAME = 'employee_mood_logs.csv'
COLUMNS = ['timestamp', 'employee_id', 'text_input', 'detected_emotion',
           'emotion_category', 'emotion_score', 'suggestion_given']


class DataLogger:
    """Handles reading/writing mood log data to CSV with analytics support."""

    def __init__(self, data_dir=None):
        if data_dir is None:
            # Resolve relative to THIS file's directory -> ../data
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, 'data')
        self.data_dir = data_dir
        self.file_path = os.path.join(self.data_dir, DATA_FILE_NAME)
        self._ensure_data_file_exists()

    def _ensure_data_file_exists(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.file_path):
            empty_df = pd.DataFrame(columns=COLUMNS)
            empty_df.to_csv(self.file_path, index=False)

    def _read_csv(self):
        """Safely read the CSV file."""
        try:
            if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
                return pd.DataFrame(columns=COLUMNS)
            df = pd.read_csv(self.file_path, dtype={
                'employee_id': str,
                'emotion_score': float,
            })
            # Ensure the emotion_category column exists (backward compat)
            if 'emotion_category' not in df.columns:
                df['emotion_category'] = df['detected_emotion'].apply(
                    lambda e: 'positive' if e in ('positive', 'happy', 'motivated', 'confident')
                    else 'negative' if e in ('negative', 'sad', 'stressed', 'frustrated', 'anxious', 'angry', 'tired')
                    else 'neutral'
                )
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return pd.DataFrame(columns=COLUMNS)

    def log_entry(self, employee_id, text, emotion, score, suggestion, category="neutral"):
        """Log a mood entry to the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        employee_id_str = str(employee_id).strip()

        new_log_data = {
            'timestamp': timestamp,
            'employee_id': employee_id_str,
            'text_input': str(text).strip(),
            'detected_emotion': str(emotion).strip(),
            'emotion_category': str(category).strip(),
            'emotion_score': float(score),
            'suggestion_given': str(suggestion).strip()
        }
        new_log = pd.DataFrame([new_log_data], columns=COLUMNS)

        try:
            df = self._read_csv()
            df = pd.concat([df, new_log], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            return True
        except Exception as e:
            print(f"Error logging entry: {e}")
            return False

    def get_logs(self, employee_id=None, limit=None):
        """Get log entries, optionally filtered by employee ID."""
        df = self._read_csv()
        if employee_id:
            employee_id_str = str(employee_id).strip()
            df = df[df['employee_id'] == employee_id_str]
        if limit:
            df = df.tail(limit)
        return df

    def get_employee_mood_summary(self, employee_id):
        """Get average mood score and entry count for an employee."""
        employee_id_str = str(employee_id).strip()
        logs = self.get_logs(employee_id=employee_id_str)

        if logs.empty or 'emotion_score' not in logs.columns:
            return None, 0

        logs['emotion_score'] = pd.to_numeric(logs['emotion_score'], errors='coerce')
        logs = logs.dropna(subset=['emotion_score'])

        if logs.empty:
            return None, 0
        return logs['emotion_score'].mean(), len(logs)

    def get_all_employee_ids(self):
        """Return a sorted list of unique employee IDs."""
        df = self._read_csv()
        if df.empty:
            return []
        return sorted(df['employee_id'].dropna().unique().tolist())

    def get_mood_trends(self, employee_id=None, days=30):
        """Get mood trends over time for charting."""
        df = self._read_csv()
        if df.empty:
            return []

        if employee_id:
            df = df[df['employee_id'] == str(employee_id).strip()]

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        cutoff = datetime.now() - timedelta(days=days)
        df = df[df['timestamp'] >= cutoff]

        if df.empty:
            return []

        df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d')
        daily = df.groupby('date').agg(
            avg_score=('emotion_score', 'mean'),
            count=('emotion_score', 'count'),
            dominant_emotion=('detected_emotion', lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown')
        ).reset_index()

        return daily.to_dict('records')

    def get_emotion_distribution(self, employee_id=None):
        """Get emotion distribution for pie/donut charts."""
        df = self._read_csv()
        if df.empty:
            return {}

        if employee_id:
            df = df[df['employee_id'] == str(employee_id).strip()]

        if df.empty:
            return {}

        return df['detected_emotion'].value_counts().to_dict()

    def get_team_stats(self):
        """Get team-level statistics: total entries, avg score, active members."""
        df = self._read_csv()
        if df.empty:
            return {
                'total_entries': 0,
                'avg_score': 0,
                'active_members': 0,
                'most_common_emotion': 'N/A',
            }

        return {
            'total_entries': len(df),
            'avg_score': round(df['emotion_score'].mean(), 2),
            'active_members': df['employee_id'].nunique(),
            'most_common_emotion': df['detected_emotion'].mode().iloc[0] if not df['detected_emotion'].mode().empty else 'N/A',
        }

    def delete_entry(self, timestamp, employee_id):
        """Delete a specific log entry."""
        df = self._read_csv()
        mask = (df['timestamp'] == timestamp) & (df['employee_id'] == str(employee_id).strip())
        df = df[~mask]
        df.to_csv(self.file_path, index=False)
        return True