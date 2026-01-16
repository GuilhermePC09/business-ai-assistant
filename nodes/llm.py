from langchain_ollama import ChatOllama as LangchainChatOllama
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from nodes.tools import calculator_tool, kpi_tool, currency_converter_tool, generate_report_tool

SYSTEM_PROMPT = """You are a helpful business assistant with access to tools. 

When a user asks you to:
- Calculate something mathematical → use the calculator_tool
- Convert currencies → use the currency_converter_tool  
- Calculate business KPIs (ROI, margin, CAGR, etc.) → use the kpi_tool
- Generate a business report → use the generate_report_tool

IMPORTANT: You MUST use the available tools to answer questions. Do NOT try to calculate, convert, or search manually. Always invoke the appropriate tool and use its result to answer the user."""

class ChatOllama:
    def __init__(self, model: str = "llama3.1:8b", temperature: float = 0):
        self.agents = {}
        self.histories = {}
        self.tools = [
            calculator_tool,
            kpi_tool,
            currency_converter_tool,
            generate_report_tool,
        ]

        self.base_llm = LangchainChatOllama(
            model=model, 
            temperature=temperature,
        )

    def get_agent(self, chat_id: str):
        if chat_id not in self.agents:
            agent = create_agent(
                model=self.base_llm,
                tools=self.tools,
                system_prompt=SYSTEM_PROMPT,
            )

            self.agents[chat_id] = agent
            self.histories[chat_id] = []

        return self.agents[chat_id]

    def generate_response(self, query: str, chat_id: str) -> str:
        agent = self.get_agent(chat_id)

        self.histories[chat_id].append(HumanMessage(content=query))
        result = agent.invoke({"messages": self.histories[chat_id]})

        messages = result["messages"]
        self.histories[chat_id] = messages

        return messages[-1].content
