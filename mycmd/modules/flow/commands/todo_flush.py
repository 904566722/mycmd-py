import os
import click
from typing import List
from mycmd.config import config
from mycmd.logger import logger

@click.command('todo-flush')
@click.option('--type', required=True, help='todo 类型 (work)')
@click.option('--project', required=False, help='项目名称列表，用逗号分隔')
def todo_flush(type: str, project: str):
    """初始化或刷新 todo 文件"""
    try:
        todo_dir = config.get('flow', 'todo-dir')
        template_file = os.path.join(todo_dir, type, f"{type}-template.todo")
        target_file = os.path.join(todo_dir, type, f"{type}.todo")

        # 检查模板文件是否存在
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"模板文件不存在: {template_file}")

        # 检查目标文件是否存在
        if os.path.exists(target_file):
            if not click.confirm(f"文件 {target_file} 已存在，是否覆盖（覆盖前请确保已经归档）？"):
                logger.info("操作已取消")
                return

        # 复制模板文件
        with open(template_file, 'r') as f:
            content = f.read()

        # 处理项目
        if type == 'work' and project:
            projects = [p.strip() for p in project.split(',')]
            content = _process_work_content(content, projects)

        # 写入目标文件
        with open(target_file, 'w') as f:
            f.write(content)

        logger.success(f"已成功创建 todo 文件: {target_file}")
        if type == 'work' and project:
            logger.success(f"已添加项目: {project}")

    except Exception as e:
        logger.error(str(e))
        raise click.Abort()

def _process_work_content(content: str, projects: List[str]) -> str:
    """处理工作类型的 todo 文件内容"""
    lines = content.splitlines()
    result = []
    in_category = False
    
    for line in lines:
        # 检查是否是根分类行
        if line and not line[0].isspace() and not line.startswith(('#', '//')):
            in_category = True
            # 确保根分类有冒号结尾
            if not line.endswith(':'):
                line = f"{line}:"
            result.append(line)
            # 添加项目
            for project in projects:
                if not project.endswith(':'):
                    project = f"{project}:"
                result.append(f"    {project}")
        # 如果是注释行或空行
        elif line.strip().startswith(('#', '//')) or not line.strip():
            result.append(line)
            in_category = False
        # 跳过分类下的所有缩进内容
        elif not in_category:
            result.append(line)
            
    return '\n'.join(result) 