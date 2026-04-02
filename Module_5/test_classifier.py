# test_classifier.py
from module_5 import sample_reviews, filter_by_label, summarize_results
import pandas as pd


def test_sample_reviews_not_empty():
    reviews = sample_reviews()
    assert len(reviews) > 0
    assert all(isinstance(r, str) for r in reviews)


def test_filter_by_label_all():
    df = pd.DataFrame({"label": ["positive", "negative", "neutral"], "text": ["a", "b", "c"]})
    assert len(filter_by_label(df, "All")) == 3


def test_filter_by_label_specific():
    df = pd.DataFrame({"label": ["positive", "negative", "neutral"], "text": ["a", "b", "c"]})
    filtered = filter_by_label(df, "positive")
    assert len(filtered) == 1
    assert filtered.iloc[0]["label"] == "positive"


def test_summarize_results():
    df = pd.DataFrame({
        "label": ["positive", "negative"],
        "confidence": [0.9, 0.8],
        "model": ["test", "test"],
    })
    summary = summarize_results(df)
    assert summary["total"] == 2
    assert summary["avg_confidence"] == 0.85