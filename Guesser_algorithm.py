import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import matplotlib.cm as cm
import matplotlib.colors as colors


def fft(path):
    sampFreq, sound = wavfile.read(path) # sampFreq = 44.1 kHz
    sound = sound / 2.0 ** 15  # normalize the frequency
    signal = sound[:, 0] # only right ear
    signal = signal[:length_of_fft * sampFreq:]
    window = int(signal.size / (length_of_fft * check_rate))
    freq = np.fft.rfftfreq(window, d=1 / sampFreq)
    points = []
    for moving in range(length_of_fft * check_rate):
        fft_spectrum = np.abs(np.fft.rfft(signal[window * moving:window * (moving + 1):]))
        for i in range(len(freq)):
            if 70 < fft_spectrum[i]:  # looking at amplitudes of the spikes higher than 200
                if freq[i] <= 0: continue
                n = round(48 * math.log(freq[i] / 110, 2)) + 110  # round to musical tone
                points.append([moving / check_rate, n, fft_spectrum[i]])
    return np.array(points)


def label_maker(lst):
    label = list(set(np.round(np.arange(0, max(lst) + 1, max(lst) / 10))))
    return np.array(label)


def plot(points):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (9, 7)
    plt.xlabel("time[s]")
    plt.ylabel("freq (log)")
    t = points[::, 0]
    x = points[::, 1]
    y = points[::, 2]
    c_norm = colors.Normalize(vmin=0, vmax=max(y))
    plt.scatter(t, x, c=y, cmap='viridis', norm=c_norm)
    y_label = label_maker(y)
    plt.colorbar(cm.ScalarMappable(cmap='viridis', norm=c_norm), ticks=y_label, label='Amplitude')
    t_label = label_maker(t)
    plt.xticks(t_label, t_label)
    x_label = label_maker(x)
    plt.yticks(x_label, x_label)
    plt.show()


if __name__ == '__main__':
    path = '110hz.wav'
    length_of_fft = 10  # seconds
    check_rate = 10  # 1/check_rate samples in a second
    plot(fft(path))