# Docker Compose Lab： おわりに

## ここまででできたこと

コンテナオーケストレーションの例として、Docker Compose を紹介しました。

Compose ファイルと呼ばれる構成ファイルにすべての構成をあらかじめ定義しておくことで、複数のコンテナが協調して動作する環境の起動と停止を、それぞれコマンド一行でできるようになりました。

ツールによっては、Docker Compose での起動・停止を前提として Compose ファイルを配布している例や、ユースケースとして Compose ファイルの記述例を公開している例も多数あります。Docker と Docker Compose が使えるだけで、相当な範囲のツールを自由に操れるようになります。

## いくつかの例（参考）

Docker の公式ドキュメントでも、Docker Compose のクイックスタートの例として、

- [Django アプリケーションをビルド・構成する例](https://docs.docker.jp/compose/django.html)
- [Rails アプリケーションをビルド・構成する例](https://docs.docker.jp/compose/rails.html)
- [Wordpress を構成する例](https://docs.docker.jp/compose/wordpress.html)

が紹介されています。Django や Rails はフレームワークを使うため少々複雑ですが、興味があれば試してみるのもよいでしょう。

また、IoT のパートで取り上げられる（かもしれない）EdgeX Foundry も、[公式の手順が Docker Compose での操作](https://docs.edgexfoundry.org/1.3/getting-started/quick-start/) です。
