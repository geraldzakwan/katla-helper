from src.utils import clean, print_dashes
from src.katla import Katla
from src.wordle import Wordle


def main():
    print_dashes(50)
    print("List of games:")
    print("1. Katla")
    print("2. Wordle")

    is_choice_valid = False

    while not is_choice_valid:
        game = input("Choose your game (1 or 2): ")

        if game == "1":
            solver = Katla()
            is_choice_valid = True
        elif game == "2":
            solver = Wordle()
            is_choice_valid = True
        else:
            print("Please type 1 or 2")
            print_dashes(50)

    print_dashes(50)

    states = []

    turn = 0
    finish = False

    while turn < 6 and not finish:
        print_dashes(50)
        print("Langkah {} dari 6".format(turn + 1))
        print_dashes(50)

        if turn == 0:
            print("Ini beberapa kata bagus sebagai pemulai:")
            print(solver.get_starters())
            print_dashes(50)

        is_guess_valid = False

        while not is_guess_valid:
            guess = clean(
                input("Ketik kata yang ingin kamu masukkan ke Katla: "))

            if len(guess) == 5:
                if solver.is_in_dictionary(guess):
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

        is_verdict_valid = False

        while not is_verdict_valid:
            verdict = clean(
                input("Petunjuk Katla untuk tebakan \"{}\": ".format(
                    guess))).lower()

            if len(verdict) == 5:
                allowed_chars = 0

                for i in range(0, 5):
                    if verdict[i] in ('a', 'k', 'h'):
                        allowed_chars += 1

                if allowed_chars == 5:
                    is_verdict_valid = True
                else:
                    print(
                        "Petunjuk hanya boleh mengandung huruf 'a', 'k' dan 'h'"
                    )
                    print(
                        "Sebagai contoh, ketik \"hakah\" jika warnanya [hijau, abu-abu, kuning, abu-abu, hijau]"
                    )
                    print_dashes(50)
            else:
                print("Petunjuk harus punya lima huruf, harap ulangi ya!")
                print(
                    "Sebagai contoh, ketik \"hakah\" jika warnanya [hijau, abu-abu, kuning, abu-abu, hijau]"
                )
                print_dashes(50)

        print_dashes(50)

        if verdict == "hhhhh":
            print("Brilian!")
            print_dashes(50)

            finish = True
        else:
            states.append({"word": guess, "verdict": verdict})
            guesses = solver.get_guesses(states)

            if len(guesses) > 0:
                if len(guesses) == 1:
                    print("Jawabannya pasti \"{}\"!".format(guesses[0]))

                    finish = True
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
