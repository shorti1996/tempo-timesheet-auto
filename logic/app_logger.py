class AppLogger:
    def log(self, *args, sep=' ', end='\n', file=None):
        print(*args, sep=sep, end=end, file=file)


logger = AppLogger()
