# Prep for Lab： Kubernetes クラスタの作成

この手順では、後続の Kubernetes ラボで利用する Kubernetes クラスタを GCP 上に作成します。

この作業は、GCP の管理コンソール（[https://console.cloud.google.com/](https://console.cloud.google.com/)）にログインした上で行います。

## プロジェクトの作成または切り替え

プロジェクトを作成していない場合は、管理コンソールの上部のメニュからプロジェクト一覧を開き、`[ 新しいプロジェクト ]` で任意の名称のプロジェクトを作成します。

[![image](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)](https://user-images.githubusercontent.com/2920259/98776476-55b7b680-2432-11eb-931b-c09d96d858f8.png)

[![image](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)](https://user-images.githubusercontent.com/2920259/98776547-7a139300-2432-11eb-9847-75727262076f.png)

プロジェクトの作成は数分で完了します。完了したら、表示される通知の `[ プロジェクトを選択 ]` をクリックするか、上部のメニュから作成したプロジェクトに切り替えます。

[![image](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)](https://user-images.githubusercontent.com/2920259/98776725-d7a7df80-2432-11eb-86f8-56ca58101b75.png)

プロジェクトを作成済みの場合は、同様の操作で作成済みのプロジェクトに切り替えます。

## クラスタの作成

GCP のコンソールのメニュから、`[ Kubernetes Engine ]` > `[ クラスタ ]` をクリックします。

[![image](https://user-images.githubusercontent.com/2920259/99140182-b2a9ab80-2682-11eb-908d-febc94012712.png)](https://user-images.githubusercontent.com/2920259/99140182-b2a9ab80-2682-11eb-908d-febc94012712.png)

!!! note "`[ 有効化する ]` ボタンが表示されたら"
    ここで **Kubernetes Engine API** の `[ 有効化する ]` ボタンが表示されたら、`[ 有効化する ]` をクリックして、画面が切り替わるまで待ちます。数分待っても切り替わらない場合は、ブラウザのリロードを試します。

    [![image](https://user-images.githubusercontent.com/2920259/118275287-35f86c80-b501-11eb-9250-5eafc1d0de2d.png)](https://user-images.githubusercontent.com/2920259/118275287-35f86c80-b501-11eb-9250-5eafc1d0de2d.png)

**Kubernetes クラスタ** 画面で `[ 作成 ]` ボタンをクリックし、続けて `[ 標準 ]` の `[ 構成 ]` をクリックして作成画面に進みます。

[![image](https://user-images.githubusercontent.com/2920259/118276259-668cd600-b502-11eb-9689-b9de9bee69bd.png)](https://user-images.githubusercontent.com/2920259/118276259-668cd600-b502-11eb-9689-b9de9bee69bd.png)

作成画面で次の変更を加えて、最下部の `[ 作成 ]` をクリックします。

| ページ                    | 項目                     | 値                  |
| ------------------------- | ------------------------ | ------------------- |
| `クラスタの基本`          | `ゾーン`                 | `asia-northeast1-a` |
| `default-pool` > `ノード` | `シリーズ`               | `N1`                |
| `default-pool` > `ノード` | `マシンタイプ`           | `g1-small`          |
| `default-pool` > `ノード` | `ブートディスクのサイズ` | `32`                |

[![image](https://user-images.githubusercontent.com/2920259/99140420-4da38500-2685-11eb-91d4-e85bcfe6f380.png)](https://user-images.githubusercontent.com/2920259/99140420-4da38500-2685-11eb-91d4-e85bcfe6f380.png)

[![image](https://user-images.githubusercontent.com/2920259/99140441-7b88c980-2685-11eb-8297-d836f8a53f09.png)](https://user-images.githubusercontent.com/2920259/99140441-7b88c980-2685-11eb-8297-d836f8a53f09.png)

数分でクラスタの作成は完了します。数分経過しても完了しない場合は、ブラウザを更新してください。

作成されたクラスタの右端の `[ ︙ ]` メニュから `[ 接続 ]` を選択します。

[![image](https://user-images.githubusercontent.com/2920259/120878818-dd952600-c5f9-11eb-84ce-1fdab77a0607.png)](https://user-images.githubusercontent.com/2920259/120878818-dd952600-c5f9-11eb-84ce-1fdab77a0607.png)

`[ gcloud ]` から始まるコマンド文字列が表示されたことを確認し、`[ Cloud Shell で実行 ]` をクリックして、`[ 続行 ]` をクリックします。

[![image](https://user-images.githubusercontent.com/2920259/120878843-09181080-c5fa-11eb-9d35-af3943c33612.png)](https://user-images.githubusercontent.com/2920259/120878843-09181080-c5fa-11eb-9d35-af3943c33612.png)

!!! note "Google Cloud Shell"
    Google Cloud Shell は、Google Kubernetes Engine だけでなく GCP のサービス全体を操作できる汎用 Linux ホストです。GCP アカウントごとにひとつ利用でき、GCP の管理に必要なツール群があらかじめ用意されています。また、このホストに保存したデータは永続化されているため、自動で消されることはありません。

    利用は無料です。

ターミナルが起動したら、`[ gcloud ]` コマンドが入力済みの状態になっているので、そのまま `[ ENTER ]` キーで実行します。承認プロンプトは `[ 承認 ]` します。エラーが出た場合は、同じコマンドを再度実行します。

[![image](https://user-images.githubusercontent.com/2920259/99140665-146c1480-2687-11eb-8ddf-77a33df498ca.png)](https://user-images.githubusercontent.com/2920259/99140665-146c1480-2687-11eb-8ddf-77a33df498ca.png)

このコマンドは、Kubernetes を管理するコマンドである `[ kubectl ]` で今回作成したクラスタを操作できるようにするために必要な操作です。

Google Cloud Shell は、右側の `[ 新しいウィンドウで開く ]` アイコンで大きくできます。または、境界のドラッグでも領域を広げられます。

完了したら、次のコマンドがエラーなく実行できることを確認します。作成したクラスタの情報が表示されます。

```bash
kubectl cluster-info
```

[![image](https://user-images.githubusercontent.com/2920259/99140706-83e20400-2687-11eb-9ce2-991c865bb5bf.png)](https://user-images.githubusercontent.com/2920259/99140706-83e20400-2687-11eb-9ce2-991c865bb5bf.png)

この段階で、下図のように、GCP 上で Kubernetes クラスタと Google Cloud Shell が完成した状態になります。

以降、特に断りのない限り、操作はこの Google Cloud Shell で行います。

[![image](https://user-images.githubusercontent.com/2920259/99185260-f63c0c80-278b-11eb-9615-7cef5f2c8e55.png)](https://user-images.githubusercontent.com/2920259/99185260-f63c0c80-278b-11eb-9615-7cef5f2c8e55.png)
