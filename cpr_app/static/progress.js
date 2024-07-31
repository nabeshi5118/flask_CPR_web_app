// static/progress.js

// サーバーから進捗状況を取得し、進捗バーとメッセージを更新する関数
// step2の時に動く
async function checkProgress(filename) {

  let currentStep = 0;
      while (currentStep < 4) {
        try {
          const response = await fetch(`/progress_status/${filename}`, {
            method: 'GET'
          });
          const data = await response.json();
          console.log('message:', data.message, 'progress:', data.progress);
          document.getElementById('message').textContent = data.message;
          document.getElementById('progress').style.width = data.progress + '%';

          if (data.progress >= 100 && data.step > currentStep) {
            currentStep = data.step;
            if (currentStep === 4) {
              console.log('All tasks completed');
              return 1;
            }
          }
        } catch (error) {
          console.error('Error checking progress:', error);
          break;
        }
        await new Promise(resolve => setTimeout(resolve, 1000));  // 1秒待機
      }
}
//   try {
//     // サーバーのエンドポイントにGETリクエストを送信
//     const response = await fetch(`/progress_status/${filename}`, {
//       method: 'GET',
//     });

//     // レスポンスが成功した場合
//     if (response.ok) {
//       // JSON形式でレスポンスを取得
//       const result = await response.json();
      
//       // メッセージ要素の内容を更新
//       document.getElementById('message').textContent = result.message;
//       console.log(result.message)
//       // 進捗バーの幅を更新
//       document.getElementById('progress').style.width = result.progress + '%';
//       console.log(result.progress)

//       // 処理が完了していない場合は再度チェック
//       if (result.progress < 100) {
//         console.log("recheck")
//         // 1秒後に再度checkProgress関数を呼び出す
//         setTimeout(() => checkProgress(filename), 5000);
        
//       }
//     }
//   } catch (error) {
//     // エラーが発生した場合にコンソールに表示
//     console.error('エラー:', error);
//   }
// }

// サーバーに処理の開始を要求し、進捗状況のチェックを開始する関数
async function startProcessing(filename) {
  // サーバーのエンドポイントにPOSTリクエストを送信
  //ここでviewspyのprogressを呼び出したい
  //alarm(filename)
  // step = 1
  // const total_step = 5
  // while(step<total_step){
  finish = 0
  const response = fetch(`/progress/${filename}`, {
    method: 'POST',
      // headers: {
      //   'Content-Type': 'application/x-www-form-urlencoded',
      // },
      //body: `step=${step}`
    }
  );
    // レスポンスが成功した場合
    //if (response.ok) {
      // 処理が開始されたら進捗状況のチェックを開始
      //console.log(step);
    finish = 0
    finish = await checkProgress(filename);
    console.log("finish checkProgress")
     // step++;
    //}
  //}
  // すべての処理が完了したらfinish.htmlにリダイレクト
    if (finish == 1){
      window.location.href = '/finish';
    }
  }


// ページが読み込まれたときに処理を開始
document.addEventListener("DOMContentLoaded", () => {
  // <body>タグのdata-filename属性からファイル名を取得
  const filename = document.querySelector('body').getAttribute('data-filename');
  startProcessing(filename);
});
