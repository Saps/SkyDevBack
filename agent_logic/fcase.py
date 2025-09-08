
print('Hello world')

from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_core.messages import HumanMessage

from langgraph.types import Command
from loguru import logger
from src.agent.graph import hr_graph

from IPython.display import Image, display
import uuid

from dotenv import find_dotenv, dotenv_values

config = dotenv_values(find_dotenv(".env"))

mermaid_src = hr_graph.get_graph(xray=1).draw_mermaid()
with open("hr_graph.mmd", "w", encoding="utf-8") as f:
    f.write(mermaid_src)
print(mermaid_src)

mermaid_src = hr_graph.get_graph(xray=1).draw_mermaid_png(draw_method=MermaidDrawMethod.API)

from uuid import uuid4
from langgraph.types import Command

cfg = {"configurable": {"thread_id": f"hr-{uuid4()}"}}

state = {
    "messages": [],
    "user_input": "",
    "intent": None,
    "meta": {},
}

for _ in hr_graph.stream(state, config=cfg, stream_mode="updates"):
    pass

# интерактив
while True:
    text = input("\nТы: ").strip()
    if text.lower() in {"q", "quit", "exit"}:
        break
    for _ in hr_graph.stream(Command(resume=text), config=cfg, stream_mode="updates"):
        pass