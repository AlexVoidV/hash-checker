import hashlib as hl
import sys
from pathlib import Path

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
        "hash_changed": "Hash type changed to ",
        "no_permission": "No access rights to the file",
        "enable_comparison": "Comparison is enabled",
        "disable_comparison": "Comparison is disabled",
    },
    "ru": {
        "path_prompt": "Укажите путь к файлу: ",
        "hash_prompt": "Введите предоставленный разработчиком хэш: ",
        "file_not_found": "Файл не найден!",
        "result_match": "Хэш совпадает!",
        "result_mismatch": "Хэш НЕ совпал!",
        "display_file_hash": "Хэш указанного файла: ",
        "display_user_hash": "Введённый хэш:        ",
        "select_hash": "Выберите нужный тип хэша: ",
        "hash_changed": "Тип хэша сменён на ",
        "no_permission": "Нет прав доступа к файлу",
        "enable_comparison": "Сравнение включено",
        "disable_comparison": "Сравнение выключено",
    },
}

HASHES = {"1": "sha256", "2": "md5", "3": "sha1", "4": "sha512"}

ART = r"""
 _    _           _____ _    _      _____ _    _ ______ _____ _  ________ _____  
| |  | |   /\    / ____| |  | |    / ____| |  | |  ____/ ____| |/ /  ____|  __ \ 
| |__| |  /  \  | (___ | |__| |   | |    | |__| | |__ | |    | ' /| |__  | |__) |
|  __  | / /\ \  \___ \|  __  |   | |    |  __  |  __|| |    |  < |  __| |  _  / 
| |  | |/ ____ \ ____) | |  | |   | |____| |  | | |___| |____| . \| |____| | \ \ 
|_|  |_/_/    \_\_____/|_|  |_|    \_____|_|  |_|______\_____|_|\_\______|_|  \_\
"""

HELP_EN = """
/h – help
/q or Ctrl-C – exit
/t – change the type of hash
/c – enable or disable comparison"""

HELP_RU = """
/h – список команд
/q или Ctrl-C – выход
/t – сменить тип хэша
/c – включить или выключить сравнение"""

HELP_TEXTS = {"en": HELP_EN, "ru": HELP_RU}

MSG_BOX = {"0": "[INFO]: ", "1": "[SUCCESS]: ", "2": "[FAILURE]: "}


def calculate_file_hash(file_path: Path, hash_type: str) -> str:
    """Calculates the hash of a file.

    Args:
        file_path (Path): Accepts a string of the form \
            like "C:\\Downloads\\file.exe".
        hash_type (str): Specifies the hash type.

    Returns:
        str: Hexadecimal hash string
    """
    hash_obj = hl.new(hash_type)
    with file_path.open("rb") as f:
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

        HELP = HELP_TEXTS.get(lang_choice, HELP_EN)

        print(HELP, end="\n\n")

        # Выбранный словарь / Selected dictionary
        lang_dict = LANGS[lang_choice]

        hash_type = "sha256"  # По умолчанию / Default
        comparison = False  # По умолчанию / Default

        while True:
            try:
                # Путь к файлу / File path
                user_input = input("\n" + lang_dict["path_prompt"]).strip()

                # Список команд / List of commands
                if user_input.startswith("/"):
                    if user_input in ("/q", "/quit"):
                        raise KeyboardInterrupt
                    elif user_input == "/h":
                        print(HELP)
                        continue
                    elif user_input == "/t":
                        # Выбор хэша / Hash selection
                        hash_type = input(
                            "1 (SHA256) | 2 (MD5) | 3 (SHA1) | 4 (SHA512)\n"
                            + lang_dict["select_hash"]
                        ).strip()
                        hash_type = HASHES.get(hash_type, "sha256")
                        print(
                            MSG_BOX["0"]
                            + lang_dict["hash_changed"]
                            + hash_type
                        )
                        continue
                    elif user_input == "/c":
                        comparison = not comparison
                        comparison_status = (
                            lang_dict["enable_comparison"]
                            if comparison
                            else lang_dict["disable_comparison"]
                        )
                        print(MSG_BOX["0"] + comparison_status)
                        continue
                else:
                    clean_input = user_input.strip().strip('"').strip("'")
                    file_path = Path(clean_input).expanduser().resolve()
                    
                    if not file_path.exists() or not file_path.is_file():
                        raise FileNotFoundError

                    # Вычисление хэша / Calculating a hash
                    file_hash = calculate_file_hash(file_path, hash_type)

                    if comparison:
                        # Получить хэш от пользователя / Get a hash from a user
                        user_hash = input(lang_dict["hash_prompt"]).strip()

                        n_sep = len(lang_dict["display_file_hash"] + file_hash)
                        print("-" * n_sep)

                        # Вывести для сравнения / Display for comparison
                        print(f"{lang_dict['display_file_hash']}{file_hash}")
                        print(f"{lang_dict['display_user_hash']}{user_hash}")

                        # Результат / Result
                        if check_hashes(file_hash, user_hash):
                            print(MSG_BOX["1"] + lang_dict["result_match"])
                        else:
                            print(MSG_BOX["2"] + lang_dict["result_mismatch"])
                    else:
                        print(f"\n{file_hash}")
            except FileNotFoundError:
                print(MSG_BOX["2"] + lang_dict["file_not_found"])
            except PermissionError:
                print(MSG_BOX["2"] + lang_dict["no_permission"])

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()


if __name__ == "__main__":
    main()
