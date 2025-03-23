import json
import requests, os
from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TRAVILY_API_KEY = os.getenv("TRAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=TRAVILY_API_KEY)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_medical_info",
            "description": "Retrieve possible conditions based on symptoms.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "User symptoms"
                    }
                },
                "required": ["symptoms"]
            }
        }
    }
]


SYSTEM_PROMPT = """
    You are an AI-based Tele Medic assistant named (JD Diaz Tele Medic) that provides possible conditions based on user symptoms. 
    Use human-like, empathetic responses while keeping medical information factual. 

    When a user starts discussing symptoms or a health issue, engage them in a natural conversation to gather more details. Its important to make
    the conversation feel natural. To do so, you can try asking follow-up questions like:

    - "How long have you been experiencing this?"
    - "Have you noticed any other symptoms along with it?"
    - "On a scale of 1-10, how severe is it?"
    - "Does anything make it better or worse?"

    But make sure not to be too pestering with these questions.

    Only after gathering enough information, process the symptoms and provide possible conditions. 
    If external data is needed, call the 'fetch_medical_info' function.

    Whenever recommending a user about some disease or giving a suggestion, ALWAYS remind users to consult a doctor for a proper diagnosis.
    Your goal is to provide guidance and support while ensuring users understand the importance of professional medical evaluation. Being empathic and professional is key.

"""  

# English System Prompt
SYSTEM_PROMPT_EN = """
    You are an AI-based Tele Medic assistant named (JD Diaz Tele Medic) that provides possible conditions based on user symptoms. 
    Use human-like, empathetic responses while keeping medical information factual. 

    When a user starts discussing symptoms or a health issue, engage them in a natural conversation to gather more details. 
    Ask follow-up questions like:
    - "How long have you been experiencing this?"
    - "Have you noticed any other symptoms along with it?"
    - "On a scale of 1-10, how severe is it?"
    - "Does anything make it better or worse?"

    Only after gathering enough information, process the symptoms and provide possible conditions. 
    If external data is needed, call the 'fetch_medical_info' function.

    Whenever recommending a user about some disease or giving a suggestion, ALWAYS remind users to consult a doctor for a proper diagnosis.
"""

# Spanish System Prompt
SYSTEM_PROMPT = """
    Eres un asistente médico virtual basado en IA llamado (JD Diaz Tele Medic) que proporciona posibles condiciones basadas en los síntomas del usuario. 
    Utiliza respuestas empáticas y parecidas a las humanas, mientras mantienes la información médica factual.

    Cuando un usuario empiece a hablar sobre síntomas o un problema de salud, involúcralo en una conversación natural para obtener más detalles. Es importante que la
    conversación se sienta natural. Para hacerlo, puedes intentar hacer preguntas de seguimiento como:

    - "¿Desde cuándo estás experimentando esto?"
    - "¿Has notado algún otro síntoma junto con esto?"
    - "En una escala del 1 al 10, ¿qué tan grave es?"
    - "¿Hay algo que lo haga mejor o peor?"

    Pero asegúrate de no ser demasiado insistente con estas preguntas.

    Solo después de obtener suficiente información, procesa los síntomas y proporciona las posibles condiciones. 
    Si se necesita información externa, llama a la función 'fetch_medical_info'.

    Siempre que recomiendes algo sobre una enfermedad o des una sugerencia, SIEMPRE recuerda a los usuarios que consulten a un médico para un diagnóstico adecuado.
    Tu objetivo es brindar orientación y apoyo mientras aseguras que los usuarios comprendan la importancia de una evaluación médica profesional. Ser empático y profesional es clave.

"""

class TeleMedicBot:
    def __init__(self, lang = "en",  model="gpt-4o-mini", tools=None, temprature=0.3,max_tokens=4096, system_prompt=None):
        self.lang = lang
        self.model = model
        self.temprature = temprature
        self.max_tokens = max_tokens
        self.tools = tools if tools else TOOLS
        self.system_prompt = SYSTEM_PROMPT_ES if self.lang == "es" else SYSTEM_PROMPT_EN
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = [{"role": "system", "content": self.system_prompt}]

        info = self.__str__()
        print(info)

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content.strip()})

    def web_search_tool(self, symptoms):
        """ Calls the external API (Tavily) to fetch medical data. """
        result = None
        query = f"possible conditions for symptoms: {symptoms}"
        response = tavily_client.search(query)
        print(response)
        if len(response.get('results', [])) > 0:
            result = [res['content'] for res in response['results']]

        print(f"[WEB_SEARCH] Result => {result}")
        return result or {"error": "No relevant information found."}

    def get_inference(self, is_tool=True, stream=False):
        """ Get response from OpenAI API with optional streaming. """
        print(f"[INFO] Conversation Lenght : {len(self.messages)}")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools if is_tool else None,
            tool_choice="auto" if is_tool else None,
            temperature=self.temprature,
            max_tokens=self.max_tokens,
            stream=stream 
        )
        return response

    def chat(self, user_message, stream=False):
        """ Process user input and generate an AI response with optional streaming. """
        self.add_message(role="user", content=user_message)

        # Step 1: Check if a function needs to be called (No Streaming)
        response = self.get_inference(stream=False)
        output = response.choices[0].message

        if hasattr(output, "tool_calls") and output.tool_calls:
            # Step 2: Execute Function if required
            tool_call = output.tool_calls[0]
            print(f'[TOOL_CALL] Tool Call => {tool_call.function}')
            if tool_call.function.name == "fetch_medical_info":
                symptoms = json.loads(tool_call.function.arguments)["symptoms"]
                medical_data = self.web_search_tool(symptoms)

                # Add retrieved data and regenerate response (With Streaming)
                self.add_message(
                    role="assistant",
                    content=f"Using the following relevant info to answer user query. Info: {str(medical_data)}. User Question: {user_message}"
                )

                # Step 3: Now generate the final response using streaming
                response_stream = self.get_inference(is_tool=False, stream=True)
                def stream_response():
                    collected_text = ""
                    for chunk in response_stream:
                        if hasattr(chunk, "choices") and chunk.choices:
                            delta = chunk.choices[0].delta
                            if hasattr(delta, "content") and delta.content:
                                collected_text += delta.content
                                yield delta.content  # Yield progressively
                    self.add_message(role="assistant", content=collected_text)

                return stream_response()

        # Step 4: If no function is required, just return streaming response
        if stream:
            response_stream = self.get_inference(stream=True)
            def stream_response():
                collected_text = ""
                for chunk in response_stream:
                    if hasattr(chunk, "choices") and chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, "content") and delta.content:
                            collected_text += delta.content
                            yield delta.content  # Yield progressively
                self.add_message(role="assistant", content=collected_text)

            return stream_response()

        return {"response": output.content}  # Fallback for non-streaming

    def __str__(self):
        return f"""[BOT] Initialized TeleMedic Bot with 
                    [-] Model::{self.model}
                    [-] Language:: {self.lang}
                    [-] MaxTokens::{self.max_tokens}
                    [-] Temprature::{self.temprature}
                    [-] SystemPrompt::{self.system_prompt[:80].strip()}
                """


if __name__ == "__main__":
    bot = TeleMedicBot()
    while True:
        user_input = input("[USER] : ")
        response_stream = bot.chat(user_input, stream=True)
        print("[BOT] : ", end="", flush=True)

        for chunk in response_stream:
            print(chunk, end="", flush=True)

        print("\n")  # New line after response




# import json
# import requests, os
# from openai import OpenAI
# from dotenv import load_dotenv
# from tavily import TavilyClient

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# TRAVILY_API_KEY = os.getenv("TRAVILY_API_KEY")


# client = OpenAI(api_key=OPENAI_API_KEY)
# tavily_client = TavilyClient(api_key=TRAVILY_API_KEY)


# # OpenAI function for external info retrieval
# TOOLS = [
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_medical_info",
#             "description": "Retrieve possible conditions based on symptoms.",
#             "parameters": {  # ✅ Ensure parameters is an object
#                 "type": "object",
#                 "properties": {
#                     "symptoms": {
#                         "type": "string",
#                         "description": "User symptoms"
#                     }
#                 },
#                 "required": ["symptoms"]
#             }
#         }
#     }
# ]

# # System prompt for guiding the chatbot
# SYSTEM_PROMPT = """
#     You are an AI based Tele Medic assistant named (JD Diaz Tele Medic) that provides possible conditions based on user symptoms. 
#     Use human-like, empathetic responses while keeping medical information factual. 
#     If external data is needed, call the 'fetch_medical_info' function.
#     When ever recomminding user about some disease or giving suggestion ALWAYS remind users to consult a doctor for a proper diagnosis. 
# """



# class TeleMedicBot:
#     def __init__(self , model = "gpt-4o-mini" , tools = None , system_prompt = None):
#         self.model = model
#         self.tools = tools if tools else TOOLS
#         self.system_prompt = system_prompt if system_prompt else SYSTEM_PROMPT
#         self.client = OpenAI(api_key=OPENAI_API_KEY)
#         self.messages = [ {"role": "system", "content": self.system_prompt} ]

#     def add_message(self , role , content) : 
#         self.messages.append({"role": role, "content": content.strip()})

#     def web_search_tool(self, symptoms):
#         result = None
#         query = f"possible conditions for symptoms: {symptoms}"
#         response = tavily_client.search(query)
#         if len(response.get('results' , [])) > 0 : 
#             result = [ result['content'] for result in response['results'] ]
        
#         print(f"[WEB_SEARCH] Result => {result}")
#         return result or {"error": "No relevant information found."}

#     def get_inference(self , is_tool = True ) : 
#         # print(f"[INFO] Messages => {self.messages}")
#         if is_tool  : 
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=self.messages,
#                 tools=self.tools,
#                 tool_choice="auto"
#             )

#         else : 
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=self.messages
#             )

#         return response

#     def chat(self , user_message):
#         self.add_message(role = "user" , content = user_message)
#         response = self.get_inference()

#         output = response.choices[0].message

#         if hasattr(output, "tool_calls") and output.tool_calls:
#             tool_call = output.tool_calls[0]
#             print(f'[TOOL_CALL] Tool Call => {tool_call.function}')
#             if tool_call.function.name == "fetch_medical_info":
#                 symptoms = json.loads(tool_call.function.arguments)["symptoms"]
#                 medical_data = self.web_search_tool(symptoms)

#                 self.add_message(role = "assistant" , content=f"Using following relevant info answer user query. Info : {str(medical_data)}. User Question : {user_message}")
#                 final_response = self.get_inference(is_tool=False)

#                 return {"response": final_response.choices[0].message.content}

#         return {"response": output.content}

#     def __str__(self) : 
#         return """[INFO] Initalized TeleMedic Bot [INFO]"""



# if __name__ == "__main__":
#     bot = TeleMedicBot()
#     while True:
#         user_input = input("[USER] : ")
#         resp = bot.chat(user_input)
#         print(f"[BOT] : {resp['response']}")
