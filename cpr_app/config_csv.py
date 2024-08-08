#Yoloのキーポイントの数だけcsvファイルを作成している
import os
from .config_json import ConfigJson

def process_initialize_csv(tmp_paths, video,data_path = None):
    #パーツごとにCSVフォルダ生成&ファイルを初期化する
    #cpr_app/output/csv/video名
    #video名はyear_month_day_hour_min
    #ファイル名はキー番号だけ
    #YOLO以外は、videoに数字を入れればその数だけtmp_paths以下に指定した数だけcsvファイルを作成する
    csv_paths = []
    if(data_path!=None):
        print("CP")
    #yoloに対応したディレクトリを作成している
        CJ = ConfigJson(data_path)
        landmark = CJ.load("landmark")
        num_landmarks = range(landmark)
        #動画名のディレクトリを作成するために動画の拡張子を取り除いてる
        temporary_video = os.path.splitext(video)[0]

    elif(isinstance(video,int)):
        temporary_video = ""
        num_landmarks = video 

    for i in num_landmarks:
          #os.path.joinは2つのパスをくっつけれる
        csv_folder = os.path.join(tmp_paths, temporary_video)
        os.makedirs(csv_folder, exist_ok=True)
        #キーポイント毎にcsvファイルを作成
        csv_file_path = os.path.join(csv_folder, f'{i}.csv')
            #パスの合成
        csv_paths.append(csv_file_path)

    set_csv(csv_paths)    
    return csv_paths

def set_csv(csv_file_paths):
    for i,csv_filename in enumerate(csv_file_paths):
        with open(csv_filename, 'w') as f:
        #ファイル内の初期化
            f.truncate(0)

