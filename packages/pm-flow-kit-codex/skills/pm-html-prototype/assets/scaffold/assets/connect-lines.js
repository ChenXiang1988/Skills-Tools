/*
 * connect-lines.js — Ptextreviewtext「text ↔ text」text
 * text（text vs text）：
 *   1. text：UI text data-link="KEY" text，Nonetext。
 *   2. text：PC text（UI text、text）→ text；mobiletext（UI text、text）→ text。
 *   3. textHightext：text，text + textHightext（class: .is-linked）。
 *   4. resize / text（ResizeObserver + text）。
 *   5. text、textPtext JS，textPtextreviewtext。
 *
 * text：
 *   <div class="review-stage" id="stage">
 *     <svg id="conn-svg"></svg>           <!-- text stage text、text -->
 *     <div class="pane-ui">  <input data-link="po-no"> ... </div>
 *     <div class="pane-doc"> <p data-link="po-no">rule...</p> ... </div>
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
      console.warn('[connect-lines] stage text svg text，text');
      return;
    }

    var SVGNS = 'http://www.w3.org/2000/svg';
    var pairs = [];          // [{ key, ui, doc, path }]
    var rafId = null;

    // textYesNotext（text display:none text）
    function isVisible(el) {
      var r = el.getBoundingClientRect();
      if (r.width < 1 && r.height < 1) return false;
      var s = global.getComputedStyle(el);
      return s.display !== 'none' && s.visibility !== 'hidden';
    }

    // text：UI text .pane-ui，text .pane-doc
    // —— text PC/text UI text key text，text「text」text。
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

    // text stage text
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

    // text（text）
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

    // Hightext
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
          // text（reviewtext）
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

    // text
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
        // text（text/text）
        stage.querySelectorAll('.pane-ui, .pane-doc').forEach(function (el) { ro.observe(el); });
      } else {
        global.addEventListener('resize', scheduleDraw);
      }
      // text/text，text
      setTimeout(drawAll, 300);
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', start);
    } else {
      start();
    }

    // text（text）
    global.__connectLines = { redraw: drawAll, rebuild: function () { collect(); drawAll(); bindHover(); } };
  }

  global.initConnectLines = initConnectLines;
})(window);
