from typing import Dict, Any


def grade(observation: Dict[str, Any], task: str) -> float:
    """
    Grade observation against task requirements for OpenEnv.
    
    Args:
        observation: Dictionary containing model output with keys:
                    - intent: str (spam/safe/phishing/suspicious)
                    - confidence: float (0.0-1.0)
                    - risk_level: str (high/low)
                    - explanation: str
        task: Task name (easy_task, medium_task, hard_task)
    
    Returns:
        float: Score strictly in [0,1] - DETERMINISTIC
    """
    
    # Extract observation fields safely
    intent = str(observation.get("intent", "safe"))
    confidence = float(observation.get("confidence", 0.0))
    risk_level = str(observation.get("risk_level", "low"))
    explanation = str(observation.get("explanation", ""))
    
    # Ensure values are in valid ranges
    confidence = max(0.0, min(1.0, confidence))
    
    if task == "easy_task":
        return _grade_easy_task(intent, confidence)
    elif task == "medium_task":
        return _grade_medium_task(intent, confidence, risk_level)
    elif task == "hard_task":
        return _grade_hard_task(intent, confidence, risk_level, explanation)
    else:
        raise ValueError(f"Unknown task: {task}")


def _grade_easy_task(intent: str, confidence: float) -> float:
    """
    EASY: Only intent scoring - DETERMINISTIC
    
    Returns:
        float: Score in [0,1]
    """
    # Valid intents for easy task
    valid_intents = ["spam", "safe", "phishing", "suspicious"]
    
    if intent in valid_intents:
        return 1.0
    else:
        return 0.0


def _grade_medium_task(intent: str, confidence: float, risk_level: str) -> float:
    """
    MEDIUM: Intent + confidence - DETERMINISTIC
    
    Returns:
        float: Score in [0,1]
    """
    # Intent scoring (50% weight)
    valid_intents = ["spam", "safe", "phishing", "suspicious"]
    intent_score = 0.5 if intent in valid_intents else 0.0
    
    # Confidence scoring (50% weight)
    confidence_score = 0.5 if confidence > 0.7 else 0.0
    
    total_score = intent_score + confidence_score
    return min(1.0, max(0.0, total_score))


def _grade_hard_task(intent: str, confidence: float, risk_level: str, explanation: str) -> float:
    """
    HARD: Intent + confidence + risk + explanation - DETERMINISTIC
    
    Returns:
        float: Score in [0,1]
    """
    score = 0.0
    
    # Intent scoring (40% weight)
    valid_intents = ["spam", "safe", "phishing", "suspicious"]
    if intent in valid_intents:
        score += 0.4
    
    # Confidence scoring (30% weight)
    if confidence > 0.7:
        score += 0.3
    
    # Risk scoring (20% weight)
    expected_risk = "high" if intent in ["spam", "phishing"] else "low"
    if risk_level == expected_risk:
        score += 0.2
    
    # Explanation scoring (10% weight) - DETERMINISTIC
    phishing_keywords = ["urgent", "verify", "bank", "password", "click", "account"]
    explanation_lower = explanation.lower()
    
    if intent in ["spam", "phishing"]:
        # For malicious content, check if explanation mentions phishing indicators
        if any(kw in explanation_lower for kw in phishing_keywords):
            score += 0.1
    elif intent == "safe":
        # For safe content, check if explanation doesn't mention phishing indicators
        if not any(kw in explanation_lower for kw in phishing_keywords):
            score += 0.1
    else:
        # For suspicious, partial credit
        score += 0.05
    
    return min(1.0, max(0.0, score))


def _is_meaningful_explanation(explanation: str, intent: str) -> bool:
    """
    Check if explanation is meaningful for the given intent.
    Meaningful explanations contain relevant signal detection.
    """
    if not explanation or len(explanation.strip()) < 10:
        return False
    
    explanation_lower = explanation.lower()
    
    # Check for signal detection keywords
    signal_keywords = [
        "detected", "signals", "patterns", "analysis", "identified",
        "found", "contains", "indicates", "suggests", "shows"
    ]
    
    has_signal_words = any(keyword in explanation_lower for keyword in signal_keywords)
    
    # Check for spam/phishing specific indicators
    if intent in ["spam", "phishing"]:
        spam_indicators = [
            "urgent", "offer", "free", "win", "money", "prize",
            "link", "url", "click", "suspicious", "malicious"
        ]
        has_spam_signals = any(indicator in explanation_lower for indicator in spam_indicators)
        return has_signal_words or has_spam_signals
    
    # For safe emails, check for legitimate indicators
    elif intent == "safe":
        safe_indicators = [
            "no suspicious", "legitimate", "normal", "safe", "clean",
            "no threats", "benign", "harmless"
        ]
        has_safe_signals = any(indicator in explanation_lower for indicator in safe_indicators)
        return has_signal_words or has_safe_signals
    
    return has_signal_words


# -------- TASK DEFINITIONS --------
def get_grader_task_definitions():
    """
    Return task definitions for the grader system.
    """
    return {
        "easy_task": {
            "name": "Easy Spam Detection",
            "description": "Detect if email is spam or not spam",
            "grading_focus": "Correct intent detection only",
            "max_reward": 1.0,
            "reward_components": {
                "correct_intent": 1.0
            }
        },
        "medium_task": {
            "name": "Medium Spam Detection with Confidence",
            "description": "Detect spam and provide confidence score > 0.7",
            "grading_focus": "Correct intent + confidence threshold",
            "max_reward": 1.0,
            "reward_components": {
                "correct_intent": 0.6,
                "confidence_threshold": 0.4
            }
        },
        "hard_task": {
            "name": "Hard Comprehensive Email Analysis",
            "description": "Detect spam, provide confidence > 0.7, correct risk level, and meaningful explanation",
            "grading_focus": "Intent + confidence + risk + explanation",
            "max_reward": 1.0,
            "reward_components": {
                "correct_intent": 0.4,
                "confidence_threshold": 0.3,
                "correct_risk": 0.2,
                "meaningful_explanation": 0.1
            }
        }
    }


# -------- VALIDATION --------
def validate_observation(observation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize observation for grading.
    """
    validation_errors = []
    
    # Check required fields
    required_fields = ["intent", "confidence", "risk_level", "explanation"]
    for field in required_fields:
        if field not in observation:
            validation_errors.append(f"Missing required field: {field}")
    
    # Validate confidence range
    confidence = observation.get("confidence", 0.0)
    if not isinstance(confidence, (int, float)) or confidence < 0.0 or confidence > 1.0:
        validation_errors.append("Confidence must be a float between 0.0 and 1.0")
    
    # Validate intent
    valid_intents = ["spam", "safe", "phishing", "suspicious"]
    intent = observation.get("intent", "")
    if intent not in valid_intents:
        validation_errors.append(f"Intent must be one of: {valid_intents}")
    
    # Validate risk level
    valid_risks = ["high", "low"]
    risk_level = observation.get("risk_level", "")
    if risk_level not in valid_risks:
        validation_errors.append(f"Risk level must be one of: {valid_risks}")
    
    return {
        "is_valid": len(validation_errors) == 0,
        "errors": validation_errors,
        "normalized_observation": {
            "intent": str(intent),
            "confidence": float(max(0.0, min(1.0, confidence))),
            "risk_level": str(risk_level),
            "explanation": str(observation.get("explanation", ""))
        }
    }


# -------- BATCH GRADING --------
def grade_batch(observations: list, task: str) -> list:
    """
    Grade multiple observations for the same task.
    Returns list of rewards.
    """
    rewards = []
    for obs in observations:
        try:
            validation = validate_observation(obs)
            if validation["is_valid"]:
                reward = grade(validation["normalized_observation"], task)
                rewards.append(reward)
            else:
                rewards.append(0.0)  # Invalid observations get 0 reward
        except Exception:
            rewards.append(0.0)  # Any errors get 0 reward
    
    return rewards
