# cursor_project

## 种子数据

已为 `jx_p_customer`（客户表）与 `jx_p_agreement`（合同表）各生成 1000 条可导入 SQL。

| 文件 | 说明 |
|------|------|
| `sql/schema/jx_p_customer.sql` | 客户表 DDL |
| `sql/schema/jx_p_agreement.sql` | 合同表 DDL |
| `sql/seed/jx_p_customer_seed_1000.sql` | 客户种子数据 1000 条 |
| `sql/seed/jx_p_agreement_seed_1000.sql` | 合同种子数据 1000 条 |
| `scripts/generate_seed_data.py` | 造数脚本（可复现，`--seed` 固定） |
| `scripts/validate_seed_data.py` | SQLite 校验脚本 |

```bash
python3 scripts/generate_seed_data.py
python3 scripts/validate_seed_data.py
```
