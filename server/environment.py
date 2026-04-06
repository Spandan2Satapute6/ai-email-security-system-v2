print("🔥 VERSION 8.0 PRODUCTION READY")
from pathlib import Path
import pickle
import re


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
        """Load model safely"""
        self.model_path = Path(__file__).resolve().parent / "model.pkl"
        self.vectorizer = None
        self.model = None
        
        try:
            with open(self.model_path, "rb") as f:
                self.vectorizer, self.model = pickle.load(f)
            print("✅ Model loaded successfully")
        except Exception as e:
            print("⚠️ MODEL LOAD ERROR:", e)
    
    def _classify_email(self, text: str):
        """Classify email with safe fallback"""
        try:
            if not text or not isinstance(text, str) or not text.strip():
                return self._safe_output("safe", 0.0, "Invalid input")
            
            text_lower = text.lower()
            
            # Try ML model first
            if self.model and self.vectorizer:
                try:
                    X = self.vectorizer.transform([text])
                    pred = self.model.predict(X)[0]
                    prob = max(self.model.predict_proba(X)[0])
                    explanation = self._generate_explanation(text, pred)
                    return self._safe_output(str(pred), float(prob), explanation)
                except Exception:
                    pass
            
            # Fallback classification
            return self._fallback(text)
            
        except Exception as e:
            return self._safe_output("safe", 0.0, f"Error: {str(e)}")
    
    def _generate_explanation(self, text, pred):
        """Generate dynamic explanation"""
        text_lower = text.lower()
        
        spam_keywords = ["free", "win", "money", "offer", "click", "urgent", "prize", "cash"]
        security_keywords = ["account", "password", "verify", "login", "suspended"]
        
        found_spam = [w for w in spam_keywords if w in text_lower]
        found_security = [w for w in security_keywords if w in text_lower]
        
        if pred == "spam":
            if found_spam:
                return f"Detected spam keywords: {', '.join(found_spam[:3])}"
            elif found_security:
                return f"Suspicious account-related terms: {', '.join(found_security[:3])}"
            else:
                return "Message shows spam-like patterns and unusual intent"
        else:
            return "No suspicious keywords or spam patterns detected"
    
    def _safe_output(self, intent, confidence, explanation=""):
        """Always return valid dict structure"""
        return {
            "intent": str(intent),
            "confidence": float(max(0.0, min(1.0, confidence))),
            "risk_level": "high" if intent in ["spam", "phishing"] else "low",
            "risk_score": 0.8 if intent in ["spam", "phishing"] else 0.1,
            "explanation": explanation if explanation else f"Classified as {intent}"
        }
    
    def _fallback(self, text):
        """Rule-based fallback classification"""
        text_lower = text.lower()
        spam_words = ["free", "win", "money", "offer", "click", "urgent"]
        
        found = [w for w in spam_words if w in text_lower]
        
        if len(found) >= 2:
            return self._safe_output("spam", 0.9, f"Multiple spam keywords: {', '.join(found[:3])}")
        elif len(found) == 1:
            return self._safe_output("spam", 0.6, f"Detected keyword: {found[0]}")
        else:
            return self._safe_output("safe", 0.3, "No strong spam signals")
    
    def reset(self):
        """Reset environment state"""
        self.current_task = None
        self.step_count = 1
        self.reward = 0.0
        self.done = False
        self.current_email = None
        self.last_observation = None
        
        return self._safe_output("safe", 0.0, "Environment reset")
    
    def set_task(self, task_name: str):
        """Set current task"""
        self.current_task = task_name
        return {"message": f"Task set to {task_name}"}
    
    def step(self, action):
        """
        MUST return EXACTLY 4 values:
        (observation: dict, reward: float, done: bool, info: dict)
        """
        try:
            print("🔥 STEP CALLED SUCCESSFULLY")
            
            if not isinstance(action, str) or not action.strip():
                raise ValueError("Invalid input")
            
            self.current_email = action.strip()
            
            # Safe classification
            result = self._classify_email(self.current_email)
            
            # Force dict type
            if not isinstance(result, dict):
                result = {}
            
            print(f" CLASSIFICATION RESULT: {result}")
            intent = str(result.get("intent", "safe"))
            confidence = float(result.get("confidence", 0.0))
            risk_level = str(result.get("risk_level", "low"))
            risk_score = float(result.get("risk_score", 0.0))
            explanation = str(result.get("explanation", "No explanation"))
            print(f" EXTRACTED VALUES: intent={intent}, conf={confidence}, risk={risk_level}, score={risk_score}, expl={explanation}")
            
            # Calculate reward
            reward = 0.0
            if intent in ["spam", "phishing"]:
                reward += 0.4
            if confidence > 0.7:
                reward += 0.3
            expected_risk = "high" if intent in ["spam", "phishing"] else "low"
            if risk_level == expected_risk:
                reward += 0.2
            if explanation and len(explanation) > 10:
                reward += 0.1
            reward = min(1.0, max(0.0, reward))
            
            # Mark episode complete
            self.done = True
            
            # Create observation dict
            observation = {
                "intent": intent,
                "confidence": confidence,
                "risk_level": risk_level,
                "risk_score": risk_score,
                "explanation": explanation,
            }
            
            # Create info dict
            info = {
                "task": self.current_task,
                "step_count": self.step_count
            }
            
            print(f"🔥 RETURNING 4 VALUES: obs={type(observation)}, reward={type(reward)}, done={type(self.done)}, info={type(info)}")
            
            # ALWAYS return exactly 4 values - HUGGINGFACE SPECIAL FIX
            print(f"🔥 HUGGINGFACE FIX: obs={type(observation)}, reward={type(reward)}, done={type(self.done)}, info={type(info)}")
            
            # HUGGINGFACE WORKAROUND: Store in instance variables first
            self._return_obs = observation
            self._return_reward = float(reward)
            self._return_done = self.done
            self._return_info = info
            
            # Create tuple using a different method
            result_tuple = (self._return_obs, self._return_reward, self._return_done, self._return_info)
            
            print(f"🔥 HUGGINGFACE TUPLE: {type(result_tuple)}, LENGTH: {len(result_tuple)}")
            
            # Force return using tuple()
            return tuple(result_tuple)
            
        except Exception as e:
            print("🔥 STEP ERROR:", e)
            
            # Safe fallback that always returns 4 values
            observation = {
                "intent": "safe",
                "confidence": 0.0,
                "risk_level": "low",
                "risk_score": 0.0,
                "explanation": f"Error: {str(e)}"
            }
            
            # HUGGINGFACE EXCEPT FIX
            print(f"🔥 HUGGINGFACE EXCEPT: Creating fallback tuple")
            
            # Store in instance variables
            self._return_obs = observation
            self._return_reward = 0.0
            self._return_done = True
            self._return_info = {"error": str(e)}
            
            # Create tuple
            except_tuple = (self._return_obs, self._return_reward, self._return_done, self._return_info)
            
            print(f"🔥 HUGGINGFACE EXCEPT TUPLE: {type(except_tuple)}, LENGTH: {len(except_tuple)}")
            
            return tuple(except_tuple)
    
    def state(self):
        """Get current environment state"""
        return {
            "step_count": self.step_count,
            "done": self.done,
            "current_task": self.current_task,
            "last_observation": self.last_observation
        }
