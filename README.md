### 如果 GPU 閒置超過3小時機器就會收回！
* 透過 `uvx nvitop` 確認目前 GPU 和 CPU 使用狀況
* 當要 run 自己的 code 時，到 ` /root/sj_Trading/keep_awake` 底下在 terminal 執行 `./termination.sh`
* `./termination.sh` 要執行兩次才會關掉所有 processes
* 當要閒置，沒有要用的時候，到同個目錄，執行 `./start.sh`

### Shioaji 環境設定
* `uv add shioaji`
