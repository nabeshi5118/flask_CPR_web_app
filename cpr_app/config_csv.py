#Yoloのキーポイントの数だけcsvファイルを作成している
import os
from .config_json import ConfigJson

def process_initialize_csv(tmp_paths, video):
        #パーツごとにCSVフォルダ生成&ファイルを初期化する
        #cpr_app/output/csv/video名
        #video名はyear_month_day_hour_min
        #ファイル名はキー番号だけ

    #yoloに対応したディレクトリを作成している
    csv_paths = []
    CJ = ConfigJson("cpr_app/information/yolo_info.json")
    landmark = CJ.load_content("landmark")
    num_landmarks = range(landmark)

    #動画名のディレクトリを作成するために動画の拡張子を取り除いてる
    temporary_video = os.path.splitext(video)[0]

    for i in num_landmarks:
          #os.path.joinは2つのパスをくっつけれる
        csv_folder = os.path.join(tmp_paths, temporary_video)
        os.makedirs(csv_folder, exist_ok=True)
        #キーポイント毎にcsvファイルを作成
        csv_file_path = os.path.join(csv_folder, f'{i}.csv')
            #パスの合成
        csv_paths.append(csv_file_path)
        
    return csv_paths

def set_csv(csv_file_paths):
    for i,csv_filename in enumerate(csv_file_paths):
        with open(csv_filename, 'w') as f:
        #ファイル内の初期化
            f.truncate(0)

