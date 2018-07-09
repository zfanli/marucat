# 从需求来看 MongoDB

## Introduction

从需求来看 MongoDB，了解能满足我们需求的最少量用法。

面向 MongoDB 的初学者。第一次阅读建议阅读全文，之后建议检索关键字或者根据索引按需阅读。

这一次我们使用 MongoDB 来储存文档，制作一个博客网站。

我们要了解文章、评论和设定，诸如此类的数据，如何储存在 MongoDB，以及如何使用和更新它们。

本文讨论的内容：

- 设计符合需求的数据结构
- document 的增删改查
- 计划获取的字段或内容
- 查询和过滤内嵌数组

基本上，就是入门知识。

## 最简内容索引

- find 查询
- project 计划字段
- update 更新
- delete 删除
- aggregate 聚合

## 设计符合需求的数据结构

<!-- TODO -->

## document 的增删改查

### 连接 MongoDB

这是一个连接 MongoDB 的示例代码，主要用来定义几个变量方便下面使用。

```python
from pymongo import MongoClient


mc = MongoClient() # connect to default client
db = mc['test'] # use 'test' database
col = db['test-collection'] # use 'test-collenction' collection

```

### find 查询

查询是使用数据库的基础需求。

```python
# Query for only one document
col.find_one({
    'some_fields': 'values',
    'array_fields': ['value1', 'value2'],
    'object_fields': {'keys': 'values'}
})
# Query for one or more than one documents
col.find({
    'some_fields': 'values',
    'array_fields': ['value1', 'value2'],
    'object_fields': {'keys': 'values'}
})
```

上面的例子我们可以了解到，传给查询方法的第一个参数即为查询的条件。

这个参数是一个 `dict`，或者 JS 中叫做对象。

在 SQL 中，这样的操作对应 `select * from ... where ...`。

#### project 计划字段

MongoDB 中，find 默认拉取整个 document 作为输出。

但处于带宽和性能考虑，有时我们不需要这么多数据，我们仅需求我们需要的字段。

`project` 帮我们解决问题，我们可以声明需要或者不需要哪些字段。

传给 find 方法的第二个参数将被视为 `projection`，同样它需要是 `dict`。

```python
col.find(
    {},
    {
        'title': 1,
        'author': 1,
        'content': 1,
    }
)
```

像上面这样，在第二个参数中列出需要的字段名，并将其值设为 `1`。

`1` 的意思就是**包含**，这样 MongoDB 就可以理解我们的需求，仅取出需要的字段。

还可以这样写。

```python
col.find(
    {},
    {
        'comments': 0,
        'timestamp': 0,
        'reviews': 0,
    }
)
```

`0` 表示**不包含**。我们也可以告诉 MongoDB 不要哪些字段。

这样它取出来的文档里面就会包含除了我们声明了不包含的其他所有字段，这在一些场景下很有用。

`_id` 字段是默认会被取出的，即使你告诉它需要的参数里没有列出它。

如果你实在不想看到它，可以在 `project` 里将它设为 `0`，它就不会出现了。

```python
col.find(
    {},
    {
        '_id': 0,
        'title': 1,
        'author': 1,
        'content': 1,
    }
)
```

**但是注意，除了 `_id` 以外，包含（`1`）和不包含（`0`）是不能同时出现的，否则你会得到下面这个错误。**

```
pymongo.errors.OperationFailure: Projection cannot have a mix of inclusion and exclusion.
```

所以记住，对于 `_id` 来说，想要不显示它需要手动设置为 `0`。

对其他字段来说，要不就告诉 MongoDB 需要哪些字段，要不就告诉它不需要哪些，同时声明需要和不需要的字段将会报错。

#### project 进阶

`project` 有更实用的功能，相应也会更复杂一些。

当查询一个数组对象时，有时我们有更多的需求。

比如做评论的分页时，我们不需要一次性取出这个文章的所有评论，我们只需要指定的几个。

```python
col.find(
    {},
    {
        # Fetch the 0-3 of comments
        'comments': {
            '$slice': 3
        }
        # Fetch the 2-6 of comments
        'comments': {
            '$slice': [2, 6]
        }
        # Fetch the last comment
        'comments': {
            '$slice': -1
        }
    }
)
```

上面的例子分别从评论数组中取出前三条、第2到第6条和最后一条评论。

或者，有时我们仅需要取出符合要求的第一个评论，

```python
col.find(
    {},
    {
        # Fetch the first deleted comment
        'comments': {
            '$elemMatch': {
                'deleted': True
            }
        }
    }
)

col.find(
    # Fetch the first element matched the condition
    {
        'comments': {
            'deleted': True
        }
    },
    {
        'comments.$': 1
    }
)
```

上面这两个查询的效果一样，获取评论数组中满足被删除这个条件的第一条评论。

但上面这个匹配实际上用处有限，通常我们需要取出满足条件的多条评论，而不仅仅是符合条件的第一条。

`project` 有办法实现，但却不是在 find 方法中，在 `aggregate` 中我们继续讨论如何使用 `project` 满足需求。

目前为止涉及的文档：

- [Query Documents](https://docs.mongodb.com/manual/tutorial/query-documents/)
- [Project Fields to Return from Query](https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/)
- [collection – Collection level operations - find()](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find)
- [collection – Collection level operations - find_one()](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find_one)

### update 更新

修改已有的数据是普遍的需求。

在博客中，用户主动或者被动的操作都会触发数据的更新。

比如用户打开一篇文章，我们需要更新这篇文章的浏览数；用户赞了这篇文章，我们需要更新这篇文章的点赞数。

当我们自己要在线编辑一篇文章并且发布更新，后台的服务器就要运作起来将我们的输入都正确更新到数据库中。



## aggregate 聚合

当我们需要在查询中做一些数据分析或者一些更精细的操作时，我们将感受到 find 方法的局限性。

我们如何实现对应 SQL 中的 `GROUP BY` 和 `SUM()` 等实用功能？

`aggregate` 帮我们做到这些。

## 总结

切实需要的东西才能在我们的记忆中保留一席之地，过多实际用不到的，或者近期用不到的信息，只会让记忆系统趋于混沌。

目前我们已经了解了足够的知识来使 MongoDB 为我们所用了。

等到需求或者求知欲继续延伸，就是进一步学习的最好时机。
