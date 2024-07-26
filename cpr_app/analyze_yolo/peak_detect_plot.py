import numpy as np
from .peak_data import PeakData

# plot_csv用
# 2種類のピーク検出
def peak_detect_window(data, window_size=80):

    peaks_upper = np.zeros(len(data))
    peaks_lower = np.zeros(len(data))

    for i in range(len(data) - window_size):
        window = data[i:i+window_size]
        recoil = max(window)
        depth = min(window)
        if data[i+window_size//2] == recoil:
            peaks_upper[i+window_size//2] = recoil
        if data[i+window_size//2] == depth:
            peaks_lower[i+window_size//2] = depth

    recoil_order_list = np.where(peaks_upper != 0)[0]
    recoil_values = np.delete(peaks_upper, np.where(peaks_upper == 0))
    depth_order_list = np.where(peaks_lower != 0)[0]
    depth_values = np.delete(peaks_lower, np.where(peaks_lower == 0))
    
    if abs( len(recoil_order_list) - len(depth_order_list)) > 1:
        recoil_order_list, depth_order_list, recoil_values, depth_values = adjust_peak(recoil_order_list, depth_order_list, recoil_values, depth_values, data)
    
    recoil_count = len(recoil_order_list)    
    depth_count = len(depth_order_list)
    
    return recoil_count, depth_count, recoil_order_list, recoil_values, depth_order_list, depth_values

def peak_detect_diff(data):
    recoil_count = 0
    depth_count = 0
    peaks_upper = np.zeros(len(data))
    peaks_lower = np.zeros(len(data))

    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            recoil_count += 1
            peaks_upper[i] = data[i]
        if data[i] < data[i-2] and data[i] < data[i+2]:
            depth_count += 1
            peaks_lower[i] = data[i]
            
    recoil_order_list = np.where(peaks_upper != 0)[0]
    recoil_values = np.delete(peaks_upper, np.where(peaks_upper == 0))
    depth_order_list = np.where(peaks_lower != 0)[0]
    depth_values = np.delete(peaks_lower, np.where(peaks_lower == 0))
    
    return recoil_count, depth_count, recoil_order_list, recoil_values, depth_order_list, depth_values

def peak_detect_find_peaks(data, pd, window_size):#利用
    #x座標,y座標,正解率
    from scipy.signal import find_peaks_cwt, find_peaks,medfilt
    from scipy.ndimage.filters import maximum_filter
    from scipy.ndimage import maximum_filter1d
    #data = maximum_filter1d(data, 10)
    #data = medfilt(data, 35)

    data = maximum_filter(data, window_size)

    #第2返り値は使わないため、_にしている
    peaks_upper, _ = find_peaks(data, height=0)
    peaks_lower, _ = find_peaks(-data)
    #peaks_upper = find_peaks_cwt(data, np.arange(1, 40))
    #peaks_lower = find_peaks_cwt(-data, np.arange(1, 40))
    
    #recoil_order_list = peaks_upper,depth_order_list = peaks_lower
    #recoil_values = data[peaks_upper],depth_values = data[peaks_lower]
    pd.setup(peaks_upper,peaks_lower,data[peaks_upper],data[peaks_lower])

    #absは絶対値をintで返す
    #圧迫の深さとリコイルの差が1以上のとき、差がなくなるように調整する
    if abs( len(pd.recoil_order_list) - len(pd.depth_order_list)) > 1:
        pd = adjust_peak(pd, data)
    
    #upper_countとlower_count
    pd.setup_count(len(pd.recoil_order_list),len(pd.depth_order_list))
    
    return pd

# recoilとdepthの個数調整
def adjust_peak(pd, data):#利用
    if len(pd.recoil_order_list()) - len(pd.depth_order_list()) > 1:
        # recoilの方が多い場合,
        for i in  range(len(pd.recoil_order_list)):
            #リコイル2回の間に圧迫が来なかった場合
            if not pd.recoil_order_list[i] < pd.depth_order_list[i] < pd.recoil_order_list[i+1]:
                #配列の中でも最小の値を新たな圧迫とする
                min_index = i + np.argmin(data[pd.recoil_order_list[i]:pd.recoil_order_list[i+1]+1])
                
                pd.depth_order_list(np.append(pd.depth_order_list, min_index))
                pd.depth_values(np.append(pd.depth_values, data[min_index]))
                if abs(len(pd.recoil_order_list) - len(pd.depth_order_list)) <= 1:
                    break
    
    else:
        # depthの方が多い場合
        for i in  range(len(pd.depth_order_list)):
            if not pd.depth_order_list[i] < pd.recoil_order_list[i] < pd.depth_order_list[i+1]:
                max_index = i + np.argmax(data[pd.depth_order_list[i]:pd.depth_order_list[i+1]+1])

                pd.recoil_order_list(np.append(pd.recoil_order_list, max_index))
                pd.recoil_values(np.append(pd.recoil_values, data[max_index]))

                if abs(len(pd.recoil_order_list) - len(pd.depth_order_list)) <= 1:
                    break
    
    return pd
