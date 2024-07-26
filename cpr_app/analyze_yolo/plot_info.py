#plot_csv用
class PlotInfo():
    def __init__(self,csv_filenames):
        # これいらない？
        # 引数が単一のファイルかリストかをチェックしてリストに変換
        # やり方間違ってるかもだから要検証
        #plot_csv.pyの40行目に存在してた
        if isinstance(csv_filenames, str):
            self._x_columns = [0]
            self._y_columns = [1]
            self._x_labels = ['Time']
            self._y_labels = ["value"]
            self._title = ['Single Plot']

        else:
            self._x_columns = 0
            self._y_columns = 1
            self._x_labels = 'Time'
            self._y_labels = ['PersonID=0', 'PersonID=1']
            self._title = 'Single Plot'

    def x_columns(self):
        return self._x_columns
    def y_columns(self):
        return self._y_columns
    def x_labels(self):
        return self._x_labels
    def y_labels(self):
        return self._y_labels
    def title(self):
        return self._title

    
