import json
from solver.katla import Katla


def print_dashes(n):
    print("-" * n)


def main():
    katla = Katla()
    states = []

    for i in range(0, 6):
        print_dashes(50)
        print("Langkah {} dari 6".format(i + 1))
        print_dashes(50)

        if i == 0:
            print("Ini beberapa kata bagus sebagai pemulai:")
            print(katla.get_starters())
            print_dashes(50)

        is_guess_valid = False

        while not is_guess_valid:
            guess = Katla.clean(
                input("Ketik kata yang kamu masukkan ke Katla: "))

            if len(guess) == 5:
                if katla.is_kbbi_word(guess):
                    is_guess_valid = True
                    print_dashes(50)
                else:
                    print("Kata tidak terdaftar di KBBI, harap ulangi ya!")
                    print_dashes(50)
            else:
                print("Kata harus punya lima huruf, harap ulangi ya!")
                print_dashes(50)

        print(
            "Sekarang, coba beritahu petunjuk warna yang kamu dapatkan dari Katla"
        )
        print(
            "Sebagai contoh, jika warnanya [hijau, abu-abu, kuning, abu-abu, hijau], harap masukkan: hakah"
        )

        verdict = input("Petunjuk Katla untuk tebakan '{}': ".format(guess))
        print_dashes(50)

        if verdict == "hhhhh":
            print("Brilian!")
            print_dashes(50)

            break
        else:
            states.append({
                "word": guess,
                "verdict": verdict
            })

            print("Berikut beberapa rekomendasi untuk tebakan selanjutnya:")
            print(katla.get_guesses(states))


if __name__ == '__main__':
    main()
