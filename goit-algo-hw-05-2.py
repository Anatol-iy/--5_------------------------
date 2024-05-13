#Повертає кортеж з кількістю ітерацій та "верхньою межею".

def binary_search(arr, x):
   
    low = 0  # Ініціалізуємо змінну `low`, яка вказує на нижню межу інтервалу пошуку.
    high = len(arr) - 1  # Ініціалізація змінної `high`, яка вказує на верхню межу інтервалу пошуку.
    mid = 0  # Ініціалізація змінної `mid`, яка вказує на середину інтервалу пошуку.
    iterations = 0  # Ініціалізація лічильника ітерацій

    while low <= high:
        mid = (high + low) // 2  # Обчислюємо середину інтервалу пошуку.
        iterations += 1  # Збільшуємо лічильник ітерацій

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return (iterations, arr[mid])  # Повертаємо кортеж з кількістю ітерацій та знайденим значенням.

    # Якщо елемент не знайдено, повертаємо "верхню межу"
    return (iterations, arr[low] if low < len(arr) else arr[high])


# Вхідні дані: відсортований масив дробових чисел
arr = [1.1, 1.3, 2.5, 3.8, 4.6, 5.9]
print(binary_search(arr, 3.5))
print(binary_search(arr, 4))
print(binary_search(arr, 6.0))