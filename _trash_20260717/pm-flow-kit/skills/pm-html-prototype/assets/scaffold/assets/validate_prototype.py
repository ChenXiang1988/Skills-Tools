#!/usr/bin/env python3
"""Validate an offline HTML prototype scaffold."""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAILS = []


def ok(message):
    print("  OK " + message)


def fail(message):
    FAILS.append(message)
    print("  FAIL " + message)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


def check_structure():
    print("== 1. Structure ==")
    for path in ("assets", "shared"):
        if exists(path):
            ok(f"{path}/ exists")
        else:
            fail(f"{path}/ is missing")
    if exists("index.html"):
        ok("index.html exists")
    else:
        fail("index.html is missing")


def check_assets():
    print("== 2. Shared assets ==")
    required = [
        "assets/design-system/tokens.css",
        "assets/prototype-chrome.css",
        "assets/fonts/DingTalk-JinBuTi.woff2",
        "shared/app-shell.js",
        "shared/menu-config.js",
    ]
    for rel in required:
        if exists(rel):
            ok(f"{rel} exists")
        else:
            fail(f"{rel} is missing")
    if exists("assets/prototype-chrome.css"):
        txt = read("assets/prototype-chrome.css")
        if "DingTalk JinBuTi" in txt:
            ok("prototype-chrome.css references DingTalk JinBuTi")
        else:
            fail("prototype-chrome.css does not reference DingTalk JinBuTi")
    if exists("assets/design-system/tokens.css"):
        dsc = read("assets/design-system/tokens.css")
        if "--color-primary" in dsc:
            ok("design-system/tokens.css defines --color-primary (Ant Design tokens)")
        else:
            fail("design-system/tokens.css missing --color-primary")


def business_pages():
    return [
        name for name in os.listdir(ROOT)
        if name.endswith(".html") and name != "index.html"
    ]


def check_pages():
    print("== 3. Page references ==")
    pages = business_pages()
    if not pages:
        ok("No business pages; skipped")
        return
    for name in pages:
        html = read(name)
        is_review = "review-stage" in html or 'id="conn-svg"' in html
        is_mobile = "device-frame.css" in html
        if is_review:
            for needle, label in (
                ("assets/connect-lines.js", "connect-lines.js"),
                ("assets/prototype-doc.css", "prototype-doc.css"),
            ):
                if needle in html:
                    ok(f"{name}: references {label}")
                else:
                    fail(f"{name}: missing {label}")
        if is_mobile and not is_review:
            for needle in ("assets/device-frame.css", "assets/prototype-chrome.css"):
                if needle in html:
                    ok(f"{name}: references {needle}")
                else:
                    fail(f"{name}: missing {needle}")
            n_frames = len(re.findall(r'class="[^"]*device-(?:iphone|android|pda)', html))
            if n_frames == 1:
                ok(f"{name}: exactly one device frame")
            elif n_frames == 0:
                fail(f"{name}: missing device frame")
            else:
                fail(f"{name}: has {n_frames} device frames; use exactly one per HTML page")
        if not is_mobile and not is_review:
            for needle in ("assets/prototype-chrome.css", "shared/app-shell.js", "shared/menu-config.js"):
                if needle in html:
                    ok(f"{name}: references {needle}")
                else:
                    fail(f"{name}: missing {needle}")


def check_menu():
    print("== 4. Menu config ==")
    if not exists("shared/menu-config.js"):
        fail("shared/menu-config.js is missing")
        return
    text = read("shared/menu-config.js")
    if "window.PROTOTYPE_MENU" not in text:
        fail("window.PROTOTYPE_MENU is not defined")
    else:
        ok("window.PROTOTYPE_MENU is defined")


def check_index():
    print("== 5. Entry page ==")
    if not exists("index.html"):
        fail("index.html is missing")
        return
    html = read("index.html")
    if "shared/menu-config.js" in html:
        ok("index.html references menu-config.js")
    else:
        fail("index.html does not reference shared/menu-config.js")


def main():
    print("Prototype directory: " + ROOT)
    check_structure()
    check_assets()
    check_pages()
    check_menu()
    check_index()
    if FAILS:
        print(f"Result: failed ({len(FAILS)} issue(s))")
        sys.exit(1)
    print("Result: passed")


if __name__ == "__main__":
    main()
