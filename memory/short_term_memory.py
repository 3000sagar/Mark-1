class ShortTermMemory:
    def __init__(self, max_items=10):
        self.history = []
        self.max_items = max_items

    def add(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })

        # 🔥 prevent memory overflow
        if len(self.history) > self.max_items:
            self.history.pop(0)

    def get_context(self) -> str:
        """Full memory (rarely used)"""
        context = ""
        for item in self.history:
            context += f"{item['role']}: {item['content']}\n"
        return context

    def get_last(self, n=2):
        """Get last N memory items (MOST IMPORTANT)"""
        return self.history[-n:]

    def get_recent_context(self, n=2) -> str:
        """Formatted recent context"""
        recent = self.get_last(n)

        context = ""
        for item in recent:
            context += f"{item['role']}: {item['content']}\n"

        return context

    def clear(self):
        self.history = []