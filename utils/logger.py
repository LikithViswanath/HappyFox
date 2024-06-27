import logging


class DualLogger:
    def __init__(self, name=__name__, log_file='app.log', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# Example usage
