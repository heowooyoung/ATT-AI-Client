import os

import httpx
import openai

from qna.repository.qna_repository import QnaRepository
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

openaiApiKey = os.getenv('OPENAI_API_KEY')
if not openaiApiKey:
    raise ValueError('API Key가 준비되어 있지 않습니다.')

# fine-tuned model ID
model = os.getenv('ENFP_TEST')

class QnaRepositoryImpl(QnaRepository):

    __instance = None
    client = OpenAI()

    headers = {
        'Authorization': f'Bearer {openaiApiKey}',
        'Content-Type': 'application/json',
    }

    OPENAI_CHAT_COMPLETIONS_URL= "https://api.openai.com/v1/chat/completions"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def dateQuestion(self, userSendMessage):
        # QnA를 위한 시스템 프롬프트
        system_prompt = {"role": "system", "content": "Summarize the context of the conversation and answer with the day of the week in one word." 
                                                      "You must not answer in a full sentence, only in the form of a day of the week." 
                                                      "If the day hasn't been decided, answer 'none'." 
                                                      "Make sure to respond in Korean."}
        # systemPrompt를 대화의 맨 앞에 추가
        userSendMessage.insert(0, system_prompt)
        data = {
            'model': model,
            'messages': userSendMessage,
            'max_tokens': 256,
            'temperature': 0.1,
        }

        # api에 추론 요청을 보내는 부분
        async with httpx.AsyncClient(timeout=10000) as client:
            try:
                response = await client.post(self.OPENAI_CHAT_COMPLETIONS_URL, headers=self.headers, json=data)
                response.raise_for_status()

                generatedText = response.json()['choices'][0]['message']['content'].strip()
                return { "generatedText": [generatedText] } # dict 형식으로 반환해주어야 함

            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {str(e)}")
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e}")

            except (httpx.RequestError, ValueError) as e:
                print(f"Request Error: {e}")
                raise HTTPException(status_code=500, detail=f"Request Error: {e}")

    async def locationQuestion(self, userSendMessage):
        system_prompt = {"role": "system", "content": "Summarize the context of the conversation and answer with the location where we are meeting in one word." 
                                                      "You must not answer in a full sentence, only in word form." 
                                                      "If the location hasn't been decided, answer 'none'." 
                                                      "Make sure to respond in Korean."}
        # systemPrompt를 대화의 맨 앞에 추가
        userSendMessage.insert(0, system_prompt)
        data = {
            'model': model,
            'messages': userSendMessage,
            'max_tokens': 256,
            'temperature': 0.1,
        }

        # api에 추론 요청을 보내는 부분
        async with httpx.AsyncClient(timeout=10000) as client:
            try:
                response = await client.post(self.OPENAI_CHAT_COMPLETIONS_URL, headers=self.headers, json=data)
                response.raise_for_status()

                generatedText = response.json()['choices'][0]['message']['content'].strip()
                return { "generatedText": [generatedText] } # dict 형식으로 반환해주어야 함

            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {str(e)}")
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e}")

            except (httpx.RequestError, ValueError) as e:
                print(f"Request Error: {e}")
                raise HTTPException(status_code=500, detail=f"Request Error: {e}")