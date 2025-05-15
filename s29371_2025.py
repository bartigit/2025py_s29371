# ===========================================
# Cel programu i kontekst zastosowania:
# 
# Program generuje losową sekwencję DNA o zadanej długości, umożliwia wstawienie imienia użytkownika 
# do sekwencji, zapisuje ciąg w formacie FASTA, wyświetla statystyki procentowe nukleotydów (A, C, G, T).
# Na koniec wizualizuje te statystyki na wykresie słupkowym przy pomocy biblioteki matplotlib.
# Program posiada zabezpieczenia wejścia (np. nie dopuszcza ujemnej długości sekwencji), generuje losowe ID,
# jeśli nie zostanie ono podane, a także został szczegółowo skomentowany.
#
# ===========================================

import random  # do generacji losowych sekwencji i ID
import matplotlib.pyplot as plt  # do wizualizacji statystyk

def generate_dna_sequence(length):
    """Generuje losową sekwencję DNA o zadanej długości."""
    return ''.join(random.choices('ACGT', k=length))


def insert_name(seq, name):
    """Wstawia imię w losowe miejsce w sekwencji DNA."""
    pos = random.randint(0, len(seq))  # losowa pozycja
    return seq[:pos] + name + seq[pos:]


def calculate_stats(seq):
    """Liczy statystyki nukleotydów oraz % par CG (z wykluczeniem liter nie-DNA)."""
    # Odfiltruj litery inne niż ACGT (np. imię)
    dna_only = ''.join([base for base in seq if base in 'ACGT'])
    total = len(dna_only)
    counts = {base: dna_only.count(base) for base in 'ACGT'}
    percentages = {base: 100 * counts[base] / total if total else 0 for base in
                   'ACGT'}  # zabezpieczenie na wypadek total == 0
    cg = counts['C'] + counts['G']
    cg_percent = 100 * cg / total if total else 0
    return percentages, cg_percent


def save_fasta(file_name, seq_id, description, seq_with_name):
    """Zapisuje sekwencję w pliku FASTA."""
    with open(file_name, 'w') as f:
        f.write(f">{seq_id} {description}\n")
        f.write(seq_with_name + '\n')


def plot_stats(percentages):
    """Wyświetla wykres słupkowy częstości nukleotydów."""
    bases = ['A', 'C', 'G', 'T']
    values = [percentages[base] for base in bases]
    plt.bar(bases, values, color=['dodgerblue', 'orange', 'green', 'red'])
    plt.ylim(0, 100)
    plt.xlabel('Nukleotyd')
    plt.ylabel('Procent [%]')
    plt.title('Zawartość nukleotydów w sekwencji DNA')
    plt.show()


def generate_random_id(length=8):
    """Generuje losowy identyfikator o podanej długości."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))


def get_valid_length():
    """Pobiera od użytkownika długość (>0) i waliduje, czy to liczba całkowita dodatnia."""
    while True:
        try:
            length = int(input("Podaj długość sekwencji: "))
            if length < 1:
                print("Długość nie może być ujemna ani zerowa. Spróbuj ponownie.")
            else:
                return length
        except ValueError:
            print("Błąd: musisz podać liczbę całkowitą!")


def main():
    # =========================
    #    WALIDACJA DANYCH
    # =========================
    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # MODIFIED (dodanie pełnej walidacji wejścia - argumentacja: ochrona przed ujemnymi długościami i wartościami niecałkowitymi):
    length = get_valid_length()

    # =========================
    #    LOSOWY ID SEKWENCJI
    # =========================
    # ORIGINAL:
    # seq_id = input("Podaj ID sekwencji: ")
    # MODIFIED (gdy użytkownik nie wpisze ID, generujemy automatyczne - argumentacja: wygoda i pewność unikalności):
    seq_id = input("Podaj ID sekwencji (możesz zostawić puste): ")
    if not seq_id.strip():
        seq_id = generate_random_id()
        print(f"Wygenerowano losowy ID: {seq_id}")

    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # Generowanie sekwencji i wstawianie imienia
    dna_seq = generate_dna_sequence(length)
    seq_with_name = insert_name(dna_seq, name)

    # Zapisywanie do pliku
    file_name = f"{seq_id}.fasta"
    save_fasta(file_name, seq_id, description, seq_with_name)
    print(f"\nSekwencja została zapisana do pliku {file_name}")
    print("Statystyki sekwencji:")

    # Obliczanie statystyk
    percentages, cg_percent = calculate_stats(seq_with_name)
    for base in 'ACGT':
        print(f"{base}: {percentages[base]:.1f}%")
    print(f"%CG: {cg_percent:.1f}")

    # =========================
    #    WYKRES MATPLOTLIB
    # =========================
    # MODIFIED (dodanie wizualizacji - argumentacja: lepsza czytelność, możliwość analizy wzrokowej):
    plot_stats(percentages)


if __name__ == "__main__":
    main()

# ==============================
# ZMIANY WZGLĘDEM KODU LLM:
# ==============================
#
# 1. Dodano walidację długości sekwencji, żeby nie była ujemna ani zerowa:
#    - ORYGINAŁ: length = int(input("Podaj długość sekwencji: "))
#    - ZMIANA: funkcja get_valid_length() z pętlą i obsługą wyjątków
#
# 2. Dodano automatyczne generowanie losowego seq_id jeśli użytkownik nie wpisze własnego:
#    - ORYGINAŁ: seq_id = input("Podaj ID sekwencji: ")
#    - ZMIANA: sprawdzanie, czy pole seq_id jest puste, jeśli tak, generate_random_id()
#
# 3. Dodano wykres słupkowy statystyk A, C, G, T za pomocą matplotlib:
#    - ORYGINAŁ: brak wykresu
#    - ZMIANA: funkcja plot_stats()
#
# ==============================