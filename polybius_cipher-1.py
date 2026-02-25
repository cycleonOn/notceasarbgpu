"""
Шифр Полибия — русский алфавит
================================
Используется квадрат 6x6 для 33 букв русского алфавита.
Ё объединяется с Е (аналогично I/J в латинице).
Итого 32 уникальные буквы → 6x6 = 36 ячеек (4 ячейки свободны, не используются).

Таблица 6x6:
      1    2    3    4    5    6
  1   А    Б    В    Г    Д    Е/Ё
  2   Ж    З    И    Й    К    Л
  3   М    Н    О    П    Р    С
  4   Т    У    Ф    Х    Ц    Ч
  5   Ш    Щ    Ъ    Ы    Ь    Э
  6   Ю    Я    —    —    —    —
"""

# ─────────────────────────────────────────────
#  Квадрат Полибия (русский алфавит, 6x6)
# ─────────────────────────────────────────────

SQUARE = [
    ['А', 'Б', 'В', 'Г', 'Д', 'Е'],
    ['Ж', 'З', 'И', 'Й', 'К', 'Л'],
    ['М', 'Н', 'О', 'П', 'Р', 'С'],
    ['Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
    ['Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э'],
    ['Ю', 'Я', '',  '',  '',  ''],
]

CHAR_TO_COORDS: dict[str, tuple[int, int]] = {}
for r, row in enumerate(SQUARE, start=1):
    for c, ch in enumerate(row, start=1):
        if ch:
            CHAR_TO_COORDS[ch] = (r, c)

CHAR_TO_COORDS['Ё'] = CHAR_TO_COORDS['Е']

COORDS_TO_CHAR: dict[tuple[int, int], str] = {
    v: k for k, v in CHAR_TO_COORDS.items() if k != 'Ё'
}


def encrypt(text: str, separator: str = ' ') -> str:
    text = text.upper().replace('Ё', 'Е')
    codes: list[str] = []
    for ch in text:
        if ch in CHAR_TO_COORDS:
            r, c = CHAR_TO_COORDS[ch]
            codes.append(f'{r}{c}')
        elif ch == ' ':
            codes.append('00')
    return separator.join(codes)


def decrypt(ciphertext: str, separator: str = ' ') -> str:
    tokens = ciphertext.split(separator)
    result: list[str] = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token == '00':
            result.append(' ')
            continue
        if len(token) != 2 or not token.isdigit():
            raise ValueError(f'Неверный токен: "{token}"')
        r, c = int(token[0]), int(token[1])
        key = (r, c)
        if key not in COORDS_TO_CHAR:
            raise ValueError(f'Координаты ({r}, {c}) вне квадрата или не используются.')
        result.append(COORDS_TO_CHAR[key])
    return ''.join(result)


def print_square() -> None:
    print('\nКвадрат Полибия (6×6, русский алфавит):')
    print('       ' + '    '.join(str(i) for i in range(1, 7)))
    labels = [
        ['А', 'Б', 'В', 'Г', 'Д', 'Е/Ё'],
        ['Ж', 'З', 'И', 'Й', 'К', 'Л'],
        ['М', 'Н', 'О', 'П', 'Р', 'С'],
        ['Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
        ['Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э'],
        ['Ю', 'Я', '—', '—', '—', '—'],
    ]
    for r, row in enumerate(labels, start=1):
        print(f'  {r}    ' + '    '.join(row))
    print()


def _run_tests() -> None:
    tests = [
        ('ПРИВЕТ',       '34 35 23 13 16 41'),
        ('МОСКВА',       '31 33 36 25 13 11'),
        ('ЕЖ',           '16 21'),
        ('ТАЙНА',        '41 11 24 32 11'),
        ('ШИФР ПОЛИБИЯ', '51 23 43 35 00 34 33 26 23 12 23 62'),
    ]
    print('\n--- Тесты ---')
    all_ok = True
    for plain, expected in tests:
        enc = encrypt(plain)
        dec = decrypt(enc)
        plain_norm = plain.replace('Ё', 'Е')
        ok = enc == expected and dec == plain_norm
        if not ok:
            all_ok = False
        status = '✓' if ok else '✗'
        print(f'{status}  "{plain}" → "{enc}" → "{dec}"')
        if not ok:
            print(f'     ожидалось: "{expected}"')
    print('\nВсе тесты прошли успешно!' if all_ok else '\nЕсть ошибки!')


def main() -> None:
    print('=' * 45)
    print('     ШИФР ПОЛИБИЯ  (русский алфавит)')
    print('=' * 45)
    print_square()
    print('Примечание: Ё обрабатывается как Е.')
    print('            Пробел кодируется как 00.')
    print()

    while True:
        print('Выберите действие:')
        print('  1 — Зашифровать')
        print('  2 — Дешифровать')
        print('  3 — Выйти')
        choice = input('Ваш выбор: ').strip()

        if choice == '1':
            text = input('Введите текст для шифрования: ')
            try:
                result = encrypt(text)
                print(f'\nЗашифрованный текст: {result}\n')
            except Exception as e:
                print(f'Ошибка: {e}\n')

        elif choice == '2':
            text = input('Введите шифротекст (коды через пробел): ')
            try:
                result = decrypt(text)
                print(f'\nРасшифрованный текст: {result}\n')
            except Exception as e:
                print(f'Ошибка: {e}\n')

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
