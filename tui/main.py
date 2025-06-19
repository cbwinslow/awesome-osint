import asyncio
import webbrowser
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Input, TextLog, Button
from textual.containers import Horizontal, Vertical
import yaml
import json
from pathlib import Path

CONFIG_FILE = Path('config.json')
TOOLS_FILE = Path('tools.yaml')
API_LOG = Path('api_keys.log')


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def load_tools():
    if TOOLS_FILE.exists():
        with open(TOOLS_FILE) as f:
            return yaml.safe_load(f)
    return {}


class OSINTApp(App):
    CSS_PATH = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config()
        self.tools = load_tools()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            self.tree = Tree('OSINT Tools')
            for group, tools in self.tools.items():
                node = self.tree.root.add(group)
                for tool in tools:
                    node.add_leaf(tool['name'], data=tool)
            yield self.tree
            self.log = TextLog()
            yield self.log
        with Footer() as footer:
            yield footer

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        tool = event.node.data
        if tool and 'url' in tool:
            self.log.write(f"Opening {tool['name']} - {tool['url']}")
            webbrowser.open(tool['url'])

    async def action_save_config(self) -> None:
        save_config(self.config)
        self.log.write('Config saved')


if __name__ == '__main__':
    OSINTApp().run()
