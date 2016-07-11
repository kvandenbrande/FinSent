import configparser
import twitter_stream


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    db_config = config_section_map("database")
    twitter_config = config_section_map("twitter api")


def config_section_map(section):
    config = configparser.ConfigParser()
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: {0}".format(option))
        except IndexError:
            print("exception on {0}!".format(option))
            dict1[option] = None
    return dict1


if __name__ == "__main__":
    main()