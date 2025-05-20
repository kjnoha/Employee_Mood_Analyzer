import os
import pandas as pd
from datetime import datetime

DATA_FILE_NAME = 'employee_mood_logs.csv'
COLUMNS = ['timestamp', 'employee_id', 'text_input', 'detected_emotion', 'emotion_score', 'suggestion_given']

class DataLogger:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.file_path = os.path.join(self.data_dir, DATA_FILE_NAME)
        self._ensure_data_file_exists()

    def _ensure_data_file_exists(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.file_path):
            # Define dtypes for an empty DataFrame to help with concat later
            empty_df = pd.DataFrame(columns=COLUMNS).astype({
                'timestamp': 'object',  # Or 'datetime64[ns]' if you parse it on read
                'employee_id': 'object', # Store as string/object
                'text_input': 'object',
                'detected_emotion': 'object',
                'emotion_score': 'float64',
                'suggestion_given': 'object'
            })
            empty_df.to_csv(self.file_path, index=False)

    def log_entry(self, employee_id, text, emotion, score, suggestion):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure employee_id is treated as a string consistently for logging
        employee_id_str = str(employee_id).strip()

        new_log_data = {
            'timestamp': timestamp,
            'employee_id': employee_id_str, # Use stripped string version
            'text_input': str(text).strip(),
            'detected_emotion': str(emotion).strip(),
            'emotion_score': float(score),
            'suggestion_given': str(suggestion).strip()
        }
        new_log = pd.DataFrame([new_log_data], columns=COLUMNS)

        try:
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                # When reading, explicitly set employee_id to string type
                df = pd.read_csv(self.file_path, dtype={'employee_id': str})
            else:
                # If file was just created empty or is truly empty, start with a correctly typed DataFrame
                df = pd.DataFrame(columns=COLUMNS).astype({
                    'employee_id': 'object', # or str
                    'emotion_score': 'float64'
                    # define others if necessary
                })
            
            # Before concat, ensure new_log also has compatible types, especially for crucial columns
            new_log = new_log.astype(df.dtypes.to_dict(), errors='ignore')

            df = pd.concat([df, new_log], ignore_index=True)
            df.to_csv(self.file_path, index=False)
            # print(f"Entry logged successfully for {employee_id_str}.") # Keep console cleaner in main
        except Exception as e:
            print(f"Error logging entry: {e}")

    def get_logs(self, employee_id=None):
        try:
            if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
                return pd.DataFrame(columns=COLUMNS)

            # Read CSV, ensuring employee_id is treated as string for consistent filtering
            df = pd.read_csv(self.file_path, dtype={'employee_id': str, 'emotion_score': float})
            
            if employee_id:
                # Ensure the filter value is also a stripped string
                employee_id_filter_str = str(employee_id).strip()
                # Debugging print statements:
                # print(f"Filtering for employee_id: '{employee_id_filter_str}' (type: {type(employee_id_filter_str)})")
                # print("Employee IDs in DataFrame sample:")
                # print(df['employee_id'].head().apply(lambda x: (x, type(x))))
                
                # Perform the filter
                filtered_df = df[df['employee_id'] == employee_id_filter_str]
                return filtered_df
            return df
        except Exception as e:
            print(f"Error retrieving logs: {e}")
            return pd.DataFrame(columns=COLUMNS)

    def get_employee_mood_summary(self, employee_id):
        # Ensure employee_id is a stripped string before passing to get_logs
        employee_id_str = str(employee_id).strip()
        logs = self.get_logs(employee_id=employee_id_str) # Use the string version for consistency
        
        if logs.empty or 'emotion_score' not in logs.columns:
            return None, 0

        # 'emotion_score' should already be float due to dtype in read_csv or log_entry
        # but an explicit conversion with error handling is safer if data could be corrupted
        logs['emotion_score'] = pd.to_numeric(logs['emotion_score'], errors='coerce')
        logs.dropna(subset=['emotion_score'], inplace=True)

        if logs.empty:
            return None, 0
        return logs['emotion_score'].mean(), len(logs)