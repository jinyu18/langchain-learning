import os
from openai import AzureOpenAI
import httpx

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


# client = OpenAI(
#     # This is the default and can be omitted
#     api_key='',
#     base_url="https://openai-felix.openai.azure.com",
#     http_client=httpx.Client(
#         proxies="http://proxy.emea.ibm.com:8080",
#         transport=httpx.HTTPTransport(local_address="0.0.0.0"),
#     ),
# )
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_completion(prompt, model="gpt-35-turbo-felix"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message.content

# response=get_completion("What is 1+1?")
# print(response)

from langchain_openai import AzureChatOpenAI

chat = AzureChatOpenAI(temperature=0.0, openai_api_version="2023-12-01-preview", azure_deployment="gpt-35-turbo-felix", openai_api_key=os.getenv("AZURE_OPENAI_KEY"))

chat

template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""

from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(template_string)

prompt_template.messages[0].prompt

prompt_template.messages[0].prompt.input_variables

customer_style = """American English \
in a calm and respectful tone
"""

customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse, \
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

customer_messages = prompt_template.format_messages(
                    style=customer_style,
                    text=customer_email)

print(type(customer_messages))
print(type(customer_messages[0]))
print(customer_messages[0])
# Call the LLM to translate to the style of the customer message
customer_response = chat(customer_messages)
print(customer_response.content)