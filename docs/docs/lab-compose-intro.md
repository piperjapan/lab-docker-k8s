# Docker Compose Lab： はじめに

このラボでは、複数のコンテナを Docker Compose でまとめてデプロイする方法を学習します。

## このラボの目的と概要

このラボでは、

- **コンテナオーケストレーションの考え方** に触れてみる
- Compose ファイルを扱えるようになる

ことを目的に、以下のトピックを取り扱います。

- Compose ファイルの内容の理解
- Docker Compose を用いたコンテナの起動と停止
- 『あるべき状態』の概念と動作の確認

## 準備

### 仮想マシンの作成

このラボでは、GCP 上の仮想マシンインスタンスで Docker を動作させます。Docker 用の仮想マシンを作成していない場合は、次の手順を実行します。

- [📖 **Prep for Lab： Docker 用仮想マシンの用意**](prep-docker-vm.md)

### リソースの取得

また、ラボで利用するリソースは GitHub 上のリポジトリで公開されています。用意した Docker 用仮想マシン上に次のコマンドで必要なリソースをクローンします。

```bash
cd ~
git clone https://github.com/piperjapan/codes.git
```

## コンテナのオーケストレーション

前のラボでは、Docker でコンテナを起動させたり、複数のコンテナを連携させたり、データを永続化したりする方法を学習しました。

しかし振り返ると、例えば、

- `p4app` と `redis` を起動する
- `p4app` は `redis` に接続できる
- `p4app` は環境変数で設定を変更する
- `redis` はデータを永続化する

ということをやりたいだけでも、起動するためには、

```bash
docker network create p4-network
docker volume create redis-data

docker run -d --name my-awesome-redis --network p4-network -v redis-data:/data redis:6.0
docker run -d --name p4app -p 80:8080 --network p4-network -e DB_HOST=my-awesome-redis kurokobo/p4app:0.0.1
```

など、いくつものコマンドと、それらのオプションを正確に記述する必要があります。また、停止・削除でも、

```bash
docker stop p4app
docker rm p4app

docker stop my-awesome-redis
docker rm my-awesome-redis

docker network rm p4-network
docker volume rm redis-data
```

が必要です。

仮想マシンを手作りしていた頃に比べれば、これでも楽ではありますが、ここには、次のような問題があります。

- 最終的にできあがる構成が、別に設計書などがないと読み取れない
- コンテナの数が増えたら、手作業では破綻する
- 作業開始時点の状態に応じて、一部のコマンドの要否や順番が変わる可能性があり、都度判断が必要である

こうした課題は、**コンテナオーケストレーション** の技術で解決できます。一般に、次のような特徴を持ちます。

- **最終的になっていてほしい構成** を **あらかじめすべて構成ファイルに記述** する
- 構成ファイルを指定して実行すると、**今の状態からの差分が自動で適用** され、**あるべき状態** に自動で収束する
- 構成ファイルにテキスト情報ですべての構成が記述されているので、**それ自体が構成管理に利用でき**、**変更管理も容易** である

## Docker Compose

コンテナオーケストレーションの実装にはいくつかありますが、このラボでは Docker Compose を取り扱います。

Docker Compose は、単一の Docker ホスト内でのオーケストレーションではデファクトスタンダードであり、多くのツールがそのドキュメント内で Docker Compose で動作させる場合の構成ファイル（後述しますが **Compose ファイル**）の例を載せています。また、そもそも公式の起動手順が Docker Compose 前提である例も増えています。
