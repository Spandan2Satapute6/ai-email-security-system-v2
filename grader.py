from typing import Dict, Any


def grade(observation: Dict[str, Any], task: str) -> float:
    try:
        intent = str(observation.get("intent", "safe")).lower()
        confidence = float(observation.get("confidence", 0.5))
        risk = str(observation.get("risk_level", "low")).lower()
        explanation = str(observation.get("explanation", "")).lower()

        confidence = max(0.0, min(1.0, confidence))

        # -------- EASY TASK --------
        if task == "easy_task":
            score = 0.5

            if intent in ["spam", "phishing"]:
                score += 0.2
            else:
                score -= 0.1

            if confidence > 0.5:
                score += 0.2

        # -------- MEDIUM TASK --------
        elif task == "medium_task":
            score = 0.4

            if intent in ["spam", "phishing", "safe", "suspicious"]:
                score += 0.2

            if confidence > 0.6:
                score += 0.2
            else:
                score -= 0.1

            if risk in ["high", "low"]:
                score += 0.1

        # -------- HARD TASK --------
        elif task == "hard_task":
            score = 0.3

            if intent in ["spam", "phishing", "safe", "suspicious"]:
                score += 0.2

            if confidence > 0.6:
                score += 0.2

            expected_risk = "high" if intent in ["spam", "phishing"] else "low"
            if risk == expected_risk:
                score += 0.2
            else:
                score -= 0.1

            if len(explanation) > 20:
                score += 0.2

        else:
            score = 0.5

        # 🔥 STRICT RANGE (CRITICAL)
        score = max(0.2, min(0.9, score))

        return float(score)

    except Exception:
        return 0.5