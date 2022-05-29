# Docker Lab： シェルの利用

コンテナを作ったり消したりしてきましたが、ここではコンテナの **中** に入る手段を実践します。

## コンテナイメージとシェル

コンテナは、OS 上で論理的に分離された空間です。プロセスもファイルシステムも、コンテナの中にはコンテナの中だけの世界が広がっています。

利用しているコンテナイメージがシェルのバイナリ（`/bin/bash` や `/bin/sh`、`/bin/ash`）を持っていれば、Docker を介してコンテナの中のシェルを操作できます。

[![image](https://user-images.githubusercontent.com/2920259/99256546-e9391f00-2858-11eb-9be6-a5b2930bccde.png)](https://user-images.githubusercontent.com/2920259/99256546-e9391f00-2858-11eb-9be6-a5b2930bccde.png)

### シェルへのアクセス

まずは `p4app` を起動させます。

```bash
docker run -d --name p4app -p 80:8080 ghcr.io/piperjapan/p4app:0.0.1
docker ps -a
```

起動できたら、次のコマンドでシェルを起動させます。

```bash
docker exec -it p4app bash
```

!!! note "オプションの意味"
    `-it` はシェルの起動時によく使われるオプションで、`-i` が標準入力の維持、`-t` が仮想 TTY の割り当てを意味しますが、意味を気にせず覚えてしまっても大丈夫です。

プロンプトが `root@afb9e0cc32c5:/app` などの文字列に変化していれば、そこはもうコンテナの中の世界です。コンテナイメージに含まれるバイナリしか使えないので、機能するコマンドは限られていますが、標準的なコマンドを試してみましょう。

```bash
hostname
ls -l /home
cat /etc/os-release
```

コンテナが論理的にまったく別の空間で動作していることがわかります。どうやら、コンテナの中は Debian のようですね。

シェルを抜けるには `exit` です。

```bash
exit
```

起動させたコンテナは、後続のラボに備えて削除します。

```bash
docker rm -f p4app
```

### サンドボックスとしての利用

次のコマンドでは、CentOS のコンテナイメージを起動させ、シェルの起動のみをさせています。また、`--rm` を加えることで、終了したら自動でコンテナが削除されるようにもしています。

```bash
docker run --rm -it quay.io/centos/centos:stream8 bash
```

プロンプトが `[root@9a10bb40b2fa /]#` などの文字列に変化していれば、コンテナイメージ `centos:8` の中のシェルにアクセスできています。いくつかのコマンドを試してみましょう。

```bash
cat /etc/os-release
apt update
dnf install -y python38
python3 -c 'print("hello world")'
```

コンテナなのでそのものではない（例えば `systemd` は起動されていませんし、プロセスも全然ありません）が、論理的には CentOS とほぼ同等の空間ができあがっています。

`exit` すると終了します。起動時に `--rm` を付けていたので、コンテナは残りません。

```bash
exit
docker ps -a
```

このように、コンテナは一時的なサンドボックスとしても非常に有用です。

## ここまででできたこと

コンテナのシェルにアクセスする方法を実践しました。

[![image](https://user-images.githubusercontent.com/2920259/99256546-e9391f00-2858-11eb-9be6-a5b2930bccde.png)](https://user-images.githubusercontent.com/2920259/99256546-e9391f00-2858-11eb-9be6-a5b2930bccde.png)

シェルへのアクセスは、次のようなシーンなどで非常に有用です。

- トラブルシュート。コンテナが意図したとおりに動かないときに、内部の状態を調べる
- Dockerfile を作るための準備。例えば `dockerfile` に書くべき `RUN` をトライアンドエラーで探る
- サンドボックス。バインドマウントなども併用すれば、開発中のスクリプトをコンテナ内で実行できる

!!! note "必ずしもシェルがあるとは限らない"
    世の中のすべてのコンテナイメージがシェルを内包しているとは限りません。シェルがあるということは、シェル（とそれが動くのに必要な諸々）のバイナリ分の容量がコンテナイメージに必要になってしまいますし、CPU やメモリも必要で、さらにはシェルそれ自体の脆弱性への対応が必要になる可能性もあります。

    このため、イメージによっては、一切のシェルを含んでいない場合があり、その場合は当然ながらシェルを使った操作はできません。

    また、イメージによっては、`bash` がなく、代わりに `sh` や `ash` が用意されている場合もあります。

## コマンドの実行（参考）

実際には、シェルに限らずコンテナ内の任意のコマンドを実行できます（というより、任意のコマンドを実行させる方法を使ってシェルを起動させている、という表現の方が正確です）。

起動済みのコンテナに対して実行すれば、ファイルの存在や環境変数を確認するために非常に便利です。データベースのコンテナにワンライナでクエリを渡す目的などでも利用できます。

```bash
docker run -d --name p4app -e SAMPLE_VALUE=hoge -p 80:8080 ghcr.io/piperjapan/p4app:0.0.1
docker exec p4app ls -l
docker exec p4app env
docker rm -f p4app
```

このほか、`--rm` と組み合わせると、コンテナイメージ内のバイナリをオンデマンドで実行でき、（初回はプルが走りはするものの二回目以降は）ローカルでコマンドを直接実行するのに近しい操作感が得られます。さらにシェルの `alias` と組み合わせるとより便利です。

```bash
docker run --rm docker/whalesay cowsay 'Hello, Piper!'
alias whalesay='docker run --rm docker/whalesay cowsay'
whalesay 'Hello, Piper!'
```