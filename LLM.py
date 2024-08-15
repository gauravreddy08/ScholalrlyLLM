from openai import OpenAI
from dotenv import load_dotenv
from RAG import RAG
import json

load_dotenv()

class LLM():
    def __init__(self, model_name='gpt-4o', system=None):
        
        self.model = OpenAI()
        self.model_name = model_name

        self.messages = []

        self.database = RAG()

        if system is not None:
            self._append('system', system)
        else:
            print("[WARNING] System Prompt Missing!")
        
        f = open('tools.json', 'r')
        self.tools = json.load(f)

    def call(self, prompt=None, tool_choice='auto'):

        if prompt: self._append('user', prompt)
        
        completion = self.model.chat.completions.create(
                        model=self.model_name,
                        messages=self.messages,
                        tools = self.tools,
                        tool_choice=tool_choice
                    )
        
        response = completion.choices[0].message.content
        self._append('assistant', str(response))

        tool_calls = completion.choices[0].message.tool_calls
        
        if tool_calls:
            self.messages.append(completion.choices[0].message)
            return self.retrieve(tool_calls)
        else:
            return response
    
    def _append(self, role: str, content: str):
        self.messages.append({'role': role,
                              'content': str(content)})
        
    def retrieve(self, tool_calls):
        for tool_call in tool_calls:
            if tool_call.function.name == 'knowledge_retriever':
                function_args = json.loads(tool_call.function.arguments)

                function_response = self.database.retrieve(
                    query=function_args.get("query")
                )

                self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": function_response,
                })

        return self.call(tool_choice='auto')