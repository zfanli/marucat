# RESTful API

REST 是表现层状态转移的缩写，虽然名称不好理解，但这是一个简单并且实用的概念。

```
REST : REpresentational State Transfer
```

RESTful API 关注下面三点：

1. URL 定义资源位置
2. HTML 动词定义对资源的操作
3. 返回状态码定义操作的结果

REST 的概念翻译成通俗易懂的人类语言大概是这样的：

> 告诉你我要的资源（URL），告诉你我要对这个资源做什么（GET、POST、UPDATE、DELETE），告诉我结果（状态码和响应内容）。

是不是感觉对要做的事情描述得很清晰？这就是 REST 的效果。

MaruCat 将实现一个 RESTful API 的服务提供者。

基于 Python 的 Flask 框架，在实现这个目标的途中遇到的所有问题和解决方法，都在这里详细记载。

## Hello?

我们先尝试一下 Flask 框架的威力。

这是目前的项目文件结构：

```
root
├── marucat_app
│   └── __init__.py
└── run.py
```

可以看到项目中有一个包 `marucat_app`，主要的代码基本放在这里。

这个包之外还有一个 `run.py`，我们定义其为程序的入口，启动的位置。

为了方便调试，`run.py` 将以 DEGUB 模式启动开发服务器。

```python
# -*- encoding: utf-8 -*-

from marucat_app import app

app.run(debug=True)
```

我们从 `marucat_app` 包导入 app 实例（这个实例将在稍后说明），以 DEBUG 模式运行它。

先不急着运行，为了尝试 Flask 的威力，我们先准备一个 Hello 场景。

假设一个场景，我们要实现这个需求：

**访问（GET）根目录（'/'）时，得到一个问候信息，这个信息需要是 JSON 格式的，并且指定返回类型为 JSON。**

这其实是一个最简单的 REST API，我们可以想象 request 头第一行会是这样的：

```
GET / HTTP/1.1
```

解释一下：我们将对位于 `/` 的资源进行 HTML 动词的 `GET` 操作，即我们想获得根目录所代表的资源。

所以在服务器这边，我们其实要做这些事：

* 给根路径（'/'）绑定一个路由
* 这个路由需要返回一个 JSON 对象
* 并且 Response 对象需要声明自己是 JSON 类型的（即 Content-Type 声明）

> Response 对象声明 Content-Type 是为了向请求资源的人描述 Response Body 的格式。

在 Flask 中要做这些事情是很简单的。

回到我们的文件结构，在 `marucat_app` 包中有一个 `__init__.py` 文件，我们就把这个 Hello 场景放在这里吧。

使用 Flask 框架，首先需要一个实例化的 Flask 对象，其后的所有操作都将通过这个对象来进行。

我们要对这个对象绑定路由，来决定什么情况下返回什么，而除此之外的细节都由框架帮我们处理了。

这是一个最简单的例子：

```python
# -*- encoding: utf-8 -*-

from flask import Flask
from json import dumps


app = Flask('marucat_app')


@app.route('/')
def hello():
    return dumps({'message': 'Hello'})


```

我们从 flask 包中导入 Flask 类，从 json 包导入 dumps 函数。

先创建一个 Flask 对象，因为之后的操作都将围绕这个对象进行。

实例化 Flask 对象时需要提供一个参数作为识别符，通常情况下我们把 `__name__` 作为识别符。

不过，

> 官方文档提示第一个参数的设置分两种情况：1）使用单独 module 时通常将 `__name__` 作为第一个参数；2）使用 package 时通常将 package 名硬编码作为第一个参数。究其原因，一部分 Flask 扩展将根据这个识别符来追踪 DEBUG 信息，设置不当的话会造成丢失 DEBUG 信息。

我们的文件结构 app 存在于 `marucat_app` 包里，我们直接将 'marucat_app' 作为第一个参数。

```python
app = Flask('marucat_app')
```

接下来创建一个 Hello 函数，直接返回问候信息。

问候信息是一个 dict 数据，使用 dumps 函数将其转成 JSON 字符串再返回。

```python
def hello():
    return dumps({'message': 'Hello'})
```

最后，将 Hello 函数绑定在根路径（'/'）上，Flask 让我们可以使用装饰器的方式简单的绑定路由。

在 Hello 函数上插入装饰器 `@app.route('/')` 。

```python
@app.route('/')
def hello():
    return dumps({'message': 'Hello'})
```

现在，这个简单的例子已经可以运行了，来试试看！

我们可以在 IDE 中配置执行脚本，直接执行 `run.py` 就可以把这个 app 跑起来。

或者使用命令行，输入下面的命令，效果是一样的。

```
$ python run.py
```

键入上面的命令后，我们会看到类似下面的输出。

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 274-620-182
```

现在 app 已经在 DEBUG 模式下运行了，可以通过 `http://127.0.0.1:5000/` 访问，我们来试试看。

```
$ curl http://127.0.0.1:5000/
{"message": "Hello"}
```

我们打开一个新的命令行界面，使用 curl 访问服务器跟路径，接着我们就得到了预设的问候信息。

同时在运行服务器的命令行界面上我们看到如下反馈。

```
127.0.0.1 - - [31/May/2018 16:12:03] "GET / HTTP/1.1" 200 -
```

同样我们也可以直接打开浏览器访问。在浏览器中访问根路径，JSON 格式的问候信息将直接显示在页面上。

我们在浏览器中打开开发者工具，切换到 Network 标签（Chrome 浏览器下），在这里可以看到我们访问根路径时得到的 Response 信息（如果你没看到，那就在打开开发者工具的情况下再访问一次根路径）。

这是我得到的一个 Response 头信息。

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 20
Server: Werkzeug/0.14.1 Python/3.6.4
Date: Thu, 31 May 2018 08:24:04 GMT
```

可以看到 Content-Type 没有像我们想象的那样声明 JSON 格式，它声明了 text/html 格式。

这是因为我们使用 dumps 方法将 dict 数据转换成了 JSON 字符串，但其本质仍然是字符串。

服务器并不知道它是一个 JSON 数据，这时需要我们手动设置 Content-Type 内容。

Flask 为我们提供了一个定制 Response 对象的方法，`make_response`。

这是修改后的代码。

```python
# -*- encoding: utf-8 -*-

from flask import Flask, make_response
from json import dumps


CONTENT_TYPE = 'Content-Type'
JSON_TYPE = 'application/json'


app = Flask('marucat_app')


@app.route('/')
def hello():
    resp = make_response(dumps({'message': 'Hello'}), 201)
    resp.headers[CONTENT_TYPE] = JSON_TYPE
    return resp


```

相比之前我们直接返回字符串，这次我们返回定制过的 response 对象。

从 flask 包中导入 `make_response` 函数，这个函数可以生成一个 response 对象。

它接受几个参数，一般我们传递两个参数给它，第一个是 response 的数据，第二个是返回状态码。

之前我们并没有显式的设置过状态码，因为默认将发送 200 状态码。

这次我们将状态码设置成 201，等会看看效果。

```python
resp = make_response(dumps({'message': 'Hello'}), 201)
```

我们拿到 `resp` 这个对象后，就可以给它设置 header 了。

为了方便使用，我们先将 Content-Type 设置为常量。

```python
CONTENT_TYPE = 'Content-Type'
JSON_TYPE = 'application/json'
```

接着，给 `resp` 设置 header。

```python
resp.headers[CONTENT_TYPE] = JSON_TYPE
```

到此基本搞定，我们再来跑跑看。如果刚才你没有关闭服务器的话，在修改代码保存之后你会看到 reload 的字眼。

如果你关闭了服务器，现在重新打开它。

在浏览器中打开开发者工具，访问 app 的地址根路径。

```
{"message": "Hello"}
```

页面上显示了我们设定的结果，再看看 Response 头信息。

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.14.1 Python/3.6.4
Date: Thu, 31 May 2018 09:02:34 GMT
```

注意两点：

1. 状态码和我们设定的一样返回了 201
2. Content-Type 和预期一样声明了 JSON 类型

我们完成了 Hello 的需求。

虽然上面碎碎念了这么多，但其实我们仅使用了差不多10行代码就完成了一个 app 的构建。

### 小结

到目前为止，我们先做一个小结。

我们实现了一个 Hello 场景，创建了一个最简单的问候语 API。依次来了解了 Flask 框架的基本用法，以及 REST API 的概念。

这些内容可以总结如下：

* Flask 框架的使用从实例化 Flask 对象开始
* 使用装饰器 `@app.route(path)` 来绑定路由
* 路由可以是一个函数，返回一个字符串或者 response 对象
* 如果路由函数返回一个字符串，response 头信息的 Content-Type 默认为 text/html
* 如果不设定返回的状态码，路由函数默认返回 200 状态码
* Flask 提供 `make_response` 函数来定制 response 对象
* response 对象定制可以设定响应内容、状态码和响应头信息

