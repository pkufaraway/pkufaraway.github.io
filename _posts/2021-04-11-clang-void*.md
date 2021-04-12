---
layout: default
title: clang void*
modified: null
categories: life
excerpt: null
tags: []
date: 2021-04-12T04:47:18-07:00
---

## 万能的 `void*`

`void*` 可以表示任何类型数据的指针，然后可以通过 `(type *)` 再反向转化成我们想要的类型。比如：

``` c
int *int_p;
void *void_p;
void_p = int_p;
int *int_p2 = (int *)void_p;
```

可这有什么用？在这学期和小臭一起学习clang的过程中，我意识到我以前一直不懂clang如何实现多态，至少如何用一个类型表示多个类型？通过这个学期的学习我意识到`void*`就是一个非常简单的解决办法，比如我想定义一个Key-Value Pair：
```c
typedef struct {
  char      *key;    // the key in the key/value pair
  void      *value;  // the value in the key/value pair
} KeyValue, *KeyValuePtr;
```
因为我可以用`void*`，我就可以让value是任何类型，获得value的时候，用户可以通过自己的方法把value转化成任意类型。不过显而易见，`void*`不像我以前学过的java多态，在编译的时候就可以发现问题，因为转换的过程是不安全的，想做到安全的转换需要使用者非常熟悉自己当初给某一个`void*`赋值的类型，并且始终记住，并且始终不忘记在使用的时候争取转换。

## 这是否是clang没有很多自带数据类型的原因？
长久以来我认为clang主要的思维方式是面向过程，或者说，clang的编写过程是组织函数们，把函数们放在不同的文件里，把围绕着这些函数的数据类型定义也分开来是主要的设计思想。但是最大的问题仍然是`void*`，尽管我们有了封装继承(struct)还有多态(void*)，但是因为`void*`的用法实在是太不安全了，这实际上是提高了对使用者的要求和门槛，使得把clang写的更面向对象是非常困难和难以理解的。也许这也是clang没有太多自带数据类型的原因吧。
