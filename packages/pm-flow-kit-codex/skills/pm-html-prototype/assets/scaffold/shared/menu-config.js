// Menu configuration for the web admin prototype shell.
window.PROTOTYPE_ROLES = {
  "Operations Admin": [
    { top: "Home", icon: "home", tabs: ["Overview"] },
    { top: "Product Management", icon: "package", tabs: ["Product List", "Publish Product", "SKU Management"] },
    { top: "Order Center", icon: "truck", tabs: ["Sales Orders", "After-sales Orders"] },
    { top: "Account Management", icon: "users", tabs: ["My Profile", "Sub-accounts"] },
    { top: "Settings", icon: "settings", tabs: ["Basic Settings"] }
  ],
  "Warehouse Admin": [
    { top: "Home", icon: "home", tabs: ["Overview"] },
    { top: "Inbound", icon: "package", tabs: ["Purchase Inbound", "Receiving Confirmation"] },
    { top: "Outbound", icon: "truck", tabs: ["Sales Outbound", "Transfer Outbound"] },
    { top: "Inventory Search", icon: "compass", tabs: ["Total Inventory", "Warehouse Inventory"] },
    { top: "Settings", icon: "settings", tabs: ["Basic Settings"] }
  ]
};

window.PROTOTYPE_MENU = [
  { key: "dashboard", label: "Workbench", href: "index.html" },
  { key: "prototype-doc", label: "Prototype Review", href: "prototype-doc.html" },
  { key: "pda", label: "Mobile / PDA", href: "pda.html" }
];
