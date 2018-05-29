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

我们下载安装包（在 Windows 平台上下载 zip 包），解压到合适的位置就完成了对 MongoDB 的安装。

我们也可以将安装路径添加到环境变量，在 Windows 上比较简单，我们打开系统属性，在高级设置中选择环境变量，找到 `PATH` 这个变量，把 MongoDB 到 bin 文件夹的路径添加进去就可以了。


