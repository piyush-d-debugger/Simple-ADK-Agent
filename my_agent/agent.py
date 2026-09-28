from google.adk.agents.llm_agent import Agent
from google.adk import Event, Workflow

classifier_agent = Agent(
    model='gemini-3.6-flash',
    name='classifier',
    description='Classifies a question as Science, History or Geography',
    instruction="Read the user's question , Respond with only one word : (SCIENCE, HISTORY OR GEOGRAPHY), Do not provide any other text or explaination."
)

def save_question(node_input: str) -> Event:
    return Event(output=node_input, state={"question": node_input})

def topic_router(node_input) -> Event:
    text = str(node_input).strip().upper()
    if text == "SCIENCE":
        return Event(route="SCIENCE")

    elif text == "HISTORY":
        return Event(route="HISTORY")

    elif text == "GEOGRAPHY":
        return Event(route="GEOGRAPHY")

    # Fallback
    return Event(route="HISTORY")

science_agent = Agent(
    model='gemini-3.6-flash',
    name='science_Agent',
    description='Answers science questions',
    instruction="Explains the science topic with 3-4 beginner friendly sentences: {question}.",
)


history_agent = Agent(
    model='gemini-3.6-flash',
    name='history_Agent',
    description='Answers history questions',
    instruction="Explains the history topic with 3-4 beginner friendly sentences: {question}.",
)

geography_agent = Agent(
    model='gemini-3.6-flash',
    name='geography_Agent',
    description='Answers geography questions',
    instruction="Explains the geography topic with 3-4 beginner friendly sentences: {question}.",
)

root_agent = Workflow(
    name='topic_router_workflow',
    edges=[
        ("START", save_question, classifier_agent, topic_router),
        (topic_router , {
            "SCIENCE": science_agent,
            "HISTORY": history_agent,
            "GEOGRAPHY": geography_agent
        })
    ]
)

