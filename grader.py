from typing import Dict, Any


def grade(observation: Dict[str, Any], task: str) -> float:
    """
    Meta Phase 2 Grader - Deterministic, stable, validator-safe
    """

    try:
        # Safe extraction
        intent = str(observation.get("intent", "safe")).lower()
        confidence = float(observation.get("confidence", 0.5))
        risk = str(observation.get("risk_level", "low")).lower()
        explanation = str(observation.get("explanation", "")).lower()

        # Clamp confidence to valid range
        confidence = max(0.0, min(1.0, confidence))

        # -------- EASY TASK (0.30-0.40) --------
        if task == "easy_task":
            score = 0.35

            if intent in ["spam", "phishing"]:
                score += 0.03
            elif intent == "safe":
                score += 0.02

            if confidence > 0.7:
                score += 0.02

            # Clamp to easy range
            score = max(0.30, min(0.40, score))

        # -------- MEDIUM TASK (0.55-0.70) --------
        elif task == "medium_task":
            score = 0.62

            if intent in ["spam", "phishing", "safe"]:
                score += 0.04
            else:
                score += 0.02

            if confidence > 0.6:
                score += 0.04
            else:
                score -= 0.02

            if risk in ["high", "low"]:
                score += 0.02

            # Clamp to medium range
            score = max(0.55, min(0.70, score))

        # -------- HARD TASK (0.75-0.90) --------
        elif task == "hard_task":
            score = 0.82

            if intent in ["spam", "phishing", "safe"]:
                score += 0.04
            else:
                score += 0.02

            if confidence > 0.7:
                score += 0.04
            else:
                score -= 0.02

            expected_risk = "high" if intent in ["spam", "phishing"] else "low"
            if risk == expected_risk:
                score += 0.03
            else:
                score -= 0.01

            if len(explanation) > 20:
                score += 0.02

            # Clamp to hard range
            score = max(0.75, min(0.90, score))

        # -------- FALLBACK --------
        else:
            score = 0.55

        # Final clamp (strict)
        score = max(0.25, min(0.9, score))

        return float(score)

    except Exception:
        return 0.55