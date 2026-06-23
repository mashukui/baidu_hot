# 百度热搜榜爬虫/Baidu Hot Search Board Crawler

> 基于Python3的百度热搜榜数据采集脚本，支持热搜标题、排名、置顶状态、热度标签、内容标签和详情链接等核心字段导出。

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="https://pypi.org/project/requests/"><img src="https://img.shields.io/badge/requests-required-green.svg" alt="requests"></a>
  <a href="https://pypi.org/project/pandas/"><img src="https://img.shields.io/badge/pandas-required-orange.svg" alt="pandas"></a>
</p>

## 📖 项目简介

本项目是一个面向Python爬虫初学者的百度热搜榜采集示例。脚本通过请求百度热搜榜接口，解析返回的JSON数据，并将热搜内容整理为Excel文件，方便后续用Excel、Python或其他数据分析工具处理。

源码结构简单，适合学习以下内容：

- 使用`requests`发送HTTP请求
- 解析接口返回的JSON数据
- 适配接口字段和嵌套列表结构变化
- 提取列表数据中的核心字段
- 使用`pandas`生成表格数据
- 将结果保存为Excel文件

## 🎬 讲解视频

源码讲解视频：https://www.bilibili.com/video/BV1Bq4y1v7p7/

## ✨ 功能特点

- 无需登录账号，不依赖Cookie
- 自动抓取百度热搜榜数据
- 兼容百度热搜新旧接口列表结构
- 支持提取标题、排名、置顶状态、标签和链接
- 自动补充批次`logid`和榜单名称
- 保存为`xlsx`文件，方便直接用Excel打开

## 📊 采集字段

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| 热搜标题 | 热搜事件标题 | 微信迎来史上最大更新 |
| 热搜排名 | 当前热搜排序，置顶内容为0，普通内容从1开始 | 1 |
| 是否置顶 | 是否为置顶热搜 | False |
| 热度标签代码 | 平台返回的热度标签代码 | 1 |
| 热度标签名 | 平台返回的热度标签名称 | 新 |
| 内容标签名 | 平台返回的内容业务标签 | 热议 |
| 特殊内容类型 | 平台返回的特殊内容类型 | 2 |
| 链接地址 | 百度移动端搜索结果链接 | [https://m.baidu.com/s?word=...](https://m.baidu.com/s?word=%E5%BE%AE%E4%BF%A1%E8%BF%8E%E6%9D%A5%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%A4%A7%E6%9B%B4%E6%96%B0&sa=fyb_news) |
| 批次logid | 本次接口请求返回的日志ID | 3813341776 |
| 榜单名称 | 当前榜单名称 | 热搜榜 |

## 📄 运行结果示例

脚本运行完成后，会在当前目录生成：

```text
百度热搜榜.xlsx
```

Excel示例：

| 热搜标题 | 热搜排名 | 是否置顶 | 热度标签代码 | 热度标签名 | 内容标签名 | 榜单名称 |
| --- | --- | --- | --- | --- | --- | --- |
| 把党的政治建设作为党的根本性建设 | 0 | True |  |  |  | 热搜榜 |
| 微信迎来史上最大更新 | 1 | False | 1 | 新 | 热议 | 热搜榜 |
| 哈兰德偷喝对方门将的水 | 2 | False | 3 | 热 |  | 热搜榜 |

## 🚀 快速开始

### 环境要求

- Python3.8+
- Windows/macOS/Linux

### 安装依赖

```bash
pip install requests pandas openpyxl
```

### 基本使用

```bash
python3 baidu_hot.py
```

运行时终端会输出接口响应状态码和抓取到的热搜标题。运行完成后，采集结果会保存到`百度热搜榜.xlsx`。

## ⚙️ 核心原理

### 请求地址

```text
https://top.baidu.com/api/board?platform=wise&tab=realtime
```

### 请求头

脚本设置了移动端`User-Agent`、`Accept`、`Referer`等基础请求头，不需要配置Cookie、Token或账号信息。

```python
header = {
    'User-Agent': 'Mozilla/5.0 ... Mobile Safari/537.36',
    'Host': 'top.baidu.com',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://top.baidu.com/board?tab=novel',
}
```

### 核心流程

1. 请求百度热搜榜接口
2. 使用`response.json()`解析接口数据
3. 兼容读取`cards[0].content[0].content`等热搜列表结构
4. 提取`word`、`index`、`isTop`、`hotTag`、`newHotName`、`labelTagName`、`url`等字段
5. 使用`pandas.DataFrame`整理数据
6. 导出为Excel文件

## 🎯 适用场景

- Python爬虫入门练习
- 热点事件观察
- 百度热搜数据归档
- Excel数据处理学习
- pandas表格生成示例

## ❓ 常见问题

### 运行后没有生成Excel怎么办？

先确认依赖是否安装成功：

```bash
pip install requests pandas openpyxl
```

再确认当前目录是否有`baidu_hot.py`，并在脚本所在目录运行命令。

### 为什么部分字段是空的？

百度热搜接口并不是每条热搜都会返回所有标签字段。例如置顶内容通常没有`hotTag`，普通内容也不一定有`newHotName`或`labelTagName`。

### 为什么脚本突然报错？

热搜接口字段可能会发生变化。如果返回结构调整，脚本中读取字段的位置也需要同步修改。

### 是否需要Cookie？

当前脚本不需要Cookie。请不要把个人Cookie、Token、账号密码等敏感信息提交到公开仓库。

## ⚠️ 注意事项

- 请合理控制运行频率，避免对目标站点造成压力。
- 本项目仅用于学习研究，不建议用于商业采集或批量抓取。
- 接口可用性和字段结构可能随目标网站调整而变化。
- 使用本项目时，请自行遵守目标网站的服务条款、robots规则以及相关法律法规。

## 📌 免责声明

本项目仅供学习和研究使用。因使用本项目产生的任何问题或后果，由使用者自行承担。
