# コントリビューションガイド

本リポジトリへのコントリビューション方法のガイドです。

## 目次

- [コントリビューションガイド](#コントリビューションガイド)
  - [目次](#目次)
  - [ディレクトリ構造](#ディレクトリ構造)
  - [コンテナイメージの修正](#コンテナイメージの修正)
    - [コンテナイメージの修正の考え方](#コンテナイメージの修正の考え方)
    - [コンテナイメージの修正方法](#コンテナイメージの修正方法)
  - [ラボガイドの修正](#ラボガイドの修正)
    - [ラボガイドの修正の考え方](#ラボガイドの修正の考え方)
    - [ラボガイドの修正方法](#ラボガイドの修正方法)
  - [ラボ用の資材の修正](#ラボ用の資材の修正)
  - [補足](#補足)
    - [GitHub Container Registry](#github-container-registry)
    - [GitHub Pages](#github-pages)
    - [MkDocs](#mkdocs)

## ディレクトリ構造

このリポジトリに含まれる各ディレクトリの役割は次の通りです。

| ディレクトリ | 内容物                                                                  |
| ------------ | ----------------------------------------------------------------------- |
| `docker`     | ラボの中で利用しているコンテナイメージ `p4app` のビルド用ソースコード群 |
| `docs`       | ラボガイドのビルド用ソースコード群                                      |
| `lab-*`      | ラボの中で利用する資材群                                                |

## コンテナイメージの修正

ラボの中で利用しているコンテナイメージ `p4app` は、`docker` ディレクトリ内のファイルを基に、**GitHub Actions により自動ビルド** されています。

### コンテナイメージの修正の考え方

コンテナイメージを修正するには、`docker` ディレクトリ内のファイルに変更をプッシュしてください。

本リポジトリは、`docker` ディレクトリ内のファイルへのプッシュで、**GitHub Actions のワークフロー** がトリガされ、**コンテナイメージのビルド** と **GitHub Container Registry での公開** が自動で行われるように構成されています。

- [トリガされる GitHub Actions のワークフローを定義したファイル](.github/workflows/ghcr.yml)
- [実行されたワークフローを確認できる GitHub Actions のページ](https://github.com/piperjapan/lab-docker-k8s/actions)
  - [実行例（`deploy` ジョブから詳細なログを確認可能）](https://github.com/piperjapan/lab-docker-k8s/actions/runs/921892410)
- [ビルドされたコンテナイメージの公開場所（GitHub Container Registry）](https://github.com/orgs/piperjapan/packages/container/package/p4app)

自動ビルドされるコンテナイメージの **名称** と **タグ** は、それぞれ次の仕組みで決定されます。

- **名称**（`p4app`）
  - [ワークフロー中でハードコード](.github/workflows/ghcr.yml#L40) されています。
  - 通常、変更は不要です。
- **タグ**（`*.*.*`）
  - [`docker` ディレクトリ内の `VERSION` ファイル](docker/VERSION) の中身が [ワークフロー中で `cat`](.github/workflows/ghcr.yml#L19) されて利用されます
  - コンテナイメージに大幅な変更を加えた場合は、`docker/VERSION` ファイル内のタグも併せて修正してください。なお、タグを変更した場合、併せてラボガイド内でタグを記載している箇所も修正が必要です

なお、本ドキュメントの執筆時点では、`lab-docker-build` ディレクトリと `docker` ディレクトリは、**`VERSION` ファイルの有無以外は完全に同じ** 状態になっています。ラボガイドの構成次第ですが、`docker` ディレクトリに変更を加えたら、同じ変更を `lab-docker-build` ディレクトリにも加えることを推奨します。

### コンテナイメージの修正方法

1. 本リポジトリをフォークしてクローンし、`docker` ディレクトリ内のソースコードを修正します
   - ラボの構成に合わせて、`lab-docker-build` ディレクトリ内のソースコードにも同じ修正をします
2. ローカルでコンテナイメージをビルドし、動作をテストします
   - `cd docker`
   - `docker build -t p4app-test:0.0.1 .`
   - `docker run -p 80:8080 p4app-test:0.0.1`
3. 必要に応じて、`lab-docker-build` ディレクトリでもビルドし、動作をテストします
4. 問題なければ変更をコミットしてプッシュし、GitHub 上でプルリクエストを作成します

## ラボガイドの修正

ラボガイドも、`docs` ディレクトリ内のファイルを基に、**GitHub Actions により自動ビルド** されています。

### ラボガイドの修正の考え方

ラボガイドを修正するには、`docs` ディレクトリ内のファイルに変更をプッシュしてください。

本リポジトリは、`docs` ディレクトリ内のファイルへのプッシュで、**GitHub Actions のワークフロー** がトリガされ、**ラボガイドを構成する HTML ファイル群のビルド** と **GitHub Pages での公開** が自動で行われるように構成されています。

- [トリガされる GitHub Actions のワークフローを定義したファイル](.github/workflows/gh-pages.yml)
- [実行されたワークフローを確認できる GitHub Actions のページ](https://github.com/piperjapan/lab-docker-k8s/actions)
  - [実行例（`deploy` ジョブから詳細なログを確認可能）](https://github.com/piperjapan/lab-docker-k8s/actions/runs/921875698)
- [ビルドされたラボガイドの公開場所（GitHub Pages）](https://piperjapan.github.io/lab-docker-k8s/)

### ラボガイドの修正方法

前述の通り、ラボガイドは MkDocs を利用して記述されています。修正する場合は、MkDocs の記法に従ってください。

1. 本リポジトリをフォークしてクローンし、`docs` ディレクトリ内のソースコードを修正します
2. ローカルで MkDocs を使って静的 Web サイトをビルドし、ブラウザで動作を確認します
   - `cd docs`
   - `python -m pip install -r requirements.txt`
   - `mkdocs serve`（結果はブラウザで `http://127.0.0.1:8000` にアクセスして確認します）
3. 問題なければ変更をコミットしてプッシュし、GitHub 上でプルリクエストを作成します

## ラボ用の資材の修正

特別な実装や自動化はしていないため、修正するには、通常通り変更をプッシュしてください。

ただし、`lab-docker-build` ディレクトリ内のファイルに修正を加えた場合は、ラボガイドの構成の都合から、`docker` ディレクトリ内にも同じ修正を加えることを検討してください。

## 補足

### GitHub Container Registry

GitHub が提供しているコンテナレジストリです。Docker Hub には [帯域制限や未使用イメージの自動削除などの制約](https://docs.docker.com/docker-hub/download-rate-limit/) がありますが、GitHub Container Registry には、現状は同等の制約はありません。GitHub のアカウントがあれば利用できます。

- [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

本リポジトリでは、コンテナレジストリへのコンテナイメージのプッシュは GitHub Actions で行っていますが、上記ドキュメントに記載のあるとおり、`docker` コマンドでも手動でプッシュできます。

### GitHub Pages

GitHub が提供している、リポジトリの特定のブランチに含まれるファイル群で静的 Web サイトをホストする仕組みです。デフォルトでは `gh-pages` ブランチ内のコンテンツがホストされますが、設定で別のブランチにも切り替えられます。

- [About GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)

本リポジトリでは、HTML ファイルの生成と `gh-pages` ブランチへの配置をすべて GitHub Actions で行っていますが、必ずしもそうする必要はなく、手作りした HTML ファイルを `gh-pages` ブランチに手動でプッシュしても動作します。気軽な Web ページの公開手段として非常に有用です。

### MkDocs

MkDocs は、Markdown 記法で記述されたテキストファイルを基に静的 Web サイトを生成する、いわゆる静的サイトジェネレータの実装の一つです。

本ラボガイドでは、通常の MkDocs に加えて、それ用のテーマである **Material for MkDocs** を利用しています。

- [Getting Started - MkDocs](https://www.mkdocs.org/getting-started/)
- [Gettign Started - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/getting-started/)
