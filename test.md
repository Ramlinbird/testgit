### Abstract

The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer,
based solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show these models to
be superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-
to-German translation task, improving over the existing best results, including
ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task,
our model establishes a new single-model state-of-the-art BLEU score of 41.8 after
training for 3.5 days on eight GPUs, a small fraction of the training costs of the
best models from the literature. We show that the Transformer generalizes well to
other tasks by applying it successfully to English constituency parsing both with
large and limited training data.

亮点：1. 完全基于Attention的模型架构，区别于传统的RNN/CNN；2. 支持并行化，训练高效；3. 实际表现优异。

### Introduction

从RNN引入，指出了RNN由于天生的顺序时间依赖所带来的训练代价，借此引出了经常一起使用的Attention机制，并提出一种新的模型框架——**Transformer**，仅仅基于Attetention，能够实现更高效、更优秀。

### Backgrounnd

谈到了同样可以实现并行的CNN，但是CNN只能获取局部信息，通常要通过层叠来扩大感受野。相比之下，Attention一步到位，能够直接获取全局信息，更加高效。

### Model Architecture

![image-20190729222035894](/Users/pengyiyu01/Library/Application Support/typora-user-images/image-20190729222035894.png)

**Transformer**整体框架如上图，分为左侧的Encoder和右侧的Decoder，都堆叠了多层。下面就模型中涉及的细节进行介绍。

##### Scaled Dot-Product Attention

论文使用的Attention是**Scaled Dot-Product Attention**，公式如下：

$$ Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d_k}})V \tag{1} $$

另外一种常见的Attention是**Additive attention**，是通过一个前馈神经网络来计算softmax里的分数值。两者理论复杂度接近，**Dot-Product Attention**实践更高效，矩阵优化比较好。当$$d_k​$$很大时，会导致$$softmax​$$初始值落在梯度极小的区域（$$d_k​$$很大，假定$q​$和$k​$是互相独立的0均值1方差的随机变量，此时$q\cdot k​$为0均值$d_k​$方差），难以优化，为了消除该负面影响而引入上式的$$\frac{1}{\sqrt{d_k}}​$$，这也正是**Scaled**的名称来源。

##### Multi-Head Attention

![image-20190730211137674](/Users/pengyiyu01/Library/Application Support/typora-user-images/image-20190730211137674.png)

可以看到**Multi-Head Attention**就是先将Q/K/V经过不同的**head**矩阵W转换到不同表达子空间，分别做Scaled Dot-Product Attention，得到结果再拼接在一起，最后过一个非线性转换得到最后的输出。从公式理解更加直观，如下：

$$MultiHead(Q,K,V)=Concat(head_1,...,head_h)W^O \\ where \ head_i=Attention(QW_i^Q,KW_i^K,VW_i^V) \\ W_i^Q \in R^{d_{model} \times d_k},\ W_i^K \in R^{d_{model} \times d_k}, \ W_i^V \in R_{d_{model}\times d_v}, \ W^O\in R^{hd_v\times d_{model}}$$

注：这里的多头注意力还带来一个好处，相比在原本$d_{model}​$的高维空间，每个头都经过了降维，计算效率更高。

##### Applications of Attention in our Model

**Transformer**框架中主要有3处利用到了Multi-head Attention机制，

1. 解码层中，decoder对encoder的attention；
2. encoder中的自注意力（self-attention）；
3. 解码层中，当前解码对已经解码的masked attention。

##### Position-wise Feed-Forward Networks

对Attention子模块的输出再经过变换，公式如下：

$$FFN(x)=max(0,xW_1+b_1)W_2+b_2 \tag{2}$$

变换矩阵在不同位置共享（可以通过卷积实现），在不同层之间独立。

