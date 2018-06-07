# MaruCat

Maru is my cat. He is Dragon Li.

## Back-end service provider of My Blog

**定义**

这是一个用 Python 写的博客后台系统。向前端界面提供 REST 风格的 API 服务。

MaruCat 的服务内容包括文章内容（包含评论等关联内容）和一些全局的设定。

**依赖**

* **MongoDB** MaruCat 依赖 MongoDB 作为持久化层。所有数据在 MongoDB 中持久化。
* **Flask** MaruCat 使用 Flask 微服务框架提供 REST 风格 API 服务。

## MaruCat 在 Blog 整体中的位置

**定位**

MaruCat 在整个 Blog 中作为一个忠实的服务提供者存在，它的职责就是提供内容服务和一些全局设定入口服务。

整个 Blog 的系统刻意采用了前后端分离的结构，而且前端较一般的结构（同一个服务内 Web 部分使用 Ajax 调用后台服务的结构）分离的更彻底。Blog 系统使用 Node.js 运行一个中间层服务器来作为页面容器调用 MaruCat 的服务。以此来做到完全的前端后端分离。

**Notice**

个人博客的程序一般都未达到需要前端后端分离结构的量级（当然人气高的博客除外）。我的博客也不例外。

通常最简单的做法就是用 Node.js 托管页面（SPA），并且在页面中直接通过 Ajax 的方式调用后台的服务。

使用前后端分离的做法在我的博客这个量级上是大材小用的。不会使应用结构更清晰，反而会增加整体的复杂度。

仅出于学习和研究的目的使用前后端分离的结构。

## 服务内容 API

### 文章相关接口

#### 获取文章列表

```
GET /articles/list

Query parameters
    size: number, the size of list, default is 10
    page: number, the required start position, default is 1

Example:
    GET /articles/list?size=10&page=1
```

如果不给查询参数则使用默认值。

```
GET /articles/list
```

等价于下面的请求。

```
GET /articles/list?size=10&page=1
```

*状态码*

* 200 OK
    * 正常
* 400 BAD REQUEST
    * size/page 非数值
    * size/page 小于等于0


#### 获取文章内容

```
GET /articles/aid<article_id>

Parameter
    article_id: string, indentity of article

Example:
    GET /articles/aid123456
```

*状态码*

* 200 OK
    * 正常
* 404 NOT FOUND
    * article id 未赋值（response 无 error 反馈）
    * article 不存在（response 有 error 反馈）


#### 获取评论

```
GET /articles/aid<article_id>/comments

Parameter
    article_id: string, indentity of article

Query parameters
    size: number, size of comments, default is 10
    page: number, start position, default is 1

Example:
    GET /articles/aid123456/comment?size=10&page=1
```

*状态码*

* 200 OK
    * 正常
* 400 BAD REQUEST
    * size/page 非数值
    * size/page 小于等于0
* 404 NOT FOUND
    * article id 未赋值（response 无 error 反馈）
    * article 不存在（response 有 error 反馈）

#### 添加评论

```
POST /articles/aid<article_id>/comments
```

#### 删除评论

```
DELETE /articles/aid<article_id>/comments
```

### Pending

现在不确定文章内容是否在线编辑和保存，下面的接口可能不会实装。

#### 更新文章

```
UPDATE /articles/aid<article_id>
```

#### 创建文章

```
POST /articles/aid<article_id>
```

#### 删除文章

```
DELETE /articles/aid<article_id>
```

### 全局设定接口

#### 获取设定

```
GET /settings
```

#### 更新设定

```
UPDATE /settings/<items>
```

## 发布&部署

待定

## 相关文档

* [部署 MongoDB 环境（本地环境和服务器环境）](docs/deploy-mongodb.md)
* [在 Flask 框架创建 RESR API 的过程和疏通](docs/create-rest-api.md)

