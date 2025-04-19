import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from llm import build_chain
import asyncio

app = FastAPI()
qa_chain = build_chain()

@app.get("/connect")
async def connect(request: Request):
    async def event_gen():
        while True:
            if await request.is_disconnected():
                break
            yield {"event": "ping", "data": "alive"}
            await asyncio.sleep(15)
    return EventSourceResponse(event_gen())

@app.post("/rpc")
async def rpc(request: Request):
    body = await request.json()
    method = body.get("method")
    query = body["params"]["query"]
    if method == "search":
        result = qa_chain.run(query)
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body["id"],
            "result": result
        })
    return JSONResponse({"error": f"Method '{method}' not implemented"}, status_code=501)
