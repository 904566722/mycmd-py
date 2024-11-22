import click
from mycmd.config import config
from mycmd.modules.flow.commands.todo_flush import todo_flush
from mycmd.modules.flow.commands.todo_archive import todo_archive

@click.group(name='flow')
def flow_group():
    """管理工作流和学习流"""
    # 验证 flow 模块必需的配置
    config.validate('flow', ['todo-dir'])

# 注册子命令
flow_group.add_command(todo_flush)
flow_group.add_command(todo_archive) 