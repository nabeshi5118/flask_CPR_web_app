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

@app.before_request
def before_request():
  #g.my_object = PeakDataOutput()
  print("peak before")

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
    #ファイル名に規則性をもたせる場合以下を利用
    #name = change_filename()
    #filepath = os.path.join(app.config['UPLOAD_FOLDER'],name)
    #file.save(filepath)
    #flash('アップロードが成功しました', 'success')
    #return redirect(url_for('analyze',filename = name))
  else:
    flash('許可されていないファイル形式です', 'error')
    return redirect(request.url)

@app.route('/analyze/<filename>')
def analyze(filename):
  return render_template('cpr_app/analyze.html', filename=filename)

@app.route('/progress/<filename>', methods=['POST'])
def progress(filename):
  step = request.form.get('step')
  video_path = app.config['UPLOAD_FOLDER'] + '/'+ filename 
  csv_paths = process_initialize_csv(app.config['CSV_PASS'], filename)
  #キャッシュフォルダを自動で作る関数を作ろう
  cache_path = app.config['CACHE_PASS'] + '/'
  video = VideoData(video_path)

  # ステップごとに適切な処理とメッセージを設定
  if step == '1':
    #初期化
    set_csv(csv_paths)
    #jsonファイル名はconfig.json
    initialize_file()
    message = '姿勢推定中'
    print("step1")

  elif step == '2':
    #以下で解析を実行する
    exe = write_csv_yolo_cpr.YOLOv8Estimator(video_path,csv_paths,cache_path,app.config['ERROR_MESSAGE'])
    exe.estimation_algorithm()
    
    message = 'データ解析中'
    print("step2")
    
    
  elif step == '3':
    #キーポイントは10番の右手首で行ってみる(要確認)
    output_name = 'output_csv.png'
    print(video.time)
    plot_csv.plot_csv_data(csv_paths,app.config['RESULT_PASS'],output_name,video.fps,video.time)
    message = '動画作成中'
    print("step3")
  
  elif step == '4':
    reconstruction_video.make_video(app.config['CACHE_PASS'] , app.config['RESULT_PASS'] + '/YOLOv8.MP4',video.fps)
    message = '解析終了'
    print("step4")

  else:
    message = '無効なステップです.'

  return jsonify({'message': message})

@app.route('/finish', methods=['GET'])
def finish():
  # ここで処理結果を取得するか、適切な方法で表示用のデータを用意

  add_tmp = {
    'message':"処理が完了しました。処理結果はここに表示されます。"
    }
  CJ =  ConfigJson(app.config['JSON_PASS']+'/'+'config.json')
  CJ.add_json(add_tmp)

  return render_template('cpr_app/finish.html', result=CJ.json_to_dict())
