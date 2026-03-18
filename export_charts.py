import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from data_logger import DataLogger
from app import EMOTION_META

# Target directory
output_dir = os.path.join(os.path.dirname(__file__), "presentation_charts")
os.makedirs(output_dir, exist_ok=True)

logger = DataLogger()

# Get data
df = logger.get_logs()

if not df.empty:
    # 1. Bar Plot: Emotion Frequencies
    dist = logger.get_emotion_distribution()
    if dist:
        labels = list(dist.keys())
        values = list(dist.values())
        colors = [EMOTION_META.get(e, EMOTION_META['unknown'])['color'] for e in labels]

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot bars
        bars = ax.bar(labels, values, color=colors)
        
        # Style
        ax.set_title('Frequency of Detected Emotions', fontsize=16, fontweight='bold')
        ax.set_xlabel('Emotions', fontsize=12)
        ax.set_ylabel('Number of Occurrences', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        path1 = os.path.join(output_dir, "emotion_frequency_barplot.png")
        plt.savefig(path1, dpi=300)
        plt.close()

    # 2. Histogram: Emotion Scores
    # Convert scores to numeric if needed, drop NaNs
    df['emotion_score'] = pd.to_numeric(df['emotion_score'], errors='coerce')
    scores = df['emotion_score'].dropna()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram. Score ranges from -1 to 1.
    counts, bins, patches = ax.hist(scores, bins=10, range=(-1, 1), color='#4f46e5', edgecolor='black', alpha=0.7)
    
    # Style
    ax.set_title('Distribution of Emotion Scores', fontsize=16, fontweight='bold')
    ax.set_xlabel('Emotion Score (Negative to Positive)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add vertical line for neutral (0)
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral (0.0)')
    ax.legend()
    
    plt.tight_layout()
    path2 = os.path.join(output_dir, "emotion_score_histogram.png")
    plt.savefig(path2, dpi=300)
    plt.close()

    print(f"Charts successfully generated in: {output_dir}")
else:
    print("No data available to plot.")
