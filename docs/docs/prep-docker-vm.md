# Prep for Lab： Docker 用仮想マシンの用意

この手順では、後続の Docker ラボで利用する仮想マシンを GCP 上に作成します。

この作業は、GCP の管理コンソール（[https://console.cloud.google.com/](https://console.cloud.google.com/)）にログインした上で行います。

## プロジェクトの作成または切り替え

プロジェクトを作成していない場合は、管理コンソールの上部のメニュからプロジェクト一覧を開き、`[ 新しいプロジェクト ]` で任意の名称のプロジェクトを作成します。

[![image](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)

[![image](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)

プロジェクトの作成は数分で完了します。完了したら、表示される通知の `[ プロジェクトを選択 ]` をクリックするか、上部のメニュから作成したプロジェクトに切り替えます。

[![image](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)

プロジェクトを作成済みの場合は、同様の操作で作成済みのプロジェクトに切り替えます。

## 仮想マシンの作成

後続のラボでは、Docker は仮想マシン上で動作させます。ここでは、この母艦となる仮想マシンを作成します。

管理コンソールのメニュから `[ Compute Engine ]` > `[ VM インスタンス ]` を開きます。

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

!!! note "コンテナ最適化 OS"
    仮想マシンの作成の過程で選択した通り、この仮想マシンの OS は **Container-Optimized OS** で、文字通り **コンテナ** の動作に最適化されたモノです。

    具体的には、Docker があらかじめインストールされているほか、それ以外の（コンテナの動作に必要ない）モノは削ぎ落とされて軽量化・堅牢化が図られています。

    このようにコンテナの動作に最適化された OS にはいくつか種類があり、例えば RHCOS、FCOS、Photon OS、RancherOS などが該当します。

完了したら、`[ SSH ]` のドロップダウンメニュから `[ ブラウザウィンドウで開く ]` を選択して、別ウィンドウでターミナルが開くことを確認します。

[![image](https://user-images.githubusercontent.com/2920259/98778035-1343a900-2435-11eb-8394-f16da4253e4f.png)](https://user-images.githubusercontent.com/2920259/98778035-1343a900-2435-11eb-8394-f16da4253e4f.png)

ターミナルウィンドウで、`docker -v` を実行し、Docker が導入されていることを確認します。

[![image](https://user-images.githubusercontent.com/2920259/98778201-569e1780-2435-11eb-8f95-38996549dbc3.png)](https://user-images.githubusercontent.com/2920259/98778201-569e1780-2435-11eb-8f95-38996549dbc3.png)

以降、特に断りのない限り、操作はこのターミナルで行います。

!!! note "コピー & ペーストの方法"
    このターミナルウィンドウでは、

    - 文字列をドラッグして **選択** するだけでクリップボードにコピーされる
    - 貼り付ける場合は **`[Ctrl] + [V]`** （設定によっては **`[Ctrl] + [Shift] + [V]`**）を押下する

    など、便利な機能が利用できます。
