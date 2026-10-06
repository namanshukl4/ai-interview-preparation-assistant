from typing import Any


class InterviewSessionEngine:
    """
    Coordinates the interview loop.

    Responsibilities:
    - store interview state
    - evaluate candidate answers
    - use the adaptive engine to decide what happens next
    - generate the next question
    """

    def __init__(
        self,
        question_generator,
        answer_evaluator,
        adaptive_engine,
        max_questions: int = 5,
    ):
        self.question_generator = question_generator
        self.answer_evaluator = answer_evaluator
        self.adaptive_engine = adaptive_engine
        self.max_questions = max_questions

    def start_session(
        self,
        candidate_profile: dict[str, Any],
        job_profile: dict[str, Any],
        interview_type: str = "technical",
        difficulty: str = "medium",
    ) -> dict[str, Any]:
        """
        Start a new interview session.
        """

        question = self.question_generator(
            candidate_profile,
            job_profile,
            interview_type,
            difficulty,
        )

        return {
            "status": "active",
            "question_number": 1,
            "question": question,
            "history": [],
        }

    def process_answer(
        self,
        session: dict[str, Any],
        answer: str,
        reference_answer: str,
        missing_concepts: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate an answer and determine the next interview action.
        """

        evaluation = self.answer_evaluator(
            answer,
            reference_answer,
        )

        decision = self.adaptive_engine(
            {
                "final_score": evaluation["final_score"],
                "missing_concepts": missing_concepts or [],
            },
            session["question_number"],
            self.max_questions,
        )

        history_entry = {
            "question": session["question"],
            "answer": answer,
            "evaluation": evaluation,
            "decision": decision,
        }

        session["history"].append(history_entry)

        return {
            "evaluation": evaluation,
            "decision": decision,
            "history": session["history"],
        }