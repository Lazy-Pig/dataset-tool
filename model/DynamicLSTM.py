# coding: utf-8

import tensorflow as tf
import logging


class DynamicLSTM(object):
    def __init__(self, train_dataset):
        self.train_dataset = train_dataset
        self.seq_len, self.feature_num, self.class_num = self.train_dataset.get_obersorvation()

    def build_graph(self, hidden_num=64):
        self.samples_x = tf.placeholder("float", [None, self.seq_len, self.feature_num])
        self.samples_y = tf.placeholder("float", [None, self.class_num])
        self.seqs_len = tf.placeholder(tf.int32, [None])

        weights = {
            'out': tf.Variable(tf.random_normal([hidden_num, self.class_num]))
        }
        biases = {
            'out': tf.Variable(tf.random_normal([self.class_num]))
        }

        x = tf.unstack(self.samples_x, self.seq_len, 1)

        lstm_cell = tf.contrib.rnn.BasicLSTMCell(hidden_num)

        outputs, states = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32,
                                                    sequence_length=self.seqs_len)
        outputs = tf.stack(outputs)
        outputs = tf.transpose(outputs, [1, 0, 2])

        batch_size = tf.shape(outputs)[0]
        index = tf.range(0, batch_size) * self.seq_len + (self.seqs_len - 1)
        outputs = tf.gather(tf.reshape(outputs, [-1, hidden_num]), index)
        self.model = tf.matmul(outputs, weights['out']) + biases['out']

    def create_training_method(self, learning_rate):
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.model, labels=self.samples_y))
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(self.cost)
        correct_pre = tf.equal(tf.argmax(self.model, 1), tf.argmax(self.samples_y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pre, tf.float32))

    def learn(self, learning_rate, training_steps, batch_size, display_freq):
        self.create_training_method(learning_rate)
        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)

            for step in range(1, training_steps + 1):
                batch_x, batch_y, batch_seqlen = self.train_dataset.next(batch_size)
                sess.run(self.optimizer,
                         feed_dict={
                             self.samples_x: batch_x,
                             self.samples_y: batch_y,
                             self.seqs_len: batch_seqlen
                         })
                if step % display_freq == 0 or step == 1:
                    acc = sess.run(self.accuracy,
                                   feed_dict={
                                       self.samples_x: batch_x,
                                       self.samples_y: batch_y,
                                       self.seqs_len: batch_seqlen
                                   })
                    loss = sess.run(self.cost,
                                    feed_dict={
                                        self.samples_x: batch_x,
                                        self.samples_y: batch_y,
                                        self.seqs_len: batch_seqlen
                                    })
                    logging.info("Step %s, Training Loss= %f, Training Accuracy= %f" % (step * batch_size,
                                                                                        loss,
                                                                                        acc))
        logging.info("训练结束")