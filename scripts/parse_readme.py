import re
import yaml
from pathlib import Path

README = Path('README.md')
TOOLS_FILE = Path('tools.yaml')


def parse_readme():
    tools = {}
    current_group = None
    pattern_heading = re.compile(r'^##\s+[^\[]*(\[.+\])?\s*(?P<group>.+)$')
    pattern_tool = re.compile(r'^\*\s+\[(?P<name>[^\]]+)\]\((?P<url>[^\)]+)\)')

    with README.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith('## '):
                m = pattern_heading.match(line)
                if m:
                    current_group = m.group('group').strip()
                    tools[current_group] = []
            elif line.startswith('* [') and current_group:
                m = pattern_tool.match(line)
                if m:
                    name = m.group('name').strip()
                    url = m.group('url').strip()
                    tools[current_group].append({'name': name, 'url': url})
    return tools


def main():
    tools = parse_readme()
    TOOLS_FILE.write_text(yaml.safe_dump(tools, sort_keys=False))
    print(f'Wrote {TOOLS_FILE}')


if __name__ == '__main__':
    main()
