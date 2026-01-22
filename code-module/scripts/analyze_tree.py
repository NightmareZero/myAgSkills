#!/usr/bin/env python3
"""
Module tree analyzer for code-module skill.

Generates directory tree structure and identifies leaf directories
for module analysis.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Set


# Common directories to ignore
IGNORED_DIRS = {
    'node_modules',
    '.git',
    '__pycache__',
    '.venv',
    'venv',
    'env',
    'dist',
    'build',
    '.next',
    '.nuxt',
    'target',
    'bin',
    'obj',
    '.pytest_cache',
    'coverage',
    '.mypy_cache',
}

# Code file extensions to consider
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx',
    '.java', '.go', '.rs', '.cpp', '.c', '.cs',
    '.rb', '.php', '.swift', '.kt', '.scala',
    '.sh', '.bash', '.zsh',
}


def is_ignored_dir(path: Path) -> bool:
    """Check if directory should be ignored."""
    return any(part in IGNORED_DIRS for part in path.parts)


def find_all_directories(root: Path) -> List[Path]:
    """Find all non-ignored directories recursively."""
    directories = []

    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)

        # Skip if any parent directory is ignored
        if is_ignored_dir(dir_path):
            continue

        # Filter out ignored subdirectories
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

        # Add this directory
        directories.append(dir_path)

    return sorted(directories)


def is_leaf_directory(dir_path: Path, all_dirs: List[Path]) -> bool:
    """Check if a directory has no subdirectories."""
    for other_dir in all_dirs:
        if other_dir.parent == dir_path and other_dir != dir_path:
            return False
    return True


def get_leaf_directories(directories: List[Path]) -> List[Path]:
    """Get all leaf directories (directories with no subdirectories)."""
    return [d for d in directories if is_leaf_directory(d, directories)]


def build_tree_string(directories: List[Path], root: Path) -> str:
    """Build a markdown-formatted tree string."""
    # Build tree structure
    tree = {}
    for dir_path in directories:
        relative = dir_path.relative_to(root)
        current = tree
        for part in relative.parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    # Convert to markdown tree
    lines = []
    lines.append(root.name)

    def add_to_tree(structure: Dict, prefix: str = "", is_last: bool = True):
        items = list(structure.items())
        for i, (name, children) in enumerate(items):
            is_item_last = (i == len(items) - 1)
            connector = "└── " if is_item_last else "├── "
            lines.append(f"{prefix}{connector}{name}")

            # Update prefix for children
            if children:
                child_prefix = prefix + ("    " if is_item_last else "│   ")
                add_to_tree(children, child_prefix, is_item_last)

    add_to_tree(tree)

    return "\n".join(lines)


def get_code_files(dir_path: Path) -> List[Path]:
    """Get all code files in a directory."""
    code_files = []
    if not dir_path.exists():
        return code_files

    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix in CODE_EXTENSIONS:
            code_files.append(file_path)

    return sorted(code_files)


def print_analysis(root: Path | None = None):
    """Print directory tree analysis."""
    if root is None:
        root = Path.cwd()

    print(f"Analyzing: {root}")
    print()

    # Find all directories
    directories = find_all_directories(root)
    print(f"Found {len(directories)} directories")

    # Find leaf directories
    leaf_dirs = get_leaf_directories(directories)
    print(f"Found {len(leaf_dirs)} leaf directories")
    print()

    # Build and print tree
    print("Directory Tree:")
    print("-" * 50)
    tree_str = build_tree_string(directories, root)
    print(tree_str)
    print()

    # Print leaf directories with code files
    print("Leaf Directories (for bottom-up analysis):")
    print("-" * 50)
    for leaf_dir in leaf_dirs:
        relative = leaf_dir.relative_to(root)
        code_files = get_code_files(leaf_dir)
        code_file_names = [f.name for f in code_files]
        code_str = ", ".join(code_file_names) if code_file_names else "No code files"
        print(f"  {relative}/ - {code_str}")


# ============================================================================
# Incremental Modules Generation Functions
# ============================================================================

def get_full_path(dir_path: Path, root: Path) -> str:
    """
    获取相对于根目录的完整路径字符串。

    Args:
        dir_path: 目录路径
        root: 项目根目录

    Returns:
        完整路径字符串（如：myproject/src/api/auth/）
    """
    relative = dir_path.relative_to(root)
    if relative == Path('.'):
        return f"{root.name}/"
    return f"{root.name}/{relative}/"


def update_progress_header(root: Path, processing_dir: str):
    """
    更新 modules.md 中的进度头信息。

    Args:
        root: 项目根目录
        processing_dir: 当前正在处理的目录
    """
    from datetime import datetime

    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        return

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 生成新的进度头
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_header = f"<!-- Last Update: {timestamp} | Processing: {processing_dir} -->"

    # 查找并替换进度头
    updated_lines = []
    for line in lines:
        if line.strip().startswith("<!-- Last Update:"):
            updated_lines.append(new_header)
        else:
            updated_lines.append(line)

    # 如果没有找到进度头，在文件末尾添加
    if not any("<!-- Last Update:" in line for line in updated_lines):
        updated_lines.append("")
        updated_lines.append(new_header)

    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def remove_progress_header(root: Path):
    """
    移除 modules.md 中的进度头信息。

    Args:
        root: 项目根目录
    """
    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        return

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 移除进度头行
    updated_lines = [line for line in lines if not line.strip().startswith("<!-- Last Update:")]

    # 移除末尾多余的空行
    while updated_lines and updated_lines[-1].strip() == "":
        updated_lines.pop()

    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def batch_update_descriptions(root: Path, updates: List[Tuple[Path, str]]):
    """
    批量更新 modules.md 中的多个描述。

    Args:
        root: 项目根目录
        updates: [(目录路径, 新描述), ...] 列表
    """
    modules_md_path = root / "modules.md"
    if not modules_md_path.exists():
        raise FileNotFoundError("modules.md not found")

    # 读取文件
    content = modules_md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 构建查找字典：完整路径 -> 新描述
    update_map = {}
    for dir_path, new_desc in updates:
        full_path = get_full_path(dir_path, root)
        update_map[full_path] = new_desc

    # 更新匹配的行
    updated_lines = []
    for line in lines:
        updated = False
        for full_path, new_desc in update_map.items():
            # 匹配格式：完整路径 - 描述
            if line.startswith(full_path + " - "):
                updated_lines.append(f"{full_path} - {new_desc}")
                updated = True
                break

        if not updated:
            updated_lines.append(line)

    # 写回文件
    modules_md_path.write_text('\n'.join(updated_lines), encoding='utf-8')


def get_directories_by_depth(directories: List[Path], root: Path) -> Dict[int, List[Path]]:
    """
    按层级分组目录。

    Args:
        directories: 所有目录路径列表
        root: 项目根目录

    Returns:
        字典 {深度: [目录列表]}
    """
    depth_map: Dict[int, List[Path]] = {}

    for dir_path in directories:
        relative = dir_path.relative_to(root)
        depth = len(relative.parts) if relative != Path('.') else 0
        if depth not in depth_map:
            depth_map[depth] = []
        depth_map[depth].append(dir_path)

    return depth_map


def generate_initial_skeleton(root: Path) -> str:
    """
    生成初始 modules.md 骨架（包含树结构和占位描述）。

    Args:
        root: 项目根目录

    Returns:
        完整的 markdown 内容
    """
    from datetime import datetime

    # 查找所有目录
    directories = find_all_directories(root)

    # 1. 标题
    lines = ["# Modules", ""]

    # 2. 目录树（树形结构）
    lines.append("## Directory Structure")
    lines.append("")
    tree_str = build_tree_string(directories, root)
    lines.append(tree_str)
    lines.append("")

    # 3. 模块描述（完整路径 + 占位符）
    lines.append("## Module Descriptions")
    lines.append("")
    for dir_path in sorted(directories):
        full_path = get_full_path(dir_path, root)
        lines.append(f"{full_path} - [待分析]")
    lines.append("")

    # 4. 进度头（在最后，方便移除）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"<!-- Last Update: {timestamp} | Processing: Initializing -->")

    return '\n'.join(lines)


def create_skeleton_file(root: Path):
    """
    创建初始 modules.md 文件。

    Args:
        root: 项目根目录
    """
    skeleton = generate_initial_skeleton(root)
    modules_md_path = root / "modules.md"
    modules_md_path.write_text(skeleton, encoding='utf-8')
    print(f"Created: {modules_md_path}")
    print(f"  Found {len(find_all_directories(root))} directories")


def analyze_directory_code(dir_path: Path) -> str:
    """
    分析目录中的代码并生成功能描述（中文）。

    Args:
        dir_path: 目录路径

    Returns:
        功能描述（10~50 个中文字符）
    """
    code_files = get_code_files(dir_path)

    # 排除脚本自身
    script_name = 'analyze_tree.py'
    code_files = [f for f in code_files if f.name != script_name]

    if not code_files:
        return "配置文件或资源目录"

    # 读取代码文件
    all_content = ""
    file_names = [f.name for f in code_files]
    for code_file in code_files[:5]:  # 最多读取 5 个文件
        try:
            content = code_file.read_text(encoding='utf-8', errors='ignore')
            all_content += content + "\n"
        except Exception:
            continue

    if not all_content:
        return "无有效代码文件"

    # 基于目录名和内容分析
    dir_name = dir_path.name.lower()
    content_lower = all_content.lower()

    # 扩展关键词映射（中文描述）
    category_map = {
        'auth': {
            'keywords': ['auth', 'login', 'register', 'session', 'token', 'signin', 'signup', 'password', 'jwt', 'oauth'],
            'description': '用户认证与权限管理模块'
        },
        'config': {
            'keywords': ['config', 'setting', 'env', 'environment', 'constant'],
            'description': '系统配置与环境变量管理'
        },
        'util': {
            'keywords': ['util', 'helper', 'common', 'shared', 'tool', 'format', 'date', 'time', 'string'],
            'description': '通用工具函数与辅助类库'
        },
        'api': {
            'keywords': ['api', 'route', 'endpoint', 'handler', 'controller', 'request', 'response'],
            'description': 'RESTful API 接口与路由处理'
        },
        'model': {
            'keywords': ['model', 'schema', 'entity', 'domain', 'dto', 'pojo'],
            'description': '数据模型与实体定义'
        },
        'service': {
            'keywords': ['service', 'business', 'logic', 'manager', 'facade'],
            'description': '业务逻辑处理与服务层'
        },
        'db': {
            'keywords': ['db', 'database', 'sql', 'query', 'repository', 'dao', 'migrate', 'migration'],
            'description': '数据库访问与持久化操作'
        },
        'test': {
            'keywords': ['test', 'spec', 'mock', 'fixture', 'assert'],
            'description': '单元测试与集成测试套件'
        },
        'view': {
            'keywords': ['view', 'template', 'render', 'html', 'component', 'ui', 'page'],
            'description': '视图层与前端组件'
        },
        'controller': {
            'keywords': ['controller', 'action', 'dispatch'],
            'description': '控制器与请求分发处理'
        },
        'middleware': {
            'keywords': ['middleware', 'interceptor', 'filter'],
            'description': '中间件与请求拦截器'
        },
        'client': {
            'keywords': ['client', 'http', 'fetch', 'request', 'axios'],
            'description': 'HTTP 客户端与请求封装'
        },
        'server': {
            'keywords': ['server', 'listen', 'port', 'host'],
            'description': '服务器启动与监听配置'
        },
        'cache': {
            'keywords': ['cache', 'redis', 'memcached', 'session'],
            'description': '缓存与会话管理'
        },
        'log': {
            'keywords': ['log', 'logger', 'monitor', 'track'],
            'description': '日志记录与监控追踪'
        },
        'validate': {
            'keywords': ['validate', 'validator', 'check', 'verify'],
            'description': '数据校验与格式验证'
        },
        'exception': {
            'keywords': ['exception', 'error', 'catch', 'throw', 'handle'],
            'description': '异常捕获与错误处理'
        },
        'event': {
            'keywords': ['event', 'emit', 'trigger', 'listener', 'observer', 'pubsub'],
            'description': '事件驱动与消息发布订阅'
        },
        'task': {
            'keywords': ['task', 'job', 'schedule', 'cron', 'queue', 'worker'],
            'description': '异步任务与定时调度'
        },
        'socket': {
            'keywords': ['socket', 'websocket', 'ws', 'io', 'connection'],
            'description': 'WebSocket 与实时通信'
        },
        'storage': {
            'keywords': ['storage', 'file', 'upload', 'download', 'bucket'],
            'description': '文件存储与上传下载'
        },
        'security': {
            'keywords': ['security', 'encrypt', 'decrypt', 'hash', 'cipher'],
            'description': '加密解密与安全防护'
        },
        'cluster': {
            'keywords': ['cluster', 'node', 'sync', 'distributed', 'raft', 'consensus'],
            'description': '集群节点初始化与数据同步'
        },
        'comm': {
            'keywords': ['comm', 'communication', 'interface', 'contract', 'protocol'],
            'description': '平台上下文与共享接口定义'
        },
        'plugin': {
            'keywords': ['plugin', 'extension', 'module', 'addon'],
            'description': '插件扩展与模块化加载'
        },
        'locale': {
            'keywords': ['locale', 'i18n', 'international', 'language', 'translation'],
            'description': '国际化与多语言支持'
        },
        'perf': {
            'keywords': ['perf', 'performance', 'optimize', 'benchmark'],
            'description': '性能优化与基准测试'
        },
        'cli': {
            'keywords': ['cli', 'command', 'terminal', 'shell', 'console'],
            'description': '命令行接口与终端工具'
        },
        'doc': {
            'keywords': ['doc', 'readme', 'example', 'sample'],
            'description': '文档说明与使用示例'
        },
    }

    # 1. 基于目录名匹配
    for category, info in category_map.items():
        if dir_name in info['keywords'] or category in dir_name:
            return info['description']

    # 2. 基于文件名匹配
    for file_name in file_names:
        file_lower = file_name.lower()
        for category, info in category_map.items():
            if any(kw in file_lower for kw in info['keywords']):
                return info['description']

    # 3. 基于代码内容匹配
    for category, info in category_map.items():
        if any(kw in content_lower for kw in info['keywords']):
            return info['description']

    # 4. 默认根据目录名生成描述
    dir_display = dir_path.name
    if dir_display in ['src', 'lib', 'core', 'source']:
        return '核心源代码与业务逻辑'
    elif dir_display in ['dist', 'build', 'out', 'release']:
        return '编译输出与构建产物'
    elif dir_display in ['public', 'static', 'assets']:
        return '静态资源与公共文件'
    elif dir_display in ['vendor', 'node_modules', 'third_party']:
        return '第三方依赖库文件'
    else:
        # 使用目录名作为基础，生成描述
        if len(dir_display) > 10:
            dir_display = dir_display[:10]
        return f'{dir_display}相关功能模块'

def propagate_summary(dir_path: Path, child_summaries: List[str]) -> str:
    """
    合并子目录摘要生成父目录摘要（中文）。
    
    Args:
        dir_path: 父目录路径
        child_summaries: 子目录的摘要列表

    Returns:
        合并后的摘要（10~50 个中文字符）
    """
    if not child_summaries:
        return analyze_directory_code(dir_path)

    dir_name = dir_path.name

    # 特殊处理常见目录名
    if dir_name in ['src', 'lib', 'core', 'source']:
        return '核心源代码与业务逻辑层'
    elif dir_name in ['test', 'tests', '__tests__', 'spec']:
        return '单元测试与集成测试套件'
    elif dir_name in ['api', 'apis', 'routes']:
        return 'RESTful API 接口与路由层'
    elif dir_name in ['components', 'ui', 'views', 'pages']:
        return '前端组件与视图页面'
    elif dir_name in ['hooks', 'composables']:
        return 'React Hooks 与组合式函数'
    elif dir_name in ['store', 'state', 'redux', 'vuex']:
        return '全局状态管理与数据存储'
    elif dir_name in ['styles', 'css', 'scss', 'less']:
        return '样式表与主题配置文件'
    elif dir_name in ['assets', 'static', 'public']:
        return '静态资源与公共文件目录'
    elif dir_name in ['vendor', 'node_modules', 'third_party']:
        return '第三方库与依赖包文件'
    elif dir_name in ['config', 'settings', 'env']:
        return '系统配置与环境变量管理'
    elif dir_name in ['utils', 'helpers', 'commons']:
        return '通用工具函数与辅助类库'
    elif dir_name in ['services', 'business']:
        return '业务逻辑处理与服务层'
    elif dir_name in ['models', 'entities', 'schemas']:
        return '数据模型与实体定义层'
    elif dir_name in ['controllers', 'handlers']:
        return '控制器与请求处理层'
    elif dir_name in ['middleware', 'interceptors']:
        return '中间件与请求拦截处理'
    elif dir_name in ['client', 'http', 'request']:
        return 'HTTP 客户端与请求封装'
    elif dir_name in ['server', 'app', 'main']:
        return '应用启动与服务器配置'
    elif dir_name in ['database', 'db', 'repositories']:
        return '数据库访问与持久化操作'
    elif dir_name in ['cache', 'redis', 'session']:
        return '缓存与会话管理模块'
    elif dir_name in ['logs', 'logging', 'monitor']:
        return '日志记录与监控追踪系统'
    elif dir_name in ['exceptions', 'errors', 'handlers']:
        return '异常捕获与错误处理模块'
    elif dir_name in ['events', 'listeners', 'observers']:
        return '事件驱动与消息发布订阅'
    elif dir_name in ['tasks', 'jobs', 'queues', 'workers']:
        return '异步任务与定时调度系统'
    elif dir_name in ['socket', 'websocket', 'ws', 'io']:
        return 'WebSocket 与实时通信模块'
    elif dir_name in ['storage', 'files', 'uploads']:
        return '文件存储与上传下载管理'
    elif dir_name in ['security', 'auth', 'permission']:
        return '加密解密与安全防护模块'
    elif dir_name in ['locale', 'i18n', 'translations']:
        return '国际化与多语言支持模块'
    elif dir_name in ['platform', 'core', 'kernel']:
        return '平台核心与基础架构模块'
    elif dir_name in ['cluster', 'distributed']:
        return '集群管理与分布式协调'
    elif dir_name in ['communication', 'comm', 'interfaces']:
        return '平台通信与共享接口定义'
    elif dir_name in ['plugins', 'extensions', 'addons']:
        return '插件扩展与模块化加载'
    elif dir_name in ['documentation', 'docs', 'readme']:
        return '项目文档与使用说明'
    
    # 分析子摘要的共同特征
    unique_summaries = list(set(child_summaries))
    
    if len(unique_summaries) == 1:
        # 所有子目录相同，直接返回
        summary = unique_summaries[0]
        # 确保长度合适
        if len(summary) > 50:
            summary = summary[:50]
        return summary
    
    # 提取关键主题词
    themes = []
    for summary in unique_summaries:
        # 简单提取第一个名词性短语
        words = summary.split()
        if len(words) > 1:
            # 取前两个词作为主题
            theme = ''.join(words[:2])
            if len(theme) >= 4:
                themes.append(theme)
    
    if len(themes) >= 2:
        # 合并两个主要主题
        combined = themes[0] + '与' + themes[1]
        if len(combined) <= 50:
            return combined
    
    # 默认：基于目录名生成描述
    dir_display = dir_name
    if len(dir_display) > 15:
        dir_display = dir_display[:15]
    
    # 尝试从目录名推断功能
    if 'config' in dir_name:
        return f'{dir_display}配置管理模块'
    elif 'test' in dir_name:
        return f'{dir_display}测试套件'
    elif 'api' in dir_name:
        return f'{dir_display}接口模块'
    else:
        return f'{dir_display}功能模块组'


def generate_modules_incremental(root: Path | None = None, batch_size: int = 5):
    """
    增量式生成 modules.md 文件（两阶段流程）。

    Args:
        root: 项目根目录（默认为当前目录）
        batch_size: 批量更新大小（默认 5 个）
    """
    if root is None:
        root = Path.cwd()

    print(f"Generating modules.md for: {root}")
    print()

    # 阶段 1：生成骨架
    print("=" * 60)
    print("Phase 1: Creating skeleton...")
    print("=" * 60)
    create_skeleton_file(root)
    print()

    # 准备数据结构
    directories = find_all_directories(root)
    leaf_dirs = get_leaf_directories(directories)
    depth_map = get_directories_by_depth(directories, root)
    dir_summaries: Dict[Path, str] = {}

    print(f"Phase 1 completed. Found {len(directories)} directories, {len(leaf_dirs)} leaf dirs.")
    print()

    # 阶段 2：增量填充
    print("=" * 60)
    print("Phase 2: Incremental population...")
    print("=" * 60)
    print()

    # 2.1 分析叶子目录
    print(f"Analyzing {len(leaf_dirs)} leaf directories...")
    updates = []
    processed_count = 0

    for leaf_dir in leaf_dirs:
        # 分析代码
        summary = analyze_directory_code(leaf_dir)
        dir_summaries[leaf_dir] = summary
        updates.append((leaf_dir, summary))
        processed_count += 1

        # 批量更新
        if len(updates) >= batch_size:
            batch_update_descriptions(root, updates)
            update_progress_header(root, get_full_path(leaf_dir, root))
            print(f"  [{processed_count}/{len(leaf_dirs)}] Updated {len(updates)} leaf directories")
            updates.clear()

    # 更新剩余的叶子目录
    if updates:
        batch_update_descriptions(root, updates)
        print(f"  [{processed_count}/{len(leaf_dirs)}] Updated {len(updates)} leaf directories")
        updates.clear()

    print()

    # 2.2 分层向上传播
    print("Propagating summaries upward (by depth)...")
    max_depth = max(depth_map.keys()) if depth_map else 0

    for depth in range(max_depth - 1, -1, -1):
        if depth not in depth_map:
            continue

        print(f"  Depth {depth}: processing {len(depth_map[depth])} directories...")

        for dir_path in depth_map[depth]:
            if dir_path in leaf_dirs:
                continue  # 跳过叶子目录

            # 获取所有子目录的摘要
            child_dirs = [d for d in directories if d.parent == dir_path and d != dir_path]
            child_summaries = [dir_summaries.get(child, "") for child in child_dirs if child in dir_summaries]

            # 合并摘要
            summary = propagate_summary(dir_path, child_summaries)
            dir_summaries[dir_path] = summary
            updates.append((dir_path, summary))

            # 批量更新
            if len(updates) >= batch_size:
                batch_update_descriptions(root, updates)
                update_progress_header(root, get_full_path(dir_path, root))
                updates.clear()

        # 更新当前层级的剩余目录
        if updates:
            batch_update_descriptions(root, updates)
            updates.clear()

    print()

    # 完成
    print("=" * 60)
    print("Phase 2 completed!")
    print("=" * 60)
    print()

    # 移除进度头
    remove_progress_header(root)

    print("[OK] Generated modules.md successfully!")
    print(f"  Total directories: {len(directories)}")
    print(f"  Leaf directories analyzed: {len(leaf_dirs)}")
    print(f"  Parent directories propagated: {len(directories) - len(leaf_dirs)}")

# ============================================================================
# Interactive Mode Functions
# ============================================================================

def backup_existing_modules(root: Path) -> Path:
    """
    备份现有的 modules.md 文件。
    """
    from datetime import datetime
    import shutil

    modules_md_path = root / 'modules.md'
    if not modules_md_path.exists():
        return None

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = root / f'modules_{timestamp}.md'
    shutil.copy2(modules_md_path, backup_path)
    print(f'Backed up: modules.md -> {backup_path.name}')
    return backup_path


def parse_existing_descriptions(root: Path) -> Dict[str, str]:
    """
    解析现有的 modules.md，提取已分析的目录描述。
    """
    modules_md_path = root / 'modules.md'
    if not modules_md_path.exists():
        return {}

    descriptions = {}
    in_descriptions_section = False

    with open(modules_md_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '## Module Descriptions':
                in_descriptions_section = True
                continue
            if in_descriptions_section and line.startswith('##'):
                break
            if in_descriptions_section and ' - ' in line and not line.startswith('<!--'):
                path, desc = line.split(' - ', 1)
                descriptions[path] = desc

    return descriptions


def get_unanalyzed_directories(directories, existing_descriptions, root):
    """
    获取未分析的目录（描述为 [待分析] 或不存在）。
    """
    unanalyzed = []
    for dir_path in directories:
        full_path = get_full_path(dir_path, root)
        desc = existing_descriptions.get(full_path, '')
        if not desc or desc == '[待分析]':
            unanalyzed.append(dir_path)
    return unanalyzed


def get_new_directories(directories, existing_descriptions, root):
    """
    获取新增的目录。
    """
    new_dirs = []
    for dir_path in directories:
        full_path = get_full_path(dir_path, root)
        if full_path not in existing_descriptions:
            new_dirs.append(dir_path)
    return new_dirs


def interactive_mode(root):
    """
    交互式模式：检测重复执行并询问用户选择。
    """
    modules_md_path = root / 'modules.md'

    if not modules_md_path.exists():
        generate_modules_incremental(root)
        return

    print('=' * 60)
    print('Existing modules.md detected!')
    print('=' * 60)
    print()
    print('Please choose an option:')
    print('  1. Full overwrite (backup existing, regenerate from scratch)')
    print('  2. Continue unanalyzed directories (skip [待分析] only)')
    print('  3. Check new directories only (not in existing list)')
    print()
    
    while True:
        try:
            choice = input('Your choice (1/2/3): ').strip()

            if choice == '1':
                print()
                print('Option 1: Full overwrite...')
                backup_existing_modules(root)
                modules_md_path.unlink()
                generate_modules_incremental(root)
                break

            elif choice == '2':
                print()
                print('Option 2: Continuing unanalyzed directories...')
                existing_descriptions = parse_existing_descriptions(root)
                directories = find_all_directories(root)
                unanalyzed = get_unanalyzed_directories(directories, existing_descriptions, root)
                
                if not unanalyzed:
                    print('No unanalyzed directories found. All directories are already analyzed!')
                    return

                print(f'Found {len(unanalyzed)} unanalyzed directories to process.')
                print()
                update_progress_header(root, 'Processing unanalyzed directories')
                process_incremental_update(root, unanalyzed, existing_descriptions)
                break

            elif choice == '3':
                print()
                print('Option 3: Checking new directories...')
                existing_descriptions = parse_existing_descriptions(root)
                directories = find_all_directories(root)
                new_dirs = get_new_directories(directories, existing_descriptions, root)
                
                if not new_dirs:
                    print('No new directories found. All directories are already in the list!')
                    return

                print(f'Found {len(new_dirs)} new directories to process.')
                print()
                update_progress_header(root, 'Processing new directories')
                process_incremental_update(root, new_dirs, existing_descriptions)
                break

            else:
                print('Invalid choice. Please enter 1, 2, or 3.')
        except KeyboardInterrupt:
            print()
            print('Operation cancelled.')
            return
        except EOFError:
            print()
            print('Non-interactive mode detected. Using option 1 (full overwrite)...')
            backup_existing_modules(root)
            modules_md_path.unlink()
            generate_modules_incremental(root)
            break


def process_incremental_update(root, target_dirs, existing_descriptions):
    """
    处理增量更新（用于选项 2 和 3）。
    """
    directories = find_all_directories(root)
    dir_summaries = {}
    batch_size = 5
    depth_map = get_directories_by_depth(directories, root)
    max_depth = max(depth_map.keys()) if depth_map else 0
    updates = []

    for depth in range(max_depth, -1, -1):
        if depth not in depth_map:
            continue
        for dir_path in depth_map[depth]:
            if dir_path not in target_dirs:
                continue
            leaf_dirs = get_leaf_directories(directories)
            if dir_path in leaf_dirs:
                summary = analyze_directory_code(dir_path)
            else:
                child_dirs = [d for d in directories if d.parent == dir_path and d != dir_path]
                child_summaries = []
                for child in child_dirs:
                    full_path = get_full_path(child, root)
                    if child in dir_summaries:
                        child_summaries.append(dir_summaries[child])
                    elif full_path in existing_descriptions:
                        child_summaries.append(existing_descriptions[full_path])
                summary = propagate_summary(dir_path, child_summaries)
            dir_summaries[dir_path] = summary
            updates.append((dir_path, summary))
            if len(updates) >= batch_size:
                batch_update_descriptions(root, updates)
                update_progress_header(root, get_full_path(dir_path, root))
                print(f'  Updated {len(updates)} directories')
                updates.clear()

    if updates:
        batch_update_descriptions(root, updates)
        print(f'  Updated {len(updates)} directories')

    remove_progress_header(root)
    print()
    print('[OK] Incremental update completed!')
    print(f'  Directories processed: {len(target_dirs)}')



def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            # 执行两阶段增量生成
            root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
            interactive_mode(root)
        else:
            # 仅分析并打印（原有行为）
            root = Path(sys.argv[1])
            print_analysis(root)
    else:
        # 默认：仅分析
        root = Path.cwd()
        print_analysis(root)


if __name__ == "__main__":
    main()
