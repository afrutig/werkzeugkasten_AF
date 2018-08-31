from scipy.signal import butter, lfilter, filtfilt, firwin
import numpy as np
    # filter the signal
N = 10
Fc = 1000
Fs = 1600
# provide them to firwin
h = firwin(numtaps=N, cutoff=40, nyq=Fs / 2)

# 'x' is the time-series data you are filtering
#filtered_signal = lfilter(h, 1.0, imported_data.data["Channel A"])


#b, a = scipy.signal.butter(N, Wn, 'low')
#output_signal = scipy.signal.filtfilt(b, a, input_signal)

def moving_average(data,order=3):
    """order = number of datapoints averaged WRONG!!"""
    data = np.asarray(data)
    dataMean = []
    dataMean.append(data[0])
    for j in range(order-2,len(data)+(1-order)):

        dataMean.append(np.mean(data[j-(order-2):j+(order-2)]))
    dataMean.append(data[-1])

    return np.asarray(dataMean)

def moving_average_std(data,order=3):
    """order = number of datapoints averaged"""
    data = np.asarray(data)
    dataMean = []
    datastd = []
    dataMean.append(data[0])

    for j in range(order-2,len(data)+(1-order)):

        datastd.append(np.std(data[j-(order-2):j+(order-2)]))
        dataMean.append(np.mean(data[j-(order-2):j+(order-2)]))

    return np.asarray(dataMean),np.asarray(datastd)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

from numpy import array, sign, zeros
from scipy.interpolate import interp1d

def create_envelope(s):
    # create the upper and lower enveloppe of a signal according to: https://stackoverflow.com/questions/34235530/python-how-to-get-high-and-low-envelope-of-a-signal
    q_u = zeros(s.shape)
    q_l = zeros(s.shape)

    #Prepend the first value of (s) to the interpolating values. This forces the model to use the same starting point for both the upper and lower envelope models.

    u_x = [0,]
    u_y = [s[0],]

    l_x = [0,]
    l_y = [s[0],]

    #Detect peaks and troughs and mark their location in u_x,u_y,l_x,l_y respectively.

    for k in xrange(1,len(s)-1):
        if (sign(s[k]-s[k-1])==1) and (sign(s[k]-s[k+1])==1):
            u_x.append(k)
            u_y.append(s[k])

        if (sign(s[k]-s[k-1])==-1) and ((sign(s[k]-s[k+1]))==-1):
            l_x.append(k)
            l_y.append(s[k])

    #Append the last value of (s) to the interpolating values. This forces the model to use the same ending point for both the upper and lower envelope models.

    u_x.append(len(s)-1)
    u_y.append(s[-1])

    l_x.append(len(s)-1)
    l_y.append(s[-1])

    #Fit suitable models to the data. Here I am using cubic splines, similarly to the MATLAB example given in the question.

    u_p = interp1d(u_x,u_y, kind = 'cubic',bounds_error = False, fill_value=0.0)
    l_p = interp1d(l_x,l_y,kind = 'cubic',bounds_error = False, fill_value=0.0)

    #Evaluate each model over the domain of (s)
    for k in xrange(0,len(s)):
        q_u[k] = u_p(k)
        q_l[k] = l_p(k)

    return q_u,q_l # upper and lower envelopes are returned