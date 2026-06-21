#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const sharp = require("sharp");

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const NS = "http://www.w3.org/2000/svg";

function usage() {
  console.error(
    "Usage: node render_mermaid.mjs <input.mmd> <output.png>"
  );
}

function setGlobal(name, value) {
  try {
    Object.defineProperty(globalThis, name, {
      value,
      configurable: true,
      writable: true,
      enumerable: true,
    });
  } catch {
    globalThis[name] = value;
  }
}

function estimateText(text, fontSize = 16) {
  const lines = String(text || "").split(/\r?\n/);
  let width = 0;
  for (const line of lines) {
    const chars = [...line];
    const wideChars = (line.match(/[\u4e00-\u9fff]/g) || []).length;
    const asciiChars = Math.max(0, chars.length - wideChars);
    width = Math.max(
      width,
      Math.ceil(
        asciiChars * fontSize * 0.72 + wideChars * fontSize * 1.18 + fontSize * 0.8
      )
    );
  }
  const height = Math.max(fontSize * 1.3, lines.length * fontSize * 1.35);
  return { width: Math.max(8, width), height };
}

function parseFontSize(node, window) {
  const attr = node.getAttribute?.("font-size");
  const style = node.style?.fontSize;
  const computed = window.getComputedStyle?.(node)?.fontSize;
  const raw = attr || style || computed || "16px";
  const parsed = parseFloat(raw);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 16;
}

function boxFromAttrs(node) {
  const x =
    parseFloat(
      node.getAttribute?.("x") ||
        node.getAttribute?.("cx") ||
        node.getAttribute?.("x1") ||
        "0"
    ) || 0;
  const y =
    parseFloat(
      node.getAttribute?.("y") ||
        node.getAttribute?.("cy") ||
        node.getAttribute?.("y1") ||
        "0"
    ) || 0;
  const width = parseFloat(node.getAttribute?.("width") || "0") || 0;
  const height = parseFloat(node.getAttribute?.("height") || "0") || 0;
  return { x, y, width, height };
}

function unionBoxes(boxes) {
  const valid = boxes.filter(
    (b) => b && Number.isFinite(b.width) && Number.isFinite(b.height)
  );
  if (!valid.length) {
    return { x: 0, y: 0, width: 0, height: 0 };
  }

  let x1 = Infinity;
  let y1 = Infinity;
  let x2 = -Infinity;
  let y2 = -Infinity;
  for (const b of valid) {
    x1 = Math.min(x1, b.x || 0);
    y1 = Math.min(y1, b.y || 0);
    x2 = Math.max(x2, (b.x || 0) + (b.width || 0));
    y2 = Math.max(y2, (b.y || 0) + (b.height || 0));
  }

  return {
    x: x1,
    y: y1,
    width: Math.max(0, x2 - x1),
    height: Math.max(0, y2 - y1),
  };
}

function patchSvgGeometry(window) {
  function bbox(node) {
    const tag = (node.tagName || "").toLowerCase();
    if (tag === "text" || tag === "tspan") {
      const fs = parseFontSize(node, window);
      const lines = String(node.textContent || "").split(/\r?\n/);
      const widths = lines.map((line) => estimateText(line, fs).width);
      const width = Math.max(0, ...widths);
      const height = Math.max(fs * 1.2, lines.length * fs * 1.2);
      const x = parseFloat(node.getAttribute?.("x") || "0") || 0;
      const y = parseFloat(node.getAttribute?.("y") || "0") || 0;
      return { x, y: y - height * 0.8, width, height };
    }

    if (tag === "rect") return boxFromAttrs(node);
    if (tag === "circle") {
      const cx = parseFloat(node.getAttribute?.("cx") || "0") || 0;
      const cy = parseFloat(node.getAttribute?.("cy") || "0") || 0;
      const r = parseFloat(node.getAttribute?.("r") || "0") || 0;
      return { x: cx - r, y: cy - r, width: r * 2, height: r * 2 };
    }
    if (tag === "ellipse") {
      const cx = parseFloat(node.getAttribute?.("cx") || "0") || 0;
      const cy = parseFloat(node.getAttribute?.("cy") || "0") || 0;
      const rx = parseFloat(node.getAttribute?.("rx") || "0") || 0;
      const ry = parseFloat(node.getAttribute?.("ry") || "0") || 0;
      return { x: cx - rx, y: cy - ry, width: rx * 2, height: ry * 2 };
    }
    if (tag === "line") {
      const x1 = parseFloat(node.getAttribute?.("x1") || "0") || 0;
      const y1 = parseFloat(node.getAttribute?.("y1") || "0") || 0;
      const x2 = parseFloat(node.getAttribute?.("x2") || "0") || 0;
      const y2 = parseFloat(node.getAttribute?.("y2") || "0") || 0;
      return {
        x: Math.min(x1, x2),
        y: Math.min(y1, y2),
        width: Math.abs(x2 - x1),
        height: Math.abs(y2 - y1),
      };
    }
    if (tag === "svg" || tag === "g" || tag === "foreignobject") {
      return unionBoxes(Array.from(node.children || []).map((child) => bbox(child)));
    }

    return unionBoxes(Array.from(node.children || []).map((child) => bbox(child)));
  }

  window.SVGElement.prototype.getBBox = function () {
    return bbox(this);
  };
  window.SVGElement.prototype.getBoundingClientRect = function () {
    return bbox(this);
  };
  window.SVGElement.prototype.getComputedTextLength = function () {
    return bbox(this).width;
  };
  window.HTMLElement.prototype.getBoundingClientRect = function () {
    const fs = parseFontSize(this, window);
    const text = this.textContent || "";
    const lines = text.split(/\r?\n/);
    let width = 0;
    for (const line of lines) {
      width = Math.max(width, estimateText(line, fs).width);
    }
    const height = Math.max(fs * 1.3, lines.length * fs * 1.35);
    return {
      x: 0,
      y: 0,
      width,
      height,
      top: 0,
      left: 0,
      right: width,
      bottom: height,
    };
  };
}

function patchBrowserGlobals(window) {
  class CSSStyleSheetPolyfill {
    constructor() {
      this.cssRules = [];
      this._text = "";
    }

    replaceSync(text) {
      this._text = String(text);
      this.cssRules = [{ cssText: this._text }];
    }

    insertRule(rule) {
      this.cssRules.push({ cssText: String(rule) });
      return this.cssRules.length - 1;
    }

    deleteRule(index) {
      this.cssRules.splice(index, 1);
    }
  }

  window.CSSStyleSheet = CSSStyleSheetPolyfill;
  setGlobal("CSSStyleSheet", CSSStyleSheetPolyfill);

  if (!("adoptedStyleSheets" in window.document)) {
    Object.defineProperty(window.document, "adoptedStyleSheets", {
      configurable: true,
      enumerable: true,
      get() {
        return this._adoptedStyleSheets || [];
      },
      set(value) {
        this._adoptedStyleSheets = Array.isArray(value) ? value : [];
      },
    });
  }

  if (window.ShadowRoot && !("adoptedStyleSheets" in window.ShadowRoot.prototype)) {
    Object.defineProperty(window.ShadowRoot.prototype, "adoptedStyleSheets", {
      configurable: true,
      enumerable: true,
      get() {
        return this._adoptedStyleSheets || [];
      },
      set(value) {
        this._adoptedStyleSheets = Array.isArray(value) ? value : [];
      },
    });
  }

  patchSvgGeometry(window);
}

function decodePoints(markerPath) {
  const data = markerPath.getAttribute("data-points");
  if (!data) return null;

  try {
    const json = Buffer.from(data, "base64").toString("utf8");
    const points = JSON.parse(json);
    if (!Array.isArray(points)) {
      return null;
    }

    return points
      .map((point) => {
        if (Array.isArray(point) && point.length >= 2) {
          const x = Number(point[0]);
          const y = Number(point[1]);
          if (Number.isFinite(x) && Number.isFinite(y)) {
            return { x, y };
          }
          return null;
        }

        if (point && typeof point === "object") {
          const x = Number(point.x);
          const y = Number(point.y);
          if (Number.isFinite(x) && Number.isFinite(y)) {
            return { x, y };
          }
        }

        return null;
      })
      .filter(Boolean);
  } catch {
    return null;
  }
}

function parseMarkerType(markerUrl) {
  const match = String(markerUrl || "").match(/#([^)]*)\)$/);
  if (!match) return null;

  const markerId = match[1];
  const size = markerId.includes("margin") ? 12 : 9;
  if (markerId.includes("point")) {
    return { kind: "point", direction: markerId.includes("Start") ? "start" : "end", size };
  }
  if (markerId.includes("circle")) {
    return { kind: "circle", direction: markerId.includes("Start") ? "start" : "end", size };
  }
  if (markerId.includes("cross")) {
    return { kind: "cross", direction: markerId.includes("Start") ? "start" : "end", size };
  }
  return { kind: "point", direction: markerId.includes("Start") ? "start" : "end", size };
}

function createArrowElement(document, kind, endPoint, prevPoint, strokeColor, size) {
  if (
    !endPoint ||
    !prevPoint ||
    !Number.isFinite(endPoint.x) ||
    !Number.isFinite(endPoint.y) ||
    !Number.isFinite(prevPoint.x) ||
    !Number.isFinite(prevPoint.y)
  ) {
    return null;
  }

  const dx = endPoint.x - prevPoint.x;
  const dy = endPoint.y - prevPoint.y;
  const angle = Math.atan2(dy, dx);
  const half = size / 2;

  if (kind === "circle") {
    const circle = document.createElementNS(NS, "circle");
    circle.setAttribute("cx", String(endPoint.x));
    circle.setAttribute("cy", String(endPoint.y));
    circle.setAttribute("r", String(Math.max(3, size * 0.45)));
    circle.setAttribute("fill", strokeColor);
    circle.setAttribute("stroke", strokeColor);
    return circle;
  }

  if (kind === "cross") {
    const group = document.createElementNS(NS, "g");
    const x1 = endPoint.x - Math.cos(angle + Math.PI / 4) * half;
    const y1 = endPoint.y - Math.sin(angle + Math.PI / 4) * half;
    const x2 = endPoint.x + Math.cos(angle + Math.PI / 4) * half;
    const y2 = endPoint.y + Math.sin(angle + Math.PI / 4) * half;
    const x3 = endPoint.x - Math.cos(angle - Math.PI / 4) * half;
    const y3 = endPoint.y - Math.sin(angle - Math.PI / 4) * half;
    const x4 = endPoint.x + Math.cos(angle - Math.PI / 4) * half;
    const y4 = endPoint.y + Math.sin(angle - Math.PI / 4) * half;

    for (const [xA, yA, xB, yB] of [
      [x1, y1, x2, y2],
      [x3, y3, x4, y4],
    ]) {
      const line = document.createElementNS(NS, "line");
      line.setAttribute("x1", String(xA));
      line.setAttribute("y1", String(yA));
      line.setAttribute("x2", String(xB));
      line.setAttribute("y2", String(yB));
      line.setAttribute("stroke", strokeColor);
      line.setAttribute("stroke-width", "2");
      line.setAttribute("stroke-linecap", "round");
      group.appendChild(line);
    }
    return group;
  }

  const baseX = endPoint.x - Math.cos(angle) * size;
  const baseY = endPoint.y - Math.sin(angle) * size;
  const leftX = baseX + Math.cos(angle + Math.PI / 2) * half;
  const leftY = baseY + Math.sin(angle + Math.PI / 2) * half;
  const rightX = baseX + Math.cos(angle - Math.PI / 2) * half;
  const rightY = baseY + Math.sin(angle - Math.PI / 2) * half;

  const polygon = document.createElementNS(NS, "polygon");
  polygon.setAttribute(
    "points",
    `${endPoint.x},${endPoint.y} ${leftX},${leftY} ${rightX},${rightY}`
  );
  polygon.setAttribute("fill", strokeColor);
  polygon.setAttribute("stroke", strokeColor);
  return polygon;
}

function simplifySvg(svgText) {
  const dom = new JSDOM(svgText, { contentType: "image/svg+xml" });
  const document = dom.window.document;
  const svg = document.documentElement;

  for (const style of [...svg.querySelectorAll("style")]) {
    style.textContent = style.textContent.replace(
      /filter:drop-shadow\([^)]*\);?/g,
      ""
    );
  }

  for (const filter of [...svg.querySelectorAll("filter")]) {
    filter.remove();
  }

  for (const marker of [...svg.querySelectorAll("marker")]) {
    marker.remove();
  }

  for (const path of [...svg.querySelectorAll("path[data-edge='true']")]) {
    const markerStart = parseMarkerType(path.getAttribute("marker-start"));
    const markerEnd = parseMarkerType(path.getAttribute("marker-end"));
    const points = decodePoints(path);
    if (points && points.length >= 2) {
      if (markerStart) {
        const start = points[0];
        const next = points[1];
        const element = createArrowElement(
          document,
          markerStart.kind,
          start,
          next,
          "#333333",
          markerStart.size
        );
        if (element) {
          path.parentNode.appendChild(element);
        }
      }
      if (markerEnd) {
        const end = points[points.length - 1];
        const prev = points[points.length - 2];
        const element = createArrowElement(
          document,
          markerEnd.kind,
          end,
          prev,
          "#333333",
          markerEnd.size
        );
        if (element) {
          path.parentNode.appendChild(element);
        }
      }
    }

    path.removeAttribute("marker-start");
    path.removeAttribute("marker-end");
  }

  return new XMLSerializer().serializeToString(svg);
}

function parseTranslate(transform) {
  let tx = 0;
  let ty = 0;
  const value = String(transform || "");

  for (const match of value.matchAll(
    /translate\(\s*([-+]?\d*\.?\d+(?:e[-+]?\d+)?)\s*(?:[ ,]\s*([-+]?\d*\.?\d+(?:e[-+]?\d+)?)\s*)?\)/gi
  )) {
    tx += Number(match[1]) || 0;
    ty += match[2] != null ? Number(match[2]) || 0 : 0;
  }

  return { tx, ty };
}

function mergeBounds(a, b) {
  if (!a) return b;
  if (!b) return a;
  const x1 = Math.min(a.x, b.x);
  const y1 = Math.min(a.y, b.y);
  const x2 = Math.max(a.x + a.width, b.x + b.width);
  const y2 = Math.max(a.y + a.height, b.y + b.height);
  return {
    x: x1,
    y: y1,
    width: Math.max(0, x2 - x1),
    height: Math.max(0, y2 - y1),
  };
}

function boundsFromNumbers(numbers) {
  if (numbers.length < 2) {
    return null;
  }

  let x1 = Infinity;
  let y1 = Infinity;
  let x2 = -Infinity;
  let y2 = -Infinity;

  for (let i = 0; i < numbers.length - 1; i += 2) {
    const x = Number(numbers[i]);
    const y = Number(numbers[i + 1]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      continue;
    }
    x1 = Math.min(x1, x);
    y1 = Math.min(y1, y);
    x2 = Math.max(x2, x);
    y2 = Math.max(y2, y);
  }

  if (!Number.isFinite(x1) || !Number.isFinite(y1)) {
    return null;
  }

  return {
    x: x1,
    y: y1,
    width: Math.max(0, x2 - x1),
    height: Math.max(0, y2 - y1),
  };
}

function parsePoints(pointsText) {
  const numbers = String(pointsText || "")
    .trim()
    .split(/[\s,]+/)
    .map((value) => Number(value))
    .filter((value) => Number.isFinite(value));

  return boundsFromNumbers(numbers);
}

function boundsFromPath(d) {
  const numbers = String(d || "")
    .match(/[-+]?\d*\.?\d+(?:e[-+]?\d+)?/gi)
    ?.map((value) => Number(value))
    .filter((value) => Number.isFinite(value)) || [];

  return boundsFromNumbers(numbers);
}

function textLines(node) {
  const directLines = [...(node.children || [])]
    .filter((child) => (child.tagName || "").toLowerCase() === "tspan")
    .map((child) => child.textContent || "")
    .filter((line) => line.length > 0);

  if (directLines.length > 0) {
    return directLines;
  }

  const text = String(node.textContent || "");
  const lines = text.split(/\r?\n/).filter((line) => line.length > 0);
  return lines.length > 0 ? lines : [text];
}

function boundsFromText(node, tx, ty) {
  const styleFontSize = parseFloat(node.getAttribute("font-size") || "0");
  const fontSize =
    Number.isFinite(styleFontSize) && styleFontSize > 0 ? styleFontSize : 16;
  const lines = textLines(node);
  const width = Math.max(...lines.map((line) => estimateText(line, fontSize).width));
  const height = Math.max(fontSize * 1.3, lines.length * fontSize * 1.35);
  const xAttr = parseFloat(node.getAttribute("x") || "0") || 0;
  const yAttr = parseFloat(node.getAttribute("y") || "0") || 0;
  const anchor = (node.getAttribute("text-anchor") || "").toLowerCase();

  let x = tx + xAttr;
  if (anchor === "middle" || anchor === "center") {
    x -= width / 2;
  } else if (anchor === "end") {
    x -= width;
  }

  const y = ty + yAttr - height * 0.8;
  return { x, y, width, height };
}

function boundsFromElement(node, tx = 0, ty = 0) {
  if (!node || !node.tagName) {
    return null;
  }

  const tag = node.tagName.toLowerCase();
  if (
    ["defs", "marker", "style", "title", "desc", "metadata", "clippath"].includes(
      tag
    )
  ) {
    return null;
  }

  const transform = parseTranslate(node.getAttribute?.("transform"));
  const nextTx = tx + transform.tx;
  const nextTy = ty + transform.ty;

  if (tag === "svg" || tag === "g") {
    let bounds = null;
    for (const child of [...(node.children || [])]) {
      bounds = mergeBounds(bounds, boundsFromElement(child, nextTx, nextTy));
    }
    return bounds;
  }

  if (tag === "rect") {
    const x = nextTx + (parseFloat(node.getAttribute("x") || "0") || 0);
    const y = nextTy + (parseFloat(node.getAttribute("y") || "0") || 0);
    const width = parseFloat(node.getAttribute("width") || "0") || 0;
    const height = parseFloat(node.getAttribute("height") || "0") || 0;
    return { x, y, width, height };
  }

  if (tag === "circle") {
    const cx = nextTx + (parseFloat(node.getAttribute("cx") || "0") || 0);
    const cy = nextTy + (parseFloat(node.getAttribute("cy") || "0") || 0);
    const r = parseFloat(node.getAttribute("r") || "0") || 0;
    return { x: cx - r, y: cy - r, width: r * 2, height: r * 2 };
  }

  if (tag === "ellipse") {
    const cx = nextTx + (parseFloat(node.getAttribute("cx") || "0") || 0);
    const cy = nextTy + (parseFloat(node.getAttribute("cy") || "0") || 0);
    const rx = parseFloat(node.getAttribute("rx") || "0") || 0;
    const ry = parseFloat(node.getAttribute("ry") || "0") || 0;
    return { x: cx - rx, y: cy - ry, width: rx * 2, height: ry * 2 };
  }

  if (tag === "line") {
    const x1 = nextTx + (parseFloat(node.getAttribute("x1") || "0") || 0);
    const y1 = nextTy + (parseFloat(node.getAttribute("y1") || "0") || 0);
    const x2 = nextTx + (parseFloat(node.getAttribute("x2") || "0") || 0);
    const y2 = nextTy + (parseFloat(node.getAttribute("y2") || "0") || 0);
    return {
      x: Math.min(x1, x2),
      y: Math.min(y1, y2),
      width: Math.abs(x2 - x1),
      height: Math.abs(y2 - y1),
    };
  }

  if (tag === "polygon" || tag === "polyline") {
    const bounds = parsePoints(node.getAttribute("points") || "");
    if (!bounds) {
      return null;
    }
    return {
      x: bounds.x + nextTx,
      y: bounds.y + nextTy,
      width: bounds.width,
      height: bounds.height,
    };
  }

  if (tag === "path") {
    const bounds = boundsFromPath(node.getAttribute("d") || "");
    if (!bounds) {
      return null;
    }
    return {
      x: bounds.x + nextTx,
      y: bounds.y + nextTy,
      width: bounds.width,
      height: bounds.height,
    };
  }

  if (tag === "text") {
    return boundsFromText(node, nextTx, nextTy);
  }

  if (tag === "foreignobject") {
    let bounds = null;
    for (const child of [...(node.children || [])]) {
      bounds = mergeBounds(bounds, boundsFromElement(child, nextTx, nextTy));
    }
    return bounds;
  }

  if (node.children && node.children.length > 0) {
    let bounds = null;
    for (const child of [...node.children]) {
      bounds = mergeBounds(bounds, boundsFromElement(child, nextTx, nextTy));
    }
    return bounds;
  }

  return null;
}

function normalizeSvgViewBox(svgText) {
  const dom = new JSDOM(svgText, { contentType: "image/svg+xml" });
  const document = dom.window.document;
  const svg = document.documentElement;
  const bounds = boundsFromElement(svg);
  if (!bounds || !Number.isFinite(bounds.x) || !Number.isFinite(bounds.y)) {
    return svgText;
  }

  const padding = 16;
  const x = Math.floor(bounds.x - padding);
  const y = Math.floor(bounds.y - padding);
  const width = Math.ceil(bounds.width + padding * 2);
  const height = Math.ceil(bounds.height + padding * 2);

  svg.setAttribute("viewBox", `${x} ${y} ${width} ${height}`);
  svg.setAttribute("width", String(width));
  svg.setAttribute("height", String(height));
  svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
  svg.removeAttribute("style");

  return new XMLSerializer().serializeToString(svg);
}

function stripFlowchartEdgeLabels(source) {
  const lines = source.split(/\r?\n/);
  return lines
    .map((line) => {
      const labeledEdges = [
        { pattern: /^(\s*.+?)\s*--\s*[^>]+?\s*-->\s*(.+)$/, arrow: "-->" },
        { pattern: /^(\s*.+?)\s*--\s*[^-]+?\s*---\s*(.+)$/, arrow: "---" },
        { pattern: /^(\s*.+?)\s*-\.\s*[^>]+?\s*\.\->\s*(.+)$/, arrow: "-.->" },
        { pattern: /^(\s*.+?)\s*==\s*[^=]+?\s*==>\s*(.+)$/, arrow: "==>" },
      ];

      for (const { pattern, arrow } of labeledEdges) {
        const match = line.match(pattern);
        if (match) {
          return `${match[1]} ${arrow} ${match[2]}`;
        }
      }

      if (/-->|---|\.->|==>/.test(line)) {
        return line.replace(/:\s*[^:]+$/, "");
      }

      return line;
    })
    .join("\n");
}

function shouldRetryFlowchartRender(source, error) {
  const message = String(error?.message || error || "");
  return (
    /Could not find a suitable point for the given distance/i.test(message) &&
    /^(?:\s*(?:flowchart|graph)\b)/im.test(source)
  );
}

async function renderMermaidToPng(inputPath, outputPath) {
  const source = await fs.readFile(inputPath, "utf8");
  const dom = new JSDOM("<!doctype html><html><body></body></html>", {
    pretendToBeVisual: true,
  });
  const { window } = dom;

  setGlobal("window", window);
  setGlobal("document", window.document);
  setGlobal("navigator", window.navigator);
  setGlobal("Element", window.Element);
  setGlobal("HTMLElement", window.HTMLElement);
  setGlobal("SVGElement", window.SVGElement);
  setGlobal("Node", window.Node);
  setGlobal("DOMParser", window.DOMParser);
  setGlobal("XMLSerializer", window.XMLSerializer);
  setGlobal("getComputedStyle", window.getComputedStyle.bind(window));
  setGlobal(
    "requestAnimationFrame",
    window.requestAnimationFrame?.bind(window) ||
      ((cb) => setTimeout(() => cb(Date.now()), 0))
  );
  setGlobal(
    "cancelAnimationFrame",
    window.cancelAnimationFrame?.bind(window) ||
      ((id) => clearTimeout(id))
  );
  if (!globalThis.btoa) {
    setGlobal("btoa", (value) =>
      Buffer.from(value, "binary").toString("base64")
    );
  }
  if (!globalThis.atob) {
    setGlobal("atob", (value) =>
      Buffer.from(value, "base64").toString("binary")
    );
  }
  if (!window.matchMedia) {
    window.matchMedia = () => ({
      matches: false,
      addListener() {},
      removeListener() {},
    });
  }

  patchBrowserGlobals(window);

  const mermaid = (await import("mermaid")).default;
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    htmlLabels: false,
    theme: "default",
    flowchart: {
      defaultRenderer: "elk",
      nodeSpacing: 80,
      rankSpacing: 120,
      padding: 24,
      curve: "basis",
    },
  });

  let svg;
  try {
    ({ svg } = await mermaid.render("diagram", source));
  } catch (error) {
    if (shouldRetryFlowchartRender(source, error)) {
      const fallbackSource = stripFlowchartEdgeLabels(source);
      ({ svg } = await mermaid.render("diagram_fallback", fallbackSource));
    } else {
      throw error;
    }
  }
  const normalizedSvg = normalizeSvgViewBox(svg);
  await sharp(Buffer.from(normalizedSvg, "utf8"))
    .flatten({ background: "#ffffff" })
    .png()
    .toFile(outputPath);
}

async function main() {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) {
    usage();
    process.exit(2);
  }

  const resolvedInput = path.resolve(SCRIPT_DIR, inputPath);
  const resolvedOutput = path.resolve(SCRIPT_DIR, outputPath);

  try {
    await renderMermaidToPng(resolvedInput, resolvedOutput);
  } catch (error) {
    console.error(String(error?.stack || error));
    process.exit(1);
  }
}

await main();
