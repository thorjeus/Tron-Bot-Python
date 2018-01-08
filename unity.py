import os


class Unity:

    @staticmethod
    def get_api_keys():
        lines = open('api.txt').read().split('\n')
        api_key = str(lines[0])
        api_secret = str(lines[1])
        return api_key, api_secret

    @staticmethod
    def clear():
        print(os.name)
        os.system("cls" if os.name == "nt" else "clear")
