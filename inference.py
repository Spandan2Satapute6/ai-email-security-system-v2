import requests
import json
import sys
import time
from server.environment import EmailEnv


class OpenEnvClient:
    """Client for interacting with OpenEnv Email Security System API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def reset_environment(self):
        """Reset environment."""
        try:
            response = self.session.post(f"{self.base_url}/reset")
            return response.json()
        except Exception as e:
            print(f"Reset error: {e}")
            return {}
    
    def set_task(self, task_name):
        """Set the current task for evaluation."""
        try:
            response = self.session.post(f"{self.base_url}/set_task", 
                                   params={"task_name": task_name})
            return response.json()
        except Exception as e:
            print(f"Set task error: {e}")
            return {}
    
    def classify_email(self, text):
        """Classify email text."""
        try:
            response = self.session.post(f"{self.base_url}/classify",
                                   json={"text": text})
            return response.json()
        except Exception as e:
            print(f"Classify error: {e}")
            return {}
    
    def get_state(self):
        """Get current environment state."""
        try:
            response = self.session.get(f"{self.base_url}/state")
            return response.json()
        except Exception as e:
            print(f"State error: {e}")
            return {}


def run_openeval_demo():
    """Run OpenEnv evaluation with proper API calls."""
    
    print("[START]")
    
    # Test emails for each task
    test_emails = {
        "EASY": "Congratulations! You've won $1,000,000! Click here NOW!",
        "MEDIUM": "Hello team, please review of quarterly report before our meeting.",
        "HARD": "URGENT: Your bank account will be suspended! Click http://fake-bank.com to verify immediately!"
    }
    
    client = OpenEnvClient()
    rewards = []
    
    for task_name, email_text in test_emails.items():
        print(f"[TASK {task_name}]")
        
        try:
            # Reset environment
            reset_result = client.reset_environment()
            time.sleep(0.1)  # Small delay between requests
            
            # Set task
            task_result = client.set_task(task_name.lower() + "_task")
            time.sleep(0.1)
            
            # Step 1: Classify email
            classify_result = client.classify_email(email_text)
            reward = classify_result.get("reward", 0.0)
            rewards.append(reward)
            
            print(f"step 1 → reward: {reward:.3f}")
            
        except Exception as e:
            print(f"Error in {task_name}: {e}")
            rewards.append(0.0)
            print(f"step 1 → reward: 0.000")
    
    # Calculate final average score
    if rewards:
        average_score = sum(rewards) / len(rewards)
        print(f"[END]")
        print(f"Final average score: {average_score:.3f}")
    else:
        print("[END]")
        print("Final average score: 0.000")


def test_api_connectivity():
    """Test if API is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print("❌ API not responding correctly")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        print("Please ensure that FastAPI server is running on http://localhost:8000")
        return False


if __name__ == "__main__":
    print("🔍 OpenEnv Email Security System Evaluation")
    print("=" * 50)
    
    # Test API connectivity first
    if not test_api_connectivity():
        sys.exit(1)
    
    # Run the evaluation demo
    run_openeval_demo()
    
    print("\n✅ Evaluation completed successfully!")
    sys.exit(0)
