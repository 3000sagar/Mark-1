from models.ollama_model import OllamaModel
import json
import re


class Planner:
    def __init__(self):
        self.model = OllamaModel()

    def extract_json(self, text: str):
        try:
            text = text.strip()

            if "```" in text:
                text = re.sub(r"```.*?\n", "", text)
                text = text.replace("```", "")

            match = re.search(r"\[.*\]", text, re.DOTALL)
            if match:
                return json.loads(match.group())

            return None

        except Exception:
            return None

    def plan(self, command: str, context: str = ""):
        prompt = f"""
You are a strict AI task planner.

Your job is to convert user requests into a sequence of steps.
IMPORTANT:
- You are NOT allowed to generate code
- You are NOT allowed to explain
- You MUST ONLY use the provided tools
- Every step MUST be a tool call

AVAILABLE TOOLS:
- read_file(path)
- write_file(path, content)
- list_directory(path)
- run_command(command)

CONTEXT:
{context}

USER REQUEST:
"{command}"

STRICT RULES:
1. NEVER invent file names
2. ONLY use file names mentioned in user request or context
3. If user refers to "it", "that", use previous context — DO NOT read file again
4. If task is reasoning (summarize, keywords, explain) → use:
   {{"tool": "none", "action": "..."}}
5. DO NOT repeat a failed action
6. DO NOT create files unless explicitly asked
7. DO NOT guess paths
8. If unsure → use "none"
9. When writing a file, use content from previous step result
10. NEVER use run_command unless explicitly required

OUTPUT FORMAT (STRICT JSON ONLY, NO TEXT):

[
  {{"tool": "read_file", "args": {{"path": "file.txt"}}}},
  {{"tool": "none", "action": "summarize"}},
  {{"tool": "write_file", "args": {{"path": "output.txt", "content": "result"}}}}
]
"""

        response = self.model.generate(prompt)
        plan = self.extract_json(response)
        plan = self.validate_plan(plan)

        # 🔥 Safe fallback
        if not plan:
            return [{"tool": "none", "action": f"respond to: {command}"}]

        return plan

    def replan(self, error, context):
        prompt = f"""
You are an AI agent fixing a failed step.

Error:
{error}

Previous context:
{context}

IMPORTANT RULES:
- DO NOT repeat the same failed action
- DO NOT retry same file if it doesn't exist
- DO NOT create files unless user asked
- If task cannot be completed → explain instead

Goal:
Fix the issue WITHOUT repeating the same mistake.

Available tools:
- read_file(path)
- write_file(path, content)
- list_directory(path)
- run_command(command)

Return ONLY JSON array:
[
  {{"tool": "tool_name", "args": {{}}}}
]
"""

        response = self.model.generate(prompt)

        plan = None

        try:
            if "```" in response:
                response = re.sub(r"```.*?\n", "", response)
                response = response.replace("```", "")

            match = re.search(r"\[.*\]", response, re.DOTALL)
            if match:
                plan = json.loads(match.group())

        except Exception:
            return None

        # 🔥 Validate replan
        return self.validate_plan(plan)

    def validate_plan(self, plan):
        valid_tools = ["read_file", "write_file", "list_directory", "run_command", "none"]

        if not isinstance(plan, list) or len(plan) == 0:
            return None

        for step in plan:
            if not isinstance(step, dict):
                return None

            if "tool" not in step:
                return None

            tool = step["tool"]

            if tool not in valid_tools:
                return None

            # 🔥 Validate args for tools
            if tool != "none":
                if "args" not in step or not isinstance(step["args"], dict):
                    return None

            # 🔥 Validate action for reasoning
            if tool == "none":
                if "action" not in step:
                    return None

            # 🔥 Block fake filenames like context.txt
            args = step.get("args", {})
            for value in args.values():
                if isinstance(value, str):
                    if "context" in value.lower():
                        return None

        return plan