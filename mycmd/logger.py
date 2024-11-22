from colorama import Fore, Style, init

# 初始化 colorama
init()

class Logger:
    @staticmethod
    def success(msg: str):
        print(f"{Fore.GREEN}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

    @staticmethod
    def error(msg: str):
        print(f"{Fore.RED}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

    @staticmethod
    def warning(msg: str):
        print(f"{Fore.YELLOW}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

    @staticmethod
    def info(msg: str):
        print(f"{Fore.BLUE}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

# 创建全局日志实例
logger = Logger() 