<h1 align="center">MaruCat</h1>

<div align="center"> Maru is my cat's name. He is Dragon Li.</div>

<br>

<div align="center"><img src="./docs/marucat.svg"></div>

## 定位

> MaruCat is a Back-End service provider of my blog.

MaruCat 是基于 Python 的博客后台程序。

其功能是向前端程序提供 REST 风格的 API 服务。

API 内容：

* 文章和评论相关 API
* 全局设定相关 API

## 依赖

**🍃MongoDB**

MaruCat 依赖 MongoDB 作为持久化层。所有数据在 MongoDB 中持久化。

**🌶️Flask**

MaruCat 使用 Flask 微服务框架提供 REST 风格 API 服务。

## 关于 Blog

**结构**

Blog 前后端分离（🌟）。

前端 UI 使用 React 构建，运行在基于 Node.js 服务器上。

这个服务器作为中间层来调用 MaruCat 的 API。

后端服务提供者，MaruCat 仅关注 API 和数据库操作。

> 🌟：出于学习与研究目的。对 Blog 来说不分离的做法会更简洁。

## API USAGE

### 📝文章相关

包括操作文章和评论的 API。

#### 获取文章列表

```
GET /articles/list

Query parameters
    size: number, fetch size, 10 by default
    page: number, fetch start position, 1 by default

Example:
    GET /articles/list?size=10&page=1
```

可以不给查询参数。

```
GET /articles/list
```

不给查询参数将等价于下面的请求。

```
GET /articles/list?size=10&page=1
```

##### 状态码

* ✔️ 200 OK
    * 正常
* ✖️ 400 BAD REQUEST
    * size/page 非数值
    * size/page 小于等于0

##### 数据结构

```python
[
     {
        # ID
        'aid': 'ID_OF_ARTICLE',
        # Author
        'author': 'THE AUTHOR',
        # Abstraction
        'peek': 'A peek of the content of requested article.',
        # Counts of views
        'views': 998,
        # Counts of comments, use reviews because of short
        'reviews': 8,
        # Timestamp for created or updated
        'timestamp': 1528969644.344048
    },
    # ...
]
```

#### 获取文章内容

```
GET /articles/aid<article_id>

Parameter
    article_id: string, identity of article

Example:
    GET /articles/aid123456
```

##### 状态码

* ✔️ 200 OK
    * 正常
* ✖️ 404 NOT FOUND
    * article id 未赋值（response 无 error 反馈）
    * article 不存在（response 有 error 反馈）

##### 数据结构

```python
{
    # ID
    'aid': 'ID_OF_ARTICLE',
    # Author
    'author': 'THE AUTHOR',
    # Full content
    'content': 'Full content of requested article.',
    # Counts of views
    'views': 241,
    # Timestamp for created or updated
    'timestamp': 1529029508.939738
}
```

#### 获取评论

```
GET /articles/aid<article_id>/comments

Parameter
    article_id: string, identity of article

Query parameters
    size: number, fetch size, 10 by default
    page: number, fetch start position, 1 by default

Example:
    GET /articles/aid123456/comment?size=10&page=1
```

##### 状态码

* ✔️ 200 OK
    * 正常
* ✖️ 400 BAD REQUEST
    * size/page 非数值
    * size/page 小于等于0
* ✖️ 404 NOT FOUND
    * article id 未赋值（response 无 error 反馈）
    * article 不存在（response 有 error 反馈）

#### 添加评论

```
POST /articles/aid<article_id>/comments
```

##### 状态码

* ✔️ 201 CREATED
    * 正常

#### 删除评论

```
DELETE /articles/aid<article_id>/comments
```

##### 状态码

* ✔️ 200 OK
    * 正常

### Pending

现在不确定文章内容是否在线编辑和保存，下面的接口可能不会实装。

#### 更新文章

```
PUT /articles/aid<article_id>
```

##### 状态码

* ✔️ 200 OK
    * 正常

#### 创建文章

```
POST /articles/aid<article_id>
```

##### 状态码

* ✔️ 201 CREATED
    * 正常

#### 删除文章

```
DELETE /articles/aid<article_id>
```

##### 状态码

* ✔️ 200 OK
    * 正常

### ⚙全局设定

操作设定的 API。

#### 获取设定

```
GET /settings
```

##### 状态码

* ✔️ 200 OK
    * 正常

#### 更新设定

```
PUT /settings/<items>
```

##### 状态码

* ✔️ 200 OK
    * 正常

### Models

#### Articles

```python
{
    'aid': 'ID of article',
    'author': 'AUTHOR',
    'peek': 'A peek of content.',
    'content': 'The content of article.',
    'views': 999,
    'comments': [
        {
            'aid': 'ID of article',
            'cid': 'ID of comment',
            'body': 'Content of comment.'
        }
    ]
    'deleted': False
}
```

## 发布&部署

// TODO

## 相关文档

* [部署 MongoDB 环境（本地环境和服务器环境）](docs/deploy-mongodb.md)
* [在 Flask 框架创建 REST API 的过程和疏通](docs/create-rest-api.md)

