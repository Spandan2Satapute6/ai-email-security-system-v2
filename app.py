import gradio as gr
from server.environment import EmailEnv

# initialize your environment
env = EmailEnv()

def analyze_email(email_text):
    try:
        env.reset()
        observation, reward, done, info = env.step(email_text)

        return f"""
Intent: {observation.get("intent")}
Confidence: {observation.get("confidence")}
Risk Level: {observation.get("risk_level")}
Risk Score: {observation.get("risk_score")}
Explanation: {observation.get("explanation")}
Reward: {reward}
"""
    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.Interface(
    fn=analyze_email,
    inputs=gr.Textbox(lines=5, placeholder="Paste email content here..."),
    outputs="text",
    title="AI Email Security System",
    description="Detect spam, phishing, and suspicious emails"
)

demo.launch(server_name="0.0.0.0", server_port=7860)