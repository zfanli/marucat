# 部署 MongoDB 环境

MaruCat 依赖 MongoDB 来储存所有的服务数据。

为了让 MaruCat 正常运行，我们需要在本地开发机器和 Linux 服务器上部署 MongoDB 环境。

## 本地搭建 MongoDB 环境

在开发机器上搭建 MongoDB 环境。

### 在 macOS 上搭建 MongoDB 环境

在官网下载 MongoDB 服务器的安装包。

[MongoDB 社区版](https://www.mongodb.com/download-center?jmp=nav#community)

在 macOS 上，我们下载一个 tgz 压缩包。下载完成后，将其内容解压到合适的地方。

安装操作就结束了。

为了方便对 MongoDB 服务器进行操作，我们可以选择将安装路径添加到环境变量中。

这样做的好处是可以从任何地方启动和关闭 MongoDB 服务器。

我们修改用户级别的环境变量 `~/.bash_profile` 文件（如果要修改系统变量则修改 `/etc/paths` 文件）。

```
$ vi ~/.bash_profile
```

将安装目录到 `bin` 文件夹为止的路径添加到环境变量文件中，用 `:` 作为区分。

例如在我的机器上环境变量是这样的：

```shell
export PATH="/Users/rick/workspaces/env/mongodb/bin:$PATH"
```

保存该文件，重新打开终端，环境变量的设置就会生效了。

现在我们可以在任何位置启动和关闭 MongoDB 服务了。

### 在 Windows 上搭建 MongoDB 环境

在 Windows 上搭建 MongoDB 环境步骤基本和 macOS 一样。

我们下载安装包。

[MongoDB 社区版](https://www.mongodb.com/download-center?jmp=nav#community)

这次我们下载 zip 格式的压缩包。

下载完成后，将其解压到合适的位置，就完成了对 MongoDB 的安装。

同样的，我们也可以将安装路径添加到环境变量。

在 Windows 上这个操作比较简单。

右击 `此电脑（This Computer）` 图标，选择属性，我们将进入系统属性面板。

在系统属性面板左侧列表，选择 `高级系统设置`。

在弹出的对话框里选择 `高级` 标签页，点击 `环境变量` 按钮进入到环境变量的设置窗口。

在这个窗口中找到 `PATH` 属性，点击 `编辑` 按钮，新建一个项目，将 MongoDB 安装目录到 bin 的路径填入其中保存，就完成里对环境变量的追加。

到此为止，在 Windows 环境中我们也可以在任意位置启动和关闭 MongoDB 服务器了。

## 在 Linux 服务器上搭建 MongoDB 环境

我们的系统将在 Linux 服务器上运行，在真正投入使用之前，我们还需要对服务器上做同样的配置。

在服务器上部署 MongoDB 与在 macOS 上部署的方法没有太大差异。

> **TODO 等待编辑**

## 图形化控制面板 MongoDB Compass

完成了 MongoDB 的部署，接下来我们将启动它。但是在此之前，先推荐一个实用工具。

Compass 是一个官方出品的 MongoDB 图形化工具，它有免费版本，而且免费版本的功能足够一般使用。

Compass 的功能就是图形化关于 MongoDB 的"一切"，值得关注的功能如下：

* 直观的数据库和数据，方便 CRUD 操作
* 数据分析，基于每个数据库的数据字段频率和类型的分析等
* 性能信息，实时读写性能分析等

Compass 专门为 MongoDB 设计，方便使用，体验良好。

[MongoDB Compass 下载地址](https://www.mongodb.com/download-center?jmp=nav#compass)

当然，这不是必须的步骤，不过还是推荐使用。
