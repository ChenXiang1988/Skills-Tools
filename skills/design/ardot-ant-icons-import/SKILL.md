---
name: ardot-ant-icons-import
description: Import Ant Design icons into Ardot prototypes by converting SVGs to
  colored transparent PNGs and applying them as image fills to rectangle nodes
agent_created: true
disable: true
---

# Ardot Ant Icons Import

## Overview

When designing Ardot prototypes for mobile or web interfaces that need real, consistent icons instead of hand-drawn geometric shapes, convert Ant Design outline icons into uniformly colored PNGs and upload them as image fills to Ardot `RECTANGLE` nodes.

## When to Use

- An Ardot prototype needs a set of recognizable, consistent icons.
- The visual system aligns with Ant Design Mobile or any brand-color system that can use Ant Design's outline icons.
- ardot has no built-in online icon search, and `upload_images` supports only PNG/JPEG/WEBP (not SVG).
- The team does not have a published Ardot icon component library.

## Prerequisites

- `rsvg-convert` is installed and available (e.g., `/opt/homebrew/bin/rsvg-convert` on macOS via Homebrew `librsvg`).
- `npm` is configured and the managed Node workspace is available at `/Users/martin/.workbuddy/binaries/node/workspace`.
- The target ardot file is open and the icon containers already exist or are about to be created.

## Workflow

### Step 1: Select Icon Names from Ant Design

Choose icon names from the `@ant-design/icons-svg` package under `inline-svg/outlined/<name>.svg`. Common names for PDA/warehouse apps include: `scan`, `inbox`, `profile`, `search`, `audit`, `swap`, `send`, `user`, `group`, `home`, `file-text`, `bell`.

### Step 2: Install/Get SVG Source Files

Install the `@ant-design/icons-svg` package into the managed Node workspace and copy the needed SVGs to a temporary directory.

```bash
cd /Users/martin/.workbuddy/binaries/node/workspace
npm install @ant-design/icons-svg
SVG_SRC="/Users/martin/.workbuddy/binaries/node/workspace/node_modules/@ant-design/icons-svg/inline-svg/outlined"
TMP_SVG="/Users/martin/Documents/Martinjob/云仓项目/.workbuddy/tmp/ant-icons/svg"
mkdir -p "$TMP_SVG"
for n in scan inbox profile search audit swap send user group home file-text bell; do
  cp "$SVG_SRC/$n.svg" "$TMP_SVG/$n.svg"
done
```

### Step 3: Inject Brand Color and Convert to PNG

Inject the brand color (e.g., `#1664FF`) into each SVG and convert to a 120×120 transparent PNG.

```bash
BRAND="#1664FF"
TMP_PNG="/Users/martin/Documents/Martinjob/云仓项目/.workbuddy/tmp/ant-icons/png"
mkdir -p "$TMP_PNG"
for n in scan inbox profile search audit swap send user group home file-text bell; do
  sed -i '' "s/<svg /<svg fill=\"$BRAND\" /" "$TMP_SVG/$n.svg"
  /opt/homebrew/bin/rsvg-convert -w 120 -h 120 "$TMP_SVG/$n.svg" -o "$TMP_PNG/$n.png"
done
```

### Step 4: Create Icon Rectangle Containers in Ardot

Use `mcp__ardot__batch_edit` to create a `RECTANGLE` node for each icon at the desired position and size. Give each node a descriptive name (e.g., `img-scan`) so that the returned IDs can be mapped to the correct PNG files.

### Step 5: Upload PNGs to Ardot Nodes

Use `mcp__ardot__upload_images` with an `items` array mapping each created `nodeId` to the matching PNG file path.

```json
{
  "fileId": "704126554514162",
  "items": [
    {"nodeId": "16:41", "filePath": ".../scan.png"},
    {"nodeId": "16:42", "filePath": ".../inbox.png"}
  ]
}
```

### Step 6: Clean Up Legacy Icons (Optional)

If legacy hand-drawn geometric icon nodes exist beneath the new image fills, either leave them covered or delete them via `mcp__ardot__batch_edit` `D("nodeId")`.

## Important Constraints

- ardot does **not** support direct SVG upload.
- ardot does **not** support online icon search or embedding.
- `upload_images` replaces the target node's fill with an image fill; place the image rectangle on top of a colored tile or button so that transparent areas show the intended background.
- Generated PNGs are raster; use at least 120×120 pixels for prototype clarity.

## Resources

This skill is a pure workflow; no bundled scripts or references are required.
