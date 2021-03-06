# Docker Lab： イメージのビルド

このラボでは、コンテナの **開発者** 側の立場で、自前のコンテナイメージを作成して使ってみます。

## 準備

このラボでは、`lab-docker-build` ディレクトリを利用します。

```bash
cd ~/lab-docker-k8s/lab-docker-build
```

## コンテナイメージを自製するメリット

コンテナの起動には、元になる **コンテナイメージ** が必要でした。これまでのラボでも、`p4app` や
 `redis` など、いくつかのコンテナイメージを実際に動かしてきました。

このようなコンテナイメージは、比較的簡単に **自分で作成** できます。コンテナイメージを自分で作れるようになると、

- 自分で開発したアプリケーションをコンテナとして動かせるようになる（Docker だけでなく Kubernetes や Heroku でも動かせる）
- コンテナレジストリに登録・公開することで、世界中から利用できる
- 公開されているイメージを自分の手でカスタマイズできる

など、さまざまなメリットが得られます。

## Dockerfile とその内容

コンテナイメージの作成になくてはならないファイルが、`Dockerfile` です。前のラボで利用した `p4app` の実際の Dockerfile が、カレントディレクトリにあるはずです。

```bash
ls -l Dockerfile
cat Dockerfile
```

中身はこのようになっています。

```docker
FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py"]
```

Dockerfile には、コンテナイメージそれ自体の定義が含まれています。基本的な考え方は、

- 最初にベースになるコンテナイメージ（`FROM`）を宣言し
- 後続の行で、ベースイメージに対する変更を記述する

です。雑に言えば、（あまり正確な表現ではないですが）コンテナイメージの構築手順が書いてあるようなものです。

この例では、ベースイメージとして `python:3.9-slim` を指定しています。これは Docker が提供する公式コンテナイメージのひとつで、Python の動作に一般に必要とされる要素があらかじめ含まれています。このベースイメージは、前のラボの `docker run` のときにそうだったように、レジストリホスト名やリポジトリ名を明示しない場合は Docker Hub から取得されます。

`WORKDIR` では、コンテナ内でのワーキングディレクトリを指定しています。このディレクトリが存在していない場合は作成されます。`ADD` では、Dockerfile のあるホスト側のカレントディレクトリ（`.`）の全ファイルを、コンテナ内の `/app` にコピーさせています。

その後、`RUN` で `pip install` を実行し、必要なモジュール（`requirements.txt` に記載）をインストールさせています。`requirements.txt` は、前の `ADD` で `/app` にコピーされており、`WORKDIR` でワーキングディレクトリが `/app` に設定されているため、相対パスで指定できているわけです。

その後、このコンテナイメージがデフォルトで公開するポートを `EXPOSE` で定義し、最後にコンテナイメージが起動された場合に実行されるコマンドを `ENTRYPOINT` と `CMD` で定義しています。

結果、このコンテナイメージが起動されると、`ENTRYPOINT` と `CMD` を合わせて `python app.py` が実行され、Web サーバが起動することになります。

## はじめてのビルド

次のコマンドで、はじめての自分のコンテナをビルドしてみましょう。末尾の `.` を忘れないでください。この `.` で、カレントディレクトリから Dockerfile が探されてビルドが実行されます。

```bash
docker build -t my-first-container:0.0.1 .
```

[![image](https://user-images.githubusercontent.com/2920259/123530682-3ad35180-d738-11eb-821a-94b16c94ef95.png)](https://user-images.githubusercontent.com/2920259/123530682-3ad35180-d738-11eb-821a-94b16c94ef95.png)

`-t` で、ビルドするコンテナイメージの名称とタグを指定します。詳しくは後述しますが、現段階では、`<イメージ名>:<バージョン>` と捉えてください。

コマンドでは、カレントディレクトリの Dockerfile からのビルド（①）を指示しました。ビルドの過程では、`FROM` で指定されたベースイメージがまずプル（②）され、それを元（③）に `ADD` などでファイルや起動時のコマンドの定義などが封入（④）されます。

できあがったコンテナイメージは、`images` コマンドで確認できます。

```bash
docker images
```

## ビルドしたイメージの起動

イメージができてしまえば、あとは前のラボと何ら変わりはありません。`docker run` で自分のイメージを指定すれば起動します。

```bash
docker run -d --name my-first-container -p 80:8080 my-first-container:0.0.1
```

アプリケーションを開けることを確認します。背景画像が前のラボのままの場合は、`[Shift] + [F5]` でスーパーリロード（ブラウザのキャッシュを利用せずに更新）してみましょう。

[![image](https://user-images.githubusercontent.com/2920259/98807222-ad1f4c00-245d-11eb-8537-4f9815477fbd.png)](https://user-images.githubusercontent.com/2920259/98807222-ad1f4c00-245d-11eb-8537-4f9815477fbd.png)

確認できたら、コンテナを削除します。

```bash
docker rm -f my-first-container
docker ps -a
```

## 少しだけカスタマイズ

前のラボとまったく同じ見た目なので、自分ならではのコンテナイメージにカスタマイズしてみましょう。

例えば、背景画像 `static/img/bg.jpg` を、インタネットからダウンロードできる任意の JPEG ファイルに置き換えてみます。

```bash
curl -o static/img/bg.jpg https://user-images.githubusercontent.com/2920259/99150875-c7199280-26da-11eb-847b-fd398c46e69a.jpg
```

あるいは、アプリケーションの本体である `app.py` にすこし変更を加えてみます。28 行目の `Hello, World.` を好きな文字列に修正してみましょう。

```bash
vi app.py
```

できあがったら、再びビルドしてみます。同じタグでもよいですし、バージョンを一つ上げてもよいでしょう。

```bash
docker build -t my-first-container:0.0.2 .
docker images
```

イメージができたら、起動させてみます。

```bash
docker run -d --name my-first-container -p 80:8080 my-first-container:0.0.2
```

背景やメッセージがうまく書き換わったでしょうか？ できていれば、成功です！ 背景画像が変わっていない場合は、`[Shift] + [F5]` でスーパーリロードを試してください。

[![image](https://user-images.githubusercontent.com/2920259/99151150-8e7ab880-26dc-11eb-9511-0439a02d3e91.png)](https://user-images.githubusercontent.com/2920259/99151150-8e7ab880-26dc-11eb-9511-0439a02d3e91.png)

## クリーンアップ

次のラボに備えて、すべてのコンテナを削除しましょう。ネットワークとボリュームも、残っている場合は削除します。

```bash
docker rm -f my-first-container
docker ps -a
docker network rm p4-network
docker network ls
docker volume prune
docker volume ls
```

!!! note "`volume prune`"
    停止中のものを含め、存在するどのコンテナからも使われていないボリュームをすべて削除するコマンドです。

ローカルに保存されているイメージは、`rmi` コマンドで削除できます。

```bash
docker rmi my-first-container:0.0.1
docker rmi my-first-container:0.0.2
docker images
```

## ここまででできたこと

[![image](https://user-images.githubusercontent.com/2920259/123530682-3ad35180-d738-11eb-821a-94b16c94ef95.png)](https://user-images.githubusercontent.com/2920259/123530682-3ad35180-d738-11eb-821a-94b16c94ef95.png)

コマンドで、カレントディレクトリの Dockerfile からのビルド（①）を指示できました。Dockerfile を目的に応じて記述することで、`FROM` で指定されたベースイメージを元（②、③）に、任意のファイルや設定を封入（④）できることを学習しました。。

さらに、作成したコンテナイメージをレジストリに登録すると、世界のどこからでもプルできるようになり、利用の幅が非常に広がります。

## コンテナイメージの公開（参考）

!!! tip "実施不要"
    このセクションは、参考として紹介しています。**手順の実施は不要** です。

できあがったイメージは、コンテナレジストリにプッシュすることで、世界中のどこからでも利用できるようになります。他人に使ってもらうだけでなく、自分がほかの Docker ホストや Kubernetes からも利用できるようにもなり、非常に便利です。

!!! warning "機微情報やライセンスに注意"
    パブリックなコンテナレジストリに登録したイメージは、ほんとうに世界中のだれからでもアクセスできるようになります。コンテナイメージに含めるファイルにだいじなパスワードなどを埋め込まないようにするほか、著作権やライセンスに注意するなど、配慮すべき点に気を付けましょう。

コンテナレジストリにもいくつものサービスがあり、これまでのラボでも Docker 公式の Docker Hub（`docker.io`）や GitHub が提供する GitHub Container Registry（`ghcr.io`）を実際に利用していました。これ以外でも、例えば GCP や AWS、Azure などのパブリッククラウドにもそれぞれ固有のコンテナレジストリサービスがありますし、オンプレミス環境などでプライベートなコンテナレジストリを構築できる製品も存在しています。

もっとも手軽に利用できるコンテナレジストリは、Docker 公式のサービスである Docker Hub です。アカウントの作成が必要で、すぐには試せないと思いますので、ここでは簡単に手順だけ紹介します。

### タグ付け

どのコンテナレジストリでも、まずはタグの付け方が重要です。正しくタグが付けられていないと、公開できません。

- Docker Hub にプッシュする場合
    - 凡例： `<リポジトリ名>/<イメージ名>:<タグ>`
        - リポジトリ名は、個人で触る範囲であれば、アカウント名と同じです
    - 実例： `username/myapp:0.0.1`
- Docker Hub 以外にプッシュする場合
    - 凡例： `<レジストリ URL>/<リポジトリ名>/<イメージ名>:<タグ>`
    - 実例： `ghcr.io/username/myapp:0.0.1`
        - `ghcr.io` は GitHub Container Registry の例です

ビルド時に `-t` で上記に従ってタグ付けするか、もしくは既存のイメージに以下のようにして別のタグを追加できます。

```bash
docker tag my-first-container:0.0.2 username/myapp:0.0.2
docker images
```

### ログインとプッシュ

コンテナイメージの準備ができたら、`login` コマンドでユーザ名とパスワードを入力して Docker Hub のアカウントにログインします。

```bash
docker login
```

この後、`push` でコンテナイメージをプッシュできます。

```bash
docker push username/myapp:0.0.2
```

!!! note "他のレジストリの場合は？"
    `docker login ghcr.io` など URL を指定してログインする場合や、事前にアクセストークンを発行して認証を構成しておく場合など、サービスによって様々です。サービスごとのドキュメントで案内されていますので、適宜確認するとよいでしょう。

    ログインできれば、プッシュの仕方は同じです。

プッシュが成功すると、Docker Hub のページからブラウザで確認できるようになります。

[![image](https://user-images.githubusercontent.com/2920259/99151681-3e055a00-26e0-11eb-82e2-4f70aa133537.png)](https://user-images.githubusercontent.com/2920259/99151681-3e055a00-26e0-11eb-82e2-4f70aa133537.png)

!!! note "プライベートリポジトリ"
    Docker Hub でも GitHub Container Registory でも、プライベートリポジトリを作成でき、それを利用すれば自分が許可したひとしか利用できないコンテナイメージも作成できます。

    この場合、コンテナイメージは秘匿される一方で、Pull するためにも認証が必要になるため、例えば Kubernetes 上で利用したい場合などに追加の認証情報の構成が必要になります。また、無償で利用できる範囲がプライベートリポジトリとパブリックリポジトリで異なることもあるため、各サービスのドキュメントを確認したうえで利用しましょう。

!!! warning "Docker Hub の制限"
    Docker Hub には、2020 年の冬ごろから、無料プランに以下のような制約が設けられました。

    - 無料プランのアカウントが登録したイメージで六か月以上未使用のものを自動的に削除する
    - 一定時間あたりの Pull 回数に上限を設ける

    一方で、GitHub Container Registory（正確には GitHub Packages）には、パブリックリポジトリであれば現時点では制限はありません（プライベートリポジトリには容量や転送量に制限があります）。

## 様々なカスタマイズ方法（参考）

!!! tip "実施不要"
    このセクションは、参考として紹介しています。**手順の実施は不要** です。

Dockerfile のベースイメージには、任意のコンテナイメージを指定できます。

このラボでは、既存の `p4app` をカスタマイズする際に、`app.py` や `bg.jpg` を変更してから元の Dockerfile をそのまま使いましたが、この方法は、元の `p4app` のビルドに必要なすべてのファイルが手元にあるからこそできたものでした。

別解として、

- 手元に元の Dockerfile やそこで必要とされているファイル群がない
- 置き換えたいファイルなど、元のイメージから変更したい点が明確である

場合は、例えば **`p4app` 自体をベースイメージにしてしまい、そこからの差分だけ記述する** と、同じ目的を達成できます。これはつまり、手元に `app.py` と `bg.jpg` だけあれば、Dockerfile が以下だけでも目的の状態のイメージをビルドできるということです。

```docker
FROM ghcr.io/piperjapan/p4app:0.0.1

ADD app.py /app
ADD bg.jpg /app/static/img
```

この方法には、Dockerfile の中身がシンプルにでき、元のイメージの Dockerfile の内容を知らなくてもカスタマイズできたり、元のイメージのバージョンアップにも追従しやすいなどメリットがある一方で、できあがるイメージのサイズが大きくなりがちな点がデメリットとして挙げられます。適宜使い分けるとよいでしょう。
