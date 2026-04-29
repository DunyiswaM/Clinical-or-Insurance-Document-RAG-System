from langchain_core.prompts import PromptTemplate

# Prompt template for Health Coach LLM
health_coach_template = """
You are a Health Coach. Create a motivating SMS under 160 chars for user with activity_score {activity_score} and last_goal_reached: {last_goal_reached}.

SMS:
"""

health_coach_prompt = PromptTemplate(
    input_variables=["activity_score", "last_goal_reached"],
    template=health_coach_template
)

# Example usage
if __name__ == "__main__":
    # Fill in the variables
    prompt = health_coach_prompt.format(activity_score=85, last_goal_reached="10,000 steps")
    print(prompt)