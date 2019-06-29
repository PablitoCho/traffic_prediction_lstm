import os.path
import numpy
import tensorflow as tf
import tensorflow.contrib.rnn as rnn

# Basic model parameters as external flags.
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('input_dir', '.', 'Input Directory.')
flags.DEFINE_string('output_dir', '.', 'Input Directory.')


def run_training():
    N_HIDDEN_LAYERS = 1000
    N_ITERAIONS = 100

    learning_rate = 0.01
    input_dimension = 50
    output_dim = 50
    seq_length = 7

    data = numpy.loadtxt('./trend_50.csv', delimiter=',')
    inputs = data[:-1, :]
    label = data[1:, :]
    dataX = []
    dataY = []
    for i in range(0, len(label) - seq_length):
        _x = inputs[i:i + seq_length]
        _y = label[i + seq_length]  # Next close price
        dataX.append(_x)
        dataY.append(_y)

    x = tf.placeholder(tf.float32, shape=(None, seq_length, input_dimension))
    y = tf.placeholder(tf.float32, shape=(None, input_dimension))

    cell = rnn.BasicLSTMCell(num_units=N_HIDDEN_LAYERS, state_is_tuple=True, activation=tf.tanh)
    outputs, state = tf.nn.dynamic_rnn(cell, x, dtype=tf.float32)

    y_pred = tf.contrib.layers.fully_connected(
        outputs[:, -1], output_dim, activation_fn=None)  # We use the last cell's output

    # cost/loss
    loss = tf.losses.mean_squared_error(y, y_pred)

    # optimizer
    optimizer = tf.train.AdamOptimizer(learning_rate)
    train = optimizer.minimize(loss)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        
        for i in range(N_ITERAIONS):
            _, step_loss = sess.run([train, loss], feed_dict={
                x: dataX,
                y: dataY})
            print("[step: {}] loss: {}".format(i, step_loss))

        saver = tf.train.Saver()
        checkpoint_file = os.path.join(FLAGS.output_dir, 'checkpoint')
        saver.save(sess, checkpoint_file, global_step=0)

        predicted = sess.run(y_pred, feed_dict={x: dataX[0]})
        print(predicted)


def main(_):
    run_training()

if __name__ == '__main__':
    tf.app.run()
