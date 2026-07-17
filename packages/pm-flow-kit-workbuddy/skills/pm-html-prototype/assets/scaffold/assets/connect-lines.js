/*
 * connect-lines.js — 原型评审件「界面 ↔ 文档」连线引擎
 * 设计目标（优化点 vs 写死连线）：
 *   1. 数据驱动：UI 元素与文档段落只需共享 data-link="KEY" 即可配对，无需手动算坐标。
 *   2. 方向自适应：PC 横向（UI 在左、文档在右）→ 水平贝塞尔；移动端纵向（UI 在上、文档在下）→ 垂直贝塞尔。
 *   3. 悬停双向高亮：悬停任意一端，曲线 + 另一端同时高亮（class: .is-linked）。
 *   4. resize / 视图切换自动重算坐标（ResizeObserver + 防抖）。
 *   5. 零依赖、纯原生 JS，可复制到任意原型评审页复用。
 *
 * 用法：
 *   <div class="review-stage" id="stage">
 *     <svg id="conn-svg"></svg>           <!-- 必须放在 stage 内、绝对定位覆盖 -->
 *     <div class="pane-ui">  <input data-link="po-no"> ... </div>
 *     <div class="pane-doc"> <p data-link="po-no">规则...</p> ... </div>
 *   </div>
 *   <script src="assets/connect-lines.js"></script>
 *   <script>initConnectLines({ stage:'stage', svg:'conn-svg' });</script>
 */
(function (global) {
  'use strict';

  function initConnectLines(opts) {
    opts = opts || {};
    var stage = document.getElementById(opts.stage || 'stage');
    var svg = document.getElementById(opts.svg || 'conn-svg');
    if (!stage || !svg) {
      console.warn('[connect-lines] stage 或 svg 未找到，跳过初始化');
      return;
    }

    var SVGNS = 'http://www.w3.org/2000/svg';
    var pairs = [];          // [{ key, ui, doc, path }]
    var rafId = null;

    // 元素是否真正可见（被 display:none 的视图切换组应跳过）
    function isVisible(el) {
      var r = el.getBoundingClientRect();
      if (r.width < 1 && r.height < 1) return false;
      var s = global.getComputedStyle(el);
      return s.display !== 'none' && s.visibility !== 'hidden';
    }

    // 收集配对：UI 端必须来自 .pane-ui，文档端必须来自 .pane-doc
    // —— 这样 PC/手机双套 UI 同 key 也不会错乱，且只连「可见」那组。
    function collect() {
      pairs.forEach(function (p) { if (p.path && p.path.parentNode) p.path.parentNode.removeChild(p.path); });
      pairs = [];
      var uiMap = {}, docMap = {};
      stage.querySelectorAll('.pane-ui [data-link]').forEach(function (n) {
        var k = n.getAttribute('data-link');
        (uiMap[k] = uiMap[k] || []).push(n);
      });
      stage.querySelectorAll('.pane-doc [data-link]').forEach(function (n) {
        var k = n.getAttribute('data-link');
        (docMap[k] = docMap[k] || []).push(n);
      });
      Object.keys(docMap).forEach(function (k) {
        if (!uiMap[k]) return;
        var ui = uiMap[k].filter(isVisible)[0];
        var doc = docMap[k].filter(isVisible)[0];
        if (!ui || !doc) return;
        var path = document.createElementNS(SVGNS, 'path');
        path.setAttribute('class', 'conn-path');
        path.setAttribute('data-key', k);
        svg.appendChild(path);
        pairs.push({ key: k, ui: ui, doc: doc, path: path });
      });
    }

    // 取元素相对 stage 的锚点
    function anchor(el, side) {
      var r = el.getBoundingClientRect();
      var s = stage.getBoundingClientRect();
      var x = r.left - s.left;
      var y = r.top - s.top;
      var w = r.width, h = r.height;
      if (side === 'right') return { x: x + w, y: y + h / 2 };
      if (side === 'left') return { x: x, y: y + h / 2 };
      if (side === 'bottom') return { x: x + w / 2, y: y + h };
      return { x: x + w / 2, y: y }; // top
    }

    // 绘制单条曲线（自适应方向）
    function draw(p) {
      var horiz = p.doc.getBoundingClientRect().left >= p.ui.getBoundingClientRect().right - 1;
      var a, b, d;
      if (horiz) {
        a = anchor(p.ui, 'right');
        b = anchor(p.doc, 'left');
        var dx = Math.max(40, (b.x - a.x) * 0.5);
        d = 'M ' + a.x + ' ' + a.y + ' C ' + (a.x + dx) + ' ' + a.y + ', ' + (b.x - dx) + ' ' + b.y + ', ' + b.x + ' ' + b.y;
      } else {
        a = anchor(p.ui, 'bottom');
        b = anchor(p.doc, 'top');
        var dy = Math.max(40, (b.y - a.y) * 0.5);
        d = 'M ' + a.x + ' ' + a.y + ' C ' + a.x + ' ' + (a.y + dy) + ', ' + b.x + ' ' + (b.y - dy) + ', ' + b.x + ' ' + b.y;
      }
      p.path.setAttribute('d', d);
    }

    function drawAll() { pairs.forEach(draw); }

    // 高亮联动
    function setLinked(key, on) {
      pairs.forEach(function (p) {
        if (p.key !== key) return;
        p.ui.classList.toggle('is-linked', on);
        p.doc.classList.toggle('is-linked', on);
        p.path.classList.toggle('is-active', on);
      });
    }

    function bindHover() {
      pairs.forEach(function (p) {
        [p.ui, p.doc].forEach(function (el) {
          el.addEventListener('mouseenter', function () { setLinked(p.key, true); });
          el.addEventListener('mouseleave', function () { setLinked(p.key, false); });
          // 点击锁定（评审时便于对照）
          el.addEventListener('click', function (e) {
            e.stopPropagation();
            var locked = el.classList.contains('is-locked');
            clearLocked();
            if (!locked) {
              setLinked(p.key, true);
              p.ui.classList.add('is-locked');
              p.doc.classList.add('is-locked');
            }
          });
        });
      });
      document.addEventListener('click', clearLocked);
    }

    function clearLocked() {
      pairs.forEach(function (p) {
        p.ui.classList.remove('is-locked');
        p.doc.classList.remove('is-locked');
        setLinked(p.key, false);
      });
    }

    // 防抖重算
    function scheduleDraw() {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(drawAll);
    }

    function start() {
      collect();
      drawAll();
      bindHover();
      if (typeof ResizeObserver !== 'undefined') {
        var ro = new ResizeObserver(scheduleDraw);
        ro.observe(stage);
        // 观察子面板尺寸变化（视图切换/折叠）
        stage.querySelectorAll('.pane-ui, .pane-doc').forEach(function (el) { ro.observe(el); });
      } else {
        global.addEventListener('resize', scheduleDraw);
      }
      // 字体/图片加载后可能位移，延迟补一次
      setTimeout(drawAll, 300);
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', start);
    } else {
      start();
    }

    // 暴露给外部（如视图切换后手动重算）
    global.__connectLines = { redraw: drawAll, rebuild: function () { collect(); drawAll(); bindHover(); } };
  }

  global.initConnectLines = initConnectLines;
})(window);
