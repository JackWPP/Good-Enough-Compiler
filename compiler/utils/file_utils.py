#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块

提供安全的文件操作和实用工具：
- 安全文件读写
- 目录管理
- 文件类型检测
- 语言检测
"""

import os
import pathlib
from typing import Optional, Tuple, List, Dict


def read_file_safe(filename: str, encoding: str = 'utf-8') -> Tuple[Optional[str], Optional[str]]:
    """
    安全读取文件
    
    Args:
        filename: 文件路径
        encoding: 文件编码
    
    Returns:
        (文件内容, 错误信息) 元组
    """
    try:
        with open(filename, 'r', encoding=encoding) as f:
            content = f.read()
        return content, None
    except FileNotFoundError:
        return None, f"文件不存在: {filename}"
    except PermissionError:
        return None, f"没有读取权限: {filename}"
    except UnicodeDecodeError as e:
        return None, f"编码错误: {e}"
    except Exception as e:
        return None, f"读取文件失败: {e}"


def write_file_safe(filename: str, content: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    安全写入文件
    
    Args:
        filename: 文件路径
        content: 文件内容
        encoding: 文件编码
    
    Returns:
        错误信息，成功时返回None
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(filename)
        if directory:
            ensure_directory(directory)
        
        with open(filename, 'w', encoding=encoding) as f:
            f.write(content)
        return None
    except PermissionError:
        return f"没有写入权限: {filename}"
    except Exception as e:
        return f"写入文件失败: {e}"


def ensure_directory(directory: str) -> bool:
    """
    确保目录存在
    
    Args:
        directory: 目录路径
    
    Returns:
        是否成功创建或目录已存在
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    
    Args:
        filename: 文件路径
    
    Returns:
        文件扩展名（小写，不包含点）
    """
    return pathlib.Path(filename).suffix.lower().lstrip('.')


def detect_language(filename: str, content: Optional[str] = None) -> str:
    """
    检测编程语言
    
    Args:
        filename: 文件路径
        content: 文件内容（可选）
    
    Returns:
        检测到的语言名称
    """
    # 基于文件扩展名的检测
    extension = get_file_extension(filename)
    
    extension_map = {
        'c': 'c',
        'h': 'c',
        'cpp': 'cpp',
        'cxx': 'cpp',
        'cc': 'cpp',
        'hpp': 'cpp',
        'hxx': 'cpp',
        'pas': 'pascal',
        'pascal': 'pascal',
        'pp': 'pascal',
        'inc': 'pascal',
        'py': 'python',
        'java': 'java',
        'js': 'javascript',
        'ts': 'typescript',
        'go': 'go',
        'rs': 'rust',
        'swift': 'swift',
        'kt': 'kotlin',
        'scala': 'scala',
        'rb': 'ruby',
        'php': 'php',
        'cs': 'csharp',
        'vb': 'vb',
        'fs': 'fsharp',
        'ml': 'ocaml',
        'hs': 'haskell',
        'elm': 'elm',
        'clj': 'clojure',
        'lisp': 'lisp',
        'scm': 'scheme',
        'pl': 'perl',
        'lua': 'lua',
        'r': 'r',
        'matlab': 'matlab',
        'm': 'matlab',
        'sql': 'sql',
        'sh': 'shell',
        'bash': 'shell',
        'zsh': 'shell',
        'fish': 'shell',
        'ps1': 'powershell',
        'bat': 'batch',
        'cmd': 'batch'
    }
    
    if extension in extension_map:
        return extension_map[extension]
    
    # 基于内容的检测（如果提供了内容）
    if content:
        content_lower = content.lower()
        
        # C语言特征
        c_keywords = ['#include', 'int main', 'printf', 'scanf', 'malloc', 'free']
        if any(keyword in content_lower for keyword in c_keywords):
            return 'c'
        
        # Pascal语言特征
        pascal_keywords = ['program ', 'begin', 'end.', 'var ', 'procedure ', 'function ']
        if any(keyword in content_lower for keyword in pascal_keywords):
            return 'pascal'
        
        # Python特征
        python_keywords = ['def ', 'import ', 'from ', 'class ', 'if __name__']
        if any(keyword in content_lower for keyword in python_keywords):
            return 'python'
        
        # Java特征
        java_keywords = ['public class', 'public static void main', 'import java']
        if any(keyword in content_lower for keyword in java_keywords):
            return 'java'
    
    return 'unknown'


def get_language_info(language: str) -> Dict[str, str]:
    """
    获取语言信息
    
    Args:
        language: 语言名称
    
    Returns:
        语言信息字典
    """
    language_info = {
        'c': {
            'name': 'C',
            'description': 'C语言',
            'extensions': ['.c', '.h'],
            'comment_single': '//',
            'comment_multi_start': '/*',
            'comment_multi_end': '*/'
        },
        'cpp': {
            'name': 'C++',
            'description': 'C++语言',
            'extensions': ['.cpp', '.cxx', '.cc', '.hpp', '.hxx'],
            'comment_single': '//',
            'comment_multi_start': '/*',
            'comment_multi_end': '*/'
        },
        'pascal': {
            'name': 'Pascal',
            'description': 'Pascal语言',
            'extensions': ['.pas', '.pascal', '.pp', '.inc'],
            'comment_single': '//',
            'comment_multi_start': '{',
            'comment_multi_end': '}'
        },
        'python': {
            'name': 'Python',
            'description': 'Python语言',
            'extensions': ['.py', '.pyw'],
            'comment_single': '#',
            'comment_multi_start': '"""',
            'comment_multi_end': '"""'
        },
        'java': {
            'name': 'Java',
            'description': 'Java语言',
            'extensions': ['.java'],
            'comment_single': '//',
            'comment_multi_start': '/*',
            'comment_multi_end': '*/'
        }
    }
    
    return language_info.get(language, {
        'name': language.title(),
        'description': f'{language.title()}语言',
        'extensions': [],
        'comment_single': '//',
        'comment_multi_start': '/*',
        'comment_multi_end': '*/'
    })


def list_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """
    列出指定目录下特定扩展名的文件
    
    Args:
        directory: 目录路径
        extensions: 扩展名列表（不包含点）
    
    Returns:
        文件路径列表
    """
    files = []
    
    try:
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if get_file_extension(filename) in extensions:
                    files.append(os.path.join(root, filename))
    except Exception:
        pass
    
    return files


def get_file_info(filename: str) -> Dict[str, str]:
    """
    获取文件信息
    
    Args:
        filename: 文件路径
    
    Returns:
        文件信息字典
    """
    try:
        stat = os.stat(filename)
        return {
            'name': os.path.basename(filename),
            'path': os.path.abspath(filename),
            'size': str(stat.st_size),
            'extension': get_file_extension(filename),
            'language': detect_language(filename),
            'exists': 'True',
            'readable': str(os.access(filename, os.R_OK)),
            'writable': str(os.access(filename, os.W_OK))
        }
    except Exception:
        return {
            'name': os.path.basename(filename),
            'path': os.path.abspath(filename),
            'size': '0',
            'extension': get_file_extension(filename),
            'language': detect_language(filename),
            'exists': 'False',
            'readable': 'False',
            'writable': 'False'
        }


def create_backup(filename: str) -> Optional[str]:
    """
    创建文件备份
    
    Args:
        filename: 原文件路径
    
    Returns:
        备份文件路径，失败时返回None
    """
    try:
        import shutil
        import datetime
        
        # 生成备份文件名
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{filename}.backup_{timestamp}"
        
        # 复制文件
        shutil.copy2(filename, backup_filename)
        return backup_filename
    except Exception:
        return None


def find_files(directory: str, pattern: str) -> List[str]:
    """
    查找匹配模式的文件
    
    Args:
        directory: 搜索目录
        pattern: 文件名模式（支持通配符）
    
    Returns:
        匹配的文件路径列表
    """
    import glob
    
    try:
        search_pattern = os.path.join(directory, '**', pattern)
        return glob.glob(search_pattern, recursive=True)
    except Exception:
        return []


def get_relative_path(filepath: str, base_path: str) -> str:
    """
    获取相对路径
    
    Args:
        filepath: 文件路径
        base_path: 基准路径
    
    Returns:
        相对路径
    """
    try:
        return os.path.relpath(filepath, base_path)
    except Exception:
        return filepath


def normalize_path(path: str) -> str:
    """
    标准化路径
    
    Args:
        path: 原始路径
    
    Returns:
        标准化后的路径
    """
    return os.path.normpath(os.path.abspath(path))


def is_text_file(filename: str) -> bool:
    """
    判断是否为文本文件
    
    Args:
        filename: 文件路径
    
    Returns:
        是否为文本文件
    """
    text_extensions = {
        'txt', 'md', 'rst', 'log', 'cfg', 'conf', 'ini', 'json', 'xml', 'yaml', 'yml',
        'c', 'h', 'cpp', 'cxx', 'cc', 'hpp', 'hxx', 'pas', 'pascal', 'pp', 'inc',
        'py', 'java', 'js', 'ts', 'go', 'rs', 'swift', 'kt', 'scala', 'rb', 'php',
        'cs', 'vb', 'fs', 'ml', 'hs', 'elm', 'clj', 'lisp', 'scm', 'pl', 'lua',
        'r', 'matlab', 'm', 'sql', 'sh', 'bash', 'zsh', 'fish', 'ps1', 'bat', 'cmd'
    }
    
    extension = get_file_extension(filename)
    return extension in text_extensions


def get_file_encoding(filename: str) -> str:
    """
    检测文件编码
    
    Args:
        filename: 文件路径
    
    Returns:
        检测到的编码
    """
    try:
        import chardet
        
        with open(filename, 'rb') as f:
            raw_data = f.read()
        
        result = chardet.detect(raw_data)
        return result.get('encoding', 'utf-8')
    except ImportError:
        # 如果没有chardet，尝试常见编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        
        return 'utf-8'  # 默认返回utf-8
    except Exception:
        return 'utf-8'