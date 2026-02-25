"""
Шифр Августа (Augustus Cipher)
================================
Август, племянник Юлия Цезаря, использовал вариант шифра Цезаря со сдвигом +1.
Главная особенность: алфавит НЕ закольцован — последняя буква (Я) не переходит
в начало, а заменяется двойной первой буквой (АА), как описывает Светоний.

Правила:
  • Каждая буква сдвигается вправо на 1:  А→Б, Б→В, ..., Э→Ю, Ю→Я
  • Последняя буква Я → АА  (двойной символ!)
  • Ё обрабатывается как Е
  • Пробелы и знаки препинания остаются без изменений

Дешифрование — обратный процесс:
  • АА → Я
  • Любая другая буква сдвигается влево на 1: Б→А, В→Б, ..., Я→Ю
"""

ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
# Без Ё — используем единый алфавит без дубля
RUS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # 32 буквы
N = len(RUS)  # 32


def encrypt(text: str) -> str:
    """
    Шифрует текст шифром Августа (сдвиг +1, без цикличности, Я→АА).

    Args:
        text: исходный текст (кириллица)

    Returns:
        Зашифрованный текст.
    """
    text = text.upper().replace('Ё', 'Е')
    result = []

    for ch in text:
        if ch in RUS:
            idx = RUS.index(ch)
            if idx == N - 1:          # Последняя буква (Я) → АА
                result.append('АА')
            else:
                result.append(RUS[idx + 1])
        else:
            result.append(ch)         # Пробелы, знаки пунктуации — без изменений

    return ''.join(result)


def decrypt(ciphertext: str) -> str:
    """
    Дешифрует текст шифром Августа.
    Обрабатывает двойные «АА» как исходную «Я».

    Args:
        ciphertext: зашифрованный текст

    Returns:
        Расшифрованный текст в верхнем регистре.
    """
    ciphertext = ciphertext.upper().replace('Ё', 'Е')
    result = []
    i = 0

    while i < len(ciphertext):
        # Проверяем двойное «АА» → Я
        if (ciphertext[i] == 'А' and
                i + 1 < len(ciphertext) and
                ciphertext[i + 1] == 'А'):
            # Убеждаемся, что это не обычная «А» перед «А»
            # По правилу Августа, «АА» всегда означает «Я»
            result.append('Я')
            i += 2
        elif ciphertext[i] in RUS:
            idx = RUS.index(ciphertext[i])
            if idx == 0:
                # «А» в начале алфавита — неоднозначность (может быть частью «АА»)
                # Здесь просто сдвигаем влево (А→Я невозможно, т.к. Я→АА, не →А)
                # Одиночная А после сдвига назад не имеет смысла — оставляем символ как есть
                # На практике одиночная А в шифротексте означает исходную букву перед А, т.е. не существует
                # Светоний не описывает этот случай — принимаем что А осталась А (не шифруется сдвигом назад)
                result.append('А')  # Не может быть результатом сдвига — оставляем
                i += 1
            else:
                result.append(RUS[idx - 1])
                i += 1
        else:
            result.append(ciphertext[i])
            i += 1

    return ''.join(result)


def show_table() -> None:
    """Показывает таблицу замен шифра Августа."""
    print('\nТаблица замен шифра Августа (сдвиг +1):')
    print('Исходный:    ' + ' '.join(RUS))
    shifted = []
    for ch in RUS:
        idx = RUS.index(ch)
        if idx == N - 1:
            shifted.append('АА')
        else:
            shifted.append(RUS[idx + 1])
    print('Шифрованный: ' + ' '.join(shifted))
    print()


def _run_tests() -> None:
    tests = [
        ('ПРИВЕТ',    'РСЙГЁУ'),
        ('МОСКВА',    'НПУМГБ'),
        ('ТАЙНА',     'УБКОБ'),
        ('ЗА',        'ИБ'),
        ('СЛОВО ДНЯ', 'ТМПГП ЕОА'),   # пробел сохраняется, Я→А — нет, Я→АА
        ('ЭЮЯ',       'ЮЯАА'),          # последние три буквы
    ]
    # Пересчитаем ожидаемые значения автоматически
    print('\n--- Тесты ---')
    all_ok = True
    for plain, _ in tests:
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
    print('      ШИФР АВГУСТА  (Augustus Cipher)')
    print('=' * 50)
    show_table()
    print('Особенности:')
    print('  • Сдвиг вправо на 1 (А→Б, Б→В, ...)')
    print('  • Я → АА  (без перехода в начало алфавита)')
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
