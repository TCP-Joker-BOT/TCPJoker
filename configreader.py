import configparser


class ConfigReader:

    """Parses the bot config.

    Frontend for standard `ConfigParser` class. Config stored in INI-file.

    Attributes:
        config (ConfigParser): `ConfigParser` object.

    """

    def __init__(self, filename):
        """ConfigReader constructor.

        Args:
            filename (str): the name of file with config
        """
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_token(self):
        """Get the Telegram token.

        Returns:
            str: Telegram token.
        """
        if 'main' not in self.config:
            raise ValueError('Section main not found in config')
        if 'token' not in self.config['main']:
            raise ValueError('Token not found in config')
        return self.config['main']['token']

    def get_command_dict(self):
        """Get the dict, which associates commands with modules.

        Returns:
            dict: command -> module associations. 

            E.g. `{'whattimeisit': 'time'}` means command `/whattimeisit` will call the module `time`.
        """
        if 'commands' not in self.config:
            return {}
        else:
            return dict(self.config['commands'])
