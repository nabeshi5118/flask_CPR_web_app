import json
class LoadJson:
    #指定した場所にあるjsomファイルを読み込む、値を返す
    def __init__(self,data):
        path_json = "cpr_app/information/"
        path = path_json + data

        with open(path,'r') as f:
            data = json.load(f)

        self._index = data
        self._path = path
    
    def load(self,word,tmp_i = None,tmp_j = None):
        if tmp_i is None:
            return self._index[word]
        elif tmp_i is not None and tmp_j is None:
            return self._index[word][tmp_i]
        else:
            return self._index[word][tmp_i][tmp_j]
    
    def index(self):
        return self._index






