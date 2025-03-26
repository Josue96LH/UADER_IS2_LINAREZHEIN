import matplotlib.pyplot as plt


def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def main():
    results = []
    for i in range(1, 10001):
        sequence = collatz_sequence(i)
        results.append((i, len(sequence)))

    x = [result[1] for result in results]
    y = [result[0] for result in results]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, marker='o', color='b', alpha=0.5)
    plt.xlabel('Número de iteraciones')
    plt.ylabel('Número de inicio de la secuencia')
    plt.title('Convergencia de la conjetura de Collatz para números entre 1 y 10000')
    plt.grid(True)
    plt.savefig('src/collatz_plot.png')
    plt.show()


if __name__ == "__main__":
    main()
