from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from tools.send_msg import MessageSender  # Add this import

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from tools.temp import Arduino

from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import AgentExecutor, create_react_agent


class vesa_agent:

    def __init__(self):
        # arduino tools
        self. ar = Arduino()
        # Memory for conversational context
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # Your LLM
        self.llm = OllamaLLM(model="mistralAgent")  # Your local Mistral7B model
        
        self.message_sender = MessageSender()

    def tool_init(self):

        # formatter_llm = OllamaLLM(model="gemma3:1b")  # or a smaller model
        # Tools
        def get_weather(location: str) -> str:
            """Gets the weather for a location"""
            temp = self.ar.temp()
            return f"The weather in {location} is sunny and {str(temp)}, reply with the celsius and weather in a friendly tone and short"

        def light_on(room: str) -> str:
            """Turns on the light"""
            self.ar.light_on()
            return f"The light has been turned on room {room}."

        def light_off(room: str) -> str:
            """Turns on the light"""
            self.ar.light_off()
            return f"The light has been turned off room {room}."

        def door_open(room: str) -> str:
            """Opens the door"""
            self.ar.servo_on()
            return f"{room} door has been opened."

        def door_close(room:str)->str:
            """Closes the door"""
            self.ar.servo_off()
            return f"{room} door has been closed"

        def fan_on(room: str) -> str:
            """Turns on the fan"""
            self.ar.relay1_on()
            return f"{room}fan has been turned ON"

        def fan_off(room: str) -> str:
            """Turns off the fan"""
            self.ar.relay1_off()
            return f"{room} fan has been turned OFF"

        def get_weather_outside(_:str) ->str:
            """gets weather if no location is given"""
            temp = self.ar.temp()
            return f"The weather outside is sunny and {str(temp)}"

        def get_location(_:str) ->str:

            return "The location is 'chennai'"

        def send_whatsapp(input_str: str) -> str:
            """Sends a WhatsApp message to a contact"""
            try:
                # Parse input: "name:message"
                name, message = input_str.split(':', 1)
                name = name.strip()
                message = message.strip()
                
                return self.message_sender.send_whatsapp(name, message)
            except ValueError:
                return "Please provide input in the format: contact_name:message"
            except Exception as e:
                return f"Error sending WhatsApp message: {str(e)}"

        tools = [
            Tool(
                name="getweather",  # Remove underscore
                func=get_weather,
                description="Use this to get the weather for a location. If no location is specified, uses 'chennai'."
            ),
            Tool(
                name="getlocation",  # Remove underscore
                func=get_location,
                description="Use this to get the current location"
            ),
            Tool(
                name="lighton",  # Make consistent naming
                func=light_on,
                description="Use this to turn on the light in a room"
            ),
            Tool(
                name = "lightoff",
                func=light_off,
                description="Use this to turn off the light in a room"

                ),

            Tool(
                name = "dooropen",
                func=door_open,
                description="Use this to open the door in a room"
                ),

            Tool(
                name = "doorclose",
                func=door_close,
                description="Use this to close the door in a room"
                ),
            
            Tool(
                name = "fanon",
                func=fan_on,
                description="Use this to turn on the fan in a room"
                ),

            Tool(
                name = "fanoff",
                func=fan_off,
                description="Use this to turn off the fan in a room"
                ),
            Tool(
                name="sendwhatsapp",
                func=send_whatsapp,
                description="Use this to send a WhatsApp message to a saved contact. Input format: contact_name:message (e.g., mom:Hello there!). Available contacts: mom, dad, sister"
            )
 
        ]

        # Initialize agent with NO custom prompt
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            system_message=(
                "You are ADAM, a friendly and helpful smart home assistant. "
                "When asked about weather with no location specified, use 'chennai' as the default location. "
                "Use the available tools to help users. Always respond in a natural, conversational tone."
            )
        )

    def get_response(self, input_text: str):
        output = self.agent.invoke({"input": input_text})
        return output['output']



 # or a smaller model

# system_prompt = (
#     "You are ADAM, a friendly and helpful smart home assistant. "
#     "Always respond in a natural spoken tone. If the user asks about the weather "
#     "and doesn't specify a location, assume it's 'chennai'. Use the tools provided to take actions."
# )

# Use LangChain's ReAct prompt builder to handle required variables
# prompt = ReActAgentPrompt.from_llm_and_tools(
#     llm=llm,
#     tools=tools,
#     system_message=system_prompt,
# )

# # Create the ReAct agent
# react_agent = create_react_agent(
#     llm=llm,
#     tools=tools,
#     prompt=prompt,
# # Now build the executor
# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=react_agent,or
#     tools=tools, AgentExecutor.from_agent_and_tools(
#     memory=memory,ent,
#     verbose=True,
#     handle_parsing_errors=True,
# )   verbose=True,
#     handle_parsing_errors=True,
# )
# formatter_prompt = PromptTemplate.from_template(
#     "you are a assitant parser, a query is given to a gent and it returned a answer, Please rephrase the following assistant reply in a friendly and concise tone:\n\n{raw_response}, No markdown JUST give the response"
# )ormatter_prompt = PromptTemplate.from_template(
# formatter_chain = LLMChain(llm=formatter_llm, prompt=formatter_prompt)rned a answer, Please rephrase the following assistant reply in a friendly and concise tone:\n\n{raw_response}, No markdown JUST give the response"
# )
# formatter_chain = LLMChain(llm=formatter_llm, prompt=formatter_prompt)

# input_prompt = ""
# # Use invoke, not run
# while True:t = ""
#     input_txt =  input("Enter you prompt: ")
#     input_prompt = f"You are a helpful home assistant named ADAM,Your job is to understand the user's voice input (transcribed text) and  perform certain actions using available tools.Your replies should be friendly and spoken naturally.,default location is 'chennai' if no location is given heres the transcribed text:{input_txt}"
      #input_txt =  input("Enter you prompt: ")
#     input_prompt = f"You are a helpful home assistant named ADAM,Your job is to understand the user's voice input (transcribed text) and  perform certain actions using available tools.Your replies should be friendly and spoken naturally.,default location is 'chennai' if no location is given heres the transcribed text:{input_txt}"
    
#     response = agent.invoke({"input": input_txt})
# # final_response = formatter_chain.run(raw_response=response)
#     response = agent.invoke({"input": input_txt})
# # print("Formatted Output:", final_response)esponse=response)
#     print(response['output'])  # or print(response) to inspect full dict
# # print("Formatted Output:", final_response)
#     print(response['output'])  # or print(response) to inspect full dict
