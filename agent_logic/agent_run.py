from pathlib import Path
from uuid import uuid4
from dotenv import find_dotenv, dotenv_values

def load_env(env_file: str = ".env") -> dict:
    from dotenv import find_dotenv, dotenv_values
    return dotenv_values(find_dotenv(env_file))

def resolve_path(base_dir: Path, p: str | Path) -> Path:
    p = Path(p)
    return p if p.is_absolute() else (base_dir / p)

def init_state(resume_dir: Path, vacancy: str, vacancy_txt: Path, mp3_path:Path) -> dict:
    return {
        "messages": [],
        "user_input": "",
        "intent": None,
        "meta": {},
        "resume_path": str(resume_dir),
        "vacancy_path": str(vacancy_txt),
        "interview_result" : {},
        "mp3_path" : str(mp3_path),
        "vacancy" : vacancy

    }

def extract_last_ai_text(state: dict) -> str:
    msgs = state.get("messages", []) if isinstance(state, dict) else []
    for m in reversed(msgs):
        m_type = getattr(m, "type", None) or m.__class__.__name__.lower()
        if "ai" in m_type:
            content = getattr(m, "content", "")
            return content if isinstance(content, str) else str(content)
    return ""


def run_interactive(in_params: dict) -> None:
    from langgraph.types import Command
    from src.agent.graph import hr_graph

    script_dir = Path(__file__).resolve().parent
    _ = load_env(in_params.get("env_file", ".env"))

    # обязательные поля
    try:
        resume_dir = resolve_path(script_dir, in_params["resume_dir"])
        vacancy_txt = resolve_path(script_dir, in_params["vacancy_path"])
        mp3_path   = resolve_path(script_dir, in_params["mp3_path"])
        vacancy    = in_params["vacancy"]
    except KeyError as e:
        print(f"[ERR] missing param: {e}")
        return

    # валидация путей
    if not resume_dir.exists() or not resume_dir.is_dir():
        print(f"[ERR] resume_dir not found or not a directory: {resume_dir}"); return
    if not vacancy_txt.exists() or not vacancy_txt.is_file():
        print(f"[ERR] vacancy_path not found or not a file: {vacancy_txt}"); return
    if not mp3_path.exists() or not mp3_path.is_file():
        print(f"[ERR] mp3_path not found or not a file: {mp3_path}"); return
    if not isinstance(vacancy, str) or not vacancy.strip():
        print(f"[ERR] vacancy must be non-empty string"); return

    thread_id = in_params.get("thread_id", f"hr-{uuid4()}")
    cfg = {"configurable": {"thread_id": thread_id}, "recursion_limit": 200}
    
    state = init_state(resume_dir, vacancy.strip(), vacancy_txt, mp3_path)

    try:
        st = hr_graph.invoke(state, config=cfg)
        print("Агент:", extract_last_ai_text(st))
    except Exception as e:
        print(f"[ERR] init error: {e}")
        return

    print("\nВведите сообщение (q/quit/exit — выход):")
    while True:
        try:
            text = input("Ты: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[exit]"); break

        if text.lower() in {"q", "quit", "exit"}:
            print("[exit]"); break

        try:
            st = hr_graph.invoke(Command(resume=text), config=cfg)
            print("Агент:", extract_last_ai_text(st))
        except Exception as e:
            print(f"[ERR] step error: {e}")


## как вызывать

# run_interactive({
#     "resume_dir":  r"data\input\biznes-analitik\biznes-analitik",
#     "vacancy":     "бизнес-аналитик",
#     "mp3_path":    r"data\input\audio\candidate_answer_01.mp3",
#     "vacancy_path":r"data\input\бизнес-аналитик.txt",
# })