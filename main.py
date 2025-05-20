import os
import sys

project_root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir_path = os.path.join(project_root_dir, "src")
if src_dir_path not in sys.path:
    sys.path.insert(0, src_dir_path)
try:
    from emotion_analyzer import TextEmotionAnalyzer
    from suggestion_engine import SuggestionEngine
    from data_logger import DataLogger
except ImportError as e:
    print(f"Error: Could not import custom modules from 'src'. Original error: {e}")
    print(f"Please ensure 'src' directory exists at: {src_dir_path}")
    print(f"And contains: __init__.py, emotion_analyzer.py, suggestion_engine.py, data_logger.py")
    sys.exit(1)

def check_and_download_nltk_data():
    try:
        from nltk.downloader import Downloader
        if not Downloader().is_installed('vader_lexicon'):
            import nltk
            print("NLTK 'vader_lexicon' not found. Downloading...")
            nltk.download('vader_lexicon')
            print("'vader_lexicon' downloaded successfully.")
    except Exception as e:
        print(f"Notice: Could not check/download NLTK 'vader_lexicon': {e}. If VADER fails, please install it manually.")

def log_mood_interaction(analyzer, suggester, logger):
    print("\n--- Log New Mood Entry ---")
    employee_id = input("Enter your Employee ID: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return

    text_input = input(f"Hi {employee_id}, how are you feeling or what's on your mind?\n> ").strip()
    if not text_input:
        print("No input provided.")
        return

    emotion, score = analyzer.get_emotion(text_input)
    suggestion = suggester.get_suggestion(emotion)

    print(f"\nAnalysis: Mood: {emotion.capitalize()} (Score: {score:.2f}), Suggestion: {suggestion}")
    logger.log_entry(employee_id, text_input, emotion, score, suggestion)
    print("Entry logged.")

def view_logs_interaction(logger):
    print("\n--- View Mood Logs ---")
    emp_id_filter = input("Enter Employee ID to filter by (or press Enter for all logs): ").strip()
    logs_df = logger.get_logs(employee_id=emp_id_filter if emp_id_filter else None)

    if not logs_df.empty:
        print("\n--- Log Entries ---")
        for _, row in logs_df.iterrows():
            print(f"[{row['timestamp']}] ID: {row['employee_id']}, Mood: {row['detected_emotion']} ({row['emotion_score']:.2f}), Input: '{row['text_input'][:30]}...'")
    else:
        print("No logs found matching your criteria.")

def mood_summary_interaction(logger):
    print("\n--- Employee Mood Summary ---")
    employee_id = input("Enter Employee ID for mood summary: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return

    avg_score, count = logger.get_employee_mood_summary(employee_id)
    if count > 0 and avg_score is not None:
        mood_desc = "Positive" if avg_score >= 0.05 else "Negative" if avg_score <= -0.05 else "Neutral"
        print(f"\nSummary for {employee_id}: {count} entries, Avg. Score: {avg_score:.2f} (Overall: {mood_desc})")
    else:
        print(f"No sufficient mood data found for {employee_id}.")

def main_menu():
    check_and_download_nltk_data()
    analyzer = TextEmotionAnalyzer()
    suggester = SuggestionEngine()
    logger = DataLogger() # Data will be stored in 'data/employee_mood_logs.csv'

    while True:
        print("\n===== Mood Analyzer Menu =====")
        print("1. Log Mood")
        print("2. View Logs")
        print("3. Employee Mood Summary")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1': log_mood_interaction(analyzer, suggester, logger)
        elif choice == '2': view_logs_interaction(logger)
        elif choice == '3': mood_summary_interaction(logger)
        elif choice == '4': print("Exiting. Goodbye!"); break
        else: print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()