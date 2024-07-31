from cpr_app import app
from flask import Flask,g, render_template, request, redirect, url_for, flash, jsonify
import os, glob
import cv2
import asyncio
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
  my_dict = {
    'insert_something1': 'views.pyのinsert_something1部分です。',
    'insert_something2': 'views.pyのinsert_something2部分です。',
    'test_titles': ['title1', 'title2', 'title3']
  }
  return render_template('cpr_app/upload.html', my_dict=my_dict)

#ファイルアップロード時の状態を確認する関数
#
@app.route('/upload', methods=['POST'])
def upload_file():
  cj = ConfigJson("cpr_app/information/input_info.json")
 #テスト用データの処理が汚いからここ直したい
  #キー名にtest_10を探している
  if "test_10" in request.form:
    print("テストデータ")
    filepath = cj.load_content("filepath_10")
    flash('アップロードが成功しました', 'success')
    return redirect(url_for('analyze', filename=cj.load_content("filename_10")))
  
  if 'file' not in request.files:
    flash('ファイルが選択されていません', 'error')
    return redirect(request.url)

  file = request.files['file']

  if file.filename == '':
    flash('ファイル名が空です', 'error')
    return redirect(request.url)

  if file and allowed_file(file.filename):
    os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
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
  #step = request.form.get('step')
  video_path = app.config['UPLOAD_FOLDER'] + '/'+ filename 
  csv_paths = process_initialize_csv(app.config['CSV_PASS'], filename)
  #キャッシュフォルダを自動で作る関数を作ろう
  cache_path = app.config['CACHE_PASS'] + '/'
  video = VideoData(video_path)
  PJ = ConfigJson(app.config['JSON_PASS']+'/progress.json')
  PJ.add_json({'message':'',"progress":0,"step":0})
  #progressの状態を保存するjsonファイル
  #print(step+"step start in views.py")
  # ステップごとに適切な処理とメッセージを設定
  PJ.add_json({"step":1})
  #if step == '1':
    #初期化
  set_csv(csv_paths)
  #jsonファイル名はconfig.json
  initialize_file()
  tmp = {'message':'姿勢推定中',"progress":100}
  PJ.add_json(tmp)
  print("finish step1")

#elif step == '2':
  if (PJ.load_content("message")=="姿勢推定中" and PJ.load_content("progress")==100):
    PJ.add_json({"step":2})
  #以下で解析を実行する
    PJ.add_json({'message':'データ解析中',"progress":0})
    exe = write_csv_yolo_cpr.YOLOv8Estimator(video_path,csv_paths,cache_path,app.config['ERROR_MESSAGE'])
    exe.estimation_algorithm(app.config['JSON_PASS']+'/progress.json',video.frame_count)
    
    PJ.add_json({"progress":100})
    print("finish step2")
    
    
#elif step == '3':
  if (PJ.load_content("message")=="データ解析中" and PJ.load_content("progress")==100):
    PJ.add_json({"step":3})
    PJ.add_json({'message':'動画作成中',"progress":0})
    #キーポイントは10番の右手首で行ってみる(要確認)
    output_name = 'output_csv.png'
    print(video.time)
    plot_csv.plot_csv_data(csv_paths,app.config['RESULT_PASS'],output_name,video.fps,video.time)
    PJ.add_json({'message':'動画作成中',"progress":100})
    print("step3")

#elif step == '4':
  if (PJ.load_content("message")=="動画作成中" and PJ.load_content("progress")==100):
    PJ.add_json({"step":4})
    PJ.add_json({'message':'解析終了',"progress":0})
    reconstruction_video.make_video(app.config['CACHE_PASS'] , app.config['RESULT_PASS'] + '/YOLOv8.MP4',video.fps)
    PJ.add_json({'message':'解析終了',"progress":100})
    print("step4")

  #else:
  #  message = '無効なステップです.'

  #ここでjson形式でresponceをjsに飛ばしている
  return jsonify(PJ.json_to_dict())

#現在の進捗を更新する
@app.route('/progress_status/<filename>', methods=['GET'])
def progress_status(filename):
    try:
        status =  ConfigJson(app.config['JSON_PASS']+'/progress.json')
        print(status.json_to_dict)
        print("進捗get中")
        return jsonify(status.json_to_dict())
    except FileNotFoundError:
        return jsonify({'progress': 0, 'message': '進捗情報が見つかりませんでした。'})



@app.route('/finish', methods=['GET'])
def finish():
  # ここで処理結果を取得するか、適切な方法で表示用のデータを用意
  
  add_tmp = {
    'message':"処理が完了しました。処理結果はここに表示されます。"
    }
  #余裕があればここを"result.json"にしたい
  CJ =  ConfigJson(app.config['JSON_PASS']+'/'+'config.json')
  CJ.add_json(add_tmp)

  return render_template('cpr_app/finish.html', result=CJ.json_to_dict())
