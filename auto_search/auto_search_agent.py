import os
import json


from config import SAVE_DATA_DIR
from llms_api import LlmBox
from tools import identify_model, convert_keyword
from function_calls import get_answer, SupportFunctionCallList

class AutoSearchAgent:
    def __init__(self):
        self.llm_box = LlmBox()

    def run_conversation(self,
                         messages,
                         functions_list=None,
                         tool_choice='auto',
                         verbose=False) -> str:
        """
        能够自动执行外部函数调用的Chat对话模型
        :param messages: 必要参数，字典类型，输入到Chat模型的messages参数对象
        :param functions_list: 可选参数，默认为None，可以设置为包含全部外部函数的列表对象
        :param tool_choice: 是否调用外部工具
        :param verbose: 是否进行过程的打印
        :return：Chat模型输出结果
        """
        # 如果没有外部函数库，则执行普通的对话任务
        if functions_list is None:
            response_message = self.llm_box.chat(messages=messages)
            final_response = response_message.content

        # 若存在外部函数库，则需要灵活选取外部函数并进行回答
        else:
            # 创建functions对象
            functions = SupportFunctionCallList
            # 创建外部函数库字典
            available_functions = {func.__name__: func for func in functions_list}

            # first response
            response_message =  self.llm_box.chat(messages=messages,
                                                  tools=functions,
                                                  tool_choice=tool_choice)
            if verbose:
                print(f"{functions=}")
                print(f"{response_message=}")

            # 判断返回结果是否存在function_call，即判断是否需要调用外部函数来回答问题
            if response_message.tool_calls:
                # 需要调用外部函数
                # 获取函数名
                function_name = response_message.tool_calls[0].function.name
                # 获取函数对象
                fuction_to_call = available_functions[function_name]
                # 获取函数参数
                function_args = json.loads(response_message.tool_calls[0].function.arguments)
                # 将函数参数输入到函数中，获取函数计算结果
                function_response = fuction_to_call(**function_args)

                if verbose:
                    print(f"{function_name=}\n{function_args=}\n{function_response=}")

                # messages中拼接first response消息
                messages.append(response_message)
                # messages中拼接函数输出结果
                md_prompt = "\n\n最后以markdown格式进行输出。"

                messages.append(
                    {
                        "role": "tool",
                        "content": function_response + md_prompt,
                        'tool_call_id': response_message.tool_calls[0].id,
                    }
                )
                # 第二次调用模型
                second_response = self.llm_box.chat(messages=messages)
                # 获取最终结果
                final_response = second_response.content
            else:
                final_response = response_message.content

        del messages

        return final_response

    def save_report(self, query:str, answer:str):
        '''进行报告结果的保存'''
        save_path = os.path.join(SAVE_DATA_DIR, f'report_{query}.md')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(answer)


    def sample_run(self, query:str,
                   use_search:bool=True,
                   use_keyword:bool=True,
                   save_report:bool=True):
        '''
        :param query: 输入的需要搜索的问题
        :param use_search: 是否启动联网搜索
        :param use_keyword: 是否将用户的搜索先进行关键词提取
        :return: 搜索结果
        '''
        if use_keyword:
            query = convert_keyword(query, self.llm_box)
            print(f">>> 🤖: 提取到搜索关键词:{query}")

        # 调用判别模型
        if (response:= identify_model(query, llm_box=self.llm_box)) is not None:
            print(f">>> 🤖: {response}")
            return response

        if use_search:
            tool_choice = {"type": "function","function": {"name": "get_answer"}}
        else:
            tool_choice = 'auto'

        print(">>> 正在调用外部搜索工具...")
        answer = self.run_conversation(
            messages=[{"role": "user", "content": query}],
            functions_list=[get_answer],
            tool_choice=tool_choice
        )

        if save_report:
            self.save_report(query, answer)

        return answer


    def chat(self, query="你好呀", system_message=None):
        if system_message is None:
            system_message = [{"role": "system", "content": "你是一位百科问答助手。"}]
        messages = system_message
        messages.append({"role": "user", "content": query})

        while True:
            print(f">>> 👤: {query}")
            answer = self.sample_run(query)
            print(f">>> 🤖: {answer}")

            # 询问用户是否还有其他问题
            query = input(">>> 🤖: 您还有其他问题吗？(输入退出以结束对话): ")
            if query == "退出":
                del messages
                break

            # 记录用户回答
            messages.append({"role": "user", "content": query})

