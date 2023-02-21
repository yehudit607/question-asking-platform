from dataclasses import dataclass

from api.helpers.base_helpers import get_session_logger
from api.helpers.constants import QuestionType
from api.models import Question, Answer

logger = get_session_logger()

@dataclass
class AnswersDto:
    text: str
    is_correct: bool = None

    @classmethod
    def from_dict(cls, records):

        answers = [cls(
            text=record.get("text"),
            is_correct=record.get("type"),
        )
           for record in records
        ]

        return answers

    @classmethod
    def from_record(cls, records):
        logger.debug(f"Mapping custom request dto from record.")

        answer = [cls(
            text=record.text,
            is_correct=record.is_correct)
            for record in records]

        logger.debug(f"Finish answer mapping record to dto..")
        return answer


@dataclass
class QuestionDto:
    text: str
    type: QuestionType = ''
    answers: list[AnswersDto] = None

    @classmethod
    def from_dict(cls, record):
        question = cls(
            text=record.get("text"),
            type=record.get("type"),
        )
        question.answers = (
            AnswersDto.from_dict(record.get("answers"))
            if record.get("answers")
            else None
        )
        return question

    @classmethod
    def from_record(cls, record: Question):
        logger.debug(f"Mapping custom request dto from record.")

        question = cls(
            text=record.text,
            type=record.type,

        )
        question.answers = AnswersDto.from_record(
                record.answers.select_related("question").all()
            )

        logger.debug(f"Finish question mapping record to dto..")
        return question
