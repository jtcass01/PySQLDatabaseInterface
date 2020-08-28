from datetime import datetime
from enum import IntEnum
import os
import platform
from typing import Union


class Logger(object):
    def __init__(self, file_log: bool = True, log_location: Union[str, None] = None) -> None:
        # Determine operating system
        self.system_platform = platform.system()

        self.file_log = file_log
        if file_log:
            if log_location is None:
                self.log_location = os.getcwd() + os.path.sep + ".." + os.path.sep + "Logs" + os.path.sep + datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3] + ".log"
            else:
                self.log_location = log_location

    def log(self, message: str, status: IntEnum) -> None:
        if self.file_log:
            Logger.log_to_file(self.log_location, message, status)
        Logger.console_log(message, status)

    @staticmethod
    def log_to_file(log_file_location: str, message: str, status: IntEnum) -> None:
        with open(log_file_location, 'a+') as log_file:
            log_file.write(datetime.now().strftime('%H:%M:%S.%f')[:-3] + ' - [{}]'.format(str(status)) + ' - ' + message + '\n')

    @staticmethod
    def console_log(message: str, status: IntEnum) -> None:
        system_platform = platform.system()

        if system_platform == 'Windows':
            from printy import printy

            if status == Logger.LogStatus.SUCCESS:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[n]' + ' ' + message + '@', predefined='w')  # SUCCESS
            elif status == Logger.LogStatus.FAIL:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[r]' + ' ' + message + '@', predefined='w')  # FAIL
            elif status == Logger.LogStatus.COMMUNICATION:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[c]' + ' ' + message + '@', predefined='w')
            elif status == Logger.LogStatus.MINOR_FAIL:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[r>]' + ' ' + message + '@', predefined='w') # Minor Fail
            elif status == Logger.LogStatus.EMPHASIS:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[y]' + ' ' + message + '@', predefined='w')
            else:
                printy((datetime.now().strftime('%H:%M:%S.%f')[:-3]) + '[r]' + ' ' + 'INVALID LOG FORMAT. Please check int value.' + '@', predefined='w')
        else:
            from colorama import Fore

            if status == Logger.LogStatus.SUCCESS:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.GREEN + ' ' + message)  #SUCCESS
            elif status == Logger.LogStatus.FAIL:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.RED + ' ' + message)   #FAIL
            elif status == Logger.LogStatus.COMMUNICATION:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.CYAN + ' ' + message)
            elif status == Logger.LogStatus.MINOR_FAIL:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.LIGHTRED_EX + ' ' + message)  #Minor fail
            elif status == Logger.LogStatus.EMPHASIS:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.YELLOW + ' ' + message)
            else:
                print(Fore.WHITE + datetime.now().strftime('%H:%M:%S.%f')[:-3] + Fore.RED + ' INVALID LOG FORMAT. Please check int value.')

    class LogStatus(IntEnum):
        SUCCESS = 1
        FAIL = 2
        COMMUNICATION = 3
        MINOR_FAIL = 4
        EMPHASIS = 5