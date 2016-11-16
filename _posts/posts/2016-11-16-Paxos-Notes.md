---
layout: post
title: Paxos 学习笔记
modified:
categories: nocategories
excerpt:
tags: []
comments: true
image:
  feature:
  date: 2016-11-16T09:27:58-010:00
---
## 要解决什么问题？(Consensus Problem)

本质上来说就是投票问题，分为三个角色，Proposer，Acceptor，Learner。 Proposer可以propose一些值，然后Acceptor可以接受一些值，Learner可以记住一些值。目标是：

- 最终只产生一个值
- 产生的值必须是propose的值其中一个
- 这个值得被记住

### Liveness/Safety

- Liveness: 必须得选出一个值
- Safety: 选定了之后不会变

> **实际上一个Process可能同时扮演三个角色，但是每个Agent都可能fail (not be accuratelly detected**

### Asynchornous network communication assumption
> An RPC time can mean

> - node failed
> - node is very slow
> - network is slow
> - network has partition


## 几个Naive模型

1. 只有一个Acceptor：
	- Acceptor死了就GG了。
2. 多个Acceptor，当足够多的Acceptor都接受了一个值的时候，就选择这个值
	- 可以，但是每个Acceptor只能接受一个值。
	- 每个Acceptor只接受一个值，当一些Acceptor死了，就影响Majority了，所以没法记住。

	> 由此推断当需要选择Majority的时候，Acceptor需要接受不止一个值。

### Strawman #1

S1, S2, S3

- every node sends its value to all others
- Wait to receive all 3 values, pick one w/ smallest node_id.

> 死了一个node，第二步就永远到不了了，就GG了 (liveness GG了）

### Strawman #2

- every node sends its value to all others
- node chooses the first value, reject the rest.
- if the original proposer has more than half nodes chooses value v, then decided on v.
- send victory msg.

> 问题是可能选不出majority (liveness GG了）

### Strawman #3, based on Strawman #2

- if a node has not seen a victory-msg in 10 sec, forget its accepted value.

> 问题是victory msg may fail（不能依靠对于时间的任何假设）

## 需求推断

```
P1. An acceptor must accept the first proposal that it receives 
```
3. 除了发送值，还发送Proposal Number
	- 先假设每个Proposal的Proposal Number不同

```
P2. If a proposal with value v is chosen, 
then every higher-numbered proposal that is chosen has value v.
```

> 在proposal number有序的情况下，这保证了总是选择相同的值，因为一个值必须要Accpetor接受之后才能被选择，所以P2a也可以满足P2。

```
P2a. If a proposal with value v is chosen, 
then every higher-numbered proposal that is chosen has value v.
```

然而一个Acceptor如果没有接受过旧值，那么就有可能接受一个新的错值，所以需要加强P2a到P2b

```
P2b. If a proposal with value v is chosen, 
then every higher-numbered proposal issued by any proposer has value v.
```
> 显然P2b保证了P2a，也就保证了P2

**所以问题变成了如何实现P2b**

## 如何证明P2b保证了我们的目标
假设某一个proposal number m，我们选择了value v， 那么我们需要证明对于某个n>m，我们也会选择v。
因为m的时候选择了v，所以对于Acceptor里选择了v的majority来说，一定在m~(n-1)里的某一个proposal number选择了v。
考虑一个

```P2c. For any v and n, if a proposal with value v and number n is issued, 
then there is a set S consisting of a majority of acceptors such that either 
(a) no acceptor in S has accepted any proposal numbered less than n, or 
(b) v is the value of the highest-numbered proposal 
among all proposals numbered less than n accepted by the acceptors in S.
```

## Paxos

### 3 Phase protocol

- to obtain prviously major accepted value
- to seek majority accpted value
- to tell others decied values.

### Multiple rounds

### Majority acceptance prevents "split-brain"

## Proposer算法

两种request：Prepare & Accept

### Prepare Request

1. 选定proposal number n;
2. 告诉一些Acceptor， 不要再接受比n小的proposal了
3. 让这些Acceptor告诉我现在自己的接受的小于n的最高的proposal number对应的值是多少。

> 我们可以称之为 \\(prepareRequest(n)\\)

### Accept Request

接收到一个majority的response之后，就可以用n作为proposal number来发值了，但是v必须是response里proposal number最高的那个proposal对应的value，所有response里都没值，就可以自己选择了。

> 我们可以称之为 \\(acceptRequest(n,v)\\)

发送这个(n,v), 就是一个Accept Request，但是这个request不一定要发送给Prepare Request的Set，可以有区别。

## Acceptor算法

我们需要考虑Acceptor面对两种request时候要如何做出选择，具体如下：

```
P1a . An acceptor can accept a proposal numbered n iff 
it has not responded to a prepare request having a number greater than n.
```

就是说，没有回复 \\(prepareRequest(m), m > n\\) 时，就可以接受 \\(n\\) 传过来的值。之所以叫P1a是因为P1a实际上是P1的子集。

> 所以当已经回复了 \\(prepareRequest(m), m > n\\) 时，\\(prepare(n)\\) 就可以直接忽略。
> Acceptor 只需要记住自己接受过的最大的n，及其对应的v。

## 流程总结

### Phase1

1. \\( prepareRequest(n) \\)
2. Acceptor responses promise or ignore it based on the largest \\(n'\\) it got.

### Phase2

1. Proposer receives enough responses(majority), \\(acceptRequest(n,v)\\). v是response里proposal number最大的，response都是没有值的话，自己选一个。
2. Acceptor没有response给一个比n更高prepare请求的时候，就接受v。

### Phase 3
1. 收到Majority水平的accept_ok, \\(decide(v')\\), send \\(decide(v')\\) to all others.

## Proposal Number

n must be unique among all nodes.

## Paxos' invariansis

- if value v is accepted by majority at round nthen all round \\(n' > n\\) propose v.

## Pseudocode

At proposer:

```
choose n (unique & higher than any seen n)
send prepare(n) to all including self
if prepare_ok(n,n_a,v_a) from majority
	v' = v_a with highest n_a or choose arbitary v if all v_a ==  nil
send accept(n,v') to all
if accpet_ok(n) from majority
	decide on v'
	send decide (n,v')
```

Acceptor OnPrepare(n)

```
if n > n_h
	n_h = n
	reply prepare_ok(n,n_a,v_a)
else reject
```

Acceptor onAccept(n)

```
if n >= n_h
	n_h = n
	n_a,v_a = n, v
	reply ok
else reject
```


> What state mu be persisted across reboot?

