/*
 * pm-html-presentation :: code-hl.js — 零依赖轻量代码高亮（替代 highlight.js）
 * 用法：
 *   <pre><code class="language-javascript">...</code></pre>
 *   PmHL.highlightAll()         —— 自动高亮页面所有 <pre code> / code.language-*
 *   PmHL.highlight(el, lang)   —— 高亮单个元素
 * 支持：js / ts / python / json / bash（基础词法）
 * 配色由引入方的内联 <style> 提供 .tok-* 类（默认 tokyo-night 调色板，见 code.html）
 */
(function () {
  "use strict";
  function esc(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
    });
  }
  var KW = {
    js: "const let var function return if else for while do switch case break continue new class extends super this typeof instanceof of in try catch finally throw async await yield import export from default null undefined true false void delete void debugger with".split(" "),
    ts: "const let var function return if else for while do switch case break continue new class extends super this typeof instanceof of in try catch finally throw async await yield import export from default null undefined true false interface type enum public private protected readonly namespace as keyof infer".split(" "),
    python: "def class return if elif else for while break continue import from as try except finally raise with lambda yield pass None True False and or not in is global nonlocal del assert async await print".split(" "),
    json: [],
    bash: "if then else fi for in do done while until case esac function echo cd export local return source unset set export declare".split(" ")
  };
  function setOf(arr) {
    var o = {};
    for (var i = 0; i < arr.length; i++) if (arr[i]) o[arr[i]] = 1;
    return o;
  }
  var KWS = {};
  Object.keys(KW).forEach(function (k) {
    KWS[k] = setOf(KW[k]);
  });

  // 扫描：1 注释 / 2 字符串 / 3 数字 / 4 函数名(后跟'(') / 5 词 / 6 空白 / 7 标点
  var RE = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|#[^\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)(?=\s*\()|([A-Za-z_$][\w$]*)|(\s+)|([^\s\w])/g;

  function tokenize(src, lang) {
    var kw = KWS[lang] || KWS.js;
    var out = [];
    var m;
    RE.lastIndex = 0;
    while ((m = RE.exec(src))) {
      if (m[1] != null) out.push(["com", m[1]]);
      else if (m[2] != null) out.push(["str", m[2]]);
      else if (m[3] != null) out.push(["num", m[3]]);
      else if (m[4] != null) out.push(["fn", m[4]]);
      else if (m[5] != null) out.push([kw[m[5]] ? "kw" : "w", m[5]]);
      else if (m[6] != null) out.push(["ws", m[6]]);
      else if (m[7] != null) out.push(["p", m[7]]);
      if (m.index === RE.lastIndex) RE.lastIndex++;
    }
    return out;
  }
  function render(toks) {
    var h = "";
    for (var i = 0; i < toks.length; i++) {
      var t = toks[i];
      if (t[0] === "ws") h += esc(t[1]);
      else if (t[0] === "w") h += esc(t[1]);
      else h += '<span class="tok-' + t[0] + '">' + esc(t[1]) + "</span>";
    }
    return h;
  }
  function highlight(el, lang) {
    if (!el) return;
    var code = el.textContent;
    if (!lang) {
      var m = (el.className || "").match(/language-(\w+)/);
      lang = m ? m[1] : "js";
    }
    try {
      el.innerHTML = render(tokenize(code, lang));
    } catch (e) {
      el.innerHTML = esc(code);
    }
  }
  function highlightAll(root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll("pre code, code.language-js, code.language-javascript, code.language-ts, code.language-typescript, code.language-python, code.language-py, code.language-json, code.language-bash, code.language-sh");
    for (var i = 0; i < nodes.length; i++) highlight(nodes[i]);
  }
  window.PmHL = { highlight: highlight, highlightAll: highlightAll, tokenize: tokenize };
})();
