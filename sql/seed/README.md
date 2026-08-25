# 种子数据说明

- 生成时间种子: `20260825`
- `jx_p_customer`: 1000 条 → `jx_p_customer_seed_1000.sql`
- `jx_p_agreement`: 1000 条 → `jx_p_agreement_seed_1000.sql`
- 合同表 `customer_id` 与客户表 `customer_id` 一一对应（第 i 条合同关联第 i 个客户，循环复用）
- 重新生成: `python3 scripts/generate_seed_data.py`

## 导入示例

```bash
mysql -uUSER -p DBNAME < sql/schema/jx_p_customer.sql
mysql -uUSER -p DBNAME < sql/schema/jx_p_agreement.sql
mysql -uUSER -p DBNAME < sql/seed/jx_p_customer_seed_1000.sql
mysql -uUSER -p DBNAME < sql/seed/jx_p_agreement_seed_1000.sql
```
