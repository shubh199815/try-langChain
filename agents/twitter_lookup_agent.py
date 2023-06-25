from tools.tools import get_profile_url

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType


from dotenv import load_dotenv

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    template = """given the name {name_of_person} I want you to find me a link to their Twitter profile page, and extract from it their username.
                    In your final answer only the person's username"""
    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile page",
            func=get_profile_url,
            description="useful for when you get the Twitter username",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))
    return twitter_username
