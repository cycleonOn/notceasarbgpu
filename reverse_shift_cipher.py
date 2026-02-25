"""
Шифр обратного сдвига (Reverse Caesar Cipher)
===============================================
Каждая буква заменяется буквой с позицией (N - index - 1) в алфавите.
То есть алфавит «отражается»: А↔Я, Б↔Э, В↔Ю, Г↔Ь, ...

Это симметричный шифр: шифрование и дешифрование — одна и та же операция.

Русский алфавит (32 буквы, Ё=Е):
А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕
Я Ю Э Ь Ы Ъ Щ Ш Ч Ц Х Ф У Т С Р П О Н М Л К Й И З Ж Е Д Г В Б А
"""

RUS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # 32 буквы (Ё=Е)
N = len(RUS)


def transform(text: str) -> str:
    """
    Шифрует / дешифрует текст (операция симметрична).
    А↔Я, Б↔Э, В↔Ю и т.д.

    Args:
        text: исходный или зашифрованный текст

    Returns:
        Преобразованный текст.
    """
    text = text.upper().replace('Ё', 'Е')
    result = []
    for ch in text:
        if ch in RUS:
            idx = RUS.index(ch)
            result.append(RUS[N - 1 - idx])
        else:
            result.append(ch)
    return ''.join(result)


# Псевдонимы для удобства
encrypt = transform
decrypt = transform


def show_table() -> None:
    """Показывает таблицу замен."""
    print('\nТаблица замен (обратный сдвиг):')
    print('Исходный:    ' + ' '.join(RUS))
    print('Шифрованный: ' + ' '.join(RUS[N - 1 - i] for i in range(N)))
    print()


def _run_tests() -> None:
    tests = [
        'ПРИВЕТ',
        'МОСКВА',
        'ТАЙНА',
        'ШИФР ОБРАТНОГО СДВИГА',
        'АЯ',
        'АБВГДЕЖ',
    ]
    print('\n--- Тесты ---')
    all_ok = True
    for plain in tests:
        enc = encrypt(plain)
        dec = decrypt(enc)
        plain_norm = plain.upper().replace('Ё', 'Е')
        ok = dec == plain_norm
        status = '✓' if ok else '✗'
        if not ok:
            all_ok = False
        print(f'{status}  "{plain}" → "{enc}" → "{dec}"')
    print('\nВсе тесты прошли успешно!' if all_ok else '\nЕсть ошибки!')


def main() -> None:
    print('=' * 50)
    print('       ШИФР ОБРАТНОГО СДВИГА')
    print('=' * 50)
    show_table()
    print('Особенности:')
    print('  • Алфавит отражается: А↔Я, Б↔Э, В↔Ю ...')
    print('  • Симметричный: шифрование = дешифрование')
    print('  • Ё обрабатывается как Е')
    print('  • Пробелы и пунктуация не меняются')
    print()

    while True:
        print('Выберите действие:')
        print('  1 — Зашифровать')
        print('  2 — Дешифровать')
        print('  3 — Выйти')
        choice = input('Ваш выбор: ').strip()

        if choice == '1':
            text = input('Введите текст для шифрования: ')
            print(f'\nЗашифрованный текст: {encrypt(text)}\n')

        elif choice == '2':
            text = input('Введите шифротекст: ')
            print(f'\nРасшифрованный текст: {decrypt(text)}\n')

        elif choice == '3':
            print('До свидания!')
            break
        else:
            print('Неверный выбор. Попробуйте снова.\n')


if __name__ == '__main__':
    import sys
    if '--test' in sys.argv:
        _run_tests()
    else:
        main()
