print("🔥 VERSION FINAL - META + HF READY")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from server.environment import EmailEnv


EPSILON = 1e-6


def _strict_unit_interval(value: float) -> float:
    """Clamp numeric scores to the open interval (0, 1)."""
    return float(max(EPSILON, min(1.0 - EPSILON, float(value))))

app = FastAPI(
    title="AI Email Security System",
    version="FINAL",
    description="Meta OpenEnv Hackathon - Email Classification System"
)

step_counter = 0


# -------- REQUEST MODEL --------
class EmailRequest(BaseModel):
    text: str = Field(..., min_length=1)


# -------- RESPONSE MODEL --------
class EmailResponse(BaseModel):
    intent: str
    confidence: float
    risk_level: str
    risk_score: float
    explanation: str
    reward: float
    step_count: int


# -------- CLASSIFY --------
@app.post("/classify", response_model=EmailResponse)
def classify_email(request: EmailRequest):
    global step_counter

    try:
        step_counter += 1

        env = EmailEnv()
        env.reset()

        observation, reward, done, info = env.step(request.text)

        intent = str(observation.get("intent", "safe"))
        confidence = _strict_unit_interval(observation.get("confidence", 0.5))
        risk_score = _strict_unit_interval(observation.get("risk_score", 0.5))
        explanation = str(observation.get("explanation", "No explanation"))

        # fix intent
        if intent not in ["spam", "safe", "phishing", "suspicious"]:
            intent = "safe"

        # fix risk level
        risk_level = observation.get("risk_level")
        if risk_level not in ["high", "low"]:
            risk_level = "high" if risk_score > 0.5 else "low"

        # 🔥 FIX: reward always between (0,1)
        reward = _strict_unit_interval(max(0.1, min(0.9, float(reward))))

        return {
            "intent": intent,
            "confidence": confidence,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "explanation": explanation,
            "reward": reward,
            "step_count": step_counter
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- RESET --------
@app.post("/reset")
def reset_environment():
    global step_counter

    try:
        step_counter = 0

        env = EmailEnv()
        env.reset()

        return {"message": "reset successful"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- STATE --------
@app.get("/state")
def get_state():
    return {
        "intent": "safe",
        "confidence": 0.5,
        "risk_level": "low",
        "risk_score": 0.5,
        "explanation": "Initial environment state",
        "reward": 0.5
    }


# -------- ROOT --------
@app.get("/")
def root():
    return {
        "message": "API running",
        "docs": "/docs",
        "status": "OK"
    }


# -------- HEALTH --------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------- RUN --------
import uvicorn

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()