class Logger:
    enabled = True
    debugmode = False
    verbose = False

    @staticmethod
    def info(msg):
        if Logger.enabled and Logger.verbose:
            print('[*]Info: ' + str(msg))

    @staticmethod
    def log(msg):
        if Logger.enabled:
            print(msg)

    @staticmethod
    def debug(msg):
        if Logger.enabled and Logger.debugmode:
            print('[#]Debug: ' + str(msg))

    @staticmethod
    def warn(msg):
        if Logger.enabled:
            print('[!]Warn: ' + str(msg))

    @staticmethod
    def error(msg):
        if Logger.enabled:
            print('[-]Error: ' + str(msg))
