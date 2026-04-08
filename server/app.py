from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from mini.openenv_env import MiniOpenEnv, MiniOpenEnvAction

app = FastAPI(title="Mini OpenEnv Server")
env = MiniOpenEnv()

# 1. Update the Model to be more flexible
class ResetRequest(BaseModel):
    task_name: Optional[str] = None

    class Config:
        extra = "allow"

class StepRequest(BaseModel):
    action: MiniOpenEnvAction

    class Config:
        extra = "allow"

# 2. Update the Route to handle a missing body
@app.post("/reset")
async def reset(request: Request) -> dict:
    # Try to parse JSON, if it fails or is empty, use default
    try:
        body = await request.json()
        task_name = body.get("task_name", "meeting_note")
    except:
        task_name = "meeting_note"
        
    observation = env.reset(task_name=task_name)
    return {
        "observation": observation.dict(),
        "reward": 0.0,
        "done": False,
        "info": {"task_name": env.task_name},
    }

# Ensure your health check is still there
@app.get("/health")
async def health():
    return {"status": "ok"}
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


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)