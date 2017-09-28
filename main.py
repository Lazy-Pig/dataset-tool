import config
import logging


def main():
    dataset = config.dataset_preprocessor()
    dataset.init()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s',
                        datefmt='%m-%d %H:%M')
    main()