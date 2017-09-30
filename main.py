# coding: utf-8
import config
import logging


def main():
    train_dataset = config.dataset_preprocessor()
    # model = config.train_model(train_dataset)
    # model.build_graph()
    # model.learn(learning_rate=0.01, training_steps=1000, batch_size=10, display_freq=10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s',
                        datefmt='%m-%d %H:%M')
    main()