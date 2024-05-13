import timeit



# Путь к файлу статья 1.txt на вашем компьютере
file_path = 'D:/Projects/ДЗ5_ВерещакаАнатолійІванович/стаття 1.txt'

# Чтение содержимого файла
with open(file_path, 'r', encoding='utf-8') as file:
    article1_text = file.read()




def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}  # Створюємо порожню таблицю зсувів
    length = len(pattern)  # Визначаємо довжину патерна

    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table  # Повертаємо таблицю зсувів

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def compute_lps(pattern):
    lps = [0] * len(pattern)  # Створюємо список lps довжиною, рівною довжині патерна, і заповнюємо його нулями
    length = 0  # Ініціалізуємо довжину lps
    i = 1  # Індекс для перебору символів патерна, починаючи з другого символа

    while i < len(pattern):
        if pattern[i] == pattern[length]:  # Порівнюємо символ патерна з символом, що збігається
            length += 1  # Збільшуємо довжину lps
            lps[i] = length  # Присвоюємо значення lps для поточного індексу
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]  # Оновлюємо довжину lps, якщо є попередній збіг
            else:
                lps[i] = 0  # Якщо немає збігу, присвоюємо 0 для поточного індексу
                i += 1

    return lps  # Повертаємо список lps

def kmp_search(main_string, pattern):
    M = len(pattern)  # Визначаємо довжину патерна
    N = len(main_string)  # Визначаємо довжину головного рядка

    lps = compute_lps(pattern)  # Обчислюємо значення lps для патерна

    i = j = 0  # Ініціалізуємо індекси для головного рядка та патерна

    while i < N:
        if pattern[j] == main_string[i]:  # Порівнюємо символи головного рядка та патерна
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]  # Оновлюємо значення j, якщо є попередній збіг
        else:
            i += 1

        if j == M:  # Якщо весь патерн знайдено в головному рядку
            return i - j  # Повертаємо позицію початку підрядка

    return -1  # Якщо підрядок не знайдено

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)  # Довжина рядка s
    hash_value = 0  # Ініціалізація хеш-значення
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus  # Потужність бази для кожного символу
        hash_value = (hash_value + ord(char) * power_of_base) % modulus  # Обчислення хеш-значення
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)  # Довжина підрядка пошуку
    main_string_length = len(main_string)  # Довжина основного рядка
    
    # Базове число для хешування та модуль
    base = 256  # Базове число для хешування
    modulus = 101  # Модуль для хешування
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)  # Хеш підрядка пошуку
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)  # Хеш поточного відрізка рядка
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus  # Попереднє значення для перерахунку хешу
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:  # Перевірка, чи співпадають хеші
            if main_string[i:i+substring_length] == substring:  # Перевірка фактичного збігу підрядка
                return i  # Повертаємо позицію, де знайдено підрядок

        if i < main_string_length - substring_length:  # Перерахунок хешу для наступного відрізка
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:  # Перевірка на від'ємне значення хешу
                current_slice_hash += modulus

    return -1  # Повертається -1 у випадку, якщо підрядок не знайдено

# Визначаємо два види підрядків - один, що дійсно існує у тексті, інший - вигаданий
existing_substring = 'алгоритми та структури даних вже давно реалізовані'
non_existing_substring = 'вьадьывдаьвыьавдыьадывьадыьады'

# Функція для вимірювання часу виконання алгоритму Боєра-Мура
def measure_boyer_moore(text, pattern):
    return timeit.timeit(lambda: boyer_moore_search(text, pattern), number=10)

# Функція для вимірювання часу виконання алгоритму Кнута-Морріса-Пратта
def measure_kmp(text, pattern):
    return timeit.timeit(lambda: kmp_search(text, pattern), number=10)

# Функція для вимірювання часу виконання алгоритму Рабіна-Карпа
def measure_rabin_karp(text, pattern):
    return timeit.timeit(lambda: rabin_karp_search(text, pattern), number=10)




# Вимірюємо час виконання для кожного алгоритму та обох видів підрядків у кожному тексті
print("Час виконання алгоритму Боєра-Мура для першого тексту (існуючий підрядок):",
      measure_boyer_moore(article1_text, existing_substring))
print("Час виконання алгоритму Боєра-Мура для першого тексту (вигаданий підрядок):",
      measure_boyer_moore(article1_text, non_existing_substring))



print("Час виконання алгоритму Кнута-Морріса-Пратта для першого тексту (існуючий підрядок):",
      measure_kmp(article1_text, existing_substring))
print("Час виконання алгоритму Кнута-Морріса-Пратта для першого тексту (вигаданий підрядок):",
      measure_kmp(article1_text, non_existing_substring))



print("Час виконання алгоритму Рабіна-Карпа для першого тексту (існуючий підрядок):",
      measure_rabin_karp(article1_text, existing_substring))
print("Час виконання алгоритму Рабіна-Карпа для першого тексту (вигаданий підрядок):",
      measure_rabin_karp(article1_text, non_existing_substring))




    






