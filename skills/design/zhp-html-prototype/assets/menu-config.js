// 菜单配置：新增原型页面时，必须在此追加一项，并保持与 index.html 同步。
// 字段：key(唯一, 对应页面 renderShell 的 activeKey)、label(显示名)、href(相对路径)
window.PROTOTYPE_MENU = [
  { key: 'dashboard', label: '工作台', href: 'index.html' },
  { key: 'collect-terminal', label: '采集终端管理', href: 'collect-terminal.html' }
];
