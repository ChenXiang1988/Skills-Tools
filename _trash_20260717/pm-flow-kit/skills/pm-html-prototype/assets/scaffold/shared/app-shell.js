// 共享外壳：Web 后台空骨架的菜单 / 角色 / 页签渲染引擎。
// index.html 底部引用本文件后自动渲染，无需额外调用。
(function () {
  'use strict';

  // 图标库（与后台骨架配色一致）
  var icons = {
    home: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
    package: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
    truck: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><path d="M16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    users: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="7" r="4"/><path d="M1 21v-2a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v2"/></svg>',
    settings: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21h-4v-.2a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1-2.8-2.8.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3v-4h.2a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1 2.8-2.8.1.1a1.7 1.7 0 0 0 1.8.3 1.7 1.7 0 0 0 1-1.5V3h4v.2a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1 2.8 2.8-.1.1a1.7 1.7 0 0 0-.3 1.8 1.7 1.7 0 0 0 1.5 1h.2v4h-.2a1.7 1.7 0 0 0-1.4 1z"/></svg>',
    compass: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8l-2 6-6 2 2-6 6-2z"/></svg>',
    store: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9h18v12H3zM5 3h14l2 6H3l2-6z"/></svg>',
    dollar: '<svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
  };

  function renderAdmin() {
    var roles = window.PROTOTYPE_ROLES || {};
    var roleKeys = Object.keys(roles);
    if (!roleKeys.length) { console.warn('[app-shell] 未找到 PROTOTYPE_ROLES'); return; }

    var state = { role: roleKeys[0], menuIndex: 0, tabIndex: 0, collapsed: false };
    var sidebar = document.getElementById('sidebar');
    var sidebarMenu = document.getElementById('sidebarMenu');
    var tabsRow = document.getElementById('tabsRow');
    var pageTitle = document.getElementById('pageTitle');
    var switcherTrigger = document.getElementById('shopSwitcherTrigger');
    var switcherMenu = document.getElementById('shopSwitcherMenu');
    var switcherLabel = document.getElementById('shopSwitcherLabel');

    function currentMenus() { return roles[state.role] || []; }

    function renderSwitcher() {
      switcherLabel.textContent = state.role;
      switcherMenu.innerHTML = roleKeys.map(function (r) {
        return '<button class="shop-switcher-item ' + (r === state.role ? 'active' : '') +
          '" data-role="' + r + '"><span>' + r + '</span><span>' + (r === state.role ? '✓' : '') + '</span></button>';
      }).join('');
      Array.prototype.forEach.call(switcherMenu.querySelectorAll('[data-role]'), function (btn) {
        btn.onclick = function () {
          state.role = btn.dataset.role; state.menuIndex = 0; state.tabIndex = 0;
          switcherMenu.classList.remove('open'); switcherTrigger.classList.remove('active');
          renderAll();
        };
      });
    }

    function renderSidebar() {
      sidebarMenu.innerHTML = currentMenus().map(function (m, i) {
        return '<button class="sidebar-item ' + (i === state.menuIndex ? 'active' : '') +
          '" data-index="' + i + '">' + (icons[m.icon] || icons.home) + '<span class="label">' + m.top + '</span></button>';
      }).join('');
      Array.prototype.forEach.call(sidebarMenu.querySelectorAll('[data-index]'), function (btn) {
        btn.onclick = function () {
          state.menuIndex = Number(btn.dataset.index); state.tabIndex = 0; renderAll();
        };
      });
    }

    function renderTabs() {
      var item = currentMenus()[state.menuIndex];
      var tabs = (item && item.tabs) || [];
      tabsRow.innerHTML = tabs.map(function (t, i) {
        return '<button class="tab ' + (i === state.tabIndex ? 'active' : '') + '" data-tab="' + i + '">' + t + '</button>';
      }).join('');
      Array.prototype.forEach.call(tabsRow.querySelectorAll('[data-tab]'), function (btn) {
        btn.onclick = function () { state.tabIndex = Number(btn.dataset.tab); renderAll(); };
      });
      pageTitle.textContent = (tabs[state.tabIndex]) || (item && item.top) || '';
    }

    function renderAll() { renderSwitcher(); renderSidebar(); renderTabs(); }

    switcherTrigger.onclick = function (e) {
      e.stopPropagation();
      switcherMenu.classList.toggle('open');
      switcherTrigger.classList.toggle('active');
    };
    document.addEventListener('click', function (e) {
      if (!document.getElementById('shopSwitcher').contains(e.target)) {
        switcherMenu.classList.remove('open'); switcherTrigger.classList.remove('active');
      }
    });
    document.getElementById('collapseBtn').onclick = function () {
      state.collapsed = !state.collapsed;
      sidebar.classList.toggle('collapsed', state.collapsed);
    };

    renderAll();
  }

  window.renderAdmin = renderAdmin;
  if (document.readyState !== 'loading') renderAdmin();
  else document.addEventListener('DOMContentLoaded', renderAdmin);
})();
