import hashlib as hsh


# Переводы
LANGS = {
    # Default / по умолчанию
    "en": {
        "big_file_prompt": "Is your file larger than 1 GB? (y / n): ",
        "path_prompt": "Specify the file path: ",
        "hash_prompt": "Enter the developer-provided hash: ",
        "file_not_found": "File not found!",
        "result_match": "Hash matches!",
        "result_mismatch": "Hash does NOT match!",
        "display_file_hash": "Hash of the specified file: ",
        "display_user_hash": "Entered hash: "
    },
    "ru": {
        "big_file_prompt": "Ваш файл тяжелее 1 ГБ? (y / n): ",
        "path_prompt": "Укажите путь к файлу: ",
        "hash_prompt": "Введите предоставленный разработчиком хэш: ",
        "file_not_found": "Файл не найден!",
        "result_match": "Хэш совпадает!",
        "result_mismatch": "Хэш не совпал!",
        "display_file_hash": "Хэш указанного файла: ",
        "display_user_hash": "Введённый хэш: "
    }
}


def calculate_file_hash(file_path, variant):
    if variant == "y":
        hash_obj = hsh.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    else:
        with open(file_path, "rb") as f:
            digest = hsh.file_digest(f, "sha256")
        return digest.hexdigest()


def check_hashes(hash1, hash2):
    if hash1.lower() == hash2.lower():
        return True
    else:
        return False


def main():
    # Выбор языка
    lang_choice = input("Select language (en / ru): ").strip().lower()
    if lang_choice not in LANGS:
        lang_choice = "en"

    # Выбранный словарь
    lang_dict = LANGS[lang_choice]

    variant = input(lang_dict["big_file_prompt"]).strip().lower()

    while True:
        try:
            # Путь к файлу
            file_path = input(lang_dict["path_prompt"]).strip()
            # Добавляем очистку от кавычек
            if (file_path.startswith('"') and file_path.endswith('"')) or \
                    (file_path.startswith("'") and file_path.endswith("'")):
                # Убираем первый и последний символ
                file_path = file_path[1:-1]
            # Преобразование в строку хэш файла
            file_hash = calculate_file_hash(file_path, variant)
            break
        except FileNotFoundError:
            print(lang_dict["file_not_found"])

    # Получить хэш от пользователя
    user_hash = input(lang_dict["hash_prompt"]).strip()

    # Вывести для сравнения
    print(f"{lang_dict['display_file_hash']}{file_hash}")
    print(f"{lang_dict['display_user_hash']}{user_hash}")

    # Результат
    if check_hashes(file_hash, user_hash):  # == True
        print(lang_dict["result_match"])
    else:
        print(lang_dict["result_mismatch"])


if __name__ == "__main__":
    main()
