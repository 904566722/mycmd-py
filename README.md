# mycmd-python3

Python 实现的命令行工具，用于管理自定义命令。

## 安装

```bash
# 开发模式安装
pip install -e .
```

## 配置

配置文件位置：`/etc/.mycmd.conf`

```yaml
flow:
    todo-dir: ~/code/bingo/AllInOne/docs-v2/todo  # todo 文件夹路径
```

## 使用

### flow 模块

管理工作流相关功能。

#### todo-flush

初始化或刷新 todo 文件。

```bash
mycmd flow todo-flush --type work --project BCS,DUALENGINE
```

#### todo-archive

归档指定日期范围内的 todo 项目。

```bash
mycmd flow todo-archive --type work --date 11/21,11/27
```

## 开发

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行测试
```bash
pytest
``` 