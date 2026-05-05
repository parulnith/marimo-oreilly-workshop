"""Tests for sentiment_classifier helpers.

a marimo notebook is just a Python file, so its helpers
can be tested with regular pytest. 

    pytest test_classifier.py
"""

from sentiment_classifier import sample_reviews


def test_sample_reviews_not_empty():
    """sample_reviews() should return at least one review."""
    reviews = sample_reviews()
    print(f"\nGot {len(reviews)} reviews. First one: {reviews[0]!r}")
    assert len(reviews) > 0


def test_sample_reviews_are_strings():
    """Every review should be a non-empty string (no None, no blank lines)."""
    reviews = sample_reviews()
    print(f"\nAll {len(reviews)} reviews are non-empty strings ✓")
    assert all(isinstance(r, str) and r.strip() for r in reviews)
