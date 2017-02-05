class Logger:
    enabled = True
    debugmode = False
    verbose = False

    def info(msg):
        if Logger.enabled and Logger.verbose:
            print('[*]Info: ' + str(msg))

    def log(msg):
        if Logger.enabled:
            print(msg)

    def debug(msg):
        if Logger.enabled and Logger.debugmode:
            print('[#]Debug: ' + str(msg))

    def warn(msg):
        if Logger.enabled:
            print('[!]Warn: ' + str(msg))

    def error(msg):
        if Logger.enabled:
            print('[-]Error: ' + str(msg))
