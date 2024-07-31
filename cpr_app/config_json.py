import json
import os
#結果出力用のjsonファイルを作成している
class ConfigJson():
    def __init__(self,json_pass):
        self._json_pass = json_pass
        #print(json_pass+ "start json")
        default = {}

        # if not os.path.exists(json_pass):
        # # 設定ファイルが存在しない場合、デフォルト設定で新しいファイルを作成
        #     with open(json_pass,'w') as f:
        #         json.dump(default,f,indent=4)
        # ファイルパスのディレクトリを確認し、存在しない場合は作成
        os.makedirs(os.path.dirname(json_pass), exist_ok=True)

        # ファイルが存在しない場合、新しいファイルを作成
        if not os.path.exists(json_pass):
            with open(json_pass, 'w') as f:
                json.dump({}, f)  # 空のJSONオブジェクトを初期化

    #既存のデータは保持され、新しいキーと内容は追加する
    #もし、既存のキー名があれば内容は変更される
    def add_json(self,add_data):
        #なんでこれが必要なのかいまいちわからない
        os.makedirs(os.path.dirname(self._json_pass), exist_ok=True)

        # ファイルが存在しない場合、新しいファイルを作成
        if not os.path.exists(self._json_pass):
            with open(self._json_pass, 'w') as f:
                json.dump({}, f)  # 空のJSONオブジェクトを初期化

        #print(self._json_pass + "add json")
        with open(self._json_pass,'r') as f:
            data = json.load(f)
        data.update(add_data)
        with open(self._json_pass,'w') as f:
            json.dump(data,f,indent=4) 

    #jsonファイルの内容物１個だけを返す
    def load_content(self,word,tmp_i=None,tmp_j=None):
        tmp_dict = dict(self._json_pass)

        if tmp_i is None:
            return tmp_dict[word]
        elif tmp_i is not None and tmp_j is None:
            return tmp_dict[word][tmp_i]
        else:
            return tmp_dict[word][tmp_i][tmp_j]

    #jsonデータを辞書にして送る
    def json_to_dict(self,json_pass = None):
        if json_pass == None:
            with open(self._json_pass, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        
        else:
            with open(json_pass, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data

#ここでしか使わない、パスから辞書を返す
def dict(json_pass ):
        with open(json_pass, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

