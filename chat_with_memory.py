from agent import run_agent
from datetime import datetime

LOG_FILE = "chat_memory.log"

def log(role, content):
    ts = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {role.upper()}: {content}\n")

history = [
    {
        "role": "system",
        "content": "Você é um assistente que conversa de forma clara e lembra do contexto."
    }
]

log("system", history[0]["content"])

print("💬 Chat iniciado. Digite 'sair' para encerrar.\n")

while True:
    user_input = input("Você: ").strip()
    if user_input.lower() == "sair":
        log("system", "Sessão encerrada.")
        break

    history.append({"role": "user", "content": user_input})
    log("user", user_input)

    answer = run_agent(history).strip()
    history.append({"role": "assistant", "content": answer})
    log("assistant", answer)

    print(f"Agente: {answer}\n")
