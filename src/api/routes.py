# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
# See LICENSE file in the project root for full license information.
import json
import logging
import os

import fastapi
import pydantic
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .shared import globals
from .util import get_logger

logger = get_logger(
    name="azureaiapp",
    log_level=logging.INFO,
    log_file_name = os.getenv("APP_LOG_FILE"),
    log_to_console=True
)

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="api/templates")


class Message(pydantic.BaseModel):
    content: str
    role: str = "user"


class ChatRequest(pydantic.BaseModel):
    messages: list[Message]


@router.get("/", response_class=HTMLResponse)
async def index_name(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat/stream")
async def chat_stream_handler(
    chat_request: ChatRequest,
) -> fastapi.responses.StreamingResponse:
    chat_client = globals["chat"]
    if chat_client is None:
        raise Exception("Chat client not initialized")

    async def response_stream():
        messages = [{"role": message.role, "content": message.content} for message in chat_request.messages]
        model_deployment_name = globals["chat_model"]
        
        prompt_messages = globals["prompt"].create_messages()
        # Use RAG model, only if we were provided index and we have found a context there.
        if globals["rag"] is not None:
            context = await globals["rag"].search(chat_request)
            if context:
                # Clean up the context to avoid non unicode characters.
                context = context.encode("ascii", "ignore").decode("utf-8")
                prompt_messages = globals["rag_prompt"].create_messages(data=dict(context=context))
                # Remove this line.
                logger.info(f"{context=}")
            else:
                logger.info("Unable to find the relevant information in the index for the request.")
            
        chat_coroutine = await chat_client.complete(
            model=model_deployment_name, messages=prompt_messages + messages, stream=True
        )
        async for event in chat_coroutine:
            if event.choices:
                first_choice = event.choices[0]
                yield (
                    json.dumps(
                        {
                            "delta": {
                                "content": first_choice.delta.content,
                                "role": first_choice.delta.role,
                            }
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    return fastapi.responses.StreamingResponse(response_stream())
