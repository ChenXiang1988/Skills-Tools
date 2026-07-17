# Component-Library Adapter

Use this reference only when the project knowledge base or the user specifies Ant Design, antd, ProComponents, Ant Design X, or a similar component library.

## Purpose

The HTML prototype is not production React code. It should visually and structurally approximate the target component library so reviewers can understand layout, density, interaction, and data requirements.

## Mapping Examples

| Product need | Prototype pattern | Ant Design concept |
|---|---|---|
| Data table | HTML table with toolbar, filters, pagination | Table |
| Search filters | Form row with inputs and selects | Form, Input, Select |
| Primary action | Button with primary styling | Button type primary |
| Confirmation | Modal-like panel or inline confirmation | Modal, Popconfirm |
| Status display | Tag or badge-like label | Tag, Badge |
| Step flow | Ordered step indicator | Steps |

## Rules

- Do not claim production API correctness from the HTML prototype alone.
- Record component mapping assumptions.
- Respect project tokens, spacing, typography, and interaction rules when present.
