"""
Employee Emotion Analyzer — CLI Interface
Original command-line emotion analyzer (kept for backward compatibility).
Use `app.py` for the web dashboard instead.
"""
import os
import sys

project_root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir_path = os.path.join(project_root_dir, "src")
if src_dir_path not in sys.path:
    sys.path.insert(0, src_dir_path)

try:
    from src.emotion_analyzer import TextEmotionAnalyzer
    from src.suggestion_engine import SuggestionEngine
    from src.data_logger import DataLogger
except ImportError as e:
    print(f"Error: Could not import custom modules from 'src'. Original error: {e}")
    print(f"Please ensure 'src' directory exists at: {src_dir_path}")
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
        print(f"Notice: Could not check/download NLTK 'vader_lexicon': {e}.")


def log_mood_interaction(analyzer, suggester, logger):
    print("\n--- Log New Mood Entry ---")
    employee_id = input("Enter your Employee ID: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return

    text_input = input(f"Hi {employee_id}, how are you feeling?\n> ").strip()
    if not text_input:
        print("No input provided.")
        return

    emotion, score, category = analyzer.get_emotion(text_input)
    suggestion = suggester.get_suggestion(emotion)
    priority = suggester.get_task_priority(emotion)

    print(f"\n  Emotion : {emotion.capitalize()} ({category})")
    print(f"  Score   : {score:.2f}")
    print(f"  Priority: {priority['priority'].upper()} — {priority['focus']}")
    print(f"  Time    : {priority['time_blocks']}")
    print(f"  Tip     : {suggestion}")

    logger.log_entry(employee_id, text_input, emotion, score, suggestion, category)
    print("  ✓ Entry logged.\n")


def view_logs_interaction(logger):
    print("\n--- View Mood Logs ---")
    emp_id = input("Enter Employee ID to filter (or Enter for all): ").strip()
    logs_df = logger.get_logs(employee_id=emp_id if emp_id else None)

    if not logs_df.empty:
        print(f"\n{'Timestamp':<22} {'ID':<10} {'Emotion':<12} {'Score':>6}  Input")
        print("─" * 80)
        for _, row in logs_df.iterrows():
            ts = row['timestamp']
            eid = row['employee_id']
            em = row['detected_emotion']
            sc = row['emotion_score']
            txt = row['text_input'][:40]
            print(f"{ts:<22} {eid:<10} {em:<12} {sc:>6.2f}  {txt}")
    else:
        print("No logs found.")


def mood_summary_interaction(logger):
    print("\n--- Employee Mood Summary ---")
    employee_id = input("Enter Employee ID: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return

    avg_score, count = logger.get_employee_mood_summary(employee_id)
    if count > 0 and avg_score is not None:
        mood = "Positive" if avg_score >= 0.05 else "Negative" if avg_score <= -0.05 else "Neutral"
        print(f"\n  Employee : {employee_id}")
        print(f"  Entries  : {count}")
        print(f"  Avg Score: {avg_score:.2f}")
        print(f"  Overall  : {mood}")
    else:
        print(f"No data found for {employee_id}.")


def main_menu():
    check_and_download_nltk_data()
    analyzer = TextEmotionAnalyzer()
    suggester = SuggestionEngine()
    logger = DataLogger()

    print("\n╔═══════════════════════════════════════════╗")
    print("║  Employee Emotion Analyzer  ·  CLI Mode  ║")
    print("╚═══════════════════════════════════════════╝")
    print("  Tip: Run 'python app.py' for the web dashboard!\n")

    while True:
        print("───── Menu ─────")
        print("  1. Log Mood")
        print("  2. View Logs")
        print("  3. Mood Summary")
        print("  4. Exit")
        choice = input("  Choice (1-4): ").strip()

        if choice == '1':
            log_mood_interaction(analyzer, suggester, logger)
        elif choice == '2':
            view_logs_interaction(logger)
        elif choice == '3':
            mood_summary_interaction(logger)
        elif choice == '4':
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main_menu()