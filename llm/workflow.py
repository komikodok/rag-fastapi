from langgraph.graph import StateGraph, START, END
from .state import State
from .node import (
    retrieve_node,
    generation_node
)

workflow = StateGraph(State)

workflow.add_node("retrieve_node", retrieve_node)
workflow.add_node("generation_node", generation_node)

workflow.add_edge(START, "retrieve_node")
workflow.add_edge("retrieve_node", "generation_node")
workflow.add_edge("generation_node", END)

app = workflow.compile()