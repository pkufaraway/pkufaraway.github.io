---
layout: post
title: Internship Tech Review (2) - Scala is Amazing(2)!
modified:
categories: nocategories
excerpt:
tags: []
comments: true
image:
  feature:
  date: 2016-07-30T02:27:58-05:00
---

## The main purpose of this series
As my internship is nearly finished, I decide to write a tech-review for all the amazing features that I have learnt during this summer.

Today I gonna talk about some important features that I've learnt in Scala.

Scala is really amazing! Although Java8 has come with lambda feature, Scala look more beatiful. Since most people will still use Java in old style, most Java code looks aweful.

### Works happier with Java
Collection convertion: scala collection to java collection are not that hard, all you need to know is `import collections.JavaConverters._` and `asJava/asScala`, such as:

```scala
scala> import collection.JavaConverters._
import collection.JavaConverters._

scala> val a = List(1,2,3).asJava
a: java.util.List[Int] = [1, 2, 3]

scala> a.asScala
res1: scala.collection.mutable.Buffer[Int] = Buffer(1, 2, 3)

scala> a.asScala.toList
res2: List[Int] = List(1, 2, 3)
scala>
```
This is so convenient! And it converts very fast!

### Option again, prevent using `a==null`
Option is an function, given a return value that could be `null`, you can always use an Option to deal with it. For example:

```scala
scala> val a = Option(null)
a: Option[Null] = None

scala> val b = Option(123)
b: Option[Int] = Some(123)
```
Which means even you got some value from other methods, such as an Java methods which possibly return a value of `null`, you can use `Option` to easy deal with it, and it can be as cute as:

```scala
scala> a.getOrElse(println("error"))
error
res5: Any = ()

scala> b.getOrElse(println("error"))
res6: AnyVal = 123
```
### Head/Tail, if you like

```scala
scala> val a = List(1,2,3)
a: List[Int] = List(1, 2, 3)

scala> a.head
res7: Int = 1

scala> a.tail
res8: List[Int] = List(2, 3)
```
It's always easy if you want to use this to deal with iteratable collections.


