import numpy as np
from .peak_data import PeakData
import copy

def cal_compare_compression(peak_recoil_count,peak_depth_count):
  # リコイルと圧迫の回数を比較して、少ない方を採用　（要修正）
  compression_count = min(peak_recoil_count, peak_depth_count)
  return compression_count


def cal_appropriate_recoil_compression(pd, upper_line, lower_line):#使った
  # 圧迫解除・深度適性率を求める
  #複製の作成

  tmp_recoil = copy.deepcopy(pd)
  tmp_compression = copy.deepcopy(pd)
  # upper_lineとlower_lineはアノテーションファイルで求める
  # upper_lineより小さいpeak_upper_valuesのインデックスをpeak_upper_indexesから消す

  appro_recoils_indexes = np.where(tmp_recoil.recoil_values <= upper_line)
  appro_recoils_indexes = np.delete(tmp_recoil.recoil_order_list, appro_recoils_indexes)
  # lower_lineより大きいpeak_lower_valuesのインデックスをpeak_lower_indexesから消す


  appro_compression_indexes = np.where(tmp_compression.depth_values > lower_line)
  appro_compression_indexes = np.delete(tmp_compression.depth_order_list, appro_compression_indexes)  
  # 適性率の計算
  appro_recoils_percent = len(appro_recoils_indexes) / len(tmp_recoil.recoil_order_list)
  appro_compression_percent = len(appro_compression_indexes) / len(tmp_compression.depth_order_list) 
  
  pd.setup_appro(appro_recoils_indexes,appro_compression_indexes,appro_recoils_percent,appro_compression_percent)


def cal_mean_tempo(peak_upper_indexes, num_person0_values,compression_count, fps,time):#使った
    # 初期化
    tempo_list_sec = np.empty_like(peak_upper_indexes, dtype=float)
    # 初期化
    tempo_list_flame = np.empty_like(peak_upper_indexes, dtype=float)


    for i, peak_upper_index in enumerate(peak_upper_indexes):
        if i == 0:
        # 最初のピーク位置の場合
            tempo_list_flame[i] = peak_upper_index
        # 一回の圧迫をフレーム単位から秒単位に変換
            tempo_list_sec[i] = fps / tempo_list_flame[i] 
        else:
            tempo_list_flame[i] = (peak_upper_index - peak_upper_indexes[i - 1])
        # フレーム数を秒単位に変換
            tempo_list_sec[i] = fps / tempo_list_flame[i] 

    if 60 % time == 0:
        mean_tempo_per_min = 60 / time * compression_count
    else:
        # 1秒あたりの平均テンポを計算
        mean_tempo_per_sec = np.sum(tempo_list_sec) / len(tempo_list_sec)
        # 1分間の平均テンポに変換
        mean_tempo_per_min = mean_tempo_per_sec * 60
    
    return mean_tempo_per_min, tempo_list_flame


def cal_appropriate_tempo(tempo_list, fps, baseline_lower_bpm=100, baseline_upper_bpm=120):#使った
    # テンポの適正率を求める
    # 初期化
    appro_tempo_flag_list = np.empty_like(tempo_list, dtype=int)

    # 適正テンポの範囲をフレーム単位で計算
    tempo_lower = 60 * fps / baseline_lower_bpm
    tempo_upper = 60 * fps / baseline_upper_bpm
    print(tempo_lower,tempo_upper)

    for i, tempo in enumerate(tempo_list):
        if tempo <= tempo_lower and tempo >= tempo_upper:
            appro_tempo_flag_list[i] = 1
        else:
            appro_tempo_flag_list[i] = 0

    appro_tempo_percent = np.sum(appro_tempo_flag_list) / len(appro_tempo_flag_list)
    return appro_tempo_percent

# def cal_mean_tempo(peak_upper_indexes, num_person0_values,fps):#使った
#   # 今後リアルタイムに適応させる
#   #初期化
#   #num_person0_valueはperson0_valueの長さ
#   tempo_list = np.empty_like(peak_upper_indexes)

#   #インデックス番号と内容を入手できる
#   #なんでここpeak_upper_indexesを使ってるの？

#   for i, peak_upper_index in enumerate(peak_upper_indexes):
#     if i == 0:
#       tempo_list[i] = num_person0_values / peak_upper_index
#     else:
#       tempo_list[i] = num_person0_values / (peak_upper_index - peak_upper_indexes[i-1])
#   mean_tempo = np.sum(tempo_list) / len(peak_upper_indexes)
#   #mean_tenpoは平均のテンポ、tempo_listはそれぞれのテンポのリスト 
#   return mean_tempo, tempo_list

#def cal_appropriate_tempo(tempo_list,time):#使った
  # # テンポの適性率を求める
  # # 初期化
  # appro_tempo_flag_list = np.empty_like(tempo_list, dtype=int)

  # tempo_lower = time * 100 // 60
  # tempo_upper = time * 120 // 60
  # for i, tempo in enumerate(tempo_list):
  #   #ここのテンポの上限下限を調整したい気持ちがある
  #   if tempo >= tempo_lower and tempo <= tempo_upper:
  #     appro_tempo_flag_list[i] = 1
  #   else:
  #     appro_tempo_flag_list[i] = 0
  # appro_tempo_percent = np.sum(appro_tempo_flag_list) / len(appro_tempo_flag_list)
  # return appro_tempo_percent
  