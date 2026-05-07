#!/usr/bin/env python3
"""Fix front matter in all markdown files: add tags, clean descriptions, fix blank lines."""

import os
import re
import yaml
from pathlib import Path

# Tag mapping by directory and filename patterns
TAG_MAP = {
    # ESP32嵌入式
    "ESP32嵌入式": {
        "ESP32-总览.md": ["ESP32", "嵌入式", "IoT", "总览"],
        "esp32-matter-guide.md": ["ESP32", "Matter", "IoT", "智能家居"],
        "esp32-family-2026.md": ["ESP32", "嵌入式", "选型"],
        "esp32-ssd1306-oled.md": ["ESP32", "OLED", "SSD1306", "嵌入式"],
        "esp32-motor-control-guide.md": ["ESP32", "电机控制", "嵌入式", "PWM"],
        "esp32-ds18b20-home-assistant-guide.md": ["ESP32", "DS18B20", "Home Assistant", "传感器"],
    },
    # 智能家居
    "智能家居": {
        "智能家居-总览.md": ["智能家居", "Home Assistant", "IoT", "总览"],
        "ha-dashboard-theme-2026.md": ["Home Assistant", "仪表盘", "主题", "UI"],
        "ha-ble-beacon-location.md": ["Home Assistant", "蓝牙", "Beacon", "室内定位"],
        "zigbee2mqtt-guide-2026.md": ["Zigbee", "Zigbee2MQTT", "智能家居", "IoT"],
        "bambu-a1-support-optimization.md": ["3D打印", "Bambu", "切片软件", "支撑优化"],
    },
    # 硬件
    "硬件": {
        "raspberry-pi.md": ["树莓派", "Raspberry Pi", "硬件", "单板机"],
        "openwrt.md": ["OpenWRT", "路由器", "Linux", "网络"],
    },
    # Linux系统
    "Linux系统": {
        "linux-admin.md": ["Linux", "系统管理", "运维", "Shell"],
        "environment-setup.md": ["开发环境", "环境配置", "工具链"],
        "environment.md": ["环境变量", "Linux", "配置"],
        "debugging.md": ["调试", "Debug", "排查"],
        "terminal.md": ["终端", "Terminal", "命令行", "Shell"],
        "ssh.md": ["SSH", "远程登录", "安全", "Linux"],
        "wsl.md": ["WSL", "Windows", "Linux", "开发环境"],
    },
    # 效率工具
    "效率工具": {
        "quickstart.md": ["快速开始", "入门", "教程"],
        "guide.md": ["指南", "教程", "阅读指南"],
        "roadmap.md": ["学习路线", "Roadmap", "规划"],
        "comparison.md": ["技术对比", "比较", "选型"],
        "changelog.md": ["更新日志", "Changelog"],
        "updates.md": ["更新", "版本记录"],
        "productivity.md": ["效率", "生产力", "工具"],
        "shortcuts.md": ["快捷键", "效率", "工具"],
        "tools.md": ["工具", "效率", "开发工具"],
        "cheatsheet.md": ["速查表", "Cheatsheet", "参考"],
        "vim.md": ["Vim", "编辑器", "文本编辑"],
        "regex.md": ["正则表达式", "Regex", "文本处理"],
        "json-yaml.md": ["JSON", "YAML", "配置文件", "数据格式"],
        "markdown.md": ["Markdown", "文档", "写作"],
        "git-advanced.md": ["Git", "版本控制", "进阶"],
        "gitignore.md": ["Git", "Gitignore", "版本控制"],
        "privacy.md": ["隐私", "安全", "保护"],
        "learning.md": ["学习方法", "学习", "技巧"],
        "time-management.md": ["时间管理", "效率", "GTD"],
        "remote-work.md": ["远程办公", "Work from Home", "效率"],
        "scrum.md": ["Scrum", "敏捷", "项目管理"],
        "faq.md": ["FAQ", "常见问题", "Q&A"],
        "troubleshooting.md": ["问题排查", "Troubleshooting", "调试"],
        "insights.md": ["经验总结", "Insights", "最佳实践"],
        "interview.md": ["面试", "求职", "技术面试"],
        "best-practices.md": ["最佳实践", "Best Practices", "规范"],
        "error-handling.md": ["错误处理", "Error Handling", "异常"],
        "scripts.md": ["脚本", "Shell", "自动化"],
        "command-line.md": ["命令行", "CLI", "Shell"],
        "resources.md": ["资源", "资料", "汇总"],
        "glossary.md": ["术语表", "Glossary", "词汇"],
        "algorithms.md": ["算法", "Algorithms", "数据结构"],
        "datastructures.md": ["数据结构", "Data Structures"],
        "functional-programming.md": ["函数式编程", "Functional Programming"],
        "logic-programming.md": ["逻辑编程", "Logic Programming"],
        "event-driven.md": ["事件驱动", "Event Driven", "架构"],
        "async-programming.md": ["异步编程", "Async", "并发"],
        "javascript-advanced.md": ["JavaScript", "进阶", "Web开发"],
        "python-advanced.md": ["Python", "进阶", "后端开发"],
        "cross-platform.md": ["跨平台", "Cross Platform"],
        "mobile-development.md": ["移动开发", "Mobile", "App"],
    },
    # 软件工程
    "软件工程": {
        "architecture.md": ["架构设计", "Architecture", "系统设计"],
        "microservices.md": ["微服务", "Microservices", "架构"],
        "design-patterns.md": ["设计模式", "Design Patterns"],
        "clean-code.md": ["Clean Code", "代码质量", "规范"],
        "docker-advanced.md": ["Docker", "容器", "DevOps"],
        "docker-compose.md": ["Docker Compose", "容器编排", "Docker"],
        "container.md": ["容器化", "Container", "虚拟化"],
        "kubernetes.md": ["Kubernetes", "K8s", "容器编排"],
        "database-design.md": ["数据库设计", "Database Design"],
        "mysql.md": ["MySQL", "数据库", "SQL"],
        "mongodb.md": ["MongoDB", "NoSQL", "数据库"],
        "postgresql.md": ["PostgreSQL", "数据库", "SQL"],
        "redis.md": ["Redis", "缓存", "NoSQL"],
        "elasticsearch.md": ["Elasticsearch", "搜索引擎", "日志"],
        "uml.md": ["UML", "建模", "软件设计"],
        "ci-cd.md": ["CI/CD", "持续集成", "持续部署"],
        "github-actions.md": ["GitHub Actions", "CI/CD", "自动化"],
        "gitlab.md": ["GitLab", "CI/CD", "DevOps"],
        "gitops.md": ["GitOps", "DevOps", "自动化"],
        "version-control.md": ["版本控制", "VCS", "Git"],
        "devops.md": ["DevOps", "开发运维", "实践"],
        "cloud-native.md": ["云原生", "Cloud Native", "架构"],
        "sre.md": ["SRE", "站点可靠性", "运维"],
        "cloud.md": ["云服务", "Cloud", "基础设施"],
        "api-design.md": ["API设计", "API", "接口设计"],
        "rest-api.md": ["REST API", "RESTful", "API"],
        "graphql.md": ["GraphQL", "API", "查询语言"],
        "openapi.md": ["OpenAPI", "API", "规范"],
        "monitoring.md": ["监控", "Monitoring", "运维"],
        "prometheus.md": ["Prometheus", "监控", "指标"],
        "grafana.md": ["Grafana", "监控", "可视化"],
        "logging.md": ["日志", "Logging", "运维"],
        "observability.md": ["可观测性", "Observability", "监控"],
        "security.md": ["安全", "Security", "指南"],
        "security-testing.md": ["安全测试", "Security Testing"],
        "cryptography.md": ["密码学", "Cryptography", "安全"],
        "ssl-tls.md": ["SSL", "TLS", "安全", "证书"],
        "testing.md": ["测试", "Testing", "QA"],
        "testing-jest.md": ["Jest", "单元测试", "JavaScript"],
        "code-review.md": ["Code Review", "代码审查"],
        "code-analysis.md": ["代码分析", "Code Analysis"],
        "serverless.md": ["Serverless", "无服务器", "云"],
        "service-mesh.md": ["Service Mesh", "服务网格", "微服务"],
        "chaos-engineering.md": ["混沌工程", "Chaos Engineering"],
        "performance.md": ["性能优化", "Performance"],
        "web-performance.md": ["Web性能", "Web Performance"],
        "caching.md": ["缓存", "Cache", "性能优化"],
        "load-balancing.md": ["负载均衡", "Load Balancing"],
        "rate-limiting.md": ["限流", "Rate Limiting"],
        "nginx.md": ["Nginx", "Web服务器", "反向代理"],
        "networking.md": ["网络", "Networking", "基础"],
        "configuration-management.md": ["配置管理", "Configuration Management"],
        "web-security.md": ["Web安全", "Web Security"],
        "websockets.md": ["WebSocket", "实时通信", "Web开发"],
        "css.md": ["CSS", "前端", "样式"],
        "contributing.md": ["贡献指南", "Contributing", "开源"],
        "documentation.md": ["文档", "Documentation", "编写"],
        "projects.md": ["项目管理", "Projects"],
    },
}

# Generic descriptions to remove or replace
GENERIC_DESCRIPTIONS = {
    "ESP32嵌入式开发总览": "ESP32是一款支持Wi-Fi和蓝牙的物联网芯片，广泛应用于智能家居和嵌入式开发",
    "系统架构设计模式": "整理常见架构设计模式",
    "Linux系统管理指南": "Linux系统管理常用命令",
    "Vim编辑器完全指南": "Vi IMproved - 强大的文本编辑器",
}

docs_root = Path("/home/liuaj/blog-jekyll/docs")

def fix_file(filepath: Path) -> bool:
    """Fix front matter in a single file. Returns True if changed."""
    content = filepath.read_text(encoding="utf-8")
    
    # Check if file has front matter
    if not content.startswith("---"):
        # No front matter at all - add one at the top
        # Determine category from path
        rel_path = filepath.relative_to(docs_root)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "其他"
        filename = rel_path.parts[-1]
        
        # Get tags
        tags = ["文档"]
        if category in TAG_MAP and filename in TAG_MAP[category]:
            tags = TAG_MAP[category][filename]
        
        front_matter = f"---\ntitle: {filename.replace('.md', '')}\ntags:\n" + "".join(f"  - {t}\n" for t in tags) + "---\n\n"
        content = front_matter + content
        filepath.write_text(content, encoding="utf-8")
        print(f"ADDED front matter: {filepath}")
        return True
    
    # Has front matter - parse it
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    
    front_raw = parts[1]
    body = parts[2]
    
    # Fix blank lines in front matter (remove empty lines within front matter)
    lines = front_raw.split('\n')
    fixed_lines = []
    for line in lines:
        if line.strip() == '' and fixed_lines and fixed_lines[-1].strip() == '---':
            continue  # skip blank line after opening ---
        fixed_lines.append(line)
    
    # Re-parse
    front_text = '\n'.join(fixed_lines)
    
    try:
        fm = yaml.safe_load(front_text)
        if fm is None:
            fm = {}
    except yaml.YAMLError as e:
        print(f"YAML parse error in {filepath}: {e}")
        return False
    
    # Determine category
    rel_path = filepath.relative_to(docs_root)
    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "其他"
    filename = rel_path.parts[-1]
    
    # Add tags if missing
    changed = False
    if "tags" not in fm or not fm["tags"]:
        if category in TAG_MAP and filename in TAG_MAP[category]:
            fm["tags"] = TAG_MAP[category][filename]
        else:
            fm["tags"] = ["文档"]
        changed = True
    
    # Clean generic description
    if "description" in fm:
        desc = str(fm["description"])
        if desc in GENERIC_DESCRIPTIONS:
            fm["description"] = GENERIC_DESCRIPTIONS[desc]
            changed = True
        elif desc.endswith("指南") or desc.endswith("总览") or desc.endswith("教程"):
            # Keep it but it's not generic
            pass
    
    # Remove description if it's just the title
    if "description" in fm and "title" in fm:
        if fm["description"] == fm["title"]:
            del fm["description"]
            changed = True
    
    if not changed:
        return False
    
    # Re-serialize front matter
    new_front = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    new_front = new_front.rstrip() + "\n"
    
    new_content = f"---\n{new_front}---{body}"
    filepath.write_text(new_content, encoding="utf-8")
    print(f"UPDATED front matter: {filepath}")
    return True


def main():
    count = 0
    for md_file in docs_root.rglob("*.md"):
        # Skip index files, 404, assets
        if "/assets/" in str(md_file):
            continue
        if md_file.name in ("index.md", "404.md"):
            continue
        try:
            if fix_file(md_file):
                count += 1
        except Exception as e:
            print(f"ERROR {md_file}: {e}")
    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
