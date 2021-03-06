# Docker Lab： はじめに

このラボでは、コンテナの概念に慣れるべく、Docker の基本的な取り扱いをざっくり総ざらいします。

## このラボの目的と概要

このラボでは、

- とにかく **コンテナ** というモノに触れてみる
- コンテナの基本的な概念をなんとなくわかった気持ちになる
- コンテナ形式で提供されている **既成のツール** を使う場合の動かし方を理解する
- 自前のアプリケーションをコンテナ化して動かせるようになる

ことを目的に、以下のトピックを取り扱います。

- 既成のコンテナの起動と停止、削除
- コンテナイメージとレジストリ
- 複数のコンテナの連携とコンテナネットワーク
- データの永続化
- コンテナの動的な設定変更
- コンテナイメージのビルド
- コンテナイメージの公開

## 準備

このラボでは、GCP 上の仮想マシンインスタンスで Docker を動作させます。Docker 用の仮想マシンを作成していない場合は、次の手順を実行します。

- [📖 **Prep for Lab： Docker 用仮想マシンの用意**](prep-docker-vm.md)

また、ラボで利用するリソースは GitHub 上のリポジトリで公開されています。用意した Docker 用仮想マシン上に次のコマンドで必要なリソースをクローンします。

```bash
cd ~
git clone https://github.com/piperjapan/lab-docker-k8s.git
```
