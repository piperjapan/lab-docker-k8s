# Docker Compose Lab： 使ってみる

このラボでは、実際に Docker Compose を使ってみます。

[![image](https://user-images.githubusercontent.com/2920259/99257462-687b2280-285a-11eb-8571-e7c7f12676df.png)](https://user-images.githubusercontent.com/2920259/99257462-687b2280-285a-11eb-8571-e7c7f12676df.png)

事前に用意したサンプルの構成ファイル（①）を元にデプロイ（②）し、アクセスを確認（③）します。

## 準備

このラボでは、`lab-compose-deploy` ディレクトリを利用します。

```bash
cd ~/codes/Module10/lab-compose-deploy
```

## Compose ファイル

これまでの説明で **構成ファイル** と記述していたものは、Docker Compose では **Compose ファイル** と呼ばれ、通常はそのファイル名は **`docker-compose.yml`** です。

今回は、サンプルを用意しています。カレントディレクトリの `docker-compose.yml` を確認してみましょう。

```bash
cat docker-compose.yml
```

次の内容です。

```yaml
version: "3.8"

volumes:
  redis-data:

services:
  p4app:
    image: kurokobo/p4app:0.0.1
    ports:
      - 80:8080
    environment:
      DB_HOST: p4db
      MESSAGE: "Hello from Docker Compose!"

  p4db:
    image: redis:6.0
    volumes:
      - redis-data:/data
```

内容はとてもシンプルで、簡単には次の通りです。

- `version` で Compose ファイル自体のバージョンを定義しています。バージョンによって利用できる機能が変わります。
- `volumes` でボリュームの存在を定義しています。ここでは、`redis-volume` という名前のボリュームを定義しています。
- `services` でコンテナの存在を定義しています。
    - サービス名 `p4app` と `p4db` を定義し、その下でそれぞれの具体的な構成を定義しています。
    - 利用するイメージ（`image`）、コンテナ名（`container_name`）、ポート（`ports`）、環境変数（`environment`）、マウント情報（`volumes`）などです。

ネットワークの定義は含めていませんが、Compose ファイルを使って環境を起動すれば、自動でその環境専用のネットワークが作成され接続されるため、凝った構成にしない場合は書かなくても問題ありません。また、そのネットワーク内では、サービス名で相互に名前解決ができるようになります。

つまり、このすこしだけのテキストファイルに、私たちが起動したい環境のすべての情報が詰まっています。このテキストファイルは **構築手順ではなく構成情報** であり、これを見ればどのようなコンテナがどうつながり、どういうボリュームがどうマウントされ、どのような設定が入るのか、簡単に理解できます。ただのテキストファイルなので、例えば Git リポジトリなどバージョン管理の仕組みとも相性がよく、変更差分なども追いかけやすくなります。

## Docker Compose の利用

では、実際に動かしてみましょう。

### Docker Compose のインストール

Docker-Compose は、通常は公開されているバイナリをダウンロードして配置するだけで使えますが、今回ラボで使っている Docker Host は、Container Optimized OS で、ハードニングされているため、バイナリの実行に制限があります。このため、インストール方法が少々特殊ですが、ラボの本質ではないのでスクリプトを用意しています。

次のコマンドを実行します。

```bash
bash install.sh
source ~/.bashrc
docker-compose version
```

最後の `docker-compose version` でエラーなくバージョンが表示されれば成功です。

```bash
$ bash install.sh 
* Add an alias for docker-compose to the shell configuration file ...
* Pull container image for docker-compose ...
Unable to find image 'docker/compose:1.27.4' locally
1.27.4: Pulling from docker/compose
aad63a933944: Pull complete 
8f5b9cdf0f6c: Pull complete 
3ba0b1476d03: Pull complete 
6e7bc5ab5405: Pull complete 
Digest: sha256:4479af5256e02c3e7710051706a7abbcd39b0b31b0e306b2c18a0cbc88aee705
Status: Downloaded newer image for docker/compose:1.27.4
docker-compose version 1.27.4, build 4052419
docker-py version: 4.3.1
CPython version: 3.7.7
OpenSSL version: OpenSSL 1.1.1g  21 Apr 2020
* Done
* To use docker-compose, run 'source ~/.bashrc' or simply re-login

$ source ~/.bashrc

$ docker-compose version
docker-compose version 1.27.4, build 4052419
docker-py version: 4.3.1
CPython version: 3.7.7
OpenSSL version: OpenSSL 1.1.1g  21 Apr 2020
```

### 起動と確認

Docker Compose を使って環境を起動するには、`docker-compose.yml` のあるディレクトリで、次のコマンドを実行します。

```bash
ls -l
docker-compose up -d
```

`docker` コマンドとよく似ていて、`-d` はデタッチドモードを意味します。

[![image](https://user-images.githubusercontent.com/2920259/99257462-687b2280-285a-11eb-8571-e7c7f12676df.png)](https://user-images.githubusercontent.com/2920259/99257462-687b2280-285a-11eb-8571-e7c7f12676df.png)

`docker-compose` コマンドは、コマンドを実行したディレクトリの `docker-compose.yml` を探して利用します（異なるファイル名や別のディレクトリのファイルを使いたい場合は `-f` で指定できます）。従って今回は、事前に取得した `docker-compose.yml`（①）が使われました。

コマンドの出力結果からは、Compose ファイルに従って、ネットワークやボリュームやコンテナがデプロイ（②）されたことがわかります。コンテナには、Compose ファイル通りのボリュームのマウントや環境変数、ポートの設定が適用されています。

!!! note "ネットワークの記述"
    Compose ファイルにはネットワークの構成を記載しませんでした。繰り返しになりますが、Compose ファイルを使って環境を起動すれば、自動でその環境専用のネットワークが作成され接続されるため、凝った構成にしない場合は、書かなくても問題ありません。もちろん、意図的に記述しても大丈夫です。記述すれば、より複雑な構成も定義できます。

Docker Compose は、あくまで **Docker 上に Compose ファイルに従って環境を構成する** ツールのため、作られたリソースはおなじみの `docker` コマンドで確認できます。それぞれ、`<ディレクトリ名>_<リソース名>` の命名規則で作成されていることがわかります。ディレクトリ名が自動で付与されるのは、複数の Compose ファイルで複数のアプリケーションを立ち上げたときに、名前の競合を防ぐためのものです。

```bash
docker ps -a
docker volume ls
docker network ls
```

`docker-compose` コマンドでも、起動状態は確認できます。

```bash
docker-compose ps
```

ブラウザでアプリケーションの動作を確認（③）します。カウンタをインクリメントさせてみましょう。これまで通り、動作しているはずです（ブラウザのキャッシュが残っていると、背景画像が正しくない場合があります。必要に応じて `[Shift] + [F5]` でスーパーリロードしてください）。

[![image](https://user-images.githubusercontent.com/2920259/98826090-a18d4e80-2478-11eb-8f72-cd7f6cc6b05c.png)](https://user-images.githubusercontent.com/2920259/98826090-a18d4e80-2478-11eb-8f72-cd7f6cc6b05c.png)

### あるべき状態への収束

コンテナオーケストレーションの説明の中で、次のように記述しました。

> 構成ファイルを指定して実行すると、**今の状態からの差分が自動で適用** され、**あるべき状態** に自動で収束する

つまり、人間は今の状態を気にせずに `docker-compose up -d` しさえすれば、勝手に Compose ファイルに記述した状態にまでもっていってくれるということです。

これを試すため、（通常あえて行う必要はありませんが）Docker Compose で作成されたコンテナのうち一つを手動で削除し、その後、`docker-compose up -d` を再実行してみましょう。

```bash
docker rm -f lab-compose-deploy_p4app_1
docker-compose up -d
```

`docker-compose` コマンドの出力で、手で無理やり消した `p4app` だけが追加で起動されたことがわかります。このように、**いわゆる構築手順とは異なり、現状からの差分を人間が考える必要はない** 状態ができています。

### 停止と削除

次のコマンドで、環境を停止できます。

```bash
docker-compose down
```

出力から、コンテナが停止され、その後削除され、ネットワークも削除されたことがわかります。次のコマンドで、残っているリソースを確認しましょう。ボリュームだけが残っていることがわかります。

```bash
docker-compose ps
docker ps -a
docker volume ls
docker network ls
```

`docker` コマンドでは、ひとつずつていねいに停止・削除をする必要があったのに対し、Docker Compose ではひとつのコマンドできれいに掃除をしてくれます。ただし、ボリュームはデータの永続化のために利用するものなので、明示しない限り削除されることはありません。

例えば、この状態で再び起動してみます。ボリュームはすでに存在するため再利用され、データが引き継がれることになります。ブラウザでアクセスすると、元のカウンタの値が維持されているはずです。

```bash
docker-compose up -d
```

ボリュームも含めて完全に削除したい場合は、`down` に `--volumes` を追加します。これで、完全に環境を削除できます。

```bash
docker-compose down --volumes
docker-compose ps
docker ps -a
docker volume ls
docker network ls
```
