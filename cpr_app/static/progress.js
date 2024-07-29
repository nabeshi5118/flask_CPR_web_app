// static/progress.js

// サーバーから進捗状況を取得し、進捗バーとメッセージを更新する関数
// step2の時に動く
async function checkProgress(filename) {
  try {
    // サーバーのエンドポイントにGETリクエストを送信
    const response = await fetch(`/progress_status/${filename}`, {
      method: 'GET',
    });

    // レスポンスが成功した場合
    if (response.ok) {
      // JSON形式でレスポンスを取得
      const result = await response.json();
      
      // メッセージ要素の内容を更新
      document.getElementById('message').textContent = result.message;
      console.log(result.message)
      // 進捗バーの幅を更新
      document.getElementById('progress').style.width = result.progress + '%';
      console.log(result.progress)

      // 処理が完了していない場合は再度チェック
      if (result.progress < 100) {
        console.log("recheck")
        // 1秒後に再度checkProgress関数を呼び出す
        setTimeout(() => checkProgress(filename), 1000);
        
      }
    }
  } catch (error) {
    // エラーが発生した場合にコンソールに表示
    console.error('エラー:', error);
  }
}

// サーバーに処理の開始を要求し、進捗状況のチェックを開始する関数
async function startProcessing(filename) {
  // サーバーのエンドポイントにPOSTリクエストを送信
  //ここでviewspyのprogressを呼び出したい
  //alarm(filename)
  const steps = [1,2,3,4];
  for(const step of steps){
    const response = await fetch(`/progress/${filename}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `step=${step}`
    }
    );
    // レスポンスが成功した場合
    if (response.ok) {
      // 処理が開始されたら進捗状況のチェックを開始
      checkProgress(filename);
    }
  }
  // すべての処理が完了したらfinish.htmlにリダイレクト
  window.location.href = '/finish';
}

// ページが読み込まれたときに処理を開始
document.addEventListener("DOMContentLoaded", () => {
  // <body>タグのdata-filename属性からファイル名を取得
  const filename = document.querySelector('body').getAttribute('data-filename');
  startProcessing(filename);
});
