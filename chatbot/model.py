"""
model.py
--------
The matching "model" for the SafeX FAQ Chatbot.

This project uses a retrieval-based approach: instead of generating new
text, it finds the FAQ question most similar to the user's input and
returns its pre-written answer. Similarity is measured using TF-IDF
(Term Frequency-Inverse Document Frequency) vectors and cosine similarity.

This is intentionally lightweight — no GPU or large model needed — and is
a standard, well-understood approach for small FAQ datasets like this one.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .preprocess import clean_text, clean_series


class FAQModel:
    def __init__(self, questions, confidence_threshold: float = 0.25):
        """
        questions: list of FAQ question strings (already cleaned or raw —
                   they will be cleaned here).
        confidence_threshold: minimum cosine similarity score (0-1)
                   required before a match is trusted.
        """
        self.raw_questions = questions
        self.cleaned_questions = clean_series(questions)
        self.confidence_threshold = confidence_threshold

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.question_vectors = self.vectorizer.fit_transform(self.cleaned_questions)

    def best_match(self, user_query: str):
        """
        Returns (best_index, confidence_score) for the FAQ question that
        best matches the user's query. best_index is None if no match
        clears the confidence threshold.
        """
        cleaned_query = clean_text(user_query)
        if not cleaned_query:
            return None, 0.0

        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.question_vectors)[0]

        best_idx = int(similarities.argmax())
        best_score = float(similarities[best_idx])

        if best_score < self.confidence_threshold:
            return None, round(best_score, 3)

        return best_idx, round(best_score, 3)
