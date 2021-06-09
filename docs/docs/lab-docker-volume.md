# Docker Lab： データの永続化

ここまでで、Web サーバのコンテナとデータベースのコンテナを協調動作させられるようになりました。データベースには、無事にアクセス数が保存されるようになりました。

しかし、よく考えると、データベースのその情報は、実際にはどこに保存されているのでしょうか？ コンテナの **中** のファイルシステムは、コンテナごとに完全に論理的に分離されています。そして、コンテナを削除すると一緒に消えてしまいます。つまり、コンテナを削除した時点で、すべてのデータは失われてしまいます。

[![image](https://user-images.githubusercontent.com/2920259/99185204-baa14280-278b-11eb-8ff3-36d9a7b310b6.png)](https://user-images.githubusercontent.com/2920259/99185204-baa14280-278b-11eb-8ff3-36d9a7b310b6.png)

例えば、今回使った Redis データベースで、コンテナイメージに新しいバージョンがリリースされたとしましょう。当然、そちらに移行したくなりますが、しかし、新しいイメージを指定して `docker run` をしても、まっさらな新しいデータベースがまっさらなファイルシステムとともに起動されるだけで、古いデータは当然維持されません。他にも、日常でバックアップを取りたい場合も、対応は困難です。

こうしたとき、**ボリューム** が利用できます。ポイントは、次の二点です。

- コンテナの **中** の任意のパスに
- コンテナの **外** のファイルシステム（またはファイル）をマウントできる

ここでは実際に、Docker でよく使われるデータ永続化の方法のうち、代表的な二つを実践します。

## ボリューム

データを永続化する方法のうち、**コンテナが削除されてもデータを残しておきたい** ときに利用されるのが、**ボリューム** です。

### ボリュームの作成

ボリュームは、Docker が管理する論理的な領域です。任意で作成・削除できます。ここでは実際にボリュームを作成し、コンテナにマウントさせます。

まずは、任意の名前でボリュームを作成します。

```bash
docker volume create redis-data
docker volume ls
```

[![image](https://user-images.githubusercontent.com/2920259/99185215-c987f500-278b-11eb-83d9-70b2732c0b7b.png)](https://user-images.githubusercontent.com/2920259/99185215-c987f500-278b-11eb-83d9-70b2732c0b7b.png)

### ボリュームの利用

これでボリュームが作成されました。続けて、今回は Redis のデータをコンテナの **外** に保管したいものとして、Redis コンテナ内の `/data` にこのボリュームをマウントした状態で起動させます。

```bash
docker run -d --name redis --network p4-network -v redis-data:/data redis:6.0
```

[![image](https://user-images.githubusercontent.com/2920259/99185224-d278c680-278b-11eb-887d-5559e65c7fd4.png)](https://user-images.githubusercontent.com/2920259/99185224-d278c680-278b-11eb-887d-5559e65c7fd4.png)

!!! note "コンテナ内のどこにマウントすべき？"
    既成コンテナイメージは、ドキュメントを読むと、永続化が必要なデータのパスが記載されている場合が多いです。今回の Redis も、[Docker Hub の Redis のページ](https://hub.docker.com/_/redis) を見ると永続化が必要なデータは `/data` にあることが読み取れます。

`-v redis-data:/data` が新しいオプションです。コロンの **前** がマウントするボリュームの名前、コロンの **後** がマウント先の（コンテナ内の）パスです。

!!! note "`-v` と `--mount`"
    書き方がシンプルなため `-v` を利用しましたが、実際には最近では `--mount` が推奨されています。上記と同様のことを行う場合は、`--mount source=redis-data,target=/data` です。

この状態で、Web サーバのコンテナを起動し、GCP の管理コンソールで `[ 外部 IP ]` 欄の IP アドレスをクリックして、動作を確認します。

```bash
docker run -d --name p4app -p 80:8080 --network p4-network kurokobo/p4app:0.0.1
```

画面を何回か更新してカウンタの値を進めてから、Redis のコンテナを停止し、削除します。

```bash
docker stop redis
docker ps -a
docker rm redis
docker ps -a
```

コンテナはきれいに消えました。一方、ボリュームはコンテナとは無関係に、消されずに残っています。

```bash
docker volume ls
```

[![image](https://user-images.githubusercontent.com/2920259/99185572-0fde5380-278e-11eb-9ae1-2a5eeba54284.png)](https://user-images.githubusercontent.com/2920259/99185572-0fde5380-278e-11eb-9ae1-2a5eeba54284.png)

### データの永続化の確認

では、再び Redis のコンテナを作成します。

```bash
docker run -d --name redis --network p4-network -v redis-data:/data redis:6.0
```

ここで起動したコンテナは、完全に新しいものです。しかし、`/data` には元のボリュームをマウントしています。このため、**新しいコンテナが既存データを使って起動する** 状態になります。

[![image](https://user-images.githubusercontent.com/2920259/99185224-d278c680-278b-11eb-887d-5559e65c7fd4.png)](https://user-images.githubusercontent.com/2920259/99185224-d278c680-278b-11eb-887d-5559e65c7fd4.png)

ブラウザでアプリケーションの動作を確認すると、カウンタは、コンテナを削除する前の続きからインクリメントされることがわかります。

### ボリュームの削除

ボリュームは `rm` コマンドで削除できます。次のラボに備えて、Redis のコンテナも削除します。

```bash
docker rm -f redis
docker volume rm redis-data
```

このように、データがコンテナの削除とは無関係に残り続け、コンテナとボリュームのライフサイクルを別に管理できる状態が実現できました。

!!! note "実際はどこに？"
    ボリュームを作ったり消したりできるのはわかりましたが、具体的にどこにあるのでしょうか？ `docker volume inspect <ボリューム名>` で調査でき、デフォルトでは Docker ホストの `/var/lib/docker/volumes` 配下に作成されていることがわかります。

## バインドマウント

ボリュームを使った永続化では、Docker が管理する論理的な領域を利用しました。それに対し、バインドマウントでは、Docker ホストの具体的なパスをコンテナ内にマウントします。

### バインドマウントを使った起動

例えば、Docker ホストのカレントディレクトリ直下の `redis` ディレクトリを、Redis コンテナの `/data` にマウントする場合は、次のコマンドを実行します。

```bash
docker run -d --name redis --network p4-network -v $PWD/redis:/data redis:6.0
ls -l
```

[![image](https://user-images.githubusercontent.com/2920259/99185237-db699800-278b-11eb-959a-3ab323eb2f6b.png)](https://user-images.githubusercontent.com/2920259/99185237-db699800-278b-11eb-959a-3ab323eb2f6b.png)

`-v` で、マウント元とマウント先をコロンで並べて与えています。Docker ホスト側のパスはフルパスである必要があるため、カレントディレクトリが保存されている変数 `$PWD` を使ってフルパスを表しています（結果的にフルパスになればよいので、`$(pwd)/redis` などでも同様です）。

!!! note "`-v` と `--mount`"
    ここでも先ほどと同様に `--mount source=$PWD/redis,target=/data` とすれば `--mount` で `-v` を代替できます。

実行すると、カレントディレクトリに `redis` ディレクトリが作成されていることがわかります。

### 保存されたデータの確認

この状態で、アプリケーションにアクセスしてカウンタをインクリメントさせ、Redis コンテナを停止・削除してみます。

```bash
docker stop redis
docker ps -a
docker rm redis
docker ps -a
```

この後、`redis` ディレクトリの中身を見ると、`dump.rdb` が存在していることがわかります。これは、インメモリデータベースである Redis が、終了処理（`stop` コマンドの実行時）中に自身で保持しているデータを出力したものです。

```bash
$ ls -l redis
total 4
-rw-r--r-- 1 999 999 108 Nov 14 13:24 dump.rdb
```

[![image](https://user-images.githubusercontent.com/2920259/99185242-e3c1d300-278b-11eb-9467-e0bd8299d28c.png)](https://user-images.githubusercontent.com/2920259/99185242-e3c1d300-278b-11eb-9467-e0bd8299d28c.png)

### データの永続化の確認

Redis は、起動時に `dump.rdb` があると、その中身を自動的にインポートします。新しい Redis コンテナの `/data` にこのパスをマウントすれば、データベースの中身が元通りになるということです。

```bash
docker run -d --name redis --network p4-network -v $PWD/redis:/data redis:6.0
```

[![image](https://user-images.githubusercontent.com/2920259/99185237-db699800-278b-11eb-959a-3ab323eb2f6b.png)](https://user-images.githubusercontent.com/2920259/99185237-db699800-278b-11eb-959a-3ab323eb2f6b.png)

アプリケーションにアクセスすると、カウンタが途中から始まることがわかります。

最後に、次のラボに備えて、コンテナを削除します。

```bash
docker rm -f p4app
docker rm -f redis
docker ps -a
sudo rm -rf redis
```

## ここまででできたこと

コンテナ内のファイルシステムの一部を、コンテナの **外** に持ってきて、データを永続化させる手段を学習しました。

バインドマウントは、コンテナの中と外で同じファイルにアクセスしたい場合に便利です。バックアップなどの用途でも使えるほか、逆に、例えば開発中のソースコードをコンテナの中に持ち込みたい（Docker ホスト側で行った変更を即座にコンテナ内でも利用できるようにしたい）場合にも使えます。

一方、コンテナ内にあるべきファイルが、比較的容易にアクセスできる場所に露出してしまうとも言えます。このため、バインドマウントでなければならない強い理由がない場合は、**ボリュームの利用が推奨** されています。
