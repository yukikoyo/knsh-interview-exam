# 康軒面試測驗 **李承桓**
## 展示用網址
https://knsh.lch.tw/exam

## 架構說明
前後端皆使用Flask架設，並封裝為Docker容器，透過Github Actions自動部署到Azure App Service。

## 題目1 發音評定
本題目中，我使用了Azure內的Speech API，由前端選擇題目及錄音後，傳送至後端轉送至Azure Speech API進行辨識，並將回傳後的結果傳回前端網頁，透過javascript處理顯示給使用者的內容。
顯示的內容包含：
- 評分結果(依照綜合分數，高於80分為及格)
- 綜合分數 (依據精確度、流暢度、完整性評分)
- 精確度
- 流暢度
- 完整性
- 發音有問題的單詞

## 題目2 文字辨識
本題目中，我使用了Azure內的Vision API，由前端上傳檔案後，傳送至後端轉送至Azure Vision AI進行辨識，並設定僅回傳文字後，就回傳的文字以及座標對圖片進行處理，將圖片文字範圍以方框標示後加上標記點，傳回前端，並在前端以圖片及文字的方式展示辨識結果。

![image](https://github.com/user-attachments/assets/ff500c0a-4a64-4117-8129-71e66b098366)
