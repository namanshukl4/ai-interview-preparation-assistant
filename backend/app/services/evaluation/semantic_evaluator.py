from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticEvaluator:
    """
    Transformer-based semantic similarity evaluator.

    This module is intentionally independent from the generative
    AI layer. It evaluates how semantically similar a candidate's
    answer is to a reference answer.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def calculate_similarity(
        self,
        candidate_answer: str,
        reference_answer: str,
    ) -> float:
        """
        Calculate cosine similarity between candidate and reference
        answer embeddings.

        Returns:
            Float between 0.0 and 1.0.
        """
        if not candidate_answer.strip() or not reference_answer.strip():
            return 0.0

        embeddings = self.model.encode(
            [candidate_answer, reference_answer]
        )

        score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]

        return round(float(score), 4)


def calculate_semantic_similarity(
    candidate_answer: str,
    reference_answer: str,
) -> float:
    """
    Convenience function for semantic similarity evaluation.
    """
    evaluator = SemanticEvaluator()
    return evaluator.calculate_similarity(
        candidate_answer,
        reference_answer,
    )
