from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile

from dotenv import load_dotenv

from third_parties.twitter import scrape_user_tweets

load_dotenv()

name = "Harrison Chase"
if __name__ == "__main__":
    print("Hello Langchain!")

    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    summary_template = """
        given the LinkedIn information {linkedin} and Twitter {twitter} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        3. A topic that may interest them
        4. 2 creative Ice breakers to open a conversation with them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin", "twitter"], template=summary_template
    )

    llm = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo"
    )  # temperature decides how creative the model would be... 0 means not creative at all!

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print(chain.run(linkedin=linkedin_data, twitter=tweets))
