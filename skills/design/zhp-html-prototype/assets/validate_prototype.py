#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zhp-html-prototype 校验脚本（仅用标准库，无需 pip 安装）。

用法（在 prototypes/ 目录内运行）：
    python3 assets/validate_prototype.py

检查项：
  1. 目录结构：assets/ 、shared/ 、index.html 是否存在
  2. 公共资源齐全：design-tokens.json / prototype.css / app-shell.js / menu-config.js
  3. 每个业务页(.html, 排除 index.html)是否引用公共 CSS 与共享脚本。
     移动端页（含 device-frame.css）走移动端检查项，PC 页走 PC 检查项。
  4. 菜单配置非空（window.PROTOTYPE_MENU 至少一项）
  5. 入口页 index.html 是否引用 shared/menu-config.js（保证菜单可渲染）
退出码 0=全部通过，1=存在失败项。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("  [FAIL] " + msg)


def ok(msg):
    print("  [ OK ] " + msg)


def check_structure():
    print("== 1. 目录结构 ==")
    for d in ("assets", "shared"):
        if os.path.isdir(os.path.join(ROOT, d)):
            ok(f"{d}/ 存在")
        else:
            fail(f"{d}/ 目录缺失")
    if os.path.isfile(os.path.join(ROOT, "index.html")):
        ok("index.html 存在")
    else:
        fail("index.html 缺失（原型集合入口页）")


def check_assets():
    print("== 2. 公共资源齐全 ==")
    required = [
        ("assets/design-tokens.json", "design-tokens.json"),
        ("assets/prototype.css", "prototype.css"),
        ("shared/app-shell.js", "app-shell.js"),
        ("shared/menu-config.js", "menu-config.js"),
    ]
    for rel, name in required:
        if os.path.isfile(os.path.join(ROOT, rel)):
            ok(f"{rel} 存在")
        else:
            fail(f"{rel} 缺失")


def check_pages():
    print("== 3. 业务页引用检查 ==")
    htmls = [
        f for f in os.listdir(ROOT)
        if f.endswith(".html") and f != "index.html"
    ]
    if not htmls:
        ok("无业务页（跳过）")
        return
    for f in htmls:
        path = os.path.join(ROOT, f)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        # 评审页（界面↔文档连线件）：含 #conn-svg 或 .review-stage 即视为评审页
        if 'id="conn-svg"' in content or 'review-stage' in content:
            if 'assets/connect-lines.js' in content:
                ok(f"{f}: 评审页 · 引用 connect-lines.js（连线引擎）")
            else:
                fail(f"{f}: 评审页 · 未引用 assets/connect-lines.js")
            if 'assets/prototype-doc.css' in content:
                ok(f"{f}: 评审页 · 引用 prototype-doc.css")
            else:
                fail(f"{f}: 评审页 · 未引用 assets/prototype-doc.css")
            if 'assets/device-frame.css' in content:
                ok(f"{f}: 评审页 · 引用 device-frame.css（手机视图）")
            else:
                fail(f"{f}: 评审页 · 未引用 assets/device-frame.css（手机视图）")
            if 'assets/prototype-mobile.css' in content:
                ok(f"{f}: 评审页 · 引用 prototype-mobile.css（手机视图）")
            else:
                fail(f"{f}: 评审页 · 未引用 assets/prototype-mobile.css（手机视图）")
            continue
        # 移动端页：含 device-frame.css 即视为移动端，走移动端检查项
        if 'device-frame.css' in content:
            if 'assets/device-frame.css' in content:
                ok(f"{f}: 移动端页 · 引用 device-frame.css")
            else:
                fail(f"{f}: 移动端页 · 未引用 assets/device-frame.css")
            if 'assets/prototype-mobile.css' in content:
                ok(f"{f}: 移动端页 · 引用 prototype-mobile.css")
            else:
                fail(f"{f}: 移动端页 · 未引用 assets/prototype-mobile.css")
            if 'assets/prototype.css' in content:
                ok(f"{f}: 移动端页 · 引用 prototype.css（设计令牌）")
            else:
                fail(f"{f}: 移动端页 · 未引用 assets/prototype.css（设计令牌）")
            continue
        # PC 页：维持原检查项
        if 'assets/prototype.css' in content:
            ok(f"{f}: 引用 prototype.css")
        else:
            fail(f"{f}: 未引用 assets/prototype.css")
        if 'shared/app-shell.js' in content:
            ok(f"{f}: 引用 app-shell.js")
        else:
            fail(f"{f}: 未引用 shared/app-shell.js")
        if 'shared/menu-config.js' in content:
            ok(f"{f}: 引用 menu-config.js")
        else:
            fail(f"{f}: 未引用 shared/menu-config.js")
        if 'renderShell(' in content:
            ok(f"{f}: 调用 renderShell（菜单激活态）")
        else:
            fail(f"{f}: 未调用 renderShell()")


def check_menu():
    print("== 4. 菜单配置非空 ==")
    mc = os.path.join(ROOT, "shared/menu-config.js")
    if not os.path.isfile(mc):
        fail("shared/menu-config.js 缺失，无法校验菜单")
        return
    with open(mc, encoding="utf-8") as fh:
        content = fh.read()
    m = re.search(r"PROTOTYPE_MENU\s*=\s*\[(.*?)\]", content, re.S)
    if not m:
        fail("menu-config.js 未定义 window.PROTOTYPE_MENU 数组")
        return
    items = re.findall(r"key\s*:\s*'([^']+)'", m.group(1))
    if items:
        ok(f"菜单含 {len(items)} 项：{', '.join(items)}")
    else:
        fail("菜单配置为空，至少要有一项")


def check_index():
    print("== 5. 入口页同步 ==")
    idx = os.path.join(ROOT, "index.html")
    if not os.path.isfile(idx):
        fail("index.html 缺失")
        return
    with open(idx, encoding="utf-8") as fh:
        content = fh.read()
    if 'shared/menu-config.js' in content:
        ok("index.html 引用 menu-config.js（菜单可渲染）")
    else:
        fail("index.html 未引用 shared/menu-config.js")


def main():
    print("校验目录：" + ROOT)
    check_structure()
    check_assets()
    check_pages()
    check_menu()
    check_index()
    print()
    if FAILS:
        print(f"结果：未通过（{len(FAILS)} 项失败）")
        for f in FAILS:
            print("  - " + f)
        sys.exit(1)
    else:
        print("结果：全部通过 ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
