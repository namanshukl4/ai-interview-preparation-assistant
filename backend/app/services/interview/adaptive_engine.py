from typing import Dict, List


class AdaptiveInterviewEngine:
    """
    Controls the next step in an adaptive interview.

    The engine uses objective NLP evaluation results rather
    than asking an LLM to decide whether an answer was good.
    """

    def __init__(
        self,
        max_questions: int = 5,
        follow_up_threshold: float = 70.0,
    ):
        self.max_questions = max_questions
        self.follow_up_threshold = follow_up_threshold

    def decide_next_action(
        self,
        evaluation: Dict,
        question_number: int,
    ) -> Dict:
        """
        Decide whether the interview should continue with a
        follow-up, move to another topic, or finish.
        """

        if question_number >= self.max_questions:
            return {
                "action": "finish",
                "reason": "Maximum interview questions reached.",
            }

        final_score = float(
            evaluation.get("final_score", 0.0)
        )

        missing_concepts: List[str] = evaluation.get(
            "missing_concepts",
            [],
        )

        if final_score < self.follow_up_threshold:
            if missing_concepts:
                return {
                    "action": "follow_up",
                    "reason": "Answer contains important knowledge gaps.",
                    "focus_concepts": missing_concepts,
                }

            return {
                "action": "follow_up",
                "reason": "Answer score is below the target threshold.",
                "focus_concepts": [],
            }

        return {
            "action": "next_topic",
            "reason": "Answer met the target quality threshold.",
            "focus_concepts": [],
        }


def decide_next_action(
    evaluation: Dict,
    question_number: int,
    max_questions: int = 5,
    follow_up_threshold: float = 70.0,
) -> Dict:
    """
    Convenience function for adaptive interview decisions.
    """

    engine = AdaptiveInterviewEngine(
        max_questions=max_questions,
        follow_up_threshold=follow_up_threshold,
    )

    return engine.decide_next_action(
        evaluation=evaluation,
        question_number=question_number,
    )