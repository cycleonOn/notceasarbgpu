"""
Шифровальщик — tkinter приложение
===================================
Поддерживаемые шифры:
  • Шифр Полибия  (квадрат 6×6, русский алфавит)
  • Шифр Цезаря   (произвольный сдвиг)
  • Шифр Августа  (сдвиг +1, Я → АА, без цикличности)

Запуск: python cipher_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ══════════════════════════════════════════════════════════
#  АЛФАВИТ
# ══════════════════════════════════════════════════════════

RUS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'   # 32 буквы (Ё=Е)
N   = len(RUS)


def normalize(text: str) -> str:
    return text.upper().replace('Ё', 'Е')


# ══════════════════════════════════════════════════════════
#  ШИФР ЦЕЗАРЯ
# ══════════════════════════════════════════════════════════

def caesar_encrypt(text: str, shift: int) -> str:
    shift = shift % N
    result = []
    for ch in normalize(text):
        if ch in RUS:
            result.append(RUS[(RUS.index(ch) + shift) % N])
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


# ══════════════════════════════════════════════════════════
#  ШИФР АВГУСТА (сдвиг +1, Я → АА)
# ══════════════════════════════════════════════════════════

def augustus_encrypt(text: str) -> str:
    result = []
    for ch in normalize(text):
        if ch in RUS:
            idx = RUS.index(ch)
            result.append('АА' if idx == N - 1 else RUS[idx + 1])
        else:
            result.append(ch)
    return ''.join(result)


def augustus_decrypt(text: str) -> str:
    text = normalize(text)
    result = []
    i = 0
    while i < len(text):
        if text[i] == 'А' and i + 1 < len(text) and text[i + 1] == 'А':
            result.append('Я')
            i += 2
        elif text[i] in RUS:
            idx = RUS.index(text[i])
            result.append(RUS[idx - 1] if idx > 0 else text[i])
            i += 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


# ══════════════════════════════════════════════════════════
#  ШИФР ПОЛИБИЯ (6×6, русский алфавит)
# ══════════════════════════════════════════════════════════

_POL_SQUARE = [
    ['А','Б','В','Г','Д','Е'],
    ['Ж','З','И','Й','К','Л'],
    ['М','Н','О','П','Р','С'],
    ['Т','У','Ф','Х','Ц','Ч'],
    ['Ш','Щ','Ъ','Ы','Ь','Э'],
    ['Ю','Я','', '', '', ''],
]

_CH2CO: dict[str, tuple[int,int]] = {}
for _r, _row in enumerate(_POL_SQUARE, 1):
    for _c, _ch in enumerate(_row, 1):
        if _ch:
            _CH2CO[_ch] = (_r, _c)
_CH2CO['Ё'] = _CH2CO['Е']
_CO2CH = {v: k for k, v in _CH2CO.items() if k != 'Ё'}


def polybius_encrypt(text: str, sep: str = ' ') -> str:
    codes = []
    for ch in normalize(text):
        if ch in _CH2CO:
            r, c = _CH2CO[ch]
            codes.append(f'{r}{c}')
        elif ch == ' ':
            codes.append('00')
    return sep.join(codes)


def polybius_decrypt(ciphertext: str, sep: str = ' ') -> str:
    result = []
    for token in ciphertext.split(sep):
        token = token.strip()
        if not token:
            continue
        if token == '00':
            result.append(' ')
            continue
        if len(token) != 2 or not token.isdigit():
            raise ValueError(f'Неверный токен: "{token}"')
        key = (int(token[0]), int(token[1]))
        if key not in _CO2CH:
            raise ValueError(f'Координаты {key} вне квадрата.')
        result.append(_CO2CH[key])
    return ''.join(result)


# ══════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════

CIPHERS = ['Шифр Цезаря', 'Шифр Августа', 'Шифр Полибия']

CIPHER_INFO = {
    'Шифр Цезаря':  'Сдвиг каждой буквы на N позиций. Укажите сдвиг (1–31).',
    'Шифр Августа': 'Сдвиг +1, Я→АА, без перехода в начало алфавита.',
    'Шифр Полибия': 'Каждая буква заменяется парой координат (строка/столбец).\nПробел → 00.',
}


class CipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Шифровальщик')
        self.resizable(False, False)
        self.configure(bg='#1e1e2e')
        self._build_ui()

    # ── Построение интерфейса ──────────────────────────────

    def _build_ui(self):
        PAD = dict(padx=16, pady=10)

        # ── Заголовок ──
        header = tk.Frame(self, bg='#313244', pady=10)
        header.pack(fill='x')
        tk.Label(header, text='🔐 Шифровальщик', font=('Segoe UI', 18, 'bold'),
                 bg='#313244', fg='#cdd6f4').pack()

        # ── Выбор шифра ──
        top = tk.Frame(self, bg='#1e1e2e')
        top.pack(fill='x', **PAD)

        tk.Label(top, text='Шифр:', bg='#1e1e2e', fg='#a6adc8',
                 font=('Segoe UI', 10)).pack(side='left', padx=(0, 8))

        self.cipher_var = tk.StringVar(value=CIPHERS[0])
        cipher_menu = ttk.Combobox(top, textvariable=self.cipher_var,
                                   values=CIPHERS, state='readonly', width=22,
                                   font=('Segoe UI', 10))
        cipher_menu.pack(side='left')
        cipher_menu.bind('<<ComboboxSelected>>', self._on_cipher_change)

        # ── Сдвиг (только для Цезаря) ──
        self.shift_frame = tk.Frame(top, bg='#1e1e2e')
        self.shift_frame.pack(side='left', padx=(16, 0))

        tk.Label(self.shift_frame, text='Сдвиг:', bg='#1e1e2e', fg='#a6adc8',
                 font=('Segoe UI', 10)).pack(side='left', padx=(0, 6))

        self.shift_var = tk.IntVar(value=3)
        shift_spin = tk.Spinbox(self.shift_frame, from_=1, to=31,
                                textvariable=self.shift_var, width=5,
                                font=('Segoe UI', 10),
                                bg='#313244', fg='#cdd6f4',
                                buttonbackground='#45475a',
                                relief='flat', bd=4)
        shift_spin.pack(side='left')

        # ── Подсказка ──
        self.info_var = tk.StringVar(value=CIPHER_INFO[CIPHERS[0]])
        info_lbl = tk.Label(self, textvariable=self.info_var, bg='#1e1e2e',
                            fg='#6c7086', font=('Segoe UI', 9),
                            justify='left', anchor='w')
        info_lbl.pack(fill='x', padx=16)

        sep = ttk.Separator(self, orient='horizontal')
        sep.pack(fill='x', padx=16, pady=6)

        # ── Вкладки ──
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TNotebook',        background='#1e1e2e', borderwidth=0)
        style.configure('TNotebook.Tab',    background='#313244', foreground='#a6adc8',
                        padding=[14, 6],    font=('Segoe UI', 10))
        style.map('TNotebook.Tab',
                  background=[('selected', '#89b4fa')],
                  foreground=[('selected', '#1e1e2e')])

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        self.enc_tab = self._make_tab(nb, 'encrypt')
        self.dec_tab = self._make_tab(nb, 'decrypt')

        nb.add(self.enc_tab, text='  🔒 Шифратор  ')
        nb.add(self.dec_tab, text='  🔓 Дешифратор  ')

    def _make_tab(self, parent, mode: str) -> tk.Frame:
        """Создаёт вкладку шифратора или дешифратора."""
        frame = tk.Frame(parent, bg='#1e1e2e')

        lbl_in  = '📝 Текст для шифрования:' if mode == 'encrypt' else '🔢 Шифротекст:'
        lbl_out = '🔒 Зашифрованный текст:'  if mode == 'encrypt' else '📝 Расшифрованный текст:'
        btn_txt = '  Зашифровать  '           if mode == 'encrypt' else '  Дешифровать  '

        tk.Label(frame, text=lbl_in, bg='#1e1e2e', fg='#cdd6f4',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(12, 4))

        inp = tk.Text(frame, height=5, width=56,
                      bg='#313244', fg='#cdd6f4', insertbackground='#cdd6f4',
                      font=('Segoe UI', 11), relief='flat', bd=6,
                      wrap='word', undo=True)
        inp.pack(fill='x')

        btn = tk.Button(frame, text=btn_txt,
                        font=('Segoe UI', 10, 'bold'),
                        bg='#89b4fa', fg='#1e1e2e',
                        activebackground='#74c7ec', activeforeground='#1e1e2e',
                        relief='flat', cursor='hand2', pady=6,
                        command=lambda: self._process(mode, inp, out))
        btn.pack(pady=10)

        tk.Label(frame, text=lbl_out, bg='#1e1e2e', fg='#cdd6f4',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 4))

        out = tk.Text(frame, height=5, width=56,
                      bg='#181825', fg='#a6e3a1', insertbackground='#cdd6f4',
                      font=('Segoe UI', 11), relief='flat', bd=6,
                      wrap='word', state='disabled')
        out.pack(fill='x')

        # Кнопка «Скопировать»
        copy_btn = tk.Button(frame, text='📋 Скопировать результат',
                             font=('Segoe UI', 9),
                             bg='#45475a', fg='#cdd6f4',
                             activebackground='#585b70', activeforeground='#cdd6f4',
                             relief='flat', cursor='hand2', pady=4,
                             command=lambda: self._copy(out))
        copy_btn.pack(pady=(6, 12))

        return frame

    # ── Логика ────────────────────────────────────────────

    def _on_cipher_change(self, _event=None):
        cipher = self.cipher_var.get()
        self.info_var.set(CIPHER_INFO[cipher])
        # показываем/скрываем поле сдвига
        if cipher == 'Шифр Цезаря':
            self.shift_frame.pack(side='left', padx=(16, 0))
        else:
            self.shift_frame.pack_forget()

    def _process(self, mode: str, inp: tk.Text, out: tk.Text):
        text   = inp.get('1.0', 'end').strip()
        cipher = self.cipher_var.get()

        if not text:
            messagebox.showwarning('Пусто', 'Введите текст!')
            return

        try:
            if cipher == 'Шифр Цезаря':
                shift = self.shift_var.get()
                result = caesar_encrypt(text, shift) if mode == 'encrypt' else caesar_decrypt(text, shift)

            elif cipher == 'Шифр Августа':
                result = augustus_encrypt(text) if mode == 'encrypt' else augustus_decrypt(text)

            elif cipher == 'Шифр Полибия':
                result = polybius_encrypt(text) if mode == 'encrypt' else polybius_decrypt(text)

            else:
                result = ''

        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
            return

        out.configure(state='normal')
        out.delete('1.0', 'end')
        out.insert('1.0', result)
        out.configure(state='disabled')

    def _copy(self, out: tk.Text):
        text = out.get('1.0', 'end').strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo('Скопировано', 'Текст скопирован в буфер обмена!')
        else:
            messagebox.showwarning('Пусто', 'Нечего копировать.')


# ══════════════════════════════════════════════════════════
#  ЗАПУСК
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    app = CipherApp()
    app.mainloop()
