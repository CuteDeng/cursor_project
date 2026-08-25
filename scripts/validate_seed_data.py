#!/usr/bin/env python3
"""Validate generated seed SQL files (row counts + customer_id linkage)."""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "sql" / "seed"


def load_into_sqlite(cur: sqlite3.Cursor) -> None:
    cur.executescript(
        """
        CREATE TABLE jx_p_customer (
          customer_id INTEGER PRIMARY KEY,
          client_id TEXT, open_id TEXT, nick_name TEXT, head_img TEXT, name TEXT, old_name TEXT,
          mobile_phone TEXT, nps_phone TEXT NOT NULL DEFAULT '', parent_phone TEXT, contract_phone TEXT,
          card_type INTEGER, card TEXT, passport TEXT, birthday INTEGER, belong_branch_id INTEGER,
          campuses_id INTEGER, edu_email TEXT, edu_branch_id INTEGER, first_tutor_email TEXT,
          second_tutor_email TEXT, selection_email TEXT, document_email TEXT,
          document_director_email TEXT NOT NULL DEFAULT '', application_email TEXT NOT NULL DEFAULT '',
          adviser_email TEXT, second_adviser_email TEXT, course_email TEXT, teaching_email TEXT,
          email TEXT, graduate_school TEXT, graduate_major TEXT, is_sign INTEGER, status INTEGER,
          is_login INTEGER, last_login_ip TEXT, last_login_time INTEGER, biz_time INTEGER,
          oper_id INTEGER, sex INTEGER, school_name TEXT, course_set_id INTEGER, home_address TEXT,
          summer_school_id INTEGER, lang_score TEXT, ielts_id INTEGER, gpa_id INTEGER, jlpt TEXT,
          toefl TEXT, sat TEXT, eju TEXT NOT NULL DEFAULT '', add_type INTEGER, other_lang TEXT,
          server_porg INTEGER, many_country TEXT, edu_area TEXT, is_change_school INTEGER,
          style_end_time INTEGER, is_better INTEGER, master_class TEXT, is_better_coach INTEGER,
          is_better_task INTEGER, is_better_review INTEGER, is_document INTEGER, is_edition INTEGER,
          remarks TEXT, created_at INTEGER, updated_at INTEGER, inter_course_subjects_and_grades TEXT,
          gpa TEXT, phonetic_name TEXT NOT NULL DEFAULT '', english_name TEXT NOT NULL DEFAULT '',
          student_number TEXT, customer_service_phone TEXT NOT NULL DEFAULT '',
          service_contact_date TEXT NOT NULL DEFAULT '1970-01-01 00:00:00'
        );
        CREATE TABLE jx_p_agreement (
          id INTEGER PRIMARY KEY,
          contract_name TEXT, is_master INTEGER NOT NULL DEFAULT 0, contract_number TEXT, qiantu_id TEXT,
          customer_name TEXT, card TEXT, card_type INTEGER, phone TEXT, address TEXT, email TEXT,
          school_year INTEGER, country_name TEXT, major_name TEXT, subject_name TEXT, degree TEXT,
          file_time INTEGER, file_money INTEGER, service_charge INTEGER, money REAL, campuses_id INTEGER,
          edu_email TEXT, document_email TEXT, adviser_email TEXT, adviser_branch_id INTEGER NOT NULL DEFAULT 0,
          start_adviser_email TEXT, teaching_email TEXT, create_time INTEGER, status INTEGER,
          pay_branch_name TEXT, status_name TEXT, class_hour TEXT, product_cate_id INTEGER,
          service_status INTEGER, budget TEXT, ag_give_hour REAL, ag_choose_hour REAL, ag_project REAL,
          ag_type REAL, be_class_hour REAL, be_give_hour REAL, be_choose_hour REAL, be_project REAL,
          be_project_modify REAL, be_type REAL, be_type_modify REAL, biz_time INTEGER, type INTEGER,
          course_start_time INTEGER, course_end_time INTEGER, out_branch_id INTEGER,
          must_class_end_time INTEGER, type_end_time INTEGER, created_at INTEGER, updated_at INTEGER,
          class_add_hours INTEGER, class_core_hours INTEGER, value_add_hours INTEGER, cf_gift INTEGER,
          cf_lesson_times TEXT, cf_content TEXT, has_add_contract INTEGER, add_contract_status INTEGER,
          pay_branch_id INTEGER NOT NULL DEFAULT 0, fid TEXT, total_end_time INTEGER, typeset_time INTEGER,
          is_recommend TEXT, is_assessed TEXT, is_listened TEXT, is_assisted TEXT, goal_school TEXT,
          special_comment TEXT, full_pay INTEGER NOT NULL DEFAULT 0, payed_class_hour INTEGER NOT NULL DEFAULT 0,
          discount_content TEXT, erp_have_class REAL NOT NULL DEFAULT 0, erp_give_class REAL NOT NULL DEFAULT 0,
          erp_chose_class REAL NOT NULL DEFAULT 0, erp_project_count REAL NOT NULL DEFAULT 0,
          erp_type_count REAL NOT NULL DEFAULT 0, must_course_sum TEXT, give_course_sum TEXT,
          is_count INTEGER, related_product INTEGER, school_edit_num INTEGER,
          customer_id INTEGER NOT NULL DEFAULT 0, previous_master_id INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    for name in ("jx_p_customer_seed_1000.sql", "jx_p_agreement_seed_1000.sql"):
        sql = (SEED_DIR / name).read_text(encoding="utf-8")
        sql = (
            sql.replace("SET NAMES utf8mb4;", "")
            .replace("SET FOREIGN_KEY_CHECKS = 0;", "")
            .replace("SET FOREIGN_KEY_CHECKS = 1;", "")
            .replace("`", "")
        )
        cur.executescript(sql)


def main() -> int:
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    load_into_sqlite(cur)
    customer_count = cur.execute("SELECT COUNT(*) FROM jx_p_customer").fetchone()[0]
    agreement_count = cur.execute("SELECT COUNT(*) FROM jx_p_agreement").fetchone()[0]
    orphans = cur.execute(
        """
        SELECT COUNT(*) FROM jx_p_agreement a
        LEFT JOIN jx_p_customer c ON a.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ).fetchone()[0]
    print(f"jx_p_customer rows: {customer_count}")
    print(f"jx_p_agreement rows: {agreement_count}")
    print(f"orphan agreements: {orphans}")
    ok = customer_count == 1000 and agreement_count == 1000 and orphans == 0
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
