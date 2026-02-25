import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import requests
import json
import threading

# ────────────────────────────────────────────────
#               НАСТРОЙКИ
# ────────────────────────────────────────────────

API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"

# Рекомендуемые модели (можно дополнять / менять)
RECOMMENDED_MODELS = [
    "minimax/minimax-m2.5",
    "x-ai/grok-4.1-fast",
    "qwen/qwen3-coder-next",
    "deepseek/deepseek-v3.2",
    "z-ai/glm-4.5-air",               # бесплатная
    "xiaomi/mimo-v2-flash",             # бесплатная, очень сильная в кодинге
    "arcee-ai/trinity-large-preview",   # бесплатная
    "stepfun/step-3.5-flash",           # бесплатная
    "x-ai/grok-code-fast-1",
]

# ────────────────────────────────────────────────
#               ФУНКЦИИ API
# ────────────────────────────────────────────────

def get_available_models():
    """Загружаем список всех доступных моделей"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        r = requests.get(f"{BASE_URL}/models", headers=headers, timeout=12)
        r.raise_for_status()
        data = r.json()
        models = [m["id"] for m in data.get("data", [])]
        return sorted(models)
    except Exception as e:
        print(f"Не удалось загрузить список моделей: {e}")
        return []


def send_to_openrouter(messages, model):
    """Отправка запроса к выбранной модели"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",           # можно поменять
        "X-Title": "Tkinter OpenRouter Chat",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False,
    }

    try:
        r = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=90
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {str(e)}"


# ────────────────────────────────────────────────
#               GUI
# ────────────────────────────────────────────────

class OpenRouterChat:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenRouter • Мульти-модельный чат")
        self.root.geometry("780x680")
        self.root.minsize(600, 500)

        self.messages = []           # история диалога
        self.current_model = None

        # ─── Верхняя панель ───
        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", padx=10, pady=8)

        tk.Label(top_frame, text="Модель:", font=("Segoe UI", 10)).pack(side="left")

        self.model_var = tk.StringVar(value="выберите модель")

        self.model_combo = ttk.Combobox(
            top_frame,
            textvariable=self.model_var,
            state="readonly",
            width=55,
            font=("Consolas", 10)
        )
        self.model_combo.pack(side="left", padx=8)
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        self.btn_reload = tk.Button(top_frame, text="↻ Обновить список", command=self.load_models)
        self.btn_reload.pack(side="left")

        # ─── Чат ───
        self.chat_text = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state="disabled",
            font=("Consolas", 11),
            bg="#f8f9fa"
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.chat_text.tag_config("user", foreground="#0066cc", justify="right", rmargin=10)
        self.chat_text.tag_config("bot", foreground="#006400", lmargin1=20, lmargin2=20)
        self.chat_text.tag_config("error", foreground="red")

        # ─── Поле ввода + кнопка ───
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=10, pady=8)

        self.entry = tk.Entry(input_frame, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", self.send_message)

        self.btn_send = tk.Button(input_frame, text="Отправить", width=12, command=self.send_message)
        self.btn_send.pack(side="right")

        # Статус
        self.status_var = tk.StringVar(value="Готов")
        tk.Label(root, textvariable=self.status_var, fg="gray", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(0,4))

        # Загружаем модели при старте
        self.load_models()

    def load_models(self):
        self.status_var.set("Загрузка моделей...")
        self.root.update()

        all_models = get_available_models()

        # Добавляем рекомендованные в начало, если они есть
        display_list = []
        seen = set()

        for m in RECOMMENDED_MODELS:
            if m in all_models and m not in seen:
                display_list.append(m)
                seen.add(m)

        # Остальные модели
        for m in sorted(all_models):
            if m not in seen:
                display_list.append(m)

        self.model_combo["values"] = display_list

        if display_list:
            self.model_combo.current(0)
            self.current_model = display_list[0]
            self.status_var.set(f"Выбрана: {self.current_model}")
        else:
            self.status_var.set("Не удалось загрузить модели")

    def on_model_change(self, event=None):
        self.current_model = self.model_var.get()
        self.status_var.set(f"Выбрана: {self.current_model}")

    def add_message(self, role, text):
        self.chat_text.configure(state="normal")

        if role == "user":
            self.chat_text.insert("end", "You:\n" + text + "\n\n", "user")
        elif role == "bot":
            self.chat_text.insert("end", f"{self.current_model}:\n" + text + "\n\n", "bot")
        elif role == "error":
            self.chat_text.insert("end", text + "\n\n", "error")

        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text or not self.current_model:
            return

        self.add_message("user", text)
        self.messages.append({"role": "user", "content": text})
        self.entry.delete(0, "end")

        self.status_var.set("Думаю...")
        self.btn_send["state"] = "disabled"
        self.root.update()

        # Запускаем в отдельном потоке, чтобы интерфейс не зависал
        threading.Thread(target=self.get_response, daemon=True).start()

    def get_response(self):
        try:
            response = send_to_openrouter(self.messages, self.current_model)

            self.root.after(0, lambda: self.add_message("bot", response))
            self.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            err_msg = f"Ошибка при обращении к API:\n{str(e)}"
            self.root.after(0, lambda: self.add_message("error", err_msg))

        finally:
            self.root.after(0, lambda: [
                self.status_var.set(f"Готов • {self.current_model}"),
                self.btn_send.configure(state="normal")
            ])


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenRouterChat(root)
    root.mainloop()
