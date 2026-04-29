from langchain_core.prompts import PromptTemplate

# Prompt template for Health Coach LLM
health_coach_template = """
You are a Health Coach. Based on the user's activity_score of {activity_score} and their last_goal_reached of {last_goal_reached}, write a motivating, non-judgmental SMS under 160 characters.

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