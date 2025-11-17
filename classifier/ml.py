from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = BASE_DIR / 'mail_data.csv'


def _load_training_frame() -> pd.DataFrame:
    dataset_path = Path(os.environ.get('MAIL_SPAM_DATA', DEFAULT_DATASET))
    if dataset_path.exists():
        df = pd.read_csv(dataset_path)
    else:
        df = pd.DataFrame(
            {
                'Message': [
                    'Congratulations! You have won a $1000 Walmart gift card. Call now to claim.',
                    'Reminder: your dental appointment is tomorrow at 10am.',
                    'Win cash prizes by replying WIN to this message!',
                    'Are we still on for lunch today?',
                ],
                'Category': ['spam', 'ham', 'spam', 'ham'],
            }
        )
    df = df.where(pd.notnull(df), '')
    df['Category'] = df['Category'].astype(str).str.strip().str.lower()
    df.loc[df['Category'] == 'spam', 'label'] = 1
    df.loc[df['Category'] == 'ham', 'label'] = 0
    df['label'] = df['label'].fillna(0).astype(int)
    return df[['Message', 'label']]


def _build_pipeline() -> Pipeline:
    df = _load_training_frame()
    min_df = 1 if len(df) < 50 else 2
    tfidf = TfidfVectorizer(
        min_df=min_df,
        stop_words='english',
        lowercase=True,
        ngram_range=(1, 2),
        max_features=10000,
    )
    model = LogisticRegression(max_iter=1000, solver='liblinear')
    pipe = Pipeline([('tfidf', tfidf), ('lr', model)])
    pipe.fit(df['Message'], df['label'])
    return pipe


@lru_cache(maxsize=1)
def get_pipeline() -> Pipeline:
    return _build_pipeline()

def predict_mail(text: str) -> dict[str, Any]:
    pipeline = get_pipeline()
    probabilities = pipeline.predict_proba([text])[0]
    spam_probability = float(probabilities[1])
    is_spam = spam_probability >= 0.5
    return {
        'label': 'Spam' if is_spam else 'Ham',
        'is_spam': is_spam,
        'confidence': spam_probability if is_spam else 1.0 - spam_probability,
        'spam_probability': spam_probability,
    }
