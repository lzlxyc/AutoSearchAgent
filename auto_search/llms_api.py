import os
import openai
from dotenv import load_dotenv

MessageDict = dict
MessageType = openai.types.chat.chat_completion_message.ChatCompletionMessage

class LlmBox:
    '''
    提供大模型调用服务
    1、默认使用deepseek-chat模型
    2、需要在根目录下配置好.env文件
    '''
    def __init__(self, model_name="deepseek-chat", env_path='../.env'):
        load_dotenv(env_path)
        ds_api_key = os.getenv("DS_API_KEY")
        ds_api_url = os.getenv("DS_API_URL")

        self.client = openai.OpenAI(
            api_key=ds_api_key,
            base_url=ds_api_url,
        )
        self.model_name = model_name

        print(f"▌ Model set to {self.model_name}")

    def build_messages(self, prompt:str, system_pt=None) -> MessageDict:
        messages = []
        if system_pt is not None:
            messages.append({"role": "system", "content": system_pt})

        messages.append({"role": "user", "content": prompt})

        return messages


    def chat(self, prompt='你好。',
             system_pt=None,
             messages=None,
             tools=None,
             tool_choice='auto') -> MessageType:
        '''基础的大模型问答接口，可以传入提示词，也可以直接传入message
        :param prompt: 提示词
        :param system_pt: 系统提示词
        :param messages: 传入的message
        :param tools: function calls工具
        :param tool_choice: 是否调用外部工具
        :return: 返回大模型输出的message
        '''
        if messages is None:
            messages = self.build_messages(prompt, system_pt)

        if tools is None:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice
            )
        return response.choices[0].message