from typing import List, Dict

from app.services.evaluation.semantic_evaluator import (
    SemanticEvaluator,
)


class AnswerEvaluator:
    """
    Independent NLP/Deep Learning based answer evaluator.

    The evaluator does NOT use a generative LLM to grade answers.

    Evaluation dimensions:
    1. Semantic similarity
    2. Concept coverage
    3. Completeness
    4. Final weighted score
    """

    def __init__(self):
        self.semantic_evaluator = SemanticEvaluator()

    @staticmethod
    def normalize_concepts(concepts: List[str]) -> List[str]:
        """
        Normalize required concepts for comparison.
        """
        return [
            concept.strip().lower()
            for concept in concepts
            if concept.strip()
        ]

    @staticmethod
    def calculate_concept_coverage(
        candidate_answer: str,
        required_concepts: List[str],
    ) -> Dict:
        """
        Calculate how many required concepts are explicitly
        mentioned in the candidate answer.
        """

        if not candidate_answer.strip():
            return {
                "covered_concepts": [],
                "missing_concepts": required_concepts,
                "coverage_score": 0.0,
            }

        answer = candidate_answer.lower()

        concepts = AnswerEvaluator.normalize_concepts(
            required_concepts
        )

        covered = []
        missing = []

        for concept in concepts:
            if concept in answer:
                covered.append(concept)
            else:
                missing.append(concept)

        if not concepts:
            coverage_score = 1.0
        else:
            coverage_score = len(covered) / len(concepts)

        return {
            "covered_concepts": covered,
            "missing_concepts": missing,
            "coverage_score": round(coverage_score, 4),
        }

    def evaluate(
        self,
        candidate_answer: str,
        reference_answer: str,
        required_concepts: List[str] | None = None,
    ) -> Dict:
        """
        Evaluate a candidate answer using independent
        transformer-based NLP metrics.

        Final score weighting:

        60% semantic similarity
        40% concept coverage
        """

        required_concepts = required_concepts or []

        semantic_score = self.semantic_evaluator.calculate_similarity(
            candidate_answer,
            reference_answer,
        )

        concept_result = self.calculate_concept_coverage(
            candidate_answer,
            required_concepts,
        )

        coverage_score = concept_result["coverage_score"]

        final_score = (
            (semantic_score * 0.60)
            + (coverage_score * 0.40)
        ) * 100

        return {
            "semantic_score": round(semantic_score * 100, 2),
            "coverage_score": round(coverage_score * 100, 2),
            "final_score": round(final_score, 2),
            "covered_concepts": concept_result[
                "covered_concepts"
            ],
            "missing_concepts": concept_result[
                "missing_concepts"
            ],
        }


def evaluate_answer(
    candidate_answer: str,
    reference_answer: str,
    required_concepts: List[str] | None = None,
) -> Dict:
    """
    Convenience function for answer evaluation.
    """

    evaluator = AnswerEvaluator()

    return evaluator.evaluate(
        candidate_answer=candidate_answer,
        reference_answer=reference_answer,
        required_concepts=required_concepts,
    )