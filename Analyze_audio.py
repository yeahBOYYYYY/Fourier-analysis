import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import matplotlib.cm as cm
import matplotlib.colors as colors


plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (9, 7)

sampFreq, sound = wavfile.read('sounds.wav')
# sampFreq = 44.1 kHz

sound = sound / 2.0 ** 15  # normalize the frequency
signal = sound[:, 0]


length_of_fft = 10  # seconds
check_rate = 10  # 1/check_rate samples in a second
signal = signal[:length_of_fft * sampFreq:]
window = int(signal.size / (length_of_fft * check_rate))
freq = np.fft.rfftfreq(window, d=1/sampFreq)
points = []

for moving in range(length_of_fft * check_rate):
    fft_spectrum = np.abs(np.fft.rfft(signal[window*moving:window*(moving+1):]))
    for i in range(len(freq)):
        if 5 < fft_spectrum[i] < 200:  # looking at amplitudes of the spikes higher than 200
            points.append([moving / check_rate, freq[i]/100, fft_spectrum[i]])
points = np.array(points)


plt.xlabel("time[s]")
plt.ylabel("freq (log)")
t = points[::, 0]
x = points[::, 1]
x = np.array([np.log(x[i]) for i in range(len(x))])
y = points[::, 2]
c_norm = colors.Normalize(vmin=0, vmax=max(y))
plt.scatter(t, x, c=y, cmap='viridis', norm=c_norm)
cl = plt.colorbar(cm.ScalarMappable(cmap='viridis', norm=c_norm), ticks=np.arange(0, max(y), 5), label='Amplitude')
plt.xticks(np.arange(0, max(t) + 1, 1), np.arange(0, max(t) + 1, 1))
plt.yticks(np.arange(0, max(x) + 1, 1), np.arange(0, max(x) + 1, 1))
plt.show()
