from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.interview.adaptive_engine import decide_next_action
from app.services.interview.session_engine import InterviewSessionEngine
from app.services.evaluation.answer_evaluator import evaluate_answer
from app.services.generation.mock_llm import MockLLM
from app.services.generation.question_generator import generate_question


router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


class StartInterviewRequest(BaseModel):
    candidate_profile: dict
    job_profile: dict
    interview_type: str = "technical"
    difficulty: str = "medium"


class AnswerRequest(BaseModel):
    session: dict
    answer: str = Field(min_length=1)
    reference_answer: str = Field(min_length=1)
    missing_concepts: list[str] = []


def create_session_engine() -> InterviewSessionEngine:
    llm = MockLLM()

    return InterviewSessionEngine(
        question_generator=lambda candidate_profile, job_profile, interview_type, difficulty: (
            generate_question(
                llm,
                candidate_profile,
                job_profile,
                interview_type,
                difficulty,
            )
        ),
        answer_evaluator=evaluate_answer,
        adaptive_engine=decide_next_action,
    )


@router.post("/start")
def start_interview(request: StartInterviewRequest):
    engine = create_session_engine()

    return engine.start_session(
        candidate_profile=request.candidate_profile,
        job_profile=request.job_profile,
        interview_type=request.interview_type,
        difficulty=request.difficulty,
    )


@router.post("/answer")
def submit_answer(request: AnswerRequest):
    engine = create_session_engine()

    if not request.session:
        raise HTTPException(
            status_code=400,
            detail="Session data is required.",
        )

    return engine.process_answer(
        session=request.session,
        answer=request.answer,
        reference_answer=request.reference_answer,
        missing_concepts=request.missing_concepts,
    )