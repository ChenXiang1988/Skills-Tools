/*
 * pm-html-presentation :: charts.js — 零依赖 SVG 图表渲染器（替代 Chart.js）
 * 用法（与 Chart.js 调用几乎一致，可直接替换）：
 *   PmChart.render(el, { type, data, options })
 *   - el: <canvas> 或 <div>（渲染时会被替换为 SVG 容器）
 *   - type: 'bar' | 'line' | 'radar' | 'doughnut' | 'pie'
 *   - data: { labels:[], datasets:[{label, data:[], backgroundColor, borderColor, fill, tension, borderWidth, pointRadius, borderRadius, barThickness}] }
 *   - options: { plugins:{legend:{position,labels:{color}}}, scales:{x:{ticks:{color},grid:{color}}, y:{...}}, cutout, suggestedMin/Max }
 * 完全离线、无外部库；配色跟随传入的 CSS 变量取值（accent 等）。
 */
(function () {
  "use strict";
  // 安全嵌套取值，避免 undefined.x 报错
  function dig(o) {
    for (var i = 1; i < arguments.length; i++) {
      if (o == null) return undefined;
      o = o[arguments[i]];
    }
    return o;
  }
  function esc(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
    });
  }
  function cssVar(name, fb) {
    try {
      var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      if (v) return v;
    } catch (e) {}
    return fb || name;
  }
  function niceMax(v) {
    if (v <= 0) return 1;
    var pow = Math.pow(10, Math.floor(Math.log10(v)));
    var n = v / pow;
    var step = n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10;
    return step * pow;
  }
  // Catmull-Rom 平滑 → SVG 路径；tension 0 = 直线。pts 坐标为 number
  function smoothPath(pts, tension) {
    if (pts.length < 2) return pts.length ? "M" + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1) : "";
    var d = "M" + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
    var t = tension || 0;
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i - 1] || pts[i];
      var p1 = pts[i];
      var p2 = pts[i + 1];
      var p3 = pts[i + 2] || p2;
      var c1x = p1[0] + ((p2[0] - p0[0]) / 6) * (1 + t);
      var c1y = p1[1] + ((p2[1] - p0[1]) / 6) * (1 + t);
      var c2x = p2[0] - ((p3[0] - p1[0]) / 6) * (1 + t);
      var c2y = p2[1] - ((p3[1] - p1[1]) / 6) * (1 + t);
      d += " C" + c1x.toFixed(1) + " " + c1y.toFixed(1) + " " + c2x.toFixed(1) + " " + c2y.toFixed(1) + " " + p2[0].toFixed(1) + " " + p2[1].toFixed(1);
    }
    return d;
  }
  function sizeOf(el) {
    var w = el.clientWidth || (el.parentElement && el.parentElement.clientWidth) || 600;
    var h = el.clientHeight || (el.parentElement && el.parentElement.clientHeight) || 360;
    return [w, h];
  }

  function renderBar(W, H, cfg, txt, grid) {
    var L = cfg.data.labels,
      ds = cfg.data.datasets;
    var padL = 46, padR = 14, padT = 16, padB = 34;
    var pw = W - padL - padR,
      ph = H - padT - padB;
    var maxV = 0;
    ds.forEach(function (d) {
      d.data.forEach(function (v) {
        if (v > maxV) maxV = v;
      });
    });
    var top = niceMax(maxV);
    var svg = "";
    var steps = 5;
    for (var s = 0; s <= steps; s++) {
      var val = (top / steps) * s;
      var y = padT + ph * (1 - val / top);
      svg += '<line x1="' + padL + '" y1="' + y.toFixed(1) + '" x2="' + (padL + pw) + '" y2="' + y.toFixed(1) + '" stroke="' + grid + '" stroke-width="1"/>';
      svg += '<text x="' + (padL - 8) + '" y="' + (y + 4).toFixed(1) + '" text-anchor="end" font-size="11" fill="' + txt + '">' + (val % 1 === 0 ? val : val.toFixed(1)) + "</text>";
    }
    var band = pw / L.length;
    var groupW = band * 0.66;
    ds.forEach(function (d, di) {
      for (var i = 0; i < L.length; i++) {
        var v = d.data[i] || 0;
        var bw = d.barThickness || groupW / ds.length;
        var gx = padL + i * band + (band - groupW) / 2 + di * (groupW / ds.length);
        var x = gx + (groupW / ds.length - bw) / 2;
        var y = padT + ph * (1 - v / top);
        var h = padT + ph - y;
        var r = Math.min(d.borderRadius || 6, bw / 2, h / 2);
        svg += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + Math.max(0, h).toFixed(1) + '" rx="' + r + '" ry="' + r + '" fill="' + (d.backgroundColor || cssVar("--accent")) + '"/>';
      }
    });
    for (var i2 = 0; i2 < L.length; i2++) {
      var cx = padL + i2 * band + band / 2;
      svg += '<text x="' + cx.toFixed(1) + '" y="' + (padT + ph + 18) + '" text-anchor="middle" font-size="11" fill="' + txt + '">' + esc(L[i2]) + "</text>";
    }
    svg += legend(W, cfg, txt);
    return svg;
  }

  function renderLine(W, H, cfg, txt, grid) {
    var L = cfg.data.labels,
      ds = cfg.data.datasets;
    var padL = 46, padR = 14, padT = 16, padB = 34;
    var pw = W - padL - padR,
      ph = H - padT - padB;
    var maxV = 0;
    ds.forEach(function (d) {
      d.data.forEach(function (v) {
        if (v > maxV) maxV = v;
      });
    });
    var top = niceMax(maxV);
    var svg = "";
    var steps = 5;
    for (var s = 0; s <= steps; s++) {
      var val = (top / steps) * s;
      var y = padT + ph * (1 - val / top);
      svg += '<line x1="' + padL + '" y1="' + y.toFixed(1) + '" x2="' + (padL + pw) + '" y2="' + y.toFixed(1) + '" stroke="' + grid + '" stroke-width="1"/>';
      svg += '<text x="' + (padL - 8) + '" y="' + (y + 4).toFixed(1) + '" text-anchor="end" font-size="11" fill="' + txt + '">' + (val % 1 === 0 ? val : val.toFixed(1)) + "</text>";
    }
    ds.forEach(function (d) {
      // 坐标保持 number，最后拼 SVG 时 toFixed
      var pts = d.data.map(function (v, i) {
        return [padL + (pw * i) / (L.length - 1), padT + ph * (1 - v / top)];
      });
      if (d.fill) {
        var area = smoothPath(pts, d.tension) + " L" + pts[pts.length - 1][0].toFixed(1) + " " + (padT + ph).toFixed(1) + " L" + pts[0][0].toFixed(1) + " " + (padT + ph).toFixed(1) + " Z";
        svg += '<path d="' + area + '" fill="' + (d.backgroundColor || (d.borderColor + "22")) + '" opacity="0.18"/>';
      }
      svg += '<path d="' + smoothPath(pts, d.tension) + '" fill="none" stroke="' + (d.borderColor || cssVar("--accent")) + '" stroke-width="' + (d.borderWidth || 3) + '" stroke-linejoin="round" stroke-linecap="round"/>';
      pts.forEach(function (p) {
        svg += '<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="' + (d.pointRadius || 4) + '" fill="' + (d.borderColor || cssVar("--accent")) + '"/>';
      });
    });
    for (var i2 = 0; i2 < L.length; i2++) {
      var cx = padL + (pw * i2) / (L.length - 1);
      svg += '<text x="' + cx.toFixed(1) + '" y="' + (padT + ph + 18) + '" text-anchor="middle" font-size="11" fill="' + txt + '">' + esc(L[i2]) + "</text>";
    }
    svg += legend(W, cfg, txt);
    return svg;
  }

  function renderRadar(W, H, cfg, txt, grid) {
    var L = cfg.data.labels,
      ds = cfg.data.datasets;
    var cx = W / 2,
      cy = H / 2 + 6;
    var R = Math.min(W, H) / 2 - Math.max(54, L.length > 6 ? 70 : 54);
    var n = L.length;
    var sugMin = dig(cfg, "options", "scales", "r", "suggestedMin") || 0;
    var sugMax = dig(cfg, "options", "scales", "r", "suggestedMax") || 10;
    var svg = "";
    function ang(i) {
      return -Math.PI / 2 + (i * 2 * Math.PI) / n;
    }
    var levels = 5;
    for (var l = 1; l <= levels; l++) {
      var rr = (R * l) / levels;
      var poly = "";
      for (var i = 0; i < n; i++) {
        poly += (cx + rr * Math.cos(ang(i))).toFixed(1) + " " + (cy + rr * Math.sin(ang(i))).toFixed(1) + " ";
      }
      svg += '<polygon points="' + poly.trim() + '" fill="none" stroke="' + grid + '" stroke-width="1"/>';
    }
    for (var i2 = 0; i2 < n; i2++) {
      var a = ang(i2);
      svg += '<line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + R * Math.cos(a)).toFixed(1) + '" y2="' + (cy + R * Math.sin(a)).toFixed(1) + '" stroke="' + grid + '" stroke-width="1"/>';
      var lx = cx + (R + 20) * Math.cos(a);
      var ly = cy + (R + 20) * Math.sin(a);
      var anchor = Math.abs(Math.cos(a)) < 0.3 ? "middle" : Math.cos(a) > 0 ? "start" : "end";
      svg += '<text x="' + lx.toFixed(1) + '" y="' + (ly + 4).toFixed(1) + '" text-anchor="' + anchor + '" font-size="13" fill="' + txt + '">' + esc(L[i2]) + "</text>";
    }
    ds.forEach(function (d) {
      var poly2 = "";
      for (var i3 = 0; i3 < n; i3++) {
        var v = (d.data[i3] - sugMin) / (sugMax - sugMin);
        if (v < 0) v = 0;
        if (v > 1) v = 1;
        poly2 += (cx + R * v * Math.cos(ang(i3))).toFixed(1) + " " + (cy + R * v * Math.sin(ang(i3))).toFixed(1) + " ";
      }
      svg += '<polygon points="' + poly2.trim() + '" fill="' + (d.backgroundColor || (d.borderColor + "33")) + '" stroke="' + (d.borderColor || cssVar("--accent")) + '" stroke-width="' + (d.borderWidth || 3) + '" stroke-linejoin="round"/>';
      for (var i4 = 0; i4 < n; i4++) {
        var v2 = (d.data[i4] - sugMin) / (sugMax - sugMin);
        if (v2 < 0) v2 = 0;
        if (v2 > 1) v2 = 1;
        svg += '<circle cx="' + (cx + R * v2 * Math.cos(ang(i4))).toFixed(1) + '" cy="' + (cy + R * v2 * Math.sin(ang(i4))).toFixed(1) + '" r="' + (d.pointRadius || 5) + '" fill="' + (d.borderColor || cssVar("--accent")) + '"/>';
      }
    });
    svg += legend(W, cfg, txt);
    return svg;
  }

  function renderDoughnut(W, H, cfg, txt, grid, isPie) {
    var L = cfg.data.labels,
      ds = cfg.data.datasets[0];
    var data = ds.data;
    var sum = data.reduce(function (a, b) {
      return a + b;
    }, 0);
    var colors = ds.backgroundColor || [cssVar("--accent"), cssVar("--accent-2"), cssVar("--accent-3"), cssVar("--good"), cssVar("--warn")];
    var cut = parseFloat(dig(cfg, "options", "cutout") || "60") || 60;
    var cx = isPie ? W / 2 : W / 2 - (W > 420 ? 90 : 0);
    var cy = H / 2;
    var R = Math.min(W, H) / 2 - 30;
    if (!isPie) R = R * (1 + cut / 100) / 2;
    var svg = "";
    var start = -Math.PI / 2;
    for (var i = 0; i < data.length; i++) {
      var frac = data[i] / sum;
      var end = start + frac * 2 * Math.PI;
      var large = frac > 0.5 ? 1 : 0;
      var x1 = cx + R * Math.cos(start),
        y1 = cy + R * Math.sin(start);
      var x2 = cx + R * Math.cos(end),
        y2 = cy + R * Math.sin(end);
      if (isPie) {
        svg += '<path d="M' + cx.toFixed(1) + " " + cy.toFixed(1) + " L" + x1.toFixed(1) + " " + y1.toFixed(1) + " A" + R.toFixed(1) + " " + R.toFixed(1) + " 0 " + large + " 1 " + x2.toFixed(1) + " " + y2.toFixed(1) + ' Z" fill="' + (colors[i % colors.length]) + '"/>';
      } else {
        var ir = R * (cut / 100);
        var ix1 = cx + ir * Math.cos(start),
          iy1 = cy + ir * Math.sin(start);
        var ix2 = cx + ir * Math.cos(end),
          iy2 = cy + ir * Math.sin(end);
        svg += '<path d="M' + x1.toFixed(1) + " " + y1.toFixed(1) + " A" + R.toFixed(1) + " " + R.toFixed(1) + " 0 " + large + " 1 " + x2.toFixed(1) + " " + y2.toFixed(1) + " L" + ix2.toFixed(1) + " " + iy2.toFixed(1) + " A" + ir.toFixed(1) + " " + ir.toFixed(1) + " 0 " + large + " 0 " + ix1.toFixed(1) + " " + iy1.toFixed(1) + ' Z" fill="' + (colors[i % colors.length]) + '"/>';
      }
      start = end;
    }
    var lx = isPie ? 0 : cx + R + 24;
    if (!isPie) {
      var ly0 = cy - (data.length * 22) / 2 + 6;
      for (var j = 0; j < L.length; j++) {
        var ly = ly0 + j * 22;
        svg += '<rect x="' + lx + '" y="' + (ly - 9) + '" width="12" height="12" rx="3" fill="' + (colors[j % colors.length]) + '"/>';
        svg += '<text x="' + (lx + 18) + '" y="' + ly + '" font-size="12" fill="' + txt + '">' + esc(L[j]) + "</text>";
      }
    } else {
      var ly02 = cy - (data.length * 22) / 2 + 6;
      for (var k = 0; k < L.length; k++) {
        var lyk = ly02 + k * 22;
        svg += '<rect x="14" y="' + (lyk - 9) + '" width="12" height="12" rx="3" fill="' + (colors[k % colors.length]) + '"/>';
        svg += '<text x="32" y="' + lyk + '" font-size="12" fill="' + txt + '">' + esc(L[k]) + "</text>";
      }
    }
    return svg;
  }

  function legend(W, cfg, txt) {
    var p = dig(cfg, "options", "plugins", "legend");
    if (!p) return "";
    var pos = (p.position || "top") + "";
    var ds = cfg.data.datasets;
    if (!ds || !ds.length) return "";
    var items = ds.map(function (d) {
      return { label: d.label || "", color: d.borderColor || d.backgroundColor || cssVar("--accent") };
    });
    var gap = 18,
      x0 = 12,
      y0 = 6;
    if (pos === "right" || pos === "top") {
      x0 = W - 168;
      y0 = 14;
      gap = 20;
    }
    var svg = "";
    items.forEach(function (it, i) {
      var yy = y0 + i * gap;
      svg += '<rect x="' + x0 + '" y="' + (yy - 9) + '" width="11" height="11" rx="3" fill="' + it.color + '"/>';
      svg += '<text x="' + (x0 + 17) + '" y="' + yy + '" font-size="12" fill="' + txt + '">' + esc(it.label) + "</text>";
    });
    return svg;
  }

  function render(el, cfg) {
    if (!el) return;
    var host = el;
    if (el.tagName === "CANVAS") {
      host = document.createElement("div");
      el.parentNode.replaceChild(host, el);
    }
    host.style.width = "100%";
    host.style.height = "100%";
    host.style.display = "block";
    var dim = sizeOf(host);
    var W = dim[0],
      H = dim[1];
    var opt = cfg.options || {};
    var txt = dig(opt, "plugins", "legend", "labels", "color") || cssVar("--text-2", "#888");
    var grid = (dig(opt, "scales", "x", "grid", "color") ||
        dig(opt, "scales", "y", "grid", "color") ||
        cssVar("--border", "rgba(127,127,127,.18)")) + "";
    var inner = "";
    var t = cfg.type;
    if (t === "bar") inner = renderBar(W, H, cfg, txt, grid);
    else if (t === "line") inner = renderLine(W, H, cfg, txt, grid);
    else if (t === "radar") inner = renderRadar(W, H, cfg, txt, grid);
    else if (t === "doughnut") inner = renderDoughnut(W, H, cfg, txt, grid, false);
    else if (t === "pie") inner = renderDoughnut(W, H, cfg, txt, grid, true);
    host.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">' + inner + "</svg>";
  }

  window.PmChart = { render: render };
})();
