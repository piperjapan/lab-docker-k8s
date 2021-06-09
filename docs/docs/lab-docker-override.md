# Docker Lab： 設定の変更

今回使っている `p4app` は、デフォルトでホスト名 `redis` に Redis クライアントとして接続を試行するように構成されています。しかし、現実的には、Redis データベースのホスト名を常に `redis` にできるとは限りません。

一般論として、既成のコンテナイメージを **完全にデフォルトのままで** 使える例は、そこまで多くありません。何らかのデータベースと連携するツールでは、データベースのホスト名だけでなく、ユーザ名やパスワードを自分の環境に合わせて変える必要があるかもしれません。動作モードに A と B と C があり、デフォルトは A だけれど B に変更したいかもしれません。

コンテナの起動後に設定を手で変えればよいかもしれませんが、変更は永続化されないので、コンテナを削除するたびに毎回その変更を手で行う必要があります。設定ファイルのありかを突き止めて、そこだけボリュームをマウントさせれば永続化はできるかもしれませんが、そうはいってもそもそも手作業はなるべく少なくするべきです。

こうした課題に対する解決策として、ほとんどのコンテナイメージは、**環境変数で設定を変更できる** ように作られています。あるいは、別の手段として、**コンテナ内のファイルをコンテナ外のファイルで置き換える** ことで設定をコントロールできる場合もあります。

ここでは、この二パタンを簡単に実践してみましょう。

## 準備

このラボでは、`lab-docker-override` ディレクトリを利用します。

```bash
cd ~/codes/Module10/lab-docker-override
```

## 環境変数による設定の変更

[![image](https://user-images.githubusercontent.com/2920259/99256361-a1b29300-2858-11eb-9265-26576af92d66.png)](https://user-images.githubusercontent.com/2920259/99256361-a1b29300-2858-11eb-9265-26576af92d66.png)

今回使っている `p4app` では、次の項目を環境変数で制御できるようにしています。

| 環境変数   | 意味                                               | デフォルト値                           |
| ---------- | -------------------------------------------------- | -------------------------------------- |
| `APP_PORT` | `p4app` 自体の待ち受けポート                       | `8080`                                 |
| `DB_HOST`  | Redis データベースのホスト名                       | `redis`                                |
| `DB_PORT`  | Redis データベースのポート番号                     | `6379`                                 |
| `MESSAGE`  | アプリケーションのカウンタの下に表示するメッセージ | `Here I'm having fun with Containers.` |

ここでは、例として `DB_HOST` と `MESSAGE` を変更してみます。

準備として、これまでと異なるホスト名で Redis コンテナを起動させておきましょう。

```bash
docker run -d --name my-awesome-redis --network p4-network redis:6.0
```

環境変数をコンテナに与えるには、`-e` を利用します。複数の環境変数を変更したい場合、単純に列挙するだけです。

```bash
docker run -d --name p4app -p 80:8080 --network p4-network -e DB_HOST=my-awesome-redis -e MESSAGE="WATASHI HA CONTENA CHOTTO WAKARU" kurokobo/p4app:0.0.1
```

アクセスすると、無事にカウンタが表示され、メッセージが書き換わったでしょうか？

[![image](https://user-images.githubusercontent.com/2920259/99149082-42754700-26cf-11eb-9eb3-599b47b0e53b.png)](https://user-images.githubusercontent.com/2920259/99149082-42754700-26cf-11eb-9eb3-599b47b0e53b.png)

このように、同じコンテナイメージを使いながらも、環境に合わせて設定を変更できるのが、環境変数による設定変更のメリットです。コンテナイメージごとのドキュメントには、環境変数で制御できる設定が説明されている場合がほとんどです。

確認できたら、次のラボに備えて、コンテナを削除します。

```bash
docker rm -f p4app
docker rm -f my-awesome-redis
docker ps -a
```

## 設定ファイルの置き換えによる設定の変更

[![image](https://user-images.githubusercontent.com/2920259/99256912-7e3c1800-2859-11eb-810f-1c5c4f4f0fd0.png)](https://user-images.githubusercontent.com/2920259/99256912-7e3c1800-2859-11eb-810f-1c5c4f4f0fd0.png)

環境変数による設定変更に対応していない場合も、**バインドマウント** をうまく使うとコンテナ外から設定を注入できます。具体的には、**コンテナ内の設定ファイルを任意のモノに置き換えてしまう** ことで実現します。

残念ながら、`p4app` のコンテナイメージには、作りが簡単すぎて設定ファイルが含まれていませんので、単純化して **背景画像を差し替える** ことを目論みます。ここでは例として、カレントディレクトリの `img/new-bg.jpg` に差し替えてみましょう。

```bash
ls -l img
```

バインドマウントの強みは、**ファイル単位で置き換えられる** ことです。次のコマンドで、`new-bg.jpg` でコンテナ内の背景画像ファイルを置き換えます。

```bash
docker run -d --name p4app -p 80:8080 --network p4-network -v $PWD/img/new-bg.jpg:/app/static/img/bg.jpg kurokobo/p4app:0.0.1
```

アプリケーションを開いて、`[Shift] + [F5]` でスーパーリロード（ブラウザのキャッシュを利用せずに更新）してみましょう。背景が挿し変わったでしょうか？

[![image](https://user-images.githubusercontent.com/2920259/99149394-18bd1f80-26d1-11eb-9ed5-b88885175dfc.png)](https://user-images.githubusercontent.com/2920259/99149394-18bd1f80-26d1-11eb-9ed5-b88885175dfc.png)

今回は画像で実践しましたが、実際には、例えばコンテナ内の `*.conf` ファイルなどを同様の手法で事前に用意した自前のファイルに置き換えられます。環境変数での変更をサポートしていない範囲も（強引に）書き換えられるため、非常に強力です。

## クリーンアップ

次のラボに備えて、すべてのコンテナとネットワークとボリュームを削除しましょう。

```bash
docker rm -f p4app
docker network rm p4-network
docker volume prune
docker ps -a
```

!!! note "`volume prune`"
    停止中のものを含め、存在するどのコンテナからも使われていないボリュームをすべて削除するコマンドです。

## ここまででできたこと

同じコンテナイメージを使う場合でも、環境に合わせて何らかの設定変更は必要で、このラボでは実際の変更方法を二種類実践しました。

[![image](https://user-images.githubusercontent.com/2920259/99256361-a1b29300-2858-11eb-9265-26576af92d66.png)](https://user-images.githubusercontent.com/2920259/99256361-a1b29300-2858-11eb-9265-26576af92d66.png)

[![image](https://user-images.githubusercontent.com/2920259/99256912-7e3c1800-2859-11eb-810f-1c5c4f4f0fd0.png)](https://user-images.githubusercontent.com/2920259/99256912-7e3c1800-2859-11eb-810f-1c5c4f4f0fd0.png)

実際には、コンテナイメージごとのドキュメントに、具体的な変更方法（設定できる環境変数や置き換えるべきファイルのパス）が記載されている場合がほとんどです。

自分でコンテナイメージをビルドしなくても、既存のコンテナイメージをうまくカスタマイズすれば、さまざまなことが実現できます。
