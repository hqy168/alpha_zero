"""Functions to plot statistics csv file."""
from absl import app
from absl import flags
import math
import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FormatStrFormatter

FLAGS = flags.FLAGS
flags.DEFINE_string('train_csv_file', 'logs/train_gomoku_v2.csv', 'A csv file contains training statistics.')
flags.DEFINE_string(
    'eval_csv_file', 'logs/eval_gomoku_v2.csv', 'A csv file contains evaluation statistics for new checkpoint.'
)
flags.DEFINE_integer('update_frequency', 15, 'The frequency (in minutes) to update plots.')


# code from
# https://stackoverflow.com/questions/59969492/how-to-print-10k-20k-1m-in-the-xlabel-of-matplotlib-plot
def label_format_func(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else math.floor(math.log10(abs(value)) / 3)
    value = round(value / 1000**num_thousands, 2)
    return f'{value:g}' + ' KMGTPEZY'[num_thousands]


def main(argv):
    train_columns = ['train_steps', 'loss']
    eval_columns = ['train_steps', 'elo_rating']

    train_csv_file = FLAGS.train_csv_file
    eval_csv_file = FLAGS.eval_csv_file
    update_frequency = FLAGS.update_frequency

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.tight_layout(pad=5, w_pad=4)

    ax1.set_title('Training Loss', fontsize=14)
    ax1.set_xlabel('Train steps', fontsize=11)
    ax1.set_ylabel('Loss', fontsize=11)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(label_format_func))
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax2.set_title('Elo Rating', fontsize=14)
    ax2.set_xlabel('Train steps', fontsize=11)
    ax2.set_ylabel('Elo', fontsize=11)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(label_format_func))
    # ax2.yaxis.set_major_formatter(plt.FuncFormatter(label_format_func))
    # ax2.yaxis.set_ticks(np.arange(-3000, 6000, 1000))

    (line1,) = ax1.plot([], [], '-', color='#123597', label='Loss')
    (line2,) = ax2.plot([], [], '-', color='#0396FF', label='AlphaZero')

    # ax1.legend(loc='upper right')
    # ax2.legend(loc='upper right')

    def plot_lines():
        if os.path.exists(train_csv_file):
            train_data = pd.read_csv(train_csv_file, usecols=train_columns)
            line1.set_data(train_data.train_steps, train_data.loss)

            ax1.relim()
            ax1.autoscale()

        if os.path.exists(eval_csv_file):
            eval_data = pd.read_csv(eval_csv_file, usecols=eval_columns)
            line2.set_data(eval_data.train_steps, eval_data.elo_rating)

            ax2.relim()
            ax2.autoscale()

    plot_lines()

    def init_function():
        return (line1, line2)

    def update_function(frame):
        plot_lines()

        return (line1, line2)

    animated = FuncAnimation(
        fig,
        update_function,
        init_func=init_function,
        interval=update_frequency * 60 * 1000,
    )  # noqa: F841

    plt.show()


if __name__ == '__main__':
    app.run(main)
