---
layout: post
title: Procalator 学习笔记
modified:
categories: nocategories
excerpt:
tags: []
comments: true
image:
  feature:
  date: 2016-11-16T17:53:58-010:00
---

# Distributed Transactions

> ACID operations for transactions(Atomic)
> Serializable

## Serializability Review

Any history of executions(set of transactions) should has same effect on the databse and produce same result as some **serial execution** of the same set of transactions

* Obey completion to issue order in the original execution history.(strict serializability)

### Related to linearizability

## Why distribution

- Scale performance: Not sufficient storage/computation resource on one Machine.
- Fault Tolerence

## Review: Design for single machine transactions

```
begin_tx
	read
	write
	commit
end_tx
```

```
begin_tx
	read & write phase:
		tx <- tx.context
		Lock(a) //return to the user
		Lock(b) //buffer the writes
	
	commit phase:
		log tx.writes
		for each x in buffer:
			write(x.key) = x.value
			Unlock(x.key)
end_tx
```

### Example

T1: W(a=1), W(b=1)

> May crash between writes

## Distributed Setting

### Shard our data 

### example

- ServerA for object A
- ServerB for object B

client/coordinator for transaction

initial state a = b = 0

exmpale: T1: W(a=1), W(b=1)

send write and do it immediately

- send(w(a==1))
- serverA.lock(a)
- serverA.log(a==1)
- serverA.write(a)

- client may crash
- two t_xs can interleave each other

Solution: 2PC

- Prepare phase:
	- ServerA.lock(a)
	- ServerA.log(a=1)
	- ServerB.lock(b)
	- ServerB.log(b=1)
- Commit phase:
	- ServerA.write(a=1)
	- ServerA.unlock(a)
	- ServerB.write(b=1)
	- ServerB.unlock(b)

### 2PC's problem

If a call is timeout:

1. Coordinator can unilaterally abort
	- if coordinator dies, outcome of a tx
	- new solution
		- log decisions to paxos
		- then decide on abort/commit
		- then send 2p-commit or abort
2. Coordinator can not unilaterally abort
	- if any of the server dies, outcome of a tx ?

# Percolator

> bootstrap(GFS) => Bigtable => Percolator

## Before google

Distributed transactions 

crawling => processing crawled documents => generated inverted index

```
insert_doc(doc) {
	content_table.put(doc.url, doc.contents);
	hash = md5sum(doc.contents);
	canonical_url = dups_table.get(hash);
	if (!canonical_url || canonical_url > doc.url) {
		dups_table.put(hash, doc.url);
	}
}
```

What can go wrong in the above code?

* Failures example.
	- doc inserted, but does not appear in the collection of canonical urls 
* Concurrency example:
  - two concurrent inserts of nyt.com nytimes.com

Why transactions help?

Why do they need distributed transactions?

Why does Percolator decide to support SI instead of serializability?
- avoid read locks so that transactions can read lots and lots of data cheaply

How to implement SI in a distributed setting?

```
begin_tx() {
	tx.start_ts = get_timestamp()
}

/**
	normal read like other SI system.
*/
read(key) {
	//issue key to the server responsible for key
	//At server
	versioned_data = db[key]
	v = highest version smaller than tx.start_ts in versioned_data
	return v.data
}

write(key, value) {
	tx.writes[key] = value
}

commit_tx(tx)  {
	foreach w in tx.writes 
		issue 2PC_prepare to server responsible for w
	if (all replies are okay) {
		tx.commit_ts = get_timestamp()
		foreach w in tx.writes 
			issue 2PC_commit to server responsible for w
	} else {
		foreach w in tx.writes 
			issue 2PC_abort to server responsible for w
	}
}

on_2PC_prepare(tx, w) {
	lock(w.key)
	if lock is unavabile 
		return 2PC_vote_no;
	//check for write-write conflict
	if there exists db[key] whose version is greater than tx.start_ts
		return 2PC_vote_no;
	log(tx.id, w.key,w.data);
	return 2PC_vote_yes;
}

on_2PC_commit(tx, w) {
	w.version = tx.commit_ts;
	add w to db[key]
	unlock(w.key)
}
```

Percolator is built on top of BigTable (a versioned multi-coloumn key-value store). 
How is its design different from one outlined above?

Let's look at Pseudocode for Perrcolator in Figure 6?

* pre-write is similar to the prepare phase in 2P commit.
  -  why line 32? (check for write-write conflict)
	- why line 34? (concurrent 2P commit on overlapping data)
* commit() 
	- can I move line 48 to after 43? 
	- ignore line 53 for now
	
How does Percolator handle failures?

* data is replicated by BigTable, hence no logging is necessary (BigTable internally logs)
* But, transaction coordiator (Percolator worker) can fail.
  Consequence: locks held during 2P commit are never cleaned up.
	The idea: if other workers notice that a lock is held for a long time, it cleans up.
	Challenge: what if B thinks A is dead but A is not dead and still in the process of committing?
	
Percolator solution: 

- Every transaction corresponds to a primary lock.
- All other locks in a transaction point to its primary lock. 
- Commit replaces the primary lock with a write record
- Cleanup erases the primary lock if it's still there.
- Access to primary lock is synchronized by the underlying BigTable single row transaction.