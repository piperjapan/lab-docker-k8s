# Prep for Lab： 事前準備

当日のラボでは、Docker と Kubernetes のハンズオン環境として Google Cloud Platform（GCP）を利用します。

この手順では、当日までに実施が必要な事前準備として、次の作業を行います。

- アカウントの作成
- 管理コンソールへのログイン
- プロジェクトの作成
- 仮想マシンの作成と削除

## アカウントの作成

はじめに、[GCP のトライアルページ](https://cloud.google.com/free/)（[https://cloud.google.com/free/](https://cloud.google.com/free/)）にアクセスし、`[ 無料で開始 ]` ボタンから、表示に従って GCP の無料アカウントを作成します。

[![image](https://user-images.githubusercontent.com/2920259/118276758-f3d02a80-b502-11eb-9207-d1aa3d6815f3.png)](https://cloud.google.com/free/)

!!! note "クレジットカード"
    途中、クレジットカード情報の入力を求められます。GCP の利用にはクレジットカードの登録が必須ですが、利用者が明示的に有償プランへの変更（アップグレード）を指示しないかぎり、費用が発生することはありません。

!!! note "Google アカウント"
    GCP の利用には、Google アカウントが必要です。Google アカウントを持っていない場合は、途中の [アカウントを作成](https://accounts.google.com/) のリンクから作成したうえで作業してください。

## 管理コンソールへのログイン

GCP の管理コンソール（[https://console.cloud.google.com/](https://console.cloud.google.com/)）にアクセスし、Google アカウントでログインします。

## プロジェクトの作成

管理コンソールの上部のメニュからプロジェクト一覧を開き、`[ 新しいプロジェクト ]` で任意の名称のプロジェクトを作成します。

[![image](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)

[![image](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)

プロジェクトの作成は数分で完了します。完了したら、表示される通知の `[ プロジェクトを選択 ]` をクリックするか、上部のメニュから作成したプロジェクトに切り替えます。

[![image](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)

## 仮想マシンの作成と削除

ラボ当日の操作のイメージアップと操作感の確認を兼ねて、実際に仮想マシンの作成と削除を行います。

### 作成

プロジェクトを先ほど作成したものに切り替えた状態で、管理コンソールのメニュから `[ Compute Engine ]` > `[ VM インスタンス ]` を開きます。

[![image](https://user-images.githubusercontent.com/2920259/98776867-1dfd3e80-2433-11eb-9d1f-6553393dbffa.png)](https://user-images.githubusercontent.com/2920259/98776867-1dfd3e80-2433-11eb-9d1f-6553393dbffa.png)

!!! note "`[ 有効化する ]` ボタンが表示されたら"
    ここで **Compute Engine API** の `[ 有効化する ]` ボタンが表示されたら、`[ 有効化する ]` をクリックして、画面が切り替わるまで待ちます。数分待っても切り替わらない場合は、ブラウザのリロードを試します。

    [![image](https://user-images.githubusercontent.com/2920259/118272624-d8aeec00-b4fd-11eb-8f92-afd2cccb3980.png)](https://user-images.githubusercontent.com/2920259/118272624-d8aeec00-b4fd-11eb-8f92-afd2cccb3980.png)

`[ インスタンスを作成 ]` をクリックして、インスタンス作成画面に進みます。

[![image](https://user-images.githubusercontent.com/2920259/118276949-36920280-b503-11eb-9686-7c59682bc507.png)](https://user-images.githubusercontent.com/2920259/118276949-36920280-b503-11eb-9686-7c59682bc507.png)

作成画面では、以下の設定を変更します。

| 項目               | 値                                         |
| ------------------ | ------------------------------------------ |
| `リージョン`       | `asia-northeast1（東京）`                  |
| `シリーズ`         | `N1`                                       |
| `マシンタイプ`     | `f1-micro`                                 |
| `ブートディスク`   | `Container Optimized OS` の最新の `stable` |
| `ファイアウォール` | `HTTP トラフィックを許可する` にチェック   |

[![image](https://user-images.githubusercontent.com/2920259/98777740-a03a3280-2434-11eb-968c-645f35957da0.png)](https://user-images.githubusercontent.com/2920259/98777740-a03a3280-2434-11eb-968c-645f35957da0.png)

[![image](https://user-images.githubusercontent.com/2920259/98777625-71bc5780-2434-11eb-86c4-f15860954ad7.png)](https://user-images.githubusercontent.com/2920259/98777625-71bc5780-2434-11eb-86c4-f15860954ad7.png)

[![image](https://user-images.githubusercontent.com/2920259/98777789-b34d0280-2434-11eb-8c35-0f3a38ca10b1.png)](https://user-images.githubusercontent.com/2920259/98777789-b34d0280-2434-11eb-8c35-0f3a38ca10b1.png)

`[ 作成 ]` をクリックし、完了を待ちます。一分以上経過しても完了しない場合は、ブラウザのリロードを試します。

完了したら、`[ SSH ]` のドロップダウンメニュから `[ ブラウザウィンドウで開く ]` を選択して、別ウィンドウでターミナルが開くことを確認します。

[![image](https://user-images.githubusercontent.com/2920259/98778035-1343a900-2435-11eb-8394-f16da4253e4f.png)](https://user-images.githubusercontent.com/2920259/98778035-1343a900-2435-11eb-8394-f16da4253e4f.png)

ターミナルウィンドウで、`docker -v` を実行し、Docker が導入されていることを確認します。

[![image](https://user-images.githubusercontent.com/2920259/98778201-569e1780-2435-11eb-8f95-38996549dbc3.png)](https://user-images.githubusercontent.com/2920259/98778201-569e1780-2435-11eb-8f95-38996549dbc3.png)

ここまでで、動作確認は完了です。

作成した仮想マシンは **起動したままだと課金対象になる** ため、当日までの不必要な無料クレジットの消費を抑える目的で、続けて **仮想マシンの削除** を行います。

### 削除

GCP のコンソールで、`[ Compute Engine ]` > `[ VM インスタンス ]` を開き、作成した仮想マシンの右端の `[ ︙ ]` メニュから `[ 削除 ]` を選択します。

[![image](https://user-images.githubusercontent.com/2920259/99261013-7f704380-285f-11eb-86cb-60260a28ca54.png)](https://user-images.githubusercontent.com/2920259/99261013-7f704380-285f-11eb-86cb-60260a28ca54.png)

確認画面で再び `[ 削除 ]` をクリックすると、削除が開始されます。数分かかるので、完了を待機します。

## まとめ

当日のラボに備え、次の作業を行いました。

- アカウントの作成
- 管理コンソールへのログイン
- プロジェクトの作成
- 仮想マシンの作成と削除

これで、準備は万端です。当日を楽しみにお待ちください。

!!! note "プロジェクトは削除しない？"
    プロジェクトそれ自体は課金対象外であり、無料クレジットは消費されないため、削除はしなくても問題ありません。もちろん削除しても構いませんが、その場合は当日改めて作成する必要があります。
