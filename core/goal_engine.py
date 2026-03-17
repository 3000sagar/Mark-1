class GoalEngine:
    def __init__(self, planner, executor, model):
        self.planner = planner
        self.executor = executor
        self.model = model

    def run(self, goal: str, max_steps=5):
        print(f"\n🎯 Goal: {goal}\n")

        current_goal = goal

        for step in range(max_steps):
            print(f"--- Step {step+1} ---")

            # 🔥 Get context
            context = self.executor.memory.get_recent_context(3)

            # 🔥 Plan next action
            plan = self.planner.plan(current_goal, context)

            if not plan:
                print("❌ Planning failed")
                return

            # 🔥 Execute
            result = self.executor.execute(plan, current_goal)

            print(f"Result: {result}")

            # 🔥 Check completion
            if self.is_goal_complete(goal, result):
                print("\n✅ Goal completed")
                return

            # 🔥 Update goal (reflection)
            current_goal = self.reflect(goal, result)

        print("\n⚠️ Max steps reached")

    def is_goal_complete(self, goal, result):
        prompt = f"""
                    Goal:
                    {goal}

                    Result:
                    {result}

                    Did we achieve the goal?

                    Answer ONLY:
                    YES or NO
                    """
        response = self.model.generate(prompt)

        return "YES" in response.upper()
        
    def reflect(self, goal, result):
        prompt = f"""
                    Goal:
                    {goal}

                    Current result:
                    {result}

                    What should be the NEXT step to complete the goal?

                    Respond with a short instruction.
                    """
        return self.model.generate(prompt)