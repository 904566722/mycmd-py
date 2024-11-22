import os
import re
from datetime import datetime
import click
from mycmd.config import config
from mycmd.logger import logger

@click.command('todo-archive')
@click.option('--type', required=True, help='todo 类型 (work)')
@click.option('--date', required=True, help='归档日期范围，格式：MM/DD,MM/DD')
def todo_archive(type: str, date: str):
    """归档指定日期范围内的 todo 项目"""
    try:
        # 解析日期范围
        start_date, end_date = date.split(',')
        
        todo_dir = config.get('flow', 'todo-dir')
        todo_file = os.path.join(todo_dir, type, f"{type}.todo")
        archive_file = os.path.join(todo_dir, type, f"{type}({start_date}~{end_date}).archive")

        if not os.path.exists(todo_file):
            raise FileNotFoundError(f"todo 文件不存在: {todo_file}")

        # 处理文件内容
        tasks = _process_todo_file(todo_file, start_date, end_date)
        
        # 生成归档内容
        archive_content = _generate_archive_content(tasks, start_date, end_date)
        
        # 写入归档文件
        with open(archive_file, 'w') as f:
            f.write(archive_content)
            
        logger.success(f"已成功创建归档文件: {archive_file}")

    except Exception as e:
        logger.error(str(e))
        raise click.Abort()

def _is_date_in_range(target_date: str, start_date: str, end_date: str) -> bool:
    """检查日期是否在范围内"""
    current_year = datetime.now().year
    
    def parse_date(date_str: str) -> datetime:
        month, day = map(int, date_str.split('/'))
        return datetime(current_year, month, day)
    
    target = datetime.strptime(target_date, '%y-%m-%d')
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    # 处理跨年的情况
    if end < start:
        if target < start:
            target = target.replace(year=target.year + 1)
        end = end.replace(year=end.year + 1)
        
    return start <= target <= end

def _parse_task_line(line: str) -> dict:
    """解析任务行信息"""
    task_info = {}
    
    # 检查任务状态
    if re.search(r'[✔✓☑\+\[x\]\[X\]\[\+\]]', line):
        task_info['status'] = '已完成'
    elif re.search(r'[✘xX\[-\]]', line):
        task_info['status'] = '已取消'
    else:
        task_info['status'] = '进行中'
    
    # 提取项目信息
    project_match = re.search(r'@project\(([^)]+)\)', line)
    if project_match:
        project = project_match.group(1)
        task_info['category'], task_info['project'] = project.split('.')
    
    # 提取时间信息
    start_match = re.search(r'@started\((\d{2}-\d{2}-\d{2})\s+[^)]+\)', line)
    if start_match:
        task_info['start_date'] = start_match.group(1)[3:8].replace('-', '/')
        
    done_match = re.search(r'@(?:done|cancelled)\((\d{2}-\d{2}-\d{2})\s+[^)]+\)', line)
    if done_match:
        task_info['end_date'] = done_match.group(1)[3:8].replace('-', '/')
    else:
        task_info['end_date'] = 'unknown'
    
    # 提取任务名称
    task_info['name'] = re.sub(r'^\s*[✔✓☑\+✘xX\[\]]\s*|\s*@.*$', '', line).strip()
    
    return task_info

def _process_todo_file(todo_file: str, start_date: str, end_date: str) -> list:
    """处理 todo 文件内容"""
    tasks = []
    in_archive = False
    
    with open(todo_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            if line == 'Archive:':
                in_archive = True
                continue
            elif line and not line[0].isspace() and in_archive:
                in_archive = False
                
            if (in_archive or '@started' in line) and line and not line.startswith(('#', '//', '/*')):
                task_info = _parse_task_line(line)
                if 'start_date' in task_info and _is_date_in_range(task_info['start_date'], start_date, end_date):
                    tasks.append(task_info)
                    
    return tasks

def _generate_archive_content(tasks: list, start_date: str, end_date: str) -> str:
    """生成归档文件内容"""
    content = [
        "---------------------------------------------",
        "format1. 状态-开始时间-结束时间-分类-项目-名称",
        "---------------------------------------------\n"
    ]
    
    # 格式1：按状态列出所有任务
    for task in tasks:
        task_line = f"{task['status']}-{task.get('start_date', 'unknown')}-{task['end_date']}-{task['category']}-{task['project']}-{task['name']}"
        content.append(task_line)
    
    content.extend([
        "\n\n---------------------------------------------",
        "format2. (把已完成和进行中的任务按照分类罗列)",
        "---------------------------------------------"
    ])
    
    # 格式2：按分类组织任务
    categories = {}
    for task in tasks:
        if task['status'] != '已取消':
            category = task['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(f"{task['project']}-{task['name']}")
    
    for category in sorted(categories.keys()):
        content.append(f"\n{category}:")
        for i, task in enumerate(categories[category], 1):
            content.append(f"{i}. {task}")
    
    return '\n'.join(content) 