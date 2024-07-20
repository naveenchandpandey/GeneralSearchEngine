from configparser import ConfigParser


class ConfigHelper:

    def __init__(self, filename):
        """
        Reads a config file and parses its structure
        :param filename: config file path
        """
        self.filename = filename

    def get_config(self):
        """
        Parses the config file and provides config object for the same
        :return: config object
        """
        config = ConfigParser()
        config.read(self.filename)
        return config
