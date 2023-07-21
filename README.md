# 目的

Multiple services that would like to access data with RESTful API.

## 專案架構

- core/ 邏輯層
- data/ 存放資料，例如csv
- db/ 連資料庫的相關功能
- docs/ 專案相關的文檔
- routers/ API的分層與設計
- tests/ 測試檔案，對程式的單元測試或API測試
- config_dev.yml 專案相關設定檔
- environment.yml 專案環境資訊
- main.py 專案的入口點
- README.md
- utils.py 一些小功能

## 環境

1. 建立虛擬環境 conda env create -f environment.yml
2. 進入虛擬環境 conda activate pegatron
3. 進入專案目錄 cd hw_pegatron
3. 啟動FastAPI服務 uvicorn main:app --reload
4. 在瀏覽器中打開 http://localhost:8000/docs 可以看到 API 文件

## 結果

