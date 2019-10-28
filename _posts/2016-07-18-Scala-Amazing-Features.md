---
layout: post
title: Internship Tech Review (1) - Scala is Amazing!
modified: null
categories: tech
excerpt: null
tags: []
comments: true
image: null
feature: null
date: 2016-07-19T07:27:58.000Z
---

## The main purpose of this series

As my internship is nearly finished, I decide to write a tech-review for all the amazing features that I have learnt during this summer.

Today I gonna talk about some important features that I've learnt in Scala.

Scala is really amazing! Although Java8 has come with lambda feature, Scala look more beatiful. Since most people will still use Java in old style, most Java code looks aweful.

## The most common function I used in Scala: Map

map is a useful function that you can use, it can be used to convert `Collection[A]` to `Collection[B]`, such as:

```scala
scala> val a = List(1,2,3)
a: List[Int] = List(1, 2, 3)

scala> a.map(x => x + 1)
res3: List[Int] = List(2, 3, 4)

scala> a.map(_+1)
res4: List[Int] = List(2, 3, 4)
```

From the above example you can see that you can use `_` if you don't want to use an arrow(for example, call a method belongs to every element).

On the other hand, you can use map with pattern matching.

```scala
scala> a.map{
     | case x if x%2 == 0 => true
     | case x if x%2 == 1 => false
     | }
res5: List[Boolean] = List(false, true, false)
```

## Absolutely, pattern matching is so cute

Scala has an important object called Option, Option is a brilliant choice for something that can be null, for example:

```scala
scala> val b = Option(1)
b: Option[Int] = Some(1)
```

When you want to figure out whether a val is parameter or not, just use match:

```scala
scala> def reveal(a : Option[Int]) : String = {
     | a match{
     | case Some(s) => s.toString
     | case None => "None"
     | }
     | }
reveal: (a: Option[Int])String

scala> reveal(b)
res7: String = 1

scala> reveal(None)
res8: String = None
```

Keep using Option can help you to deal with any kind of data that can be null, you won't need to worry about using `a == null` any more.

## The lovely fold series function

What will you do to sum a `List[int]`? For most programming language, you may expect that the class `List` has an inner method to do, or some existing lib to use. What if I only want to sum all the even numbers? There is no easy way to do that for traditional language. How to do that in scala?

```scala
scala> val a = List(1,2,3,4,5)
a: List[Int] = List(1, 2, 3, 4, 5)

scala> a.fold(0){
     | case (sum,x) if x%2==0 => sum + x
     | case (sum,x) => sum
     | }
res1: Int = 6
```

You may think that it looks not simple enough compare to a for loop, But how about more complex logic during this `fold`?

The number 0 after fold is the basic value for sum, and I use pattern matching here too.
