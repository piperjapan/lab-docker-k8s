# 環境のクリーンアップ

ラボが完了したら、利用した仮想マシンや Kubernetes クラスタは削除します。

無料枠を使っている場合は、削除しなくても勝手に課金が開始されることはありませんが、残りの無料枠を無駄にしないためにも、使い終わったら削除する運用を心がけるとよいでしょう。これまでのラボで体験したとおり、必要になったらいつでも簡単に再作成できます。

## Kubernetes クラスタの削除

GCP のコンソールで、`[ Kubernetes Engine ]` > `[ クラスタ ]` を開き、作成したクラスタの右端の `[ ︙ ]` メニュから `[ 削除 ]` を選択します。

[![image](https://user-images.githubusercontent.com/2920259/120880106-3ae1a500-c603-11eb-9a78-eb85cc2c522f.png)](https://user-images.githubusercontent.com/2920259/120880106-3ae1a500-c603-11eb-9a78-eb85cc2c522f.png)

確認画面で再び `[ 削除 ]` をクリックすると、削除が開始されます。数分かかるので、完了を待機します。

## Docker 用仮想マシンの削除

GCP のコンソールで、`[ Compute Engine ]` > `[ VM インスタンス ]` を開き、作成した仮想マシンの右端の `[ ︙ ]` メニュから `[ 削除 ]` を選択します。

[![image](https://user-images.githubusercontent.com/2920259/99261013-7f704380-285f-11eb-86cb-60260a28ca54.png)](https://user-images.githubusercontent.com/2920259/99261013-7f704380-285f-11eb-86cb-60260a28ca54.png)

確認画面で再び `[ 削除 ]` をクリックすると、削除が開始されます。数分かかるので、完了を待機します。

## プロジェクトの削除

GCP のコンソールで、画面上部のプロジェクト名をクリックして、さらに `[ リソース管理 ]` アイコンをクリックします。

[![image](https://user-images.githubusercontent.com/2920259/99261487-2523b280-2860-11eb-9c4a-4df951b9e213.png)](https://user-images.githubusercontent.com/2920259/99261487-2523b280-2860-11eb-9c4a-4df951b9e213.png)

削除したいプロジェクトにチェックをいれ、上部の `[ 削除 ]` をクリックし、表示された確認画面で指示に従ってプロジェクト ID を入力してから、`[ シャットダウン ]` をクリックします。

[![image](https://user-images.githubusercontent.com/2920259/99261735-75027980-2860-11eb-88e4-e33f58024b55.png)](https://user-images.githubusercontent.com/2920259/99261735-75027980-2860-11eb-88e4-e33f58024b55.png)

数分かかるので、完了を待機します。
