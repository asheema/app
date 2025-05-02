import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=500):
    data = {
        'phq_9_scores': [np.random.randint(0, 4, size=9).tolist() for _ in range(num_samples)],
        'gad_7_scores': [np.random.randint(0, 4, size=7).tolist() for _ in range(num_samples)],
    }
    df = pd.DataFrame(data)
    df['total_score'] = df['phq_9_scores'].apply(sum) + df['gad_7_scores'].apply(sum)
    df['label'] = pd.cut(
        df['total_score'],
        bins=[-1, 9, 14, 19, 27, 100],
        labels=[0, 1, 2, 3, 4]
    ).astype(int)
    return df
