import json
import os
import sys


class JsonTestFileUtil:

    @staticmethod
    def save_test(test_name: str, test: list[dict]) -> None:
        if not test_name == "":
            current_path = os.path.dirname(sys.argv[0])  # needs to be configured in config.ini
            path = f'{current_path}\\surveys'
            os.makedirs(path, exist_ok=True)
            with open(f'surveys/{test_name}.json', 'w', encoding='utf-8') as f:
                json.dump(test, f, ensure_ascii=False, indent=4)
