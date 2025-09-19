from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, Annotated, List, Dict, Any, Literal
import json
from .llm import LLMService
from .tool import AGENT_TOOLS

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The list of messages in the conversation"]
    employee_emails: List[str]
    pending_email: Dict[str, str]  

class EmailAgentGraph:
    def __init__(self):
        self.llm_service = LLMService()
        self.graph = self.create_graph()
    
    def create_graph(self):
        workflow = StateGraph(AgentState)
        
        tool_node = ToolNode(AGENT_TOOLS)
        
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", tool_node)
        
        workflow.add_edge(START, "agent")
        
        workflow.add_conditional_edges(
            "agent",
            self.should_continue,
            {
                "tools": "tools",
                "end": END
            }
        )
        
        workflow.add_edge("tools", "agent")
        
        return workflow.compile()
    
    async def call_model(self, state: AgentState) -> AgentState:
        messages = state["messages"]
        employee_emails = state.get("employee_emails", [])
        
        response = await self.llm_service.generate_response_with_tools(messages, employee_emails)
        
        return {
            **state,
            "messages": messages + [response]
        }
    
    def should_continue(self, state: AgentState) -> Literal["tools", "end"]:
        last_message = state["messages"][-1]
        
        if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return "end"
    
    async def process_message(self, message: str, employee_emails: List[str] = None) -> Dict[str, Any]:
        if employee_emails is None:
            employee_emails = []
        
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "employee_emails": employee_emails,
            "pending_email": {}
        }
        
        result = await self.graph.ainvoke(initial_state)
        
        final_response = ""
        email_draft = ""
        send_result = None
        
        for msg in result["messages"]:
            if isinstance(msg, ToolMessage):
                try:
                    tool_result = json.loads(msg.content)
                    if "subject" in tool_result and "body" in tool_result:
                        email_draft = msg.content
                        result["pending_email"] = tool_result
                    elif "sent_count" in tool_result and "total_count" in tool_result:
                        send_result = tool_result
                except:
                    pass
        
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                final_response = msg.content
                break
        
        return {
            "response": final_response,
            "email_draft": email_draft,
            "send_result": send_result,
            "pending_email": result.get("pending_email", {})
        }