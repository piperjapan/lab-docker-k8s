# Docker Lab： コンテナ間通信

ここまでで、既成のコンテナイメージをひとつだけ起動させられるようになりました。しかし、実情として、多くの Web アプリケーションは、バックエンドに何らかのデータベースを必要とします。いわゆる Web サーバの機能は先ほど動かせましたが、データベースとはどのように連携させればよいでしょうか。

実はこのラボで使ってきた `p4app` も、これまでの操作では単なる静的な Web サイトなだけでしたが、本当は Redis と連携して動作します。ここからは、複数のコンテナが協調して動作できるように構成する方法を実践していきます。

## Docker の内部ネットワーク

Docker は、Docker ホスト内で独自のネットワーク空間を持っています。ここでのポイントは次の三点です。

- コンテナごとにひとつの内部 IP アドレスを持つ
- IP アドレスはコンテナの作成時に動的に払いだされる（固定できない）
- コンテナ同士は、お互いに相手の IP アドレスを知らないし、相互に名前解決もできない

このため、例えば Web アプリケーションのために Web サーバのコンテナとデータベースのコンテナを動作させたとしても、データベースのコンテナの IP アドレスを事前に把握できず、起動ごとに IP アドレスを調べて Web サーバに設定を投入するなど、支障があります。かといって、同一ホストの全コンテナが他のコンテナの名前解決ができるようになると、今度は運用中の事故やセキュリティ上の懸念が生じます。

こうした目的に対する手段として、Docker は次のような仕組みを持っています。

- Docker のネットワーク空間内に、さらに **論理的に分離されたネットワークを任意で追加できる**
- 任意のコンテナを Docker 内の **任意のネットワークに接続できる**
- 任意で追加したネットワークに接続したコンテナ同士は、**お互いにコンテナ名で名前解決できる**

ここでは、この仕組みを実際に使って、これまでつかってきたツールを Redis との二層構造で動作させます。

[![image](https://user-images.githubusercontent.com/2920259/99185496-98a8bf80-278d-11eb-8cdc-dd5cda81f114.png)](https://user-images.githubusercontent.com/2920259/99185496-98a8bf80-278d-11eb-8cdc-dd5cda81f114.png)

まずは内部ネットワークを追加（①）し、その後、そのネットワークに接続するようにコンテナを起動（②、③）させます。最後に、動作を確認（④）します。

## ネットワークの追加

Docker が管理しているネットワークは、`docker network` コマンドで操作できます。一覧は `ls` サブコマンドです。

```bash
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
2c64394b1a1a        bridge              bridge              local
cc2f27d291a9        host                host                local
4f55cea04d4a        none                null                local
```

デフォルトでは、すべてのコンテナは `bridge` ネットワークに接続され、このネットワーク内で IP アドレスが振られます。ただし、前述の通り、このネットワークでは名前解決ができません。

ここでは、次のコマンドで新しいネットワーク `p4-network` を追加し、追加できたことを確認します。

```bash
$ docker network create p4-network
49693f100706f4846765548e9bd915c6284501db2d2ba13d791f06daad139078

$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
2c64394b1a1a        bridge              bridge              local
cc2f27d291a9        host                host                local
4f55cea04d4a        none                null                local
49693f100706        p4-network          bridge              local
```

## コンテナの起動

続けて、次のコマンドで Redis が動作するコンテナを起動させます。

```bash
docker run -d --name redis --network p4-network redis:6.0
```

このコマンドの意味は次の通りです。

- `--network p4-network` で、このコンテナの接続先として `p4-network` を指定しています。
- `--name` でコンテナ名を `redis` に指定しています。この指定と前述の `--network` オプションの効果で、`p4-network` に接続しているコンテナから、ホスト名 `redis` でこのコンテナに接続できるようになります
- `-d` は前述した通り、デタッチドモードを指定するオプションです
- 起動させるコンテナイメージとして `redis:6.0` を指定しています。Redis のバージョン 6.0 が動作する、Redis が公式に提供しているコンテナイメージです。これも Docker Hub でホストされています。

この前のラボで解説した通り、`redis:6.0` は未知のコンテナイメージのため、公開レジストリである Docker Hub が検索され、プルされ、起動されます。

起動状態を確認します。ついでに、Redis のログも `docker logs` で確認します。

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
8c89a57c370f        redis:6.0           "docker-entrypoint.s…"   8 minutes ago       Up 8 minutes        6379/tcp            redis

$ docker logs redis
1:C 11 Nov 2020 14:27:38.817 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 11 Nov 2020 14:27:38.817 # Redis version=6.0.9, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 11 Nov 2020 14:27:38.818 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 11 Nov 2020 14:27:38.819 * Running mode=standalone, port=6379.
1:M 11 Nov 2020 14:27:38.820 # Server initialized
1:M 11 Nov 2020 14:27:38.820 * Ready to accept connections
```

!!! note "コンテナのログの確認"
    `docker logs` コマンドは、トラブルシュートや動作の追跡でたいへん便利なコマンドです。また、`docker logs -f` とすれば、`tail -f` のようにリアルタイムにログを確認できます。

Redis が起動できたので、Web サーバを起動します。これまで使ってきた `p4app` は、デフォルトでホスト名 `redis` に Redis クライアントとして接続を試行するように構成されています。

次のコマンドで Web サーバを起動し、GCP の管理コンソールで `[ 外部 IP ]` 欄の IP アドレスをクリックして、動作を確認します。

```bash
docker run -d --name p4app -p 80:8080 --network p4-network kurokobo/p4app:0.0.1
```

[![image](https://user-images.githubusercontent.com/2920259/98825991-7c98db80-2478-11eb-8c22-c0a0e6077cf2.png)](https://user-images.githubusercontent.com/2920259/98825991-7c98db80-2478-11eb-8c22-c0a0e6077cf2.png)

ブラウザを更新して、カウンタがインクリメントしていく動作が確認できれば、成功です！ このカウンタの値は、Redis に保存されています。

[![image](https://user-images.githubusercontent.com/2920259/98826090-a18d4e80-2478-11eb-8f72-cd7f6cc6b05c.png)](https://user-images.githubusercontent.com/2920259/98826090-a18d4e80-2478-11eb-8f72-cd7f6cc6b05c.png)

## 掃除

後続のラボに備えて掃除します。

```bash
$ docker rm -f redis p4app
redis
p4app

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

なお、ネットワーク `p4-network` はこの後も利用するため、削除せず残しておきます。

## ここまででできたこと

[![image](https://user-images.githubusercontent.com/2920259/99185496-98a8bf80-278d-11eb-8cdc-dd5cda81f114.png)](https://user-images.githubusercontent.com/2920259/99185496-98a8bf80-278d-11eb-8cdc-dd5cda81f114.png)

Docker のネットワーク空間に新しいネットワークを追加（①）し、コンテナをそこに接続させる（②、③）ことで、コンテナ名による名前解決ができるようになり、IP アドレスを意識せずに複数のコンテナが協調して動作できる状態（④）を構成できました。

この構成は、任意のコンテナ同士がコンテナ名で疎通できるようになるだけでなく、**意図しないコンテナ同士が通信してしまう事態の抑制** としても効果があります。同一の Docker ホスト内で複数のコンテナで構成されるアプリケーションを複数動作させる場合は、アプリケーションごとにネットワークを分離するような設計を考えると安全です。

!!! note "Redis コンテナに `-p` がないけれど"
    Redis コンテナの起動時、`-p` は指定していませんでしたが、Web サーバとは疎通できています。`-p` はコンテナ側のポートを **Docker ホスト自体のポートと紐づける** ためのものなので、**コンテナ同士の通信には一切関係がありません**。逆に言えば、コンテナ同士は特別な指定をしなくても相互に必要なポートで通信できます（全ポートが解放状態なわけではなく、コンテナイメージごとに通信を待ち受けるポートがあらかじめ決められてはいます）。

!!! warning "--link オプション？"
    古いドキュメントでは、コンテナ間通信の実現方式として `--link` オプションを紹介している場合がありますが、現在は非推奨扱いで、将来的に削除される可能性があるため、使わないようにしましょう。
