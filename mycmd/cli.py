import click
from mycmd.modules.flow.flow import flow_group

@click.group()
def cli():
    """mycmd - 管理自定义命令的工具"""
    pass

# 注册子命令组
cli.add_command(flow_group)

if __name__ == '__main__':
    cli() 