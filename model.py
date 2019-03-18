import tensorflow as tf


class The3dcnn_lstm_Model(tf.keras.Model):

    def __init__(self, rnn_units, num_class):
        super(The3dcnn_lstm_Model, self).__init__()
        self.rnn_units = rnn_units
        self.num_class = num_class

        # 3DCNN
        self.conv3d1 = tf.keras.layers.Conv3D(filters=16, kernel_size=[3, 3, 3], strides=[1, 1, 1], use_bias=True,
                                              activation=tf.nn.relu, padding='same',
                                              kernel_initializer=tf.keras.initializers.normal(stddev=0.01),
                                              bias_initializer=tf.zeros_initializer(),
                                              data_format='channels_last')
        self.pooling1 = tf.keras.layers.MaxPool3D(pool_size=[2, 2, 2], strides=[2, 2, 2], padding='same',
                                                  data_format='channels_last')

        self.conv3d2 = tf.keras.layers.Conv3D(filters=32, kernel_size=[3, 3, 3], strides=[1, 1, 1], use_bias=True,
                                              activation=tf.nn.relu, padding='same',
                                              kernel_initializer=tf.keras.initializers.normal(stddev=0.01),
                                              bias_initializer=tf.zeros_initializer(),
                                              data_format='channels_last')
        self.pooling2 = tf.keras.layers.MaxPool3D(pool_size=[2, 2, 2], strides=[2, 2, 2], padding='same',
                                                  data_format='channels_last')

        self.conv3d3 = tf.keras.layers.Conv3D(filters=16, kernel_size=[3, 3, 3], strides=[1, 1, 1], use_bias=True,
                                              activation=tf.nn.relu, padding='same',
                                              kernel_initializer=tf.keras.initializers.normal(stddev=0.01),
                                              bias_initializer=tf.zeros_initializer(),
                                              data_format='channels_last')
        self.pooling3 = tf.keras.layers.MaxPool3D(pool_size=[3, 2, 3], strides=[3, 2, 2], padding='same',
                                                  data_format='channels_last')

        # FC
        self.fc = tf.keras.layers.Dense(units=num_class, use_bias=True, activation=None,
                                        kernel_initializer=tf.keras.initializers.normal(stddev=0.01),
                                        bias_initializer=tf.constant_initializer)

    def call(self, inputs, dropout=0.2, **kwargs):
        """
        :param **kwargs:
        :param **kwargs:
        :param input: [?, 10, 80, 200, 1]
        :return:
        """
        conv1 = self.conv3d1(inputs)
        conv1 = tf.layers.batch_normalization(conv1, training=True)
        pool1 = self.pooling1(conv1)  # (?, 5, 40, 100, 16)
        print('pool1: ', pool1.get_shape().as_list())

        conv2 = self.conv3d2(pool1)
        conv2 = tf.layers.batch_normalization(conv2, training=True)
        pool2 = self.pooling2(conv2)  # (?, 3, 20, 50, 32)
        print('pool2: ', pool2.get_shape().as_list())

        conv3 = self.conv3d3(pool2)
        conv3 = tf.layers.batch_normalization(conv3, training=True)
        pool3 = self.pooling3(conv3)  # (?, 1, 10, 25, 16)
        print('pool3: ', pool3.get_shape().as_list())

        x = tf.squeeze(pool3, axis=1)  # (?, 10, 25, 16)

        print('lstm :\n', x.get_shape().as_list())  # [?, 10, 25, 16]
        ##################################################################
        # 该方法效果不理想
        # x = tf.transpose(x, [0, 2, 1, 3])  # [?, 25, 10, 16]
        #
        # # print(x.get_shape().as_list())  # [?, 25, 10, 16]
        # # treat `feature_w` as max_timestep in lstm.
        # # vac_len = tf.shape(x)[2] * tf.shape(x)[3]
        # x = tf.reshape(x, [self.batch_size, 25, 160])
        # print('lstm input shape: {}'.format(tf.shape(x)))  # [?, 25, 160]
        #
        # outputs1, _ = self.gru1(x)  # [?, 25, 1024]
        # outputs2, _ = self.gru2(outputs1)  # [?, 25, 1024]
        # outputs3, h_state = self.gru3(outputs2)  # [?, 25, 1024]
        #
        # output = outputs3[:, -1, :]  # [?, 1024]
        ####################################################################

        h_conv3_features = tf.unstack(x, axis=-1)  # [[?, 10, 25], ....16]
        channel = x.get_shape().as_list()[-1]
        rnn_output = []
        for channel_index in range(channel):
            name = "gru_" + str(channel_index)
            item_x = tf.transpose(h_conv3_features[channel_index], [0, 2, 1])  # [?, 25, 10] for item in 16
            cell = tf.keras.layers.CuDNNLSTM(units=self.rnn_units, name=name)
            item_out = cell(inputs=item_x)  # [?, 25, 32]
            cell = None

            rnn_output.append(item_out)

        output = tf.concat(rnn_output, 1)  # [?, self.rnn_units*16=32*16]

        d = tf.keras.layers.Dropout(dropout)(output)
        logits = self.fc(d)

        return logits
