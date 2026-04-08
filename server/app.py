from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from mini.openenv_env import MiniOpenEnv, MiniOpenEnvAction

app = FastAPI(title="Mini OpenEnv Server")

env = MiniOpenEnv()


class ResetRequest(BaseModel):
    task_name: Optional[str] = None

    # Add this inner class to allow empty bodies
    class Config:
        extra = "allow"

class StepRequest(BaseModel):
    action: MiniOpenEnvAction

@app.get("/")
async def root():
    return {"status": "running", "message": "OpenEnv Environment Live"}

@app.post("/reset")
def reset(request: Optional[ResetRequest] = None) -> dict:
    # If request is None or task_name is missing, default to a task
    task = request.task_name if (request and request.task_name) else "meeting_note"
    observation = env.reset(task_name=task)
    return {
        "observation": observation.dict(),
        "reward": 0.0,
        "done": False,
        "info": {"task_name": env.task_name},
    }


@app.post("/step")
def step(request: StepRequest) -> dict:
    try:
        observation, reward, done, info = env.step(request.action)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "observation": observation.dict(),
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/state")
def state() -> dict:
    observation = env.state()
    return {
        "observation": observation.dict(),
        "info": {"task_name": env.task_name},
    }


@app.get("/ping")
def ping() -> dict:
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)