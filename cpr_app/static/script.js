// static/progress.js

// サーバーから進捗状況を取得し、進捗バーとメッセージを更新する関数
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
        
        // 進捗バーの幅を更新
        document.getElementById('progress').style.width = result.progress + '%';
  
        // 処理が完了していない場合は再度チェック
        if (result.progress < 100) {
          // 1秒後に再度checkProgress関数を呼び出す
          setTimeout(() => checkProgress(filename), 1000);
        } else {
          // 処理が完了したらfinishページにリダイレクト
          window.location.href = '/finish';
        }
      }
    } catch (error) {
      // エラーが発生した場合にコンソールに表示
      console.error('エラー:', error);
    }
  }
  
  // サーバーに処理の開始を要求し、進捗状況のチェックを開始する関数
  async function startProcessing(filename) {
    try {
      // サーバーのエンドポイントにPOSTリクエストを送信
      //ここでviewspyのprogressを呼び出したい
      const response = await fetch(`/start_processing/${filename}`, {
        method: 'POST',
      });
  
      // レスポンスが成功した場合
      if (response.ok) {
        // 処理が開始されたら進捗状況のチェックを開始
        checkProgress(filename);
      }
    } catch (error) {
      // エラーが発生した場合にコンソールに表示
      console.error('エラー:', error);
    }
  }
  
  // ページが読み込まれたときに処理を開始
  document.addEventListener("DOMContentLoaded", () => {
    const filename = document.querySelector('body').getAttribute('data-filename');
    alert(filename)
    startProcessing(filename);
  });
  