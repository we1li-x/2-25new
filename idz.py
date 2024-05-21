#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import multiprocessing


def compute_sum(x, eps, result_queue):
    n = 0
    sum_result = 0
    bernoulli_numbers = [1]  # Начальное значение B_0 = 1

    while True:
        # Вычисление числа Бернулли по рекуррентному соотношению
        if n > 0:
            bernoulli_number = (1 / (n + 1)) * sum(
                (-1) ** k * math.comb(n, k) * bernoulli_numbers[k] for k in range(n)
            )
            bernoulli_numbers.append(bernoulli_number)

        # Вычисление члена ряда
        term = (-1)
        n * (x(2 * n)) / (2 * n + 1) * bernoulli_numbers[n]

        if abs(term) < eps:
            break

        sum_result += term
        n += 1

    result_queue.put(sum_result)


def compare_sums(x, y, eps):
    result_queue1 = multiprocessing.Queue()
    result_queue2 = multiprocessing.Queue()

    process1 = multiprocessing.Process(target=compute_sum, args=(x, eps, result_queue1))
    process2 = multiprocessing.Process(target=compute_sum, args=(y, eps, result_queue2))

    process1.start()
    process2.start()
    process1.join()
    process2.join()

    sum1 = result_queue1.get()
    sum2 = result_queue2.get()

    print(f"Сумма ряда для x: {sum1}")
    print(f"Сумма ряда для y: {sum2}")

    if abs(sum1 - sum2) < eps:
        print("Суммы рядов равны.")
    else:
        print("Суммы рядов не равны.")


if name == "__main__":
    compare_sums(0, 3, 10 ** -7)