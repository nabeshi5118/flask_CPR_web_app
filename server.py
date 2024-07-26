from cpr_app import app

#撮影した動画を格納するパス
app.config['UPLOAD_FOLDER'] = 'cpr_app/uploads'
#許可する拡張子をまとめたもの
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
#出力をまとめたパス CSV_PASSの後ろには動画名を足す
app.config['CACHE_PASS'] = "cpr_app/outputs/cache"
app.config['CSV_PASS'] = "cpr_app/outputs/csv"

app.config['RESULT_PASS'] = "cpr_app/static/result"

app.config['JSON_PASS'] = "cpr_app/outputs/json"
app.config['ERROR_MESSAGE'] = "yes"
app.secret_key = 'hogehoge'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8080)