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
        "assets/prototype.css",
        "assets/fonts/DingTalk-JinBuTi.woff2",
        "shared/app-shell.js",
        "shared/menu-config.js",
    ]
    for rel in required:
        if exists(rel):
            ok(f"{rel} exists")
        else:
            fail(f"{rel} is missing")
    if exists("assets/design-system/tokens.css"):
        tokens = read("assets/design-system/tokens.css")
        if "--color-primary" in tokens:
            ok("design-system/tokens.css defines --color-primary")
        else:
            fail("design-system/tokens.css missing --color-primary")
        if "--font-family" in tokens or "DingTalk JinBuTi" in tokens:
            ok("design-system/tokens.css defines font guidance")
        else:
            fail("design-system/tokens.css missing font guidance")
    if exists("assets/design-tokens.json"):
        try:
            data = json.loads(read("assets/design-tokens.json"))
            family = json.dumps(data)
            if "DingTalk" in family:
                ok("design-tokens.json references DingTalk JinBuTi")
            else:
                fail("design-tokens.json does not reference DingTalk JinBuTi")
        except Exception as exc:
            fail(f"design-tokens.json cannot be parsed: {exc}")


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
                ("assets/design-system/tokens.css", "design-system/tokens.css"),
                ("assets/connect-lines.js", "connect-lines.js"),
                ("assets/prototype-doc.css", "prototype-doc.css"),
            ):
                if needle in html:
                    ok(f"{name}: references {label}")
                else:
                    fail(f"{name}: missing {label}")
        if is_mobile and not is_review:
            for needle in ("assets/design-system/tokens.css", "assets/device-frame.css", "assets/prototype-mobile.css", "assets/prototype.css"):
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
            for needle in ("assets/design-system/tokens.css", "assets/prototype.css", "shared/app-shell.js", "shared/menu-config.js"):
                if needle in html:
                    ok(f"{name}: references {needle}")
                else:
                    fail(f"{name}: missing {needle}")


def check_local_references():
    print("== 4. Local references ==")
    pages = [name for name in os.listdir(ROOT) if name.endswith(".html")]
    for name in pages:
        html = read(name)
        refs = re.findall(r'(?:href|src)="([^"]+)"', html)
        for ref in refs:
            if ref.startswith(("http://", "https://", "mailto:", "#")):
                fail(f"{name}: external or non-local reference {ref}")
                continue
            if "://" in ref:
                fail(f"{name}: unsupported reference {ref}")
                continue
            path = ref.split("#", 1)[0].split("?", 1)[0]
            if path and exists(path):
                ok(f"{name}: local reference exists {path}")
            elif path:
                fail(f"{name}: local reference missing {path}")


def check_menu():
    print("== 5. Menu config ==")
    if not exists("shared/menu-config.js"):
        fail("shared/menu-config.js is missing")
        return
    text = read("shared/menu-config.js")
    if "window.PROTOTYPE_MENU" not in text:
        fail("window.PROTOTYPE_MENU is not defined")
    else:
        ok("window.PROTOTYPE_MENU is defined")


def check_index():
    print("== 6. Entry page ==")
    if not exists("index.html"):
        fail("index.html is missing")
        return
    html = read("index.html")
    if "assets/design-system/tokens.css" in html:
        ok("index.html references design-system/tokens.css")
    else:
        fail("index.html does not reference assets/design-system/tokens.css")
    if "shared/menu-config.js" in html:
        ok("index.html references menu-config.js")
    else:
        fail("index.html does not reference shared/menu-config.js")


def main():
    print("Prototype directory: " + ROOT)
    check_structure()
    check_assets()
    check_pages()
    check_local_references()
    check_menu()
    check_index()
    if FAILS:
        print(f"Result: failed ({len(FAILS)} issue(s))")
        sys.exit(1)
    print("Result: passed")


if __name__ == "__main__":
    main()
