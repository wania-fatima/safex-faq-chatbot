"""
chatbot.py
----------
Main chatbot class for the SafeX FAQ Chatbot.

Loads the FAQ dataset (data/SafeX_FAQ_Dataset.xlsx) and uses FAQModel
(model.py) to match user questions to the closest FAQ answer.
"""

import os
import pandas as pd

from .model import FAQModel

DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "SafeX_FAQ_Dataset.xlsx",
)


class SafeXFAQChatbot:
    def __init__(self, dataset_path: str = DEFAULT_DATA_PATH, confidence_threshold: float = 0.25):
        self.df = pd.read_excel(dataset_path)
        self.df.columns = [c.strip() for c in self.df.columns]

        self.questions = self.df["Question"].astype(str).tolist()
        self.answers = self.df["Answer"].astype(str).tolist()
        self.categories = (
            self.df["Category"].astype(str).tolist()
            if "Category" in self.df.columns
            else [""] * len(self.questions)
        )

        self.model = FAQModel(self.questions, confidence_threshold=confidence_threshold)

    def get_response(self, user_query: str) -> dict:
        """
        Returns a dict with:
          answer            -> the chatbot's reply text
          matched_question  -> the FAQ question that was matched (or None)
          category          -> the FAQ category matched (or None)
          confidence        -> similarity score between 0 and 1
        """
        if not user_query or not user_query.strip():
            return {
                "answer": "Please type a question so I can help you.",
                "matched_question": None,
                "category": None,
                "confidence": 0.0,
            }

        idx, confidence = self.model.best_match(user_query)

        if idx is None:
            return {
                "answer": (
                    "I'm not fully sure about that one. Could you rephrase your question, "
                    "or contact SafeX Solutions directly at contact@safexsolutions.com "
                    "or +92 327 5781580?"
                ),
                "matched_question": None,
                "category": None,
                "confidence": confidence,
            }

        return {
            "answer": self.answers[idx],
            "matched_question": self.questions[idx],
            "category": self.categories[idx],
            "confidence": confidence,
        }
