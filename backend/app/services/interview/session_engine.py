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

        generated_question = self.question_generator(
            candidate_profile,
            job_profile,
            interview_type,
            difficulty,
        )

        # Support both the legacy string generator and the new
        # question-with-context generator.
        if isinstance(generated_question, str):
            question = generated_question
            evaluation_context = {}
        else:
            question = generated_question["question"]
            evaluation_context = {
                "skill": generated_question.get("skill"),
                "reference_answer": generated_question.get(
                    "reference_answer"
                ),
                "required_concepts": generated_question.get(
                    "required_concepts",
                    [],
                ),
            }

        return {
            "status": "active",
            "question_number": 1,
            "question": question,
            "evaluation_context": evaluation_context,
            "history": [],
        }

    def process_answer(
        self,
        session: dict[str, Any],
        answer: str,
        reference_answer: str | None = None,
        missing_concepts: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate an answer and determine the next interview action.

        Evaluation context is preferably taken from the server-side
        interview session. Legacy explicit values are supported temporarily
        for backwards compatibility with existing tests.
        """

        evaluation_context = session.get(
            "evaluation_context",
            {},
        )

        session_reference_answer = evaluation_context.get(
            "reference_answer"
        )

        required_concepts = evaluation_context.get(
            "required_concepts",
            [],
        )

        # Backwards compatibility for older sessions/tests.
        effective_reference_answer = (
            session_reference_answer
            or reference_answer
            or ""
        )

        effective_missing_concepts = (
            missing_concepts
            if missing_concepts is not None
            else []
        )

        try:
            evaluation = self.answer_evaluator(
                answer,
                effective_reference_answer,
                required_concepts,
            )
        except TypeError:
            # Backwards compatibility for simple/mock evaluators
            evaluation = self.answer_evaluator(
                answer,
                effective_reference_answer,
            )

        # Prefer concepts identified by the evaluator itself.
        adaptive_missing_concepts = evaluation.get(
            "missing_concepts",
            effective_missing_concepts,
        )

        decision = self.adaptive_engine(
            {
                "final_score": evaluation["final_score"],
                "missing_concepts": adaptive_missing_concepts,
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

