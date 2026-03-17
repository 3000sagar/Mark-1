from memory.short_term_memory import ShortTermMemory


class Executor:
    def __init__(self, registry, model, planner):
        self.registry = registry
        self.model = model
        self.planner = planner
        self.memory = ShortTermMemory()
 
    def execute(self, plan, user_command="", retries=0, max_retries=3):
        context = None

        for step in plan:
            tool_name = step.get("tool")

            try:
                # 🔹 CASE 1: reasoning step
                if tool_name == "none":
                    action = step.get("action", "")

                    context_text = self.memory.get_recent_context(2)

                    context = self.model.generate(
                        f"{action} based on this:\n{context_text}"
                    )

                    self.memory.add("assistant", context)
                    continue

                # 🔹 CASE 2: invalid tool
                if tool_name not in self.registry.list_tools():
                    raise Exception(f"Unknown tool: {tool_name}")

                tool = self.registry.get(tool_name)

                args = step.get("args", {})

                # 🔥 inject previous result
                if "content" in args and args["content"] == "result":
                    args["content"] = context

                result = tool.execute(**args)

                if not result["success"]:
                    raise Exception(result["error"])

                context = result["result"]
                self.memory.add("tool", context)
                


                # 🔥 INTENT VALIDATION (ADD HERE)
                if isinstance(user_command, str) and "read" in user_command.lower() and tool_name == "list_directory":
                    files = context

                    import difflib
                    requested = step.get("args", {}).get("path", "")

                    suggestion = difflib.get_close_matches(requested, files, n=1)

                    if suggestion:
                        return f"❌ File not found.\nDid you mean: {suggestion[0]} ?\nAvailable files: {files}"
                    else:
                        return f"❌ File not found.\nAvailable files: {files}"

            except Exception as e:
                print(f"⚠️ Step failed: {e}")

                # 🔥 STOP infinite loop
                if retries >= max_retries:
                    files = self.registry.get("list_directory").execute(path="")

                    if files["success"]:
                        file_list = files["result"]

                        # 🔥 try to suggest closest match
                        import difflib
                        suggestion = difflib.get_close_matches(
                            step.get("args", {}).get("path", ""),
                            file_list,
                            n=1
                        )

                        if suggestion:
                            return f"❌ File not found.\nDid you mean: {suggestion[0]} ?\nAvailable files: {file_list}"
                        else:
                            return f"❌ File not found.\nAvailable files: {file_list}"

                # 🔥 SELF-CORRECTION
                new_plan = self.planner.replan(str(e), context)

                if not new_plan:
                    return f"❌ Could not recover: {e}"

                print("🔁 Replanning...")

                return self.execute(new_plan, user_command, retries + 1)

        return context