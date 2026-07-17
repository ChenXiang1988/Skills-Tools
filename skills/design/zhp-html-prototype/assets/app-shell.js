// 共享外壳：渲染侧边菜单、激活态、弹窗显隐。
// 每个业务页面底部调用 renderShell({ activeKey }) 即可。
(function () {
  // 兼容 file:// 与 http:// 两种打开方式
  function currentDir() {
    var p = window.location.pathname;
    var i = p.lastIndexOf('/');
    return p.slice(0, i + 1); // 含结尾 '/'
  }

  function renderShell(opts) {
    opts = opts || {};
    var menu = window.PROTOTYPE_MENU || [];
    var base = currentDir();
    var ul = document.getElementById('menu');
    if (!ul) return;
    ul.innerHTML = '';
    menu.forEach(function (item) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.textContent = item.label;
      a.href = base + item.href;
      if (item.key === opts.activeKey) a.className = 'active';
      li.appendChild(a);
      ul.appendChild(li);
    });
  }

  // 弹窗控制（新增/编辑共用 #modal）
  window.openModal = function (mode) {
    var m = document.getElementById('modal');
    var t = document.getElementById('modal-title');
    if (t) t.textContent = (mode === 'edit') ? '编辑' : '新增';
    if (m) m.classList.add('open');
  };
  window.closeModal = function () {
    var m = document.getElementById('modal');
    if (m) m.classList.remove('open');
  };
  // 点击遮罩关闭
  document.addEventListener('click', function (e) {
    var m = document.getElementById('modal');
    if (m && e.target === m) m.classList.remove('open');
  });

  window.renderShell = renderShell;
})();
