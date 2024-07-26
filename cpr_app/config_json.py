import json
import os
#結果出力用のjsonファイルを作成している
class ConfigJson():
    def __init__(self,json_pass):
        self._json_pass = json_pass
        default = {}

        if not os.path.exists(json_pass):
        # 設定ファイルが存在しない場合、デフォルト設定で新しいファイルを作成
            with open(json_pass,'w') as f:
                json.dump(default,f,indent=4)

    
    def add_json(self,add_data):
        with open(self._json_pass,'r') as f:
            data = json.load(f)
        data.update(add_data)
        with open(self._json_pass,'w') as f:
            json.dump(data,f,indent=4)

    def json_to_dict(self):
        with open(self._json_pass, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
        
