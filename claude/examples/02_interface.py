import json
from anthropic.types import ToolParam
from common import DRAFT

if __name__ == "__main__":
    tool: ToolParam = DRAFT
    print(json.dumps(tool, indent=2))
