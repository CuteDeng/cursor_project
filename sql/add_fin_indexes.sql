-- 当前环境不支持独立 CREATE INDEX，需使用 ALTER TABLE 建索引
USE sfk_fa_db;

ALTER TABLE fin_document_progress
  ADD INDEX idx_fdp_del_update (del_status, update_time DESC);

ALTER TABLE fin_contract_tax_rate
  ADD INDEX idx_ctr_contract_status_del (contract_name, status, del_status);

ALTER TABLE fin_inventor_base_info
  ADD INDEX idx_ibi_contract_month_del (contract_number, attribution_month, del_status);
