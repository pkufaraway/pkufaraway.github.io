---
layout: default
title: code-server
modified: null
categories: tech
excerpt: null
tags: []
date: 2021-05-02T23:49:34-07:00
---

# `code-server`
随着IDE as web的越来越兴起，我最近开始研究用chrome写代码了，搜索之下，发现了开的[code-server项目](https://github.com/cdr/code-server)。项目本质上是给开源的Visual Studio Code做了一个前段，这样任何人可以在任何浏览器里打开VS Code写代码。

# 几个东西之间的关系
一般意义上提到VS Code的时候，我们理解的是微软出品的一款编辑器/IDE，但是这款IDE本质上还有一个开源项目在支持核心部分。核心部分就是https://github.com/microsoft/vscode， 往往被称作`Code - OSS`， 而微软自己在这个项目的基础上开发了自己的distribution，这个distribution才是我们日常提到的VS Code。`code-server`是根据`Code - OSS`开发的IDE as Web，所以很多微软distrubtion的原生功能是不支持的，比如登陆账号同步设置，比如不许安装某些微软开发的插件。

# 插件，最痛的地方
除了插件以外，几乎各个地方都让人满意，我认为这是IDE发展的方向：
- 真正的runtime和lib都在云端，例如jdk
- 一切通过web来链接，云端负责运算
- 简单好用的web ide提供随时随地的开发环境

code-server最痛的地方就是无法提供和VS Code一样的插件市场，但是我相信随着IDE as web的越来越流行，微软会意识到这片市场的重要性。

