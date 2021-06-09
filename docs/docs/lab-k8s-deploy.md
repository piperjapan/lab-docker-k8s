# Kubernetes Lab： 使ってみる

このラボでは、Docker ラボと同じアプリケーションを、実際に Kubernetes 上で動かします。

## Kubernetes の考え方

Kubernetes は、複数のノードからなる **クラスタ** として構成されます。GCP 上の Kubernetes Engine では、実体は仮想マシンです（他のパブリッククラウドのマネージド K8s サービスでも通常は仮想マシンで構成されます）。

クラスタやノードの情報は、次のコマンドで確認できます。

```bash
kubectl cluster-info
kubectl get nodes
```

クラスタはノードで構成されます。クラスタ作成時のデフォルトノード数が 3 のため、この段階で表示されるノードは 3 台です。

Kubernetes では、コンテナ単位ではなく、ひとつ以上のコンテナをまとめた **Pod** を基本単位として動作します。この段階では、ポッドは存在していません。

```bash
kubectl get pods
```

!!! note "Pod の分け方"
    ひとつの Pod には、ひとつ **以上** のコンテナを含められますが、多くの場合はひとつの Pod にはひとつのコンテナのみを入れて扱います。

    Kubernetes のリソース管理は Pod 単位であり、スケールやヘルスチェックも Pod 単位です。つまり、例えば Web サーバのコンテナと DB サーバのコンテナをひとつの Pod に入れてしまうことも技術的には可能ですが、この場合、Web サーバと DB サーバを別々にスケールできなくなりますし、Web サーバのコンテナで障害が発生すると、オートヒーリングにより DB サーバのコンテナもまとめて再起動されてしまいます。
    
    逆に、例えば、Web サーバのコンテナと AP サーバのコンテナが常に一対一で対応するようなアーキテクチャのアプリケーションの場合は、ひとつの Pod に両方を含めてしまう設計も効果的でしょう。この場合、ひとつの Pod 内のコンテナは必ず同一ノード上で動作するため、コンテナ間の通信もより効率的に行えます。

## アプリケーションの起動

### 最初のデプロイ

Kubernetes は **コンテナ** のオーケストレーションを行うものです。このため、Kubernetes 上でなにかを動作させたい場合、それの **コンテナイメージ** が必要です。

ここでは、任意のコンテナイメージを実際に動作させてみます。

この目的では、後述する **マニフェスト**（今の段階では **Compose ファイルの Kubernetes 版** くらいに捉えてください）を利用する場合も多いですが、さっとなにかを試したい場合などは、次のコマンドで直接デプロイしてしまう手も有効です。実際に試してみましょう。

```bash
kubectl create deployment p4app --image=kurokobo/p4app:0.0.1 --port 8080
kubectl get pods
```

`get pods` コマンドを複数回実行すると、Pod のステータスが `[ ContainerCreating ]` から `[ Running ]` に変化する様子が観測できます。

### リソースの役割と自律動作

Kubernetes は、アプリケーションのデプロイの単位として、後述する `[ ReplicaSet ]` を子要素とする `[ Deployment ]` の概念を持ちます。Deployment は主にアプリケーションのデプロイそれ自体を管理するリソースで、ローリングアップデートや、過去のデプロイへのロールバックなど、メンテナンス作業にも利用されます。

実行した `create deployment` コマンドは、Pod ではなく、Deployment を作成するコマンドです（下図 ①）。しかし結果として、指定したイメージを使った Pod ができています（同 ②）。何がおきたのでしょうか。

[![image](https://user-images.githubusercontent.com/2920259/99185264-fdfbb100-278b-11eb-8324-9b9b38fc9f68.png)](https://user-images.githubusercontent.com/2920259/99185264-fdfbb100-278b-11eb-8324-9b9b38fc9f68.png)

この動きを理解するには、この段階ではざっくり、

- Deployment は ReplicaSet を管理している
- ReplicaSet は Pod を管理している
- Deployment や ReplicaSet や Pod は、自分が管理すべき対象の **あるべき状態** を持っている
- Kubernetes は、常に **現在の状態** を **あるべき状態** に一致させつづけようとしている
    - 存在していなければ必要な数だけ新しく作成する
    - 必要な数より多く存在していたら削除する
    - ヘルスチェックに失敗していたら削除して再度作成する

ことを踏まえておくとよいでしょう。

!!! note "あるべき状態の自動的な維持"
    **あるべき姿** は、英語だと **Desired State** と表現されます。Kubernetes は基本的に、

    - **最終的になっていてほしい姿** を（手動または暗黙的に）**宣言的に定義** し
    - 内部では **その姿を自動で維持する** 機能が動作することで
    - 最終的に **あるべき姿で動作し続ける**

    ようにできています。技術な詳細は割愛しますが、興味があれば Reconciliation Loop をキーワードに周辺を調べてみるとよいでしょう。

今回の `create deployment` コマンドは、操作としては非常に（宣言的ではなく）手続き的ですが、正確に言えば、**Deployment を作れと人間が操作を命令したのではなく**、**こういう設定の Deployment があるべきである** と、**あるべき姿の変更** が行われています。その結果として、Kubernetes の **あるべき姿に一致させつづけようとする機能** 機能により **あるべきなのにないからその設定どおりの Deployment が実際に作られた**、と考えるとイメージしやすいでしょう。

同様に、**Deployment によって ReplicaSet が 1 つあるべきであることが定義** され、さらに **ReplicaSet によって Pod が 1 つあるべきであることが定義** され、結果として **あるべきなのにない** ことで ReplicaSet や Pod が実際に作られた、と解釈できます。

!!! note "デフォルト設定"
    `create deployment` にイメージとポート以外のオプションを設定しなかったため、内部的にそれ以外の設定はデフォルト値が採用されます。例えば、レプリカ数は 1 がデフォルトのため、今回は Pod が 1 つだけできあがっています。

### 状態の確認

この段階で、指定したコンテナイメージをもとにコンテナがひとつ稼働し、それを要素とする Pod がひとつできた状態になっています。

以下のコマンドで、実際の Deployment や ReplicaSet、Pod が確認できます。

```bash
$ kubectl get deployments
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
p4app   1/1     1            1           71m

$ kubectl get replicasets
NAME               DESIRED   CURRENT   READY   AGE
p4app-697568cdf7   1         1         1       72m

$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
p4app-697568cdf7-d54dq   1/1     Running   0          72m
```

!!! note "いろいろな `get`"
    リソースをサクッと一覧したい場合は、`get all` も便利です。ただし、言葉通りの完全な `all` ではなく、表示されないリソース種別もある（例えば、ラボでは触れませんが、永続ボリューム関連は表示されません）点には注意が必要です。

    ```bash
    $ kubectl get all
    NAME                         READY   STATUS    RESTARTS   AGE
    pod/p4app-697568cdf7-d54dq   1/1     Running   0          73m
    
    NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
    service/kubernetes   ClusterIP   10.4.0.1     <none>        443/TCP   97m
    
    NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/p4app   1/1     1            1           73m
    
    NAME                               DESIRED   CURRENT   READY   AGE
    replicaset.apps/p4app-697568cdf7   1         1         1       73m
    ```
    
    また、`get` にはカンマ区切りで複数のリソース種別路列挙できます。
    
    ```bash
    $ kubectl get replicasets,pods
    NAME                               DESIRED   CURRENT   READY   AGE
    replicaset.apps/p4app-697568cdf7   1         1         1       75m
    
    NAME                         READY   STATUS    RESTARTS   AGE
    pod/p4app-697568cdf7-d54dq   1/1     Running   0          75m
    ```

### アプリケーションの公開

現在はポッドがひとつのため、`[ READY ]` が `1/1` になっていますが、この段階では、まだ Web アプリケーションにはアクセスできません。明示的に操作しない限り、Kubernetes で動作したアプリケーションが外部に公開されることはありません。

では、`p4app` を外部に公開するため、**Service** をデプロイします。Service は、アプリケーションを外部に公開するために必要なリソースです。

[![image](https://user-images.githubusercontent.com/2920259/99256145-4bddeb00-2858-11eb-80e7-6dcf6f458e24.png)](https://user-images.githubusercontent.com/2920259/99256145-4bddeb00-2858-11eb-80e7-6dcf6f458e24.png)

ここではタイプとして **LoadBalancer** を指定して Service を作成します（①）。これにより、仮想ロードバランサが自動で構成され、アプリケーション（Pod）にロードバランサ経由で外部から接続できる（②）ようになります。`--port` オプションは外部に公開するポート、`--target-port` はアプリケーション側（Pod 側）のポートです。

```bash
kubectl expose deployment p4app --type=LoadBalancer --port 80 --target-port 8080
```

次のコマンドで、作成したサービスの状態を確認します。

```bash
kubectl get services
```

このコマンドで、接続に必要な情報を確認できます。`[ EXTERNAL-IP ]` 欄が `<pending>` から実際の IP アドレス
に変わるのを待って、実際にブラウザの新しいタブでこの IP アドレスにアクセスしてみましょう。

```bash
http://<EXTERNAL-IP>/
```

これで、アプリケーションが外部に公開されました。

[![image](https://user-images.githubusercontent.com/2920259/99142042-9878c900-2694-11eb-9826-a160a0725233.png)](https://user-images.githubusercontent.com/2920259/99142042-9878c900-2694-11eb-9826-a160a0725233.png)

Pod がクラスタのどのノードで動作していたとしても、IP アドレスは変わりません。この IP アドレスに対するアクセスは、Kubernetes の機能によって、Pod の居場所にかかわらず適切にルーティングされます。これは Kubernetes の強力な機能の一つです。

!!! note "Ingress"
    ここでは Service だけを利用してサービスを公開しましたが、外部からアクセスするプロトコルが HTTP または HTTPS の場合は、Service は直接はインタネットに公開せず、Service とインタネットとの間に追加で Ingress リソースをデプロイする構成も一般的です。

    このラボでは取り扱いませんが、Service は L4 相当の経路制御を担うのに対し、Ingress は L7 相当での経路制御を担います。SSL の終端のほか、ホスト名やパスベースのルーティング（アクセスされた URL に応じて、受け付ける Service を切り替える機能）などが可能です。

## アプリケーションのスケール

この段階では、Web サーバの Pod は 1 つしかないため、Service は外部からのアクセスを毎回同じ Pod にルーティングします。

ここでは、アプリケーションのスケールアウトを実際に試し、非常に簡単にロードバランスが実現できることを確認します。

次のコマンドで Deployment をスケールさせて、結果として即座にポッドが増え、Deployment の `[ READY ]` が `1/2` から
`2/2` になることを確認しましょう。

```bash
kubectl scale deployment p4app --replicas=2
kubectl get pods
kubectl get deployments
kubectl get replicaset
```

これでスケールアウトは完了です。

ブラウザで Web アプリケーションを再度開き、画面を複数回更新すると、Service によって 2 つの Pod に振り分けられていることが、ページの `Served by:` のホスト名の変化から見て取れます。

[![image](https://user-images.githubusercontent.com/2920259/99142297-0e7e2f80-2697-11eb-9d05-bf195208ee25.png)](https://user-images.githubusercontent.com/2920259/99142297-0e7e2f80-2697-11eb-9d05-bf195208ee25.png)

[![image](https://user-images.githubusercontent.com/2920259/99185286-1a97e900-278c-11eb-97f4-1952d8fa9ea2.png)](https://user-images.githubusercontent.com/2920259/99185286-1a97e900-278c-11eb-97f4-1952d8fa9ea2.png)

今回、コマンドでの `scale` は Deployment に対して行いました（①）。これによって、**レプリカが 2 つあるべき** と **あるべき状態の定義が変更** ています。そして、実際には **2 つあるべきなのに 1 つしかない** ため、**2 つある状態** に自動的に構成され、アクセス時にロードバランスされるようになった（②）ことになります。

同時に起動する Pod の数は、Deployment の下の ReplicaSet が管理しています。ReplicaSet は、指定された同時起動数を常に保とうとするため、例えばホストの障害などで Pod が 1 つ停止した場合でも、別のホストで即座にポッドが起動され、合計で 2 つのポッドが動いている状態が自動的に維持されます（**セルフヒーリング**）。また、設定すれば、ポッドの負荷状況に応じたオートスケールもも可能です。

## アプリケーションの完成

今回の `p4app` は Redis と連携することで完成するため、ここでも Redis を実際に動かしてみます。

[![image](https://user-images.githubusercontent.com/2920259/99185293-24b9e780-278c-11eb-9934-00a66b5843a4.png)](https://user-images.githubusercontent.com/2920259/99185293-24b9e780-278c-11eb-9934-00a66b5843a4.png)

次のコマンドで、Redis データベースをデプロイします（①）。6379 番ポートは、Redis のデフォルトポートです。このコマンドの結果、先ほどと同様、自動でポッドとデプロイメントが作成されます。イメージは自動的にプル（②）されます。

```bash
kubectl create deployment redis --image=redis:6.0 --port 6379
kubectl get all
```

さらに、先ほどと同様、この Redis データベースのポートを外部に公開するよう Service を作成します。ただし、今回はインタネットからのアクセスが必要なわけではなく、あくまでクラスタ内の別の Pod からアクセスできればよいだけです。

このようなクラスタ内部でのみ利用する目的では、Service 作成時のオプションには、先ほど利用した `[ LoadBalancer ]` ではなく `[ ClusterIP ]` を指定します。

```bash
kubectl expose deployment redis --type=ClusterIP --port 6379
kubectl get services
```

Service が作成されると、Service の名称は、Kubernetes が持つ組み込みの DNS サーバの機能に登録され、名前解決ができるようになります（③）。`p4app` はデフォルトでホスト名 `redis` に Redis クライアントとして接続しにいくため、コマンドでもこれに合わせた名称でデプロイしています。

ブラウザで Web アプリケーションを再度開き、ページを何度か更新して、カウンタが動作することを確認します（④）。

データベースはスケールさせていないため、Web サーバが別の Pod にロードバランスされても、カウンタの数字は一貫してインクリメントします。

## ここまででできたこと

Kubernetes クラスタを作成して、そこに任意のコンテナイメージ上にデプロイし、動作を確認しました。また、存在する各種リソースを概観し、**あるべき状態に自動で収束する** 考え方を学習しました。

[![image](https://user-images.githubusercontent.com/2920259/99185260-f63c0c80-278b-11eb-9615-7cef5f2c8e55.png)](https://user-images.githubusercontent.com/2920259/99185260-f63c0c80-278b-11eb-9615-7cef5f2c8e55.png)

[![image](https://user-images.githubusercontent.com/2920259/99185264-fdfbb100-278b-11eb-8324-9b9b38fc9f68.png)](https://user-images.githubusercontent.com/2920259/99185264-fdfbb100-278b-11eb-8324-9b9b38fc9f68.png)

その後、アプリケーションを実際にスケールさせ、簡単に外部からのアクセスとロードバランスが提供できることを確認し、データベースも追加でデプロイしてアプリケーションを完成させました。

[![image](https://user-images.githubusercontent.com/2920259/99185286-1a97e900-278c-11eb-97f4-1952d8fa9ea2.png)](https://user-images.githubusercontent.com/2920259/99185286-1a97e900-278c-11eb-97f4-1952d8fa9ea2.png)

[![image](https://user-images.githubusercontent.com/2920259/99185293-24b9e780-278c-11eb-9934-00a66b5843a4.png)](https://user-images.githubusercontent.com/2920259/99185293-24b9e780-278c-11eb-9934-00a66b5843a4.png)

内部の実装は実際にはものすごく複雑ですが、任意のコンテナを動作させて公開するだけであれば、そこまで難しいものではないことが体感できたでしょうか。
