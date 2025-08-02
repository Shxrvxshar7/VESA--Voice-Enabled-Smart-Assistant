from langchain_ollama import OllamaLLM # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore
from langchain_core.output_parsers import StrOutputParser
import json
from typing import Optional  
from pydantic import BaseModel, Field  # Use native pydantic v2
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish

from langchain.tools import StructuredTool

#tools section
from tools.temp import Arduino


Ar = Arduino()

class agent:
    """Agent class to handle the agent initialization and tools"""


        
    #Tools
    class TemperatureCheckInput(BaseModel):
        room: str = Field(..., description="Name of the room to check temperature")

    class WeatherDataInput(BaseModel):
        latitude: Optional[float] = Field(None, description="Latitude coordinate (optional)")
        longitude: Optional[float] = Field(None, description="Longitude coordinate (optional)")

    def __init__(self,model="gemmaGpu"):
        self.model = self._initalize_model(model)
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()

    def _initalize_model(self,model="gemmaGpu"):
        return OllamaLLM(model=model)
    
    def _initialize_tools(self):
        """Initialize the tools for the agent"""
        @tool(args_schema=self.TemperatureCheckInput)
        def indoor_temperature_check(room:str) -> str:
            """Gets the temperature of the room in celsius
            Args:
            room: the name of the room to check the temperature
            Example: Bedroom, Kitchen, Living room etc.
            Returns:
            temperature: temperature of that room in celsius"""
            
            return str(Ar.temp())
        
        temperature_handler = StructuredTool.from_function(
        func=indoor_temperature_check,
        name="indoor_temperature_check",
        description="Gets the temperature of the room in Celsius",
        args_schema=self.TemperatureCheckInput
        )

        @tool(args_schema=self.WeatherDataInput)
        def get_current_weather(latitude: float = 13.0878, longitude: float = 80.2785) -> dict:
            """Gets the weather of the city 
            Args:
            latitude: the latitude of the city
            longitude: the longitude of the city
            Example: latitude: 13.0878, longitude: 80.2785 (chennai)
            Returns:
            weather: weather of that city in celsius"""
            result = {
            "time":"2025-04-15T00:45",
            "temperature_2m":	29.6,
            "wind_speed_10m":	4.1,
            "relative_humidity_2m":	76,
            "rain":	0.0,
            "precipitation":	0.0
            }
            return result # dummy data for now
        weather_handler = StructuredTool.from_function(
        func=get_current_weather,
        name="get_current_weather",
        description="Gets the weather of a city",
        args_schema=self.WeatherDataInput
        )
        
        return [
            temperature_handler,
            weather_handler
        ]

    def _initialize_agent(self):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
        You are a helpful home assistant named ADAM. Your job is to understand the user's voice input (transcribed text)
        and perform certain actions using available tools. Your replies should be friendly and spoken naturally.

        Use the tools *only when relevant*, and provide the correct format for inputs.

        IMPORTANT:
        - Do NOT include field descriptions, titles, or data types in the input.
        - ONLY provide direct values (e.g., "room": "Bedroom", NOT "room": {{...schema...}})
        - If you're unsure, ask the user to clarify.

        Tools available:

        1. **Indoor Temperature Check**:
        - Purpose: Get the temperature of a specific room.
        - INPUT: 
            room -> ONLY STRING (e.g., "Bedroom", "Kitchen", "Living room")
        - OUTPUT: Temperature in Celsius (e.g., "25 degrees Celsius")
        DO NOT include any other information in the input other than room name
        - Usage example:
            Input: "What is the temperature in the bedroom?"
            Tool Call:
            ```json
            { "action": "indoor_temperature_check", "action_input": { "room": "Bedroom" } }
            ```
            Response: "The temperature in the bedroom is 25 degrees Celsius, quite comfortable!"

        2. **Weather Check**:
        - Purpose: Get current outdoor weather (temperature, wind, humidity, rain).
        - Usage example:
            Input: "What's the weather like in Chennai?"
            Tool Call:
            ```json
            { "action": "get_current_weather", "action_input": { "latitude": 13.0878, "longitude": 80.2785 } }
            ```
            Response: "In Chennai, it's 29.6°C with 76% humidity and a gentle 4.1 km/h breeze. No rain expected!"

        If the user says something casual like "How are you?", just respond kindly:
        → Response: "I'm doing great, thanks for asking!"

        If the request doesn't match any tool, say:
        → Response: "I'm not able to help you with that."

        Now here’s the input:
        "{text}"

        Return a normal text with no markdowns like a converstation
        """
        )
   

        return initialize_agent(
                tools=self.tools,
                llm=self.model,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

   
       
    def get_response(self, input_text: str):
        try:
            output = self.agent.invoke({"input": input_text})
            print("raw Output:\n", output)
            # Parse the output to get the response tex
            return output['output']
        except Exception as e:
            return {"response": f"Error processing request: {str(e)}"}



# class TemperatureCheckInput(BaseModel):
#     room: str = Field(..., description="Name of the room to check temperature")

# @tool(args_schema=TemperatureCheckInput)
# def temperature_check(room:str) -> str:
#     """Gets the temperature of the room in celsius
#     Args:
#         room: the name of the room to check the temperature of
#     Example: Bedroom, Kitchen, Living room etc.
#     Returns:
#          temperature: temperature of that room in celsius"""
#     temp = temperature()
#     return str(temp.check())
#model = OllamaLLM(model="gemmaGpu")
# agent = initialize_agent(
#     tools=tools,
#     llm=model,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# input_text = "Can i go out today ?"

# # Invoke directly
# response = agent.invoke({"input": input_text})


# print("raw Output:\n", response)

# # Usage example
# if __name__ == "__main__":
#     assistant = agent(model="gemmaGpu")
#     response = assistant.get_response("Is it windy in chennai?")
#     print("Raw Output:\n", response)
