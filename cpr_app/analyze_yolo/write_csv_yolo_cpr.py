from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2
from cpr_app.analyze_yolo import reconstruction_video as kari
import os
import glob
import shutil
import csv
import torch
import json

class YOLOv8Estimator:
    def __init__(self, video, csv_paths, cache_path, error_message):
        #video videoの存在するパス
        self.video = video
        #csv_paths 
        self.csv_paths = csv_paths
        self.cache_path = cache_path
        self.error_message = error_message
        print(self.csv_paths,self.cache_path)

    def estimation_algorithm(self):
        """
        YOLOv8を使用して人体パーツの推定を行い、GUI描画と結果のCSVファイルへの書き込みを行うメソッド
        """
        print("start")
        # Load a model
        model = YOLO('model/yolov8x-pose-p6.pt') 
        
        # Loop through the video images
        count = 0
        cap = cv2.VideoCapture(self.video)
        while cap.isOpened():
            # Read a image from the video
            success, image = cap.read()
            if not success and count == 0:
                print("Ignoring empty camera image.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            if success and count == 0:
                print("\n" + self.video + " processing ...\n")
            if not success:
                print("Finish\n")
                break
                
            # Run YOLOv8 inference on the image、画像をnumpyで読み込んで処理すると早くなるかも？ model.predict(np_image)
            results = model(image, verbose=False)
            #model.track(image, persist=True, half=False, conf=0.3)
            annotated_image = results[0].plot()
            
            # keypointsの整理
            conn_person_keypoints = []
            if len(results[0].keypoints) > 0:
                for person_keypoints in results[0].keypoints:
                    conn_person_keypoints.append(person_keypoints.data[0])
                    #print(conn_person_keypoints)
                conn_person_keypoints = torch.cat(conn_person_keypoints,1)
                conn_person_keypoints = conn_person_keypoints.cpu().numpy()
                #print(conn_person_keypoints)
            
            # keypointをcsvに書き込む、
                #print(self.csv_paths)
                for i in range(17):
                    self.write_results_to_csv(self.csv_paths[i], i, count, conn_person_keypoints[i])
            
            #cv2.imshow('YOLOv8 Inference', annotated_image)
            cv2.imwrite(self.cache_path + str(format(count,'06')) + '.jpg', annotated_image)
            count += 1
            #ここで100枚ごとにコメントを書いてる
            if count%100 is 0:
                print("finished",count)

            
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
                
        cap.release()
        cv2.destroyAllWindows()
        
    def write_results_to_csv(self, csv_path, i, count, keypoint):

        with open(csv_path, 'a') as f:
            writer = csv.writer(f)
            try:
                writer.writerow(keypoint)

            except AttributeError as e:
                print(e)
                writer.writerow(['None', 'None', 'None', 'None'])
                if self.error_message == 'yes':
                    print(e)
                    print(self.video + '|  frame ' + str(count) + "| " + '| keypoints ' \
                    + str(i) + '\n')
                

    #進捗バーを変更するために存在。ここに居ちゃいけないやつだからいつか引っ越す
    #def update_progress():


# テストコード (インスタンス作成とメソッド呼び出し)
if __name__ == "__main__":
    # Input and Output Path

    video_path = '/CPR-dataset/CPR_video_trimming/GroupA_trim/GoPro2/s1270037_01_Trim.MP4'
    cache_path = '/Container/cpr_app/outputs/cache/'
    output_path = '/Container/cpr_app/outputs/video/s1270037_01_Trim_yolo_v8.MP4'
    csv_paths = ['/Container/cpr_app/outputs/csv/s1270037_07_pose_0_Trim.csv', 
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_1_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_2_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_3_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_4_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_5_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_6_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_7_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_8_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_9_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_10_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_11_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_12_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_13_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_14_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_15_Trim.csv',
                '/Container/cpr_app/outputs/csv/s1270037_07_pose_16_Trim.csv']
    
    # Cacheフォルダの初期化
    shutil.rmtree(cache_path, ignore_errors=True)
    os.makedirs(cache_path, exist_ok=True)
    exe = YOLOv8Estimator(video_path, csv_paths, cache_path, 'yes')
    exe.estimation_algorithm()
    kari.make_video(cache_path, video_path, output_path)


