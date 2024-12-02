def binary_search_iterative(sorted_list: list, target: int) -> int:

    print("Ricerca binaria iterativa")

    inf = 0
    sup = len(sorted_list)-1

    while inf <= sup:
        med = (inf + sup) // 2 # Per ottenere un indice intero
        print(f"Estremo inferiore: {inf}, Espremo superiore: {sup}, Elemento medio: {sorted_list[med]}")

        if sorted_list[med] == target:
            print(f"Target {target} trovato, indice: {med}")
            return med
        elif sorted_list[med] < target:
            inf = med + 1
        else:
            sup = med - 1

    print(f"Target {target} non trovato")
    return -1


def binary_search_recursive(sorted_list: list, target: int, left: int, right: int) -> int:

    print("Ricerca binaria ricorsiva")

    if left > right:
        print(f"Target {target} non trovato")
        return -1

    med = (left + right) // 2
    print(f"Estremo inferiore: {left}, Espremo superiore: {right}, Elemento medio: {sorted_list[med]}")

    if sorted_list[med] == target:
        print(f"Target {target} trovato, indice: {med}")
        return med
    elif sorted_list[med] < target:
        return binary_search_recursive(sorted_list, target, med + 1, right)
    else:
        return binary_search_recursive(sorted_list, target, left, med - 1)


def check_input(sorted_list, target):

    if sorted_list==0:
        print("La lista è vuota")
    if not all(isinstance(x, (int, float)) for x in sorted_list):
        print("Tutti gli elementi della lista devono essere numeri")
    if not isinstance(target, (int, float)):
        print("Il target deve essere un numero")
    return True