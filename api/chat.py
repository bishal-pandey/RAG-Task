from fastapi import APIRouter
from pydantic import BaseModel

from combineService import CombineService

router = APIRouter()

combine_service = CombineService()


class ChatRequest(BaseModel):
    session_id: str
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    answer = combine_service.run_process(
        request.session_id,
        request.question
    )

    return {
       
        "answer": answer
    }