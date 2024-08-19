import toml


def load_config_file(request_dir: str) -> dict:
    try:
        with open(f"{request_dir}/requests.toml", "r") as file:
            existing_data = toml.load(file)
        return existing_data
    except FileNotFoundError:
        existing_data = {}
        return existing_data


def save_config_file(existing_data: dict, request_dir: str) -> bool:
    try:
        with open(f"{request_dir}/requests.toml", "w") as file:
            toml.dump(existing_data, file)
        return True
    except FileNotFoundError:
        print("Error. File not found.")
        return False
