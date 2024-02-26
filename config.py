from configparser import ConfigParser
import configparser, os


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser(interpolation=EnvInterpolation())
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config


if __name__ == '__main__':
    config = load_config()
    print(config)
