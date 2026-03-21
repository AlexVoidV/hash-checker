import hashlib as hl
import sys


# Переводы / Translations
LANGS = {
    # По умолчанию / Default
    "en": {
        "path_prompt": "Specify the file path: ",
        "hash_prompt": "Enter the developer-provided hash: ",
        "file_not_found": "File not found!",
        "result_match": "Hash matches!",
        "result_mismatch": "Hash does NOT match!",
        "display_file_hash": "Hash of the specified file: ",
        "display_user_hash": "Entered hash:               ",
        "select_hash": "Select the desired hash type: ",
        "hash_comparison": "Need a hash comparison? ",
    },
    "ru": {
        "path_prompt": "Укажите путь к файлу: ",
        "hash_prompt": "Введите предоставленный разработчиком хэш: ",
        "file_not_found": "Файл не найден!",
        "result_match": "Хэш совпадает!",
        "result_mismatch": "Хэш не совпал!",
        "display_file_hash": "Хэш указанного файла: ",
        "display_user_hash": "Введённый хэш:        ",
        "select_hash": "Выберите нужный тип хэша: ",
        "hash_comparison": "Требуется сравнение хэша? ",
    },
}

HASHES = {"1": "sha256", "2": "md5", "3": "sha1"}

ART = r"""
 _    _           _____ _    _      _____ _    _ ______ _____ _  ________ _____  
| |  | |   /\    / ____| |  | |    / ____| |  | |  ____/ ____| |/ /  ____|  __ \ 
| |__| |  /  \  | (___ | |__| |   | |    | |__| | |__ | |    | ' /| |__  | |__) |
|  __  | / /\ \  \___ \|  __  |   | |    |  __  |  __|| |    |  < |  __| |  _  / 
| |  | |/ ____ \ ____) | |  | |   | |____| |  | | |___| |____| . \| |____| | \ \ 
|_|  |_/_/    \_\_____/|_|  |_|    \_____|_|  |_|______\_____|_|\_\______|_|  \_\
"""


def calculate_file_hash(file_path: str, hash_type: str) -> str:
    """Calculates the hash of a file.

    Args:
        file_path (str): Accepts a string of the form \
            like "C:\\Downloads\\file.exe".
        hash_type (str): Specifies the hash type.

    Returns:
        str: Hexadecimal hash string
    """
    hash_obj = hl.new(hash_type)
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def check_hashes(hash1: str, hash2: str) -> bool:
    """Compares two different hashes (strings)
    in a case-insensitive manner.

    Args:
        hash1 (str): Hash of the selected file.
        hash2 (str): The hash entered by the user into the terminal.

    Returns:
        bool: Returns True if the hashes (strings) are the same,
        and False otherwise.
    """
    return hash1.lower() == hash2.lower()


# TODO: 1. New input system
def main() -> None:
    try:
        print(ART)

        # Выбор языка / Language selection
        lang_choice = (
            input("Select language / Выберите язык (en / ru): ")
            .strip()
            .lower()
        )
        if lang_choice not in LANGS:
            lang_choice = "en"

        # Выбранный словарь / Selected dictionary
        lang_dict = LANGS[lang_choice]

        # Выбор хэша / Hash selection
        hash_type = input(
            "1 (SHA256) | 2 (MD5) | 3 (SHA1)\n" + lang_dict["select_hash"]
        ).strip()
        hash_type = HASHES.get(hash_type, "sha256")

        comparison = (
            input(lang_dict["hash_comparison"] + "(y / n): ").strip().lower()
        )

        while True:
            try:
                # Путь к файлу / File path
                file_path = input("\n" + lang_dict["path_prompt"]).strip()

                # Очистка от кавычек / Clearing quotes
                if (file_path.startswith('"') and file_path.endswith('"')) or (
                    file_path.startswith("'") and file_path.endswith("'")
                ):
                    file_path = file_path[1:-1]
                # Вычисление хэша / Calculating a hash
                file_hash = calculate_file_hash(file_path, hash_type)

                if comparison == "y":
                    # Получить хэш от пользователя / Get a hash from a user
                    user_hash = input(lang_dict["hash_prompt"]).strip()

                    n_sep = 107
                    print("-" * n_sep)

                    # Вывести для сравнения / Display for comparison
                    print(f"{lang_dict['display_file_hash']}{file_hash}")
                    print(f"{lang_dict['display_user_hash']}{user_hash}")

                    # Результат / Result
                    if check_hashes(file_hash, user_hash):
                        print(lang_dict["result_match"])
                    else:
                        print(lang_dict["result_mismatch"])
                else:
                    print(f"\n{file_hash}")
            except FileNotFoundError:
                print(lang_dict["file_not_found"])

    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
