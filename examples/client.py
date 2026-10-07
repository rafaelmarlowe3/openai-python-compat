import os
from openai import OpenAI,AsyncOpenAI
client=OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url=os.getenv('OPENAI_BASE_URL','https://argolink.io/v1'))
def chat():
 return client.chat.completions.create(model=os.getenv('TEXT_MODEL','gpt-5.4'),messages=[{'role':'user','content':'Say hello.'}])
def response():
 return client.responses.create(model=os.getenv('TEXT_MODEL','gpt-5.4'),input='Give one sentence.')
def image():
 return client.images.generate(model=os.getenv('IMAGE_MODEL','gpt-image-2'),prompt='A blue paper boat',size='1024x1024')
