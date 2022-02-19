import json
from solver.katla import Katla


def print_dashes(n):
    print("-" * n)


def main():
    katla = Katla()
    states = []

    turn = 0
    finish = False

    while turn < 6 and not finish:
        print_dashes(50)
        print("Langkah {} dari 6".format(turn + 1))
        print_dashes(50)

        if turn == 0:
            print("Ini beberapa kata bagus sebagai pemulai:")
            print(katla.get_starters())
            print_dashes(50)

        is_guess_valid = False

        while not is_guess_valid:
            guess = Katla.clean(
                input("Ketik kata yang ingin kamu masukkan ke Katla: "))

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

        if turn == 0:
            print(
                "Sekarang, coba beritahu petunjuk warna yang kamu dapatkan dari Katla"
            )
            print(
                "Sebagai contoh, ketik \"hakah\" jika warnanya [hijau, abu-abu, kuning, abu-abu, hijau]"
            )
            print(
                "Jika kata kamu sudah benar, masukkan \"hhhhh\" atau tekan Ctrl + C untuk keluar dari program"
            )
            print_dashes(75)

        verdict = input("Petunjuk Katla untuk tebakan \"{}\": ".format(guess))
        print_dashes(50)

        if verdict == "hhhhh":
            print("Brilian!")
            print_dashes(50)

            finish = True
        else:
            states.append({"word": guess, "verdict": verdict})
            guesses = katla.get_guesses(states)

            if len(guesses) > 0:
                if len(guesses) == 1:
                    print("Jawabannya pasti \"{}\"!".format(guesses[0]))
                else:
                    print(
                        "Berikut beberapa rekomendasi untuk tebakan selanjutnya:"
                    )
                    print(guesses)
            else:
                print(
                    "Mohon maaf kami sekarang tidak menemukan kata apapun yang cocok dari kamus kami :)"
                )
                print_dashes(75)

                finish = True

        turn = turn + 1


if __name__ == '__main__':
    main()
