import tkinter as tk

RUS_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def caesar_cipher(text, shift, direction):
    result = ''
    for char in text:
        if char in RUS_ALPHABET or char == ' ':
            if char == ' ':
                result += ' '
            else:
                index = RUS_ALPHABET.index(char)
                if direction == 'encrypt':
                    new_index = (index + shift) % len(RUS_ALPHABET)
                else:
                    new_index = (index - shift) % len(RUS_ALPHABET)
                result += RUS_ALPHABET[new_index]
        else:
            result += char
    return result

def encrypt(text, shift):
    return caesar_cipher(text, shift, 'encrypt')

def decrypt(text, shift):
    return caesar_cipher(text, shift, 'decrypt')

def validate_shift(new_value):
    try:
        val = int(new_value)
        if 0 <= val <= 31:
            return True
        else:
            return False
    except ValueError:
        return False

def main():
    root = tk.Tk()
    root.title('Шифр Цезаря')

    FONT_SIZE_LABEL = 16
    FONT_SIZE_ENTRY = 18
    FONT_SIZE_BUTTON = 16

    vcmd = (root.register(validate_shift), '%P')

    encrypt_frame = tk.Frame(root, padx=20, pady=20)
    encrypt_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(encrypt_frame, text='Текст:', font=('Times New Roman', FONT_SIZE_LABEL)).grid(row=0, column=0, sticky=tk.W, pady=10)
    text_var = tk.StringVar()
    text_entry = tk.Entry(encrypt_frame, textvariable=text_var, width=60, font=('Times New Roman', FONT_SIZE_ENTRY))
    text_entry.grid(row=0, column=1, pady=10, sticky=tk.EW)

    tk.Label(encrypt_frame, text='Сдвиг (0-31):', font=('Times New Roman', FONT_SIZE_LABEL)).grid(row=1, column=0, sticky=tk.W, pady=10)
    shift_var = tk.StringVar()
    shift_entry = tk.Entry(encrypt_frame, textvariable=shift_var, width=5, validate='key', validatecommand=vcmd, font=('Times New Roman', FONT_SIZE_ENTRY))
    shift_entry.grid(row=1, column=1, sticky=tk.W, pady=10)

    def encrypt_command():
        try:
            shift_value = int(shift_var.get())
        except ValueError:
            shift_value = 0
        print(encrypt(text_var.get(), shift_value))
    tk.Button(encrypt_frame, text='Шифровать', command=encrypt_command, font=('Times New Roman', FONT_SIZE_BUTTON)).grid(row=2, column=0, columnspan=2, pady=15)

    decrypt_frame = tk.Frame(root, padx=20, pady=20)
    decrypt_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(decrypt_frame, text='Зашифрованный текст:', font=('Times New Roman', FONT_SIZE_LABEL)).grid(row=0, column=0, sticky=tk.W, pady=10)
    encrypted_text_var = tk.StringVar()
    encrypted_text_entry = tk.Entry(decrypt_frame, textvariable=encrypted_text_var, width=60, font=('Times New Roman', FONT_SIZE_ENTRY))
    encrypted_text_entry.grid(row=0, column=1, pady=10, sticky=tk.EW)

    def paste_from_clipboard():
        try:
            clip_text = root.clipboard_get()
            encrypted_text_var.set(clip_text)
        except tk.TclError:
            pass
    tk.Button(decrypt_frame, text='Вставить', command=paste_from_clipboard, font=('Times New Roman', FONT_SIZE_BUTTON)).grid(row=0, column=2, padx=10)

    tk.Label(decrypt_frame, text='Сдвиг (0-31):', font=('Times New Roman', FONT_SIZE_LABEL)).grid(row=1, column=0, sticky=tk.W, pady=10)
    decrypt_shift_var = tk.StringVar()
    decrypt_shift_entry = tk.Entry(decrypt_frame, textvariable=decrypt_shift_var, width=5, validate='key', validatecommand=vcmd, font=('Times New Roman', FONT_SIZE_ENTRY))
    decrypt_shift_entry.grid(row=1, column=1, sticky=tk.W, pady=10)

    def decrypt_command():
        try:
            shift_value = int(decrypt_shift_var.get())
        except ValueError:
            shift_value = 0
        print(decrypt(encrypted_text_var.get(), shift_value))
    tk.Button(decrypt_frame, text='Расшифровать', command=decrypt_command, font=('Times New Roman', FONT_SIZE_BUTTON)).grid(row=2, column=0, columnspan=3, pady=15)

    for i in range(3):
        decrypt_frame.columnconfigure(i, weight=1)
    for i in range(3):
        encrypt_frame.columnconfigure(i, weight=1)

    root.mainloop()

if __name__ == '__main__':
    main()