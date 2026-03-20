import hashlib as hsh
import sys


# NOTE: Works well only with Python 3.11+

# Переводы / Translations
LANGS = {
    # Default / По умолчанию
    "en": {
        "big_file_prompt": "Is your file larger than 1 GB? (y / n): ",
        "path_prompt": "Specify the file path: ",
        "hash_prompt": "Enter the developer-provided hash: ",
        "file_not_found": "File not found!",
        "result_match": "Hash matches!",
        "result_mismatch": "Hash does NOT match!",
        "display_file_hash": "Hash of the specified file: ",
        "display_user_hash": "Entered hash: ",
        "exit_instructions": "To exit, press <Q>"
    },
    "ru": {
        "big_file_prompt": "Ваш файл тяжелее 1 ГБ? (y / n): ",
        "path_prompt": "Укажите путь к файлу: ",
        "hash_prompt": "Введите предоставленный разработчиком хэш: ",
        "file_not_found": "Файл не найден!",
        "result_match": "Хэш совпадает!",
        "result_mismatch": "Хэш не совпал!",
        "display_file_hash": "Хэш указанного файла: ",
        "display_user_hash": "Введённый хэш: ",
        "exit_instructions": "Чтобы выйти, нажмите <Q>"
    }
}

HASHES = {
    "1": "sha256",
    "2": "md5",
    "3": "sha1"
}

ART = r"""
 _    _           _____ _    _      _____ _    _ ______ _____ _  ________ _____  
| |  | |   /\    / ____| |  | |    / ____| |  | |  ____/ ____| |/ /  ____|  __ \ 
| |__| |  /  \  | (___ | |__| |   | |    | |__| | |__ | |    | ' /| |__  | |__) |
|  __  | / /\ \  \___ \|  __  |   | |    |  __  |  __|| |    |  < |  __| |  _  / 
| |  | |/ ____ \ ____) | |  | |   | |____| |  | | |___| |____| . \| |____| | \ \ 
|_|  |_/_/    \_\_____/|_|  |_|    \_____|_|  |_|______\_____|_|\_\______|_|  \_\
"""


def calculate_file_hash(file_path, hash_type):
    """Calculates the hash of a file.

    Args:
        file_path (str): Accepts a string 
        of the form like "C:\\Downloads\\file.exe".
        ~variant (str): Specifies the hash 
        calculation path (chunk-wise or as a whole).~

    Returns:
        str: HASH256
    """
    # if variant == "n":
    #     with open(file_path, "rb") as f:
    #         digest = hsh.file_digest(f, "sha256")
    #     return digest.hexdigest()
    # else:
    hash_obj = hsh.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def check_hashes(hash1, hash2):
    """Compares two different hashes (strings) 
    in a case-insensitive manner.

    Args:
        hash1 (str): Hash of the selected file.
        hash2 (str): The hash entered by the user into the terminal.

    Returns:
        bool: Returns True if the hashes (strings) are the same, 
        and False otherwise.
    """
    if hash1.lower() == hash2.lower():
        return True
    else:
        return False


def main():
    print(ART)

    # Выбор языка / Language selection
    lang_choice = input("Select language (en / ru): ").strip().lower()
    if lang_choice not in LANGS:
        lang_choice = "en"

    # Выбранный словарь / Selected dictionary
    lang_dict = LANGS[lang_choice]

    # Выбор хэша
    hash_type = input('''1 (HASH256) | 2 (MD5) | 3 (SHA1)
    Выберите нужный тип хэша: ''')

    comparison = input("Требуется сравнение хэша? (y / n): ").strip().lower()

    # DELETE THIS!
    # variant = input(lang_dict["big_file_prompt"]).strip().lower()

    print(lang_dict["exit_instructions"])

    while True:
        try:
            # Путь к файлу / File path
            file_path = input(lang_dict["path_prompt"]).strip()

            # TODO: ↓.
            # Выход по требованию / Exit on demand
            if file_path == "q":
                sys.exit()

            # Очистка от кавычек / Clearing quotes
            if (file_path.startswith('"') and file_path.endswith('"')) or \
                    (file_path.startswith("'") and file_path.endswith("'")):
                # Убираем первый и последний символ
                # / Remove the first and last characters
                file_path = file_path[1:-1]
            # Преобразование в строку хэш файла
            # / Converting a hash file to a string
            file_hash = calculate_file_hash(file_path, hash_type)
            break
        except FileNotFoundError:
            print(lang_dict["file_not_found"])

    if comparison == "y":
        # Получить хэш от пользователя / Get a hash from a user
        user_hash = input(lang_dict["hash_prompt"]).strip()

        print("-----------------------------------------------", end="")
        print("------------------------------------------------------------")

        # Вывести для сравнения / Display for comparison
        print(f"{lang_dict['display_file_hash']}{file_hash}")
        print(f"{lang_dict['display_user_hash']}{user_hash}")

        # Результат / Result
        if check_hashes(file_hash, user_hash):  # == True
            print(lang_dict["result_match"])
        else:
            print(lang_dict["result_mismatch"])
    else:
        print(file_hash)


if __name__ == "__main__":
    main()
