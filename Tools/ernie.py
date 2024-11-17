from openai import OpenAI
import json

class ErnieClass(object):
    """
    ErnieBot API封装类

    Args:
        access_token (str): 用于访问ErnieBot API的access token。
        api_type (str, optional): 使用的ErnieBot API的类型。默认为"aistudio"。

    Returns:
        None

    """
    def __init__(self, access_token):
        self.client = OpenAI(
             api_key=access_token,  # 含有 AI Studio 访问令牌的环境变量，https://aistudio.baidu.com/account/accessToken,
             base_url="https://aistudio.baidu.com/llm/lmapi/v3",  # aistudio 大模型 api 服务域名
        )
        self.chat_history = []

    def chat(self, prompt, role='user'):
        self.chat_history.append({'role': role, 'content': prompt})
        chat_completion = self.client.chat.completions.create(
            messages=self.chat_history,
            model="ernie-3.5-8k",
        )

        result = chat_completion.choices[0].message.content
        self.chat_history.append({'role': 'assistant', 'content': result})
        return result

    def get_llm_answer_with_msg(self, msg):
        chat_completion = self.client.chat.completions.create(
            messages=msg,
            model="ernie-3.5-8k",
        )

        result = chat_completion.choices[0].message.content

        return result

    def get_llm_answer(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            model="ernie-3.5-8k",
        )

        result = chat_completion.choices[0].message.content

        return result

    def extract_json_from_llm_answer(self, result, start_str="```json", end_str="```", replace_list=["\n"]):
        s_id = result.index(start_str)
        e_id = result.index(end_str, s_id+len(start_str))
        json_str = result[s_id+len(start_str):e_id]
        for replace_str in replace_list:
            json_str = json_str.replace(replace_str,"")
        # print(json_str)
        try:
            json_dict = json.loads(json_str)
        except Exception as e:
            print("Error: ", e)
            print("json_str: ", json_str)
            json_dict = {}
        return json_dict

    def extract_markdown_from_llm_answer(self, result, start_str="```markdown", end_str="```", replace_list=["\n"]):
        s_id = result.index(start_str)
        e_id = result.index(end_str, s_id + len(start_str))
        markdown_str = result[s_id + len(start_str):e_id]
        return markdown_str

    def get_llm_json_answer(self, prompt):
        result = self.get_llm_answer(prompt)
        try:
            json_dict = self.extract_json_from_llm_answer(result)
        except Exception as e:
            print("Error: ", e)
            print("result: ", result)
            json_dict = {}
        return json_dict

    def get_llm_markdown_answer(self, prompt, raw_flag=False):
        result = self.get_llm_answer(prompt)
        if raw_flag == True:
            markdown_str = result
        else:
            try:
                markdown_str = self.extract_markdown_from_llm_answer(result)
            except Exception as e:
                print("Error: ", e)
                print("result: ", result)
                markdown_str = ""
        return markdown_str