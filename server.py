from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from mini.openenv_env import MiniOpenEnv, MiniOpenEnvAction

app = FastAPI(title="Mini OpenEnv Server")

env = MiniOpenEnv()


class ResetRequest(BaseModel):
    task_name: Optional[str] = None


class StepRequest(BaseModel):
    action: MiniOpenEnvAction


@app.post("/reset")
def reset(request: ResetRequest) -> dict:
    observation = env.reset(task_name=request.task_name)
    return {
        "observation": observation.dict(),
        "reward": 0.0,
        "done": False,
        "info": {"task_name": env.task_name},
    }


@app.post("/step")
def step(request: StepRequest) -> dict:
    observation, reward, done, info = env.step(request.action)
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
