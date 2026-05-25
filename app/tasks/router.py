from fastapi import APIRouter
from celery.result import AsyncResult

router = APIRouter()


@router.get('/{task_id}/')
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)

    if not result.ready():
        return {'status': 'pending', 'result': None}
    if result.failed():
        return {'status': 'failed', result: None}

    return {'status': 'success', 'result': result.result}
