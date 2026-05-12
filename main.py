#!/usr/bin/env python3

def greet(name):
    return f"Hola, {name}!"

def add(a, b):
    return a + b

def main():
    name = input("Tu nombre: ").strip() or "Mundo"
    print(greet(name))

    try:
        x = int(input("Pon un número: "))
    except ValueError:
        print("Ese no es un número. Usando 0.")
        x = 0

    nums = [add(i, x) for i in range(1, 6)]
    print("Números:", nums)

    for i, v in enumerate(nums, 1):
        print(f"{i}: {v}")

if __name__ == "__main__":
    main()