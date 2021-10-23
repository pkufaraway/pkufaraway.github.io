---
layout: default
title: lombok + jackson
modified: null
categories: tech
excerpt: null
tags: []
date: 2021-10-23T15:08:28-07:00
---

之前知道google有个annotation叫[autovalue](https://github.com/google/auto/tree/master/value/src/main/java/com/google/auto/value), 作用就是方便构造value class，比如自动添加builder/getter/setter。对于google来说，复杂的数据往往都是用[protobuf](https://developers.google.com/protocol-buffers)，因为protobuf不仅提供了builder/setter/getter，而且可以跨多个编程语言通用，更重要的是可以提供简单方便地serialization/deserialization的功能。

一直以来我都知道JSON是很普遍的结构数据表示方式，但是没怎么研究过在JSON的世界里有没有类似protobuf的功能，但是显然JSON只是个轻量级的表示法，并不会通过一个额外的结构语法（像protobuf那样先写一个定义文件）从而生成各个编程语言的对应代码。既然如此，我猜JSON至少需要我写一个模板，或者退一步说，只要我写好了一个文件有哪些变量，就应该可以按照这个文件来serialize/deserialize JSON.

那么究竟是否存在现成的工具么？还真有。小臭今年的课程里老师提到了一个类似autovalue的框架叫[lombok](https://projectlombok.org/)，MIT license。起初我只是意识到lombok比autovalue有更多方便的annotation，之后一次小臭开会后告诉我老师提到JSON Parser可以更通用，我意识到没准说的就是我上面提到的只写模板的模式。

于是乎发现了lombok的jacksonized, 以coindesk这个[比特币价格api](https://api.coindesk.com/v1/bpi/currentprice.json)为例, 我简单取其中一部分：
```json
{
    "code": "USD",
    "symbol": "&#36;",
    "rate": "61,329.4033",
    "description": "United States Dollar",
    "rate_float": 61329.4033
}
```
我需要一个price class表示它，想要支持lombok和json，只要简单加几个annotaiton就行。
```java
package bitcoin;

import lombok.Builder;
import lombok.Data;
import lombok.extern.jackson.Jacksonized;

@Builder
@Data
@Jacksonized
final class Price {
    private String code;
    private String symbol;
    private double rate;
    private String description;
    private double rate_float;
}
```
那么如果我想解析这段json，只需要如下代码：
```java
package bitcoin;

import static org.junit.jupiter.api.Assertions.assertEquals;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

final class PriceTest {
    private static final String PRICE = "{ \"code\": \"USD\", \"symbol\": \"&#36;\","
            + "\"rate\": \"61,329.4033\", \"description\": \"United States Dollar\","
            + " \"rate_float\": 61329.4033 }";

    @Test
    public void testAdd() throws Exception {
        Price price = new ObjectMapper().readValue(PRICE, Price.class);

        Price expectedPrice = Price.builder().code("USD").symbol("&#36;").rate("61,329.4033")
                .description("United States Dollar").rate_float(61329.4033).build();

        assertEquals(price, expectedPrice);
    }
}
```

如此一来对于不同JSON，只需要写一个简单的data class辅之以lombok annotation就好了。
