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
        self.filename = filename
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

    def set_command(self, command, module):
        """Set command -> module association

        Args:
            command (str): command without `/`
            module (str): the module to be associated with `command`
        """
        if not self.config.has_section('commands'):
            self.config.add_section('commands')
        self.config.set('commands', command, value=module)
        self.config.write(open(self.filename, 'w'))

    def unset_command(self, command):
        """Remove command -> module association

        Args:
            command (str): command to be removed
        Raises:
            IndexError: if `command` is not present in config
        """
        if self.config.has_option('commands', command):
            self.config.remove_option('commands', command)
        else:
            raise IndexError
        self.config.write(open(self.filename, 'w'))
