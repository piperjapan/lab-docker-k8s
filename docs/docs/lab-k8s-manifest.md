# Kubernetes Lab： 使ってみる

このラボでは、Kubernetes の重要な概念のひとつであるマニフェストの活用を実践します。

## 準備

このラボでは、`lab-k8s-manifest` ディレクトリを利用します。

```bash
cd ~/codes/Module10/lab-k8s-manifest
```

## マニフェストを利用した移植性

これまで、Pod の作成や Service の構成などの操作はすべて手動で行ってきました。この手法は、ちょっとだけ試したいとき、とにかくサクッと動かしてみたいときなどにはたいへん便利ですが、実際のところ、エンタプライズ環境での一般的な手法とは言えません。

Docker Compose での Compose ファイルのように、Kubernetes でもアプリケーション全体の構成を YAML 形式で記述された **マニフェスト** で定義して管理できます。YAML ファイルですべての構成を定義し宣言することで、テキストファイルで構成を管理できるほか、同じ構成のアプリケーションを簡単に他の環境へ移植できるなどのメリットが生まれます。

ここでは、実際にマニフェストファイルを作成し、それを元に再デプロイしてみます。

## 既存のリソースからのマニフェストの作成と利用

Kubernetes では、`get` コマンドに `-o yaml` を与えることで、その時点の構成を YAML フォーマットで出力できます。これによって得られた YAML ファイルは、そのままマニフェストファイルとして利用可能です。

[![image](https://user-images.githubusercontent.com/2920259/99185297-2e434f80-278c-11eb-9a2b-010350e3cac8.png)](https://user-images.githubusercontent.com/2920259/99185297-2e434f80-278c-11eb-9a2b-010350e3cac8.png)

ここでは、実際に現在のリソースの情報をマニフェストとして出力（①）し、環境を削除後、マニフェストによるデプロイ（②）を実勢します。

### マニフェストの作成

まずは、YAML 形式での出力を確認してみましょう。

```bash
kubectl get pods -o yaml
kubectl get deployment -o yaml
kubectl get service -o yaml
```

このうち、例として Deployment の出力を YAML ファイルとして保存します。

```bash
kubectl get deployments -o yaml > deployments.yaml
```

このファイルをエディタで開き、 **19 行目付近** にある `p4app` の Deployment の `replicas` を `2` から `3` に修正して、上書きします。

```yaml
  spec:
    progressDeadlineSeconds: 600
    replicas: 3
    revisionHistoryLimit: 10
    selector:
      matchLabels:
        app: p4app
```

!!! note "編集方法"
    右上の `[ エディタを開く ]` アイコンから、**Cloud Shell Editor** を起動して、GUI でファイルを操作できます。保存は `[Ctrl] + [S]` です。

    [![image](https://user-images.githubusercontent.com/2920259/99142917-c6620b80-269c-11eb-8120-0b25685ab159.png)](https://user-images.githubusercontent.com/2920259/99142917-c6620b80-269c-11eb-8120-0b25685ab159.png)

    Cloud Shell Editor でなく、`vi` も利用できます。

### マニフェストの利用

編集した YAML ファイル、すなわち Deployment のマニフェストを使ったデプロイを試すため、現在稼働している Deployment を削除します。

```bash
kubectl delete deployment p4app
kubectl delete deployment redis
kubectl get all
```

しばらく待って `get all` の結果が Service だけになったら、Deployment の削除は完了です。YAML ファイルを基にした構築が行える準備が整いました。

!!! note "存在するはずのないリソース"
    ここでも、やはり **あるべき状態** の定義が変更されています。つまり、Deployment や ReplicaSet、Pod が **ない状態が正しい** と定義が変更されたため、それに一致させるように削除処理が動いたことになります。

次のコマンドで、YAML ファイルを基にリソースを作成できます。

```bash
kubectl apply -f deployments.yaml
kubectl get all
```

レプリカを 3 つにしたため、`[ READY ]` が `3/3` になり、実際にブラウザでアクセスすると、今度は 3 つの Web サーバにロードバランスされていることが確認できます。

## きれいなマニフェストを手作りする

`get` コマンドにより、YAML ファイルが作成できました。しかしこの YAML ファイルは、情報が多く、人間が管理するのは少し大変そうです。

実際には、この全行が必須なわけではなく、不要な行は削除しても動作します。また、先の例では Deployment だけのマニフェストにしましたが、ひとつのマニフェストファイルに任意のリソースを列挙できるため、Service も含められます。

[![image](https://user-images.githubusercontent.com/2920259/99185301-37ccb780-278c-11eb-8433-918313ed0724.png)](https://user-images.githubusercontent.com/2920259/99185301-37ccb780-278c-11eb-8433-918313ed0724.png)

ここでは、GitHub にあらかじめ配置しておいたサンプルのマニフェスト（①）を使って、マニフェストの中身の確認と再デプロイ（②）を実践します。

### サンプルマニフェストの確認

サンプルのマニフェストは、ラボの準備のために `git clone` した中に含まれています。このマニフェストは、ここまでで作ってきた構成を極力シンプルに単一のマニフェストとして表現した例です。

カレントディレクトリに `manifest.yml` があるはずです。右上の `[ エディタを開く ]` アイコンから、**Cloud Shell Editor** を起動して、`manifest.yaml` ファイルを開きます（中身を確認するだけなので、`cat` などでもかまいませんが、Cloud Shell Editor だと見た目がきれいです）。

```yaml
apiVersion: v1
kind: List
items:

- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: p4app
    labels:
      app: p4app
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: p4app
    template:
      metadata:
        labels:
          app: p4app
      spec:
        containers:
        - name: p4app
          image: kurokobo/p4app:0.0.1
          ports:
          - containerPort: 8080
            protocol: TCP
        restartPolicy: Always
        
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: redis
    labels:
      app: redis
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: redis
    template:
      metadata:
        labels:
          app: redis
      spec:
        containers:
        - name: redis
          image: redis:6.0
          ports:
          - containerPort: 6379
            protocol: TCP
        restartPolicy: Always

- apiVersion: v1
  kind: Service
  metadata:
    name: p4app
    labels:
      app: p4app
  spec:
    selector:
      app: p4app
    ports:
    - port: 80
      protocol: TCP
      targetPort: 8080
    type: LoadBalancer

- apiVersion: v1
  kind: Service
  metadata:
    name: redis
    labels:
      app: redis
  spec:
    selector:
      app: redis
    ports:
    - port: 6379
      protocol: TCP
      targetPort: 6379
    type: ClusterIP
```

Deployment と Service が 2 つずつ定義されていることがわかります。行数は非常に少なく、読めばなんとなく意味がわからなくもなさそうなレベルになっています。

コマンドで手作りした環境を元にマニフェストを作成することももちろんありますが、その場合でも、実際の運用に持ち込むためには、不要な行を削除したりファイルの分け方を工夫したりして、ファイルをシンプルに保つ工夫をする場合がほとんどです。

### サンプルマニフェストの利用

実際に使ってみましょう。

まずは、すべての環境を削除します。サンプルマニフェストは Service も含んでいるため、Service もすべて削除します。

```bash
kubectl delete deployments --all
kubectl delete services --all
kubectl get all
```

しばらく待って、`get all` の結果が `service/kubernetes` のみになったら、削除は完了です。

!!! note "セルフヒーリング"
    `delete services --all` で問答無用ですべての Service を削除していますが、`service/kubernetes` は管理上必要な Service です。**1 つあるべき** と定義されているため、手で消したとしても自動的に再度作成されます。

デプロイします。

```bash
kubectl apply -f manifest.yaml
kubectl get all
```

`service/p4app` の `EXTERNAL-IP` が実際の IP アドレスに変わったら、ブラウザでアクセスしてみましょう。削除前と同じアプリケーションにアクセスできるはずです。

[![image](https://user-images.githubusercontent.com/2920259/99144246-b4399a80-26a7-11eb-846a-f600c5a51105.png)](https://user-images.githubusercontent.com/2920259/99144246-b4399a80-26a7-11eb-846a-f600c5a51105.png)

このように、シンプルなマニフェストファイルでも目的を達成できることがわかりました。

マニフェストファイルに書くべき内容はほとんど決まっており、使いまわせる部分も非常に多いため、コマンドで手作りして `-o yaml` しなくても、慣れてくればゼロから目的のマニフェストファイルを作ることも（凝ったことをしない範囲では）難しくありません。

## ここまででできたこと

マニフェストの作成方法を理解し、実際にマニフェストを使ったリソースのデプロイを実践しました。

[![image](https://user-images.githubusercontent.com/2920259/99185301-37ccb780-278c-11eb-8433-918313ed0724.png)](https://user-images.githubusercontent.com/2920259/99185301-37ccb780-278c-11eb-8433-918313ed0724.png)

YAML ファイルはただのテキストファイルなので、Git リポジトリなどでのバージョン管理も容易です。あらかじめマニフェストファイルを作ってしまえば、Kubernetes クラスタへのデプロイを CI/CD や GitOps の概念と組み合わせて自動化も可能です。
