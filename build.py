"""Build script for vivarium_ai_tools dual-platform plugin.

Generates platform-specific plugin output for both GitHub Copilot (VS Code)
and Claude Code from canonical source definitions in src/.

Usage:
    python build.py              # Build both platforms
    python build.py copilot      # Build only Copilot output
    python build.py claude-code  # Build only Claude Code output
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
DIST_DIR = ROOT / "dist"

COPILOT_DIR = DIST_DIR / "copilot"
CLAUDE_DIR = DIST_DIR / "claude-code"

# Metadata shared across both manifests
PLUGIN_META = {
    "name": "vivarium-ai-tools",
    "version": "0.1.0",
    "description": "Custom agent workflows for vivarium development.",
    "publisher": "ihmeuw",
}

# Frontmatter fields per platform
COPILOT_FIELDS = {
    "name",
    "description",
    "argument-hint",
    "tools",  # mapped from copilot-tools
    "agents",
    "user-invocable",
}

CLAUDE_FIELDS = {
    "name",
    "description",
    "tools",  # mapped from claude-tools
    "disallowedTools",
    "model",
    "effort",
    "maxTurns",
    "skills",
    "memory",
    "background",
    "isolation",
    "user-invocable",
}

# ---------------------------------------------------------------------------
# YAML frontmatter parser (minimal, no pyyaml dependency)
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body) where body is the content after the
    closing --- delimiter.
    """
    if not text.startswith("---"):
        return {}, text

    # Find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[4:end]  # skip opening ---\n
    body = text[end + 4 :]  # skip \n---\n

    frontmatter = _parse_yaml_block(yaml_block)
    return frontmatter, body


def _parse_yaml_block(block: str) -> dict:
    """Parse a simple YAML block into a dict.

    Handles: string values (quoted/unquoted), arrays (inline [...]),
    booleans, and numbers. Does NOT handle nested objects or multi-line values.
    """
    result = {}
    for line in block.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Split on first colon
        colon_idx = line.find(":")
        if colon_idx == -1:
            continue
        key = line[:colon_idx].strip()
        value = line[colon_idx + 1 :].strip()
        result[key] = _parse_yaml_value(value)
    return result


def _parse_yaml_value(value: str):
    """Parse a single YAML value."""
    if not value:
        return None

    # Quoted string
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    # Inline array [a, b, c]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
        if not inner.strip():
            return []
        items = []
        for item in inner.split(","):
            item = item.strip()
            # Strip quotes from items
            if (item.startswith('"') and item.endswith('"')) or (
                item.startswith("'") and item.endswith("'")
            ):
                item = item[1:-1]
            items.append(item)
        return items

    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Number
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass

    # Plain string (may contain commas for space-separated tool lists)
    return value


# ---------------------------------------------------------------------------
# Frontmatter serializer
# ---------------------------------------------------------------------------


def serialize_frontmatter(data: dict) -> str:
    """Serialize a dict back to YAML frontmatter string."""
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {_serialize_value(value)}")
    lines.append("---")
    return "\n".join(lines)


def _serialize_value(value) -> str:
    """Serialize a single value to YAML."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, list):
        items = ", ".join(
            f'"{v}"' if " " in str(v) or "," in str(v) else str(v) for v in value
        )
        return f"[{items}]"
    # String — quote if it contains special chars
    s = str(value)
    if any(c in s for c in ":{}[]#,&*!|>'\"%@`"):
        return f'"{s}"'
    return s


# ---------------------------------------------------------------------------
# Platform-conditional block stripping
# ---------------------------------------------------------------------------


def strip_platform_blocks(body: str, keep: str) -> str:
    """Remove conditional blocks for the other platform, unwrap kept ones."""
    other = "claude-code" if keep == "copilot" else "copilot"
    # Remove other platform's blocks entirely
    body = re.sub(
        rf"<!-- {re.escape(other)}-only -->\n.*?<!-- /{re.escape(other)}-only -->\n",
        "",
        body,
        flags=re.DOTALL,
    )
    # Unwrap this platform's blocks (keep content, remove markers)
    body = re.sub(rf"<!-- {re.escape(keep)}-only -->\n", "", body)
    body = re.sub(rf"<!-- /{re.escape(keep)}-only -->\n", "", body)
    return body


# ---------------------------------------------------------------------------
# Build functions
# ---------------------------------------------------------------------------


def build_copilot_agent(src_path: Path, dest_dir: Path) -> None:
    """Build a single agent file for Copilot."""
    text = src_path.read_text()
    frontmatter, body = parse_frontmatter(text)

    # Map copilot-tools → tools
    copilot_fm = {}
    for key in ("name", "description", "argument-hint", "agents", "user-invocable"):
        if key in frontmatter:
            copilot_fm[key] = frontmatter[key]

    if "copilot-tools" in frontmatter:
        copilot_fm["tools"] = frontmatter["copilot-tools"]

    # Strip platform-conditional blocks
    body = strip_platform_blocks(body, "copilot")

    # Write with .agent.md extension
    stem = src_path.stem
    dest_path = dest_dir / f"{stem}.agent.md"
    dest_path.write_text(serialize_frontmatter(copilot_fm) + "\n" + body)


def build_claude_agent(src_path: Path, dest_dir: Path) -> None:
    """Build a single agent file for Claude Code."""
    text = src_path.read_text()
    frontmatter, body = parse_frontmatter(text)

    # Map claude-tools → tools
    claude_fm = {}
    for key in (
        "name",
        "description",
        "model",
        "effort",
        "maxTurns",
        "skills",
        "memory",
        "background",
        "isolation",
        "disallowedTools",
    ):
        if key in frontmatter:
            claude_fm[key] = frontmatter[key]

    if "claude-tools" in frontmatter:
        claude_fm["tools"] = frontmatter["claude-tools"]

    # user-invocable: false → not included (Claude uses description-based invocation)
    # But we can keep it for skills if needed

    # Strip platform-conditional blocks
    body = strip_platform_blocks(body, "claude-code")

    # Write with .md extension
    dest_path = dest_dir / src_path.name
    dest_path.write_text(serialize_frontmatter(claude_fm) + "\n" + body)


def build_claude_command(src_path: Path, dest_dir: Path) -> bool:
    """Emit a slash-command wrapper for an agent flagged user-invocable.

    Returns True if a command file was written, False if the agent opted out.
    """
    frontmatter, _body = parse_frontmatter(src_path.read_text())
    if not frontmatter.get("user-invocable"):
        return False

    agent_name = frontmatter["name"]
    command_fm = {}
    if "description" in frontmatter:
        command_fm["description"] = frontmatter["description"]
    if "argument-hint" in frontmatter:
        command_fm["argument-hint"] = frontmatter["argument-hint"]

    body = (
        f"\nUse the `{agent_name}` subagent to handle the following request.\n"
        f"\n$ARGUMENTS\n"
    )
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f"{agent_name}.md"
    dest_path.write_text(serialize_frontmatter(command_fm) + body)
    return True


def build_copilot(src_dir: Path, dest_dir: Path) -> None:
    """Build the full Copilot plugin."""
    # Clean and recreate
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    agents_dir = dest_dir / "agents"
    agents_dir.mkdir(parents=True)

    # Generate plugin.json
    manifest = {
        "name": PLUGIN_META["name"],
        "displayName": "Vivarium AI Tools",
        "description": PLUGIN_META["description"],
        "publisher": PLUGIN_META["publisher"],
    }
    (dest_dir / "plugin.json").write_text(json.dumps(manifest, indent=4) + "\n")

    # Build each agent
    for src_file in sorted((src_dir / "agents").glob("*.md")):
        build_copilot_agent(src_file, agents_dir)

    print(f"  Copilot plugin built → {dest_dir.relative_to(ROOT)}/")


def build_claude_code(src_dir: Path, dest_dir: Path) -> None:
    """Build the full Claude Code plugin in marketplace-of-one layout.

    dest_dir/
      .claude-plugin/marketplace.json
      plugins/<name>/
        .claude-plugin/plugin.json
        agents/  hooks/  skills/
    """
    # Clean and recreate
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    plugin_root = dest_dir / "plugins" / PLUGIN_META["name"]
    agents_dir = plugin_root / "agents"
    agents_dir.mkdir(parents=True)

    # Plugin manifest: <plugin_root>/.claude-plugin/plugin.json
    plugin_meta_dir = plugin_root / ".claude-plugin"
    plugin_meta_dir.mkdir(parents=True)
    plugin_manifest = {
        "name": PLUGIN_META["name"],
        "version": PLUGIN_META["version"],
        "description": PLUGIN_META["description"],
        "author": {"name": PLUGIN_META["publisher"]},
    }
    (plugin_meta_dir / "plugin.json").write_text(
        json.dumps(plugin_manifest, indent=4) + "\n"
    )

    # Marketplace manifest: <dest_dir>/.claude-plugin/marketplace.json
    marketplace_meta_dir = dest_dir / ".claude-plugin"
    marketplace_meta_dir.mkdir(parents=True)
    marketplace_manifest = {
        "name": PLUGIN_META["name"],
        "owner": {"name": PLUGIN_META["publisher"]},
        "plugins": [
            {
                "name": PLUGIN_META["name"],
                "source": f"./plugins/{PLUGIN_META['name']}",
                "description": PLUGIN_META["description"],
                "version": PLUGIN_META["version"],
            }
        ],
    }
    (marketplace_meta_dir / "marketplace.json").write_text(
        json.dumps(marketplace_manifest, indent=4) + "\n"
    )

    # Build each agent, and a slash-command wrapper for any agent
    # whose source frontmatter sets user-invocable: true.
    commands_dir = plugin_root / "commands"
    for src_file in sorted((src_dir / "agents").glob("*.md")):
        build_claude_agent(src_file, agents_dir)
        build_claude_command(src_file, commands_dir)

    # Copy skills if they exist
    skills_src = src_dir / "skills"
    if skills_src.exists() and any(skills_src.iterdir()):
        shutil.copytree(skills_src, plugin_root / "skills")

    # Copy hooks if they exist
    hooks_src = src_dir / "hooks"
    if hooks_src.exists() and any(hooks_src.iterdir()):
        hooks_dest = plugin_root / "hooks"
        hooks_dest.mkdir(parents=True, exist_ok=True)
        for hook_file in hooks_src.glob("*.json"):
            shutil.copy2(hook_file, hooks_dest)

    print(f"  Claude Code plugin built → {dest_dir.relative_to(ROOT)}/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["copilot", "claude-code"]

    print("Building vivarium-ai-tools plugin:")
    for target in targets:
        if target == "copilot":
            build_copilot(SRC_DIR, COPILOT_DIR)
        elif target == "claude-code":
            build_claude_code(SRC_DIR, CLAUDE_DIR)
        else:
            print(f"  Unknown target: {target}", file=sys.stderr)
            sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
