from cpr_app import app
from flask import Flask,g, render_template, request, redirect, url_for, flash, jsonify
import os, glob
import cv2
import asyncio
import shutil
from .analyze_yolo import write_csv_yolo_cpr
from .analyze_yolo import plot_csv
from .analyze_yolo import reconstruction_video
from .config_json import ConfigJson
from .config_csv import process_initialize_csv,set_csv

from .video_data import VideoData

#allowed_extensionsにある有効な拡張子を持つ場合にTrueを返す
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def initialize_file():
  for file in glob.glob('cpr_app/outputs/**/*', recursive=True):
    try :
      os.remove(file)
    except IsADirectoryError :
      print()

# @app.before_request
# def before_request():
#   #g.my_object = PeakDataOutput()
#   print("peak before")

#最初に飛ぶ所
@app.route('/')
def index():
  my_dict = {}
  initialize_file()
  print("Now route(/)")
  cj = ConfigJson(app.config['JSON_PROGRESS'])
  cj.add_json({'message':'',"progress":0,"step":0})
  # my_dict = {
  #   'insert_something1': 'views.pyのinsert_something1部分です。',
  #   'insert_something2': 'views.pyのinsert_something2部分です。',
  #   'test_titles': ['title1', 'title2', 'title3']
  # }
  return render_template('cpr_app/upload.html', my_dict=my_dict)

#ファイルアップロード時の状態を確認する関数
#
@app.route('/upload', methods=['POST'])
def upload_file():
  II = ConfigJson(app.config['INPUT_INFO'])
 #テスト用データの処理が汚いからここ直したい
  #キー名にtest_10を探している
  if II.load_content("name") in request.form:
    print("テストデータ")
    Filepath = II.load_content("filepath_10")
    Filename = II.load_content("filename_10")
    print(Filepath)
    print(Filename)
    shutil.copy(Filepath,app.config['UPLOAD_FOLDER'])
    flash('アップロードが成功しました', 'success')
    return redirect(url_for('analyze', filename=Filename))
  
  if 'file' not in request.files:
    flash('ファイルが選択されていません', 'error')
    return redirect(request.url)

  file = request.files['file']

  if file.filename == '':
    flash('ファイル名が空です', 'error')
    return redirect(request.url)

  if file and allowed_file(file.filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    flash('アップロードが成功しました', 'success')
    return redirect(url_for('analyze', filename=file.filename))
  else:
    flash('許可されていないファイル形式です', 'error')
    return redirect(request.url)

@app.route('/analyze/<filename>')
def analyze(filename):
  return render_template('cpr_app/analyze.html', filename=filename)

@app.route('/progress/<filename>', methods=['POST'])
def progress(filename):
  #progressの状態を保存するjsonファイル
  JP = ConfigJson(app.config['JSON_PROGRESS'])
  OI = ConfigJson(app.config['OUTPUT_INFO'])
  JR = ConfigJson(app.config['JSON_RESULT'])

  video_path = app.config['UPLOAD_FOLDER'] + '/'+ filename 
  print(video_path)
  cache_path = app.config['CACHE_PASS'] + '/'
  csv_paths = process_initialize_csv(app.config['CSV_PASS'], filename,app.config['YOLO_INFO'])
  video = VideoData(video_path)
  output_video = app.config['RESULT_PASS'] + '/'+ OI.load_content("video")

  print(output_video)
  print("outputあああ")


  #実際には、姿勢推定しつつ、csvに書き込んでいる
  JP.add_json({'message':'姿勢推定中',"progress":0,"step":1})
  exe = write_csv_yolo_cpr.YOLOv8Estimator(video_path,csv_paths,cache_path,app.config['ERROR_MESSAGE'])
  exe.estimation_algorithm(app.config['JSON_PROGRESS'],video.frame_count)
  JP.add_json({"progress":100})
  print("finish step1")


  JP.add_json({'message':'データ解析中',"progress":0,"step":2})
  #ここに本来データ解析(plot_csv.pyの前半部分)が入るはず
  JP.add_json({"progress":100})
  print("finish step2")
    

  JP.add_json({"message":"グラフ作成中","progress":0,"step":3})
  #キーポイントは10番の右手首で行ってみる(要確認)
  print(video.time)
  plot_csv.plot_csv_data(csv_paths,video.fps,video.time,app.config['RESULT_PASS'],OI.load_content("csv"))
  JP.add_json({"progress":100})
  print("finish step3")


  JP.add_json({'message':'動画作成中',"progress":0,"step":4})
  reconstruction_video.make_video(app.config['CACHE_PASS'] , output_video ,video.fps)
  JP.add_json({"progress":100})
  print("finish step4")

  #ここでjson形式でresponceをjsに飛ばしている
  return jsonify(JP.json_to_dict())

#現在の進捗を更新する
@app.route('/progress_status/<filename>', methods=['GET'])
def progress_status(filename):
    try:
        status =  ConfigJson(app.config['JSON_PROGRESS'])
        print(status.json_to_dict)
        print("進捗get中")
        return jsonify(status.json_to_dict())
    except FileNotFoundError:
        return jsonify({'progress': 0, 'message': '進捗情報が見つかりませんでした。'})



@app.route('/finish', methods=['GET'])
def finish():
  # ここで処理結果を取得するか、適切な方法で表示用のデータを用意
  print("finish来たよ")
  add_tmp = {
    'message':"処理が完了しました。処理結果はここに表示されます。"
    }
  #余裕があればここを"result.json"にしたい
  CJ =  ConfigJson(app.config['JSON_RESULT'])
  CJ.add_json(add_tmp)

  return render_template('cpr_app/finish.html', result=CJ.json_to_dict())
