from prompt_templates import *
from functions.utils import *
from openai import OpenAI


class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model="gpt-3.5-turbo",
    ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

           
    def get_completion(self, prompt, temperature=0.3):
        self.messages = []
        self.messages.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content}
        )
        return completion.choices[0].message.content
    

filomena_core =  GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior=prompt_templates2['Instruction Identification'])

def get_instruction(query, chat_history):
    prompt = f"""
            The User Message is:{query}
            The Chat History is:{chat_history}
            """

    query_formatted = filomena_core.get_completion(prompt)
    return query_formatted
