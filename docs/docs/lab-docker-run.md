# Docker Lab： 使ってみる

最近は、新しいアプリケーションがコンテナイメージで提供される形態も増えてきました。このラボでは、コンテナの **ユーザ** 側の立場で、まずはコンテナを動かしてみます。

## 既成のコンテナの起動と停止、削除

なにはともあれ、習うより慣れろ、まずは動かしてみましょう。

現段階では、

- コンテナは、めちゃくちゃ軽量でオーバヘッドが少ない仮想マシンみたいなもので
- できあいの仮想マシンイメージがインタネット上で公開されていて
- そこから好きなモノをダウンロードしてデプロイできる

くらいのぼんやりとしたイメージをしておくと、とっかかりやすいでしょう。もちろん、**これは技術的にはだいぶウソ** なので、追って説明は加えていきます。

### 最初の起動

とてもおもしろそうなツールを見つけて使ってみようとしたら、提供形態が **コンテナ** だった、というシナリオを考えます。

細かいことはさておき、とにかく動かしてみましょう。仮想マシンのターミナルで、次のコマンドを実行します。

```bash
docker run -p 80:8080 kurokobo/p4app:0.0.1
```

[![image](https://user-images.githubusercontent.com/2920259/98806878-2f5b4080-245d-11eb-9cfa-4a8e9b396a2d.png)](https://user-images.githubusercontent.com/2920259/98806878-2f5b4080-245d-11eb-9cfa-4a8e9b396a2d.png)

コマンドの実行後、なにやら処理が行われ、`[ Running on http://0.0.0.0:8080/ (Press CTRL+C to quit) ]` の表示を確認したら、GCP の管理コンソールに戻って、操作している仮想マシンの `[ 外部 IP ]` をクリックします。これは、HTTP でその IP アドレスにアクセスできるリンクです。

[![image](https://user-images.githubusercontent.com/2920259/98807136-8f51e700-245d-11eb-92ce-ab92327a75a9.png)](https://user-images.githubusercontent.com/2920259/98807136-8f51e700-245d-11eb-92ce-ab92327a75a9.png)

ブラウザの新しいタブで、おもしろそうなツールが起動しましたね。

[![image](https://user-images.githubusercontent.com/2920259/98807222-ad1f4c00-245d-11eb-8537-4f9815477fbd.png)](https://user-images.githubusercontent.com/2920259/98807222-ad1f4c00-245d-11eb-8537-4f9815477fbd.png)

成功です！ この段階ですでに、

- インタネットの向こう側にある GCP の 仮想マシン上で
- **コンテナ** を起動させて
- ブラウザ越しにインタネットを経由して、その **コンテナにアクセス** した

状態です。このおもしろそうなツールは、つい先ほど自分の手で起動させたコンテナによってホストされています。

!!! note "うまく表示されない場合"
    `docker run` コマンドの結果に目立ったエラーがないのであれば、仮想マシンの作成時にファイアウォールの構成が漏れていた可能性があります。仮想マシンの構成を見直すとよいでしょう。

### 起きていたこと

さて、コマンドを一行実行しただけでツールが起動してきたわけですが、すこしだけ、行われた処理を説明します。

最初に、GCP 上に Docker の母艦となる仮想マシンを作成しました。

[![image](https://user-images.githubusercontent.com/2920259/99185186-92b1df00-278b-11eb-851a-7fb551df69dc.png)](https://user-images.githubusercontent.com/2920259/99185186-92b1df00-278b-11eb-851a-7fb551df69dc.png)

続けて、`docker run` コマンドを実行し、あとはブラウザからアクセスしただけです。

これを少しだけ細かく図示すると、次のようになります。

[![image](https://user-images.githubusercontent.com/2920259/99185194-a52c1880-278b-11eb-95e0-8c1f6b3c2a1a.png)](https://user-images.githubusercontent.com/2920259/99185194-a52c1880-278b-11eb-95e0-8c1f6b3c2a1a.png)

実行したコマンド `docker run -p 80:8080 kurokobo/p4app:0.0.1` を紐解くと、実は、次のような意味でした。

- コンテナイメージ `kurokobo/p4app:0.0.1` を起動する（`docker run kurokobo/p4app:0.0.1`）
- 起動時には、コンテナの `8080` 番ポートをコンテナホストの `80` 番ポートとして公開する（`-p 80:8080`）

この段階では、いくつかの用語を抑えておくとよいでしょう。技術的な詳細は、ラボを進めるともう少しイメージできるようになるはずです。

#### コンテナレジストリ

Docker は、コンテナイメージが指定され、それが未知のモノだった場合、インタネットで公開されている **コンテナレジストリ** を勝手に検索し、合致するものをダウンロードしてくれます。デフォルトでは、検索先は [Docker Hub](https://hub.docker.com/) です。

今回は、`kurokobo/p4app:0.0.1` を指定しました。今回が初回実行であり、未知のイメージのため、Docker Hub でリポジトリ `kurokobo` の `p4app` イメージが検索され、その中で `0.0.1` のタグがつけられたものが自動でダウンロードされたわけです（図中 ①）。なお、二回目以降の実行時には、初回実行時にローカルにダウンロードされたイメージが再利用されます。

なお、コンテナイメージのダウンロードは正確には **プル** といい、起動させずにダウンロードだけ行う `docker pull` コマンドも用意されています。

#### コンテナイメージ

ダウンロードしたコンテナイメージには、ツールそのものだけでなく、ツールの実行に必要な周辺環境（ランタイム、ライブラリ、モジュールなど）が丸ごと含まれています。また、そのイメージが実際にコンテナとして起動された際の起動方法などのメタデータも含まれています。

!!! warning "コンテナイメージのタグ指定"
    この例では、`kurokobo` の `p4app` イメージの `0.0.1` タグを利用しました。タグの指定は必須ではなく、省略した場合は `latest` タグが検索されますが、今日では `latest` タグの利用は推奨されません。

    `latest` タグは通常は **その時点の最新** がポイントしますが、これはつまり、**実行時点によってプルされるイメージが変わる可能性がある** ことを意味します。同じタグであればいつでも同じイメージがプルできる状態が望ましいことから、利用者側もコンテナイメージの作成者側もなるべく `latest` は使わず、バージョンを明示することを心がけましょう。

#### コンテナ

コンテナイメージを実際に起動させたモノが、コンテナです。

今回は、ダウンロードしたコンテナイメージ `kurokobo/p4app:0.0.1` が、そのコンテナイメージにあらかじめ設定された起動方法（所定の Python スクリプトの実行）に従って起動されました（図中 ②）。このコンテナはデフォルトでは `8080` 番ポートで待ち受けますが、Docker ホスト内からしかアクセスできないので、コマンドの `-p` オプションで、明示的に Docker ホストの `80` 番ポートとして公開を指示していました。

### 停止と削除

ターミナルに戻って、`[Ctrl] + [C]` を押下して、コンテナを停止させます。ここでのポイントは、次の二点です。

- コンテナは、起動時に明示しない限り、**フォアグラウンドモード**（手動で終了させるまでプロンプトが返らない）**で起動する**
- コンテナは、**停止しただけでは、削除されない**

動作中のコンテナは、`docker ps` コマンドで確認できます。

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

何も表示されませんが、正常です。`docker ps` コマンドでは、**動作中の** コンテナしか表示されません。先ほど起動したコンテナは、すでに `[Ctrl] + [C]` で停止しています。

停止中のコンテナを含めたすべてのコンテナを確認するには、`docker ps -a` コマンドを実行します。コンテナ名（`NAME` 列）には見慣れない英単語が表示されますが、これは、コンテナ名をコンテナの起動時に指定しなかったことで、二つの英単語からランダムに自動生成されたためです。

```bash
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS                     PORTS               NAMES
a908d558fa48        kurokobo/p4app:0.0.1   "python app.py"     About an hour ago   Exited (0) 5 minutes ago                       reverent_kepler
```

停止中のコンテナは、`docker rm` コマンドで削除できます。引数で、コンテナ ID（`CONTAINER ID` 列）かコンテナ名（`NAME` 列）のどちらかを指定します。

```bash
$ docker rm reverent_kepler
reverent_kepler

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

実際にコンテナを削除し、`docker ps -a` に何も表示されない状態にして、次に進みます。

### その他の基本的な操作

コンテナをフォアグラウンドで起動させてしまうと、今回の Web ベースのツールのように常時起動させておきたい場合に都合がよくありません。起動時のオプションで `-d` を指定すると、**デタッチドモード** になり、バックグラウンドで実行できます。

実際に、デタッチドモードで起動させ、`docker ps` で起動していることを確認します。

```bash
$ docker run -d -p 80:8080 kurokobo/p4app:0.0.1
6979de0938a5178ae2930e1baf7d6e702e950cc634624bae683be9d80c89b319

$ docker ps
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS                  NAMES
6979de0938a5        kurokobo/p4app:0.0.1   "python app.py"     3 seconds ago       Up 2 seconds        0.0.0.0:80->8080/tcp   epic_darwin
```

起動したコンテナは、`docker stop` で停止できます。削除時と同様に、引数でコンテナ ID かコンテナ名を指定します。

```bash
$ docker stop epic_darwin
epic_darwin

$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS                       PORTS               NAMES
6979de0938a5        kurokobo/p4app:0.0.1   "python app.py"     7 minutes ago       Exited (137) 4 seconds ago                       epic_darwin
```

さて、ここで、停止したコンテナを **削除しない** 状態で、再び `docker run` して、`docker ps -a` してみます。

```bash
$ docker run -d -p 80:8080 kurokobo/p4app:0.0.1
77ed4288697f7122d8e94df555ec78c681a5fee5364b757b11802497865adcae

$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS                       PORTS                  NAMES
77ed4288697f        kurokobo/p4app:0.0.1   "python app.py"     4 seconds ago       Up 2 seconds                 0.0.0.0:80->8080/tcp   gallant_ptolemy
6979de0938a5        kurokobo/p4app:0.0.1   "python app.py"     9 minutes ago       Exited (137) 2 minutes ago                          epic_darwin
```

この結果から、`docker run` で起動させると、**常に新しいコンテナが新規に作成される** ことがわかります。削除をしないとコンテナが残り続けるだけでなく、**起動のたびに増えていく** ことになるので、掃除が必要です。

少しお行儀の悪い掃除の方法として、`docker rm -f` を紹介します。このコマンドでは、起動中のコマンドも強制的に停止させて削除できます。また、引数で複数のコンテナを列挙すると、同時に削除が可能です。

```bash
$ docker rm -f 77ed4288697f 6979de0938a5
77ed4288697f
6979de0938a5

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

また、`docker run` にオプション `--rm` を追加すると、**そのコンテナの停止時に自動で削除される** ようになります。

```bash
$ docker run --rm -d -p 80:8080 kurokobo/p4app:0.0.1
38108887b580658641c6dd44a0091ce507ea1751af9725eb8cdf30ee839564b4

$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS                  NAMES
38108887b580        kurokobo/p4app:0.0.1   "python app.py"     6 seconds ago       Up 5 seconds        0.0.0.0:80->8080/tcp   naughty_mayer

$ docker stop 38108887b580
38108887b580

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### ここまででできたこと

既成のコンテナイメージの様々な起動と、停止、削除の操作方法を実践しました。**任意のコンテナイメージを起動できる** だけでも、世の中の多数の OSS を実際に動かせる力が得られます。
