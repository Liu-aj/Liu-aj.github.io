#!/usr/bin/env python3
"""Wiki 文档质量批量修复"""
import os, re

BASE = '/home/liuaj/blog-jekyll'
DOCS = os.path.join(BASE, 'docs')

def clean_description_redundancy(path):
    """Step A: 清理 description 冗余后缀"""
    with open(path, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Match description lines with redundant suffixes
    # Pattern: description: ... — 核心知识点与实战指南 或类似
    new_content = re.sub(
        r'^(\s*description:\s*.+?)[\s—]+[—\-]*\s*核心知识点.*实战指南.*$',
        r'\1',
        content,
        flags=re.MULTILINE
    )
    # Also catch cases where just "— 核心知识点与实战指南" suffix exists
    new_content = re.sub(
        r'^(\s*description:\s*.+?)[\s—]+[—\-]*\s*核心知识点.*$',
        r'\1',
        new_content,
        flags=re.MULTILINE
    )
    new_content = re.sub(
        r'^(\s*description:\s*.+?)[\s—]+[—\-]*\s*实战指南.*$',
        r'\1',
        new_content,
        flags=re.MULTILINE
    )
    
    # Truncate description to 50 chars
    def truncate_desc(m):
        desc = m.group(1)
        if len(desc) > 50:
            desc = desc[:50]
        return f"description: {desc}"
    
    new_content = re.sub(
        r'^(\s*description:\s*.{1,200})',
        truncate_desc,
        new_content,
        flags=re.MULTILINE
    )
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def fix_separators(path):
    """Step C: 修复正文内孤立 --- 分隔符"""
    with open(path, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    fm = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm:
        return False
    
    fm_end_pos = fm.end()
    rest = content[fm_end_pos:]
    
    lines = rest.split('\n')
    in_code_block = False
    new_lines = []
    changed = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```') or stripped.startswith(':::'):
            in_code_block = not in_code_block
            new_lines.append(line)
        elif not in_code_block and stripped == '---':
            new_lines.append('***')
            changed = True
        else:
            new_lines.append(line)
    
    if not changed:
        return False
    
    new_rest = '\n'.join(new_lines)
    new_content = content[:fm_end_pos] + new_rest
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def handle_missing_description(path):
    """Step D: 处理缺失 description"""
    with open(path, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    fm = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm:
        return False
    
    frontmatter = fm.group(1)
    fm_end_pos = fm.end()
    
    if 'description:' in frontmatter:
        # Already has description - skip D
        return False
    
    # Extract H1 title
    rest = content[fm_end_pos:]
    h1_match = re.search(r'^#\s+(.+)$', rest, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else ''
    
    # Generate description
    if '404' in path:
        desc = '页面不存在'
    elif 'CLI' in path or '命令行' in title:
        desc = '命令行工具合集'
    elif title:
        # Take first 30 chars of title as description
        desc = title[:30]
    else:
        desc = os.path.basename(path).replace('.md', '')
    
    # Add description to frontmatter
    new_frontmatter = frontmatter.rstrip() + f'\ndescription: {desc}\n'
    new_content = '---\n' + new_frontmatter + '---\n' + rest
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


# ============ STEP A: Clean description redundancy ============
print("=== STEP A: 清理 description 冗余后缀 ===")
step_a_files = [
    'docs/ESP32嵌入式/esp32-family-2026.md',
    'docs/ESP32嵌入式/esp32-ds18b20-home-assistant-guide.md',
    'docs/ESP32嵌入式/esp32-motor-control-guide.md',
    'docs/ESP32嵌入式/esp32-ssd1306-oled.md',
    'docs/ESP32嵌入式/esp32-matter-guide.md',
    'docs/效率工具/changelog.md',
    'docs/效率工具/faq.md',
    'docs/效率工具/quickstart.md',
    'docs/软件工程/documentation.md',
    'docs/软件工程/contributing.md',
    'docs/软件工程/projects.md',
    'docs/智能家居/智能家居-总览.md',
    'docs/其他/2026-03-20-LangGraph-Workflow-Guide.md',
    'docs/硬件/raspberry-pi.md',
]
count_a = 0
for rel in step_a_files:
    path = os.path.join(BASE, rel)
    if os.path.exists(path):
        if clean_description_redundancy(path):
            print(f"  CLEANED: {rel}")
            count_a += 1
print(f"Step A 完成: {count_a} 个文件已清理\n")


# ============ STEP C: Fix --- separators ============
print("=== STEP C: 修复正文内孤立 --- 分隔符 ===")
count_c = 0
for root, dirs, files in os.walk(DOCS):
    for f in files:
        if not f.endswith('.md') or f == 'index.md':
            continue
        path = os.path.join(root, f)
        if fix_separators(path):
            rel = os.path.relpath(path, BASE)
            print(f"  FIXED: {rel}")
            count_c += 1
print(f"Step C 完成: {count_c} 个文件已修复\n")


# ============ STEP D: Handle missing description ============
print("=== STEP D: 处理缺失 description ===")

# First, find all files missing description
missing_desc = []
for root, dirs, files in os.walk(DOCS):
    for f in files:
        if not f.endswith('.md') or f == 'index.md':
            continue
        path = os.path.join(root, f)
        with open(path, encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        fm = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if fm and 'description:' not in fm.group(1):
            rel = os.path.relpath(path, BASE)
            missing_desc.append(rel)

count_d = 0
for rel in missing_desc:
    path = os.path.join(BASE, rel)
    if handle_missing_description(path):
        print(f"  ADDED desc: {rel}")
        count_d += 1
print(f"Step D 完成: {count_d} 个文件已补充 description")
print(f"仍缺失 description 的文件: {len(missing_desc) - count_d} 个")
