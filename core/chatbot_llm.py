# Import modules and libraries
from utils import prompt, logger
import requests
import json

log = logger.get_logger(__name__)

def chat_llm(model: str, history: list[dict], question: str) -> str:
    # Formatting the default prompt
    llm_prompt = [{"role": "system", "content": prompt.DEFAULT_PROMPT}]
    # Checking if history is avaible
    if history:
        llm_prompt.extend(history)

    # Adding the user message to the prompt
    llm_prompt.append({"role": "user", "content": question})

    # Send the the complete prompt to local model
    log.info("Parsing user messages into local model")
    try:
        response = requests.post(
            url="http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": llm_prompt,
                "options": {"temperature": 0.3}
            },
            stream=True,
            timeout=180
        )

        # Cleaning up the answer given by Local model
        answer_part = []
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    answer_part.append(data["message"]["content"])
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue

        # Return local model's response
        log.info("Return local model's response")
        return "".join(answer_part).strip() or "No response received."
    
    except Exception as e:
        log.error(f"Error in chat_llm: {e}")
        return "⚠️ Sorry, something went wrong while contacting the local model."
