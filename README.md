# Mini Productivity OpenEnv

A desktop productivity environment for the OpenEnv framework, simulating real-world tasks like drafting meeting notes, customer support responses, and incident reports.

## OpenEnv Environment

This environment provides a desktop workspace where agents can:
- Open a task workspace
- Type text content
- Submit completed work

## Tasks

- **meeting_note**: Compose a short meeting note with agenda and next steps
- **customer_response**: Draft a polite customer support reply
- **incident_report**: Write a brief incident report with root cause and resolution

## Installation

```bash
pip install -r requirements.txt
```

## Running

### Local Environment
```python
from mini.openenv_env import MiniOpenEnv, MiniOpenEnvAction

env = MiniOpenEnv(task_name="meeting_note")
obs = env.reset()
action = MiniOpenEnvAction(type="OPEN_WORKSPACE")
obs, reward, done, info = env.step(action)
```

### Server
```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

### Inference
```bash
export HF_TOKEN="your-token"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="gpt-4o-mini"
python inference.py
```

## Validation

Run the pre-submission validator:

```bash
chmod +x validate-submission.sh
./validate-submission.sh https://your-space.hf.space
```

## Docker

Build and run:

```bash
docker build -t mini-openenv .
docker run -p 7860:7860 mini-openenv
```
