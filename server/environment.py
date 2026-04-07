print("🔥 VERSION FINAL - META COMPLIANT")

from pathlib import Path
import pickle


class EmailEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 1
        self.reward = 0.0
        self.done = False
        self.current_email = None
        self.last_observation = None

        self._load_model()

    def _load_model(self):
        self.model_path = Path(__file__).resolve().parent / "model.pkl"
        self.vectorizer = None
        self.model = None

        try:
            with open(self.model_path, "rb") as f:
                self.vectorizer, self.model = pickle.load(f)
            print("✅ Model loaded successfully")
        except Exception as e:
            print("⚠️ MODEL LOAD ERROR:", e)

    def _safe_output(self, intent, confidence, explanation=""):
        return {
            "intent": str(intent),
            "confidence": float(max(0.0, min(1.0, confidence))),
            "risk_level": "high" if intent in ["spam", "phishing"] else "low",
            "risk_score": 0.8 if intent in ["spam", "phishing"] else 0.1,
            "explanation": explanation if explanation else f"Classified as {intent}"
        }

    def _fallback(self, text):
        text_lower = text.lower()
        spam_words = ["free", "win", "money", "offer", "click", "urgent"]

        found = [w for w in spam_words if w in text_lower]

        if len(found) >= 2:
            return self._safe_output("spam", 0.9, "Multiple spam indicators detected")
        elif len(found) == 1:
            return self._safe_output("spam", 0.6, "Single spam indicator detected")
        else:
            return self._safe_output("safe", 0.3, "No spam indicators detected")

    def _classify_email(self, text: str):
        try:
            if not text or not isinstance(text, str) or not text.strip():
                return self._safe_output("safe", 0.1, "Invalid input")

            if self.model and self.vectorizer:
                try:
                    X = self.vectorizer.transform([text])
                    pred = self.model.predict(X)[0]
                    prob = max(self.model.predict_proba(X)[0])
                    return self._safe_output(str(pred), float(prob), "Model prediction")
                except Exception:
                    pass

            return self._fallback(text)

        except Exception as e:
            return self._safe_output("safe", 0.1, f"Error: {str(e)}")

    def reset(self):
        self.current_task = None
        self.step_count = 1
        self.done = False
        return self._safe_output("safe", 0.5, "Environment reset")

    def set_task(self, task_name: str):
        self.current_task = task_name
        return {"message": f"Task set to {task_name}"}

    def step(self, action):
        try:
            if not isinstance(action, str) or not action.strip():
                raise ValueError("Invalid input")

            result = self._classify_email(action)

            intent = result.get("intent", "safe")
            confidence = float(result.get("confidence", 0.5))
            risk_level = result.get("risk_level", "low")
            risk_score = float(result.get("risk_score", 0.5))
            explanation = result.get("explanation", "")

            # -------- REWARD CALCULATION --------
            reward = 0.2

            if intent in ["spam", "phishing"]:
                reward += 0.3

            if confidence > 0.7:
                reward += 0.2

            expected_risk = "high" if intent in ["spam", "phishing"] else "low"
            if risk_level == expected_risk:
                reward += 0.2

            if explanation and len(explanation) > 10:
                reward += 0.1

            # 🔥 FINAL FIX (STRICT RANGE)
            reward = max(0.1, min(0.9, reward))

            observation = {
                "intent": intent,
                "confidence": confidence,
                "risk_level": risk_level,
                "risk_score": risk_score,
                "explanation": explanation,
            }

            info = {
                "task": self.current_task,
                "step_count": self.step_count
            }

            return observation, float(reward), True, info

        except Exception as e:
            observation = {
                "intent": "safe",
                "confidence": 0.1,
                "risk_level": "low",
                "risk_score": 0.1,
                "explanation": f"Error: {str(e)}"
            }

            return observation, 0.1, True, {"error": str(e)}