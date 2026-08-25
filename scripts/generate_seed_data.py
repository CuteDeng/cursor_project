#!/usr/bin/env python3
"""Generate 1000 seed rows each for jx_p_customer and jx_p_agreement."""

from __future__ import annotations

import argparse
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

SEED = 20260825
COUNT = 1000

SURNAMES = list("赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻")
GIVEN = [
    "伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
    "勇", "艳", "杰", "涛", "明", "超", "秀英", "霞", "平", "刚",
    "桂英", "建华", "文", "华", "红", "建国", "志强", "秀兰", "桂兰", "玉兰",
]
PINYIN_MAP = {
    "赵": "Zhao", "钱": "Qian", "孙": "Sun", "李": "Li", "周": "Zhou",
    "吴": "Wu", "郑": "Zheng", "王": "Wang", "冯": "Feng", "陈": "Chen",
    "褚": "Chu", "卫": "Wei", "蒋": "Jiang", "沈": "Shen", "韩": "Han",
    "杨": "Yang", "朱": "Zhu", "秦": "Qin", "尤": "You", "许": "Xu",
    "何": "He", "吕": "Lv", "施": "Shi", "张": "Zhang", "孔": "Kong",
    "曹": "Cao", "严": "Yan", "华": "Hua", "金": "Jin", "魏": "Wei",
    "陶": "Tao", "姜": "Jiang", "戚": "Qi", "谢": "Xie", "邹": "Zou",
    "喻": "Yu",
}
GIVEN_PINYIN = {
    "伟": "Wei", "芳": "Fang", "娜": "Na", "敏": "Min", "静": "Jing",
    "丽": "Li", "强": "Qiang", "磊": "Lei", "军": "Jun", "洋": "Yang",
    "勇": "Yong", "艳": "Yan", "杰": "Jie", "涛": "Tao", "明": "Ming",
    "超": "Chao", "秀英": "Xiuying", "霞": "Xia", "平": "Ping", "刚": "Gang",
    "桂英": "Guiying", "建华": "Jianhua", "文": "Wen", "华": "Hua",
    "红": "Hong", "建国": "Jianguo", "志强": "Zhiqiang", "秀兰": "Xiulan",
    "桂兰": "Guilan", "玉兰": "Yulan",
}
ENGLISH_NAMES = [
    "Alice", "Bob", "Cindy", "David", "Emma", "Frank", "Grace", "Henry",
    "Iris", "Jack", "Kate", "Leo", "Mia", "Noah", "Olivia", "Peter",
    "Quinn", "Ryan", "Sophia", "Tom", "Uma", "Victor", "Wendy", "Xavier",
]
SCHOOLS = [
    "北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
    "南京大学", "武汉大学", "中山大学", "四川大学", "山东大学",
    "厦门大学", "同济大学", "哈尔滨工业大学", "北京师范大学", "中国人民大学",
    "华东师范大学", "南开大学", "天津大学", "西安交通大学", "东南大学",
]
MAJORS = [
    "计算机科学", "视觉传达", "产品设计", "建筑设计", "工业设计",
    "金融学", "工商管理", "英语", "日语", "传媒",
]
COUNTRIES = ["美国", "英国", "加拿大", "澳大利亚", "日本", "新加坡", "德国", "法国"]
DEGREES = ["本科", "硕士", "博士", "预科"]
SUBJECTS = ["艺术设计", "商科", "理工", "人文社科", "传媒"]
BRANCH_IDS = [1, 2, 3, 5, 8, 10, 12, 15, 20, 25]
STATUS_AGREEMENT = [
    (1, "正常"),
    (2, "履行中"),
    (3, "已结课"),
    (4, "已退费"),
    (5, "暂停"),
]
PRODUCT_CATE = [1, 2, 3, 4, 5, 10, 20]
GOAL_SCHOOLS = [
    "哈佛大学", "耶鲁大学", "斯坦福大学", "MIT", "牛津大学",
    "剑桥大学", "哥伦比亚大学", "芝加哥大学", "东京大学", "早稻田大学",
]


def sql_str(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def sql_num(value) -> str:
    if value is None:
        return "NULL"
    return str(value)


def sql_ts(dt: datetime) -> str:
    return f"'{dt.strftime('%Y-%m-%d %H:%M:%S')}'"


def rand_phone(rng: random.Random, prefix: str = "138") -> str:
    return prefix + "".join(rng.choice(string.digits) for _ in range(8))


def rand_id_card(rng: random.Random, birthday: datetime) -> str:
    area = rng.choice(["110101", "310101", "440103", "330106", "320102", "510104"])
    birth = birthday.strftime("%Y%m%d")
    seq = f"{rng.randint(0, 999):03d}"
    body = area + birth + seq
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = "10X98765432"
    total = sum(int(body[i]) * weights[i] for i in range(17))
    return body + check_map[total % 11]


def rand_passport(rng: random.Random) -> str:
    return "E" + "".join(rng.choice(string.digits) for _ in range(8))


def rand_email(rng: random.Random, local: str, domain: str = "example.com") -> str:
    return f"{local}{rng.randint(1, 9999)}@{domain}"


def teacher_email(rng: random.Random, role: str) -> str:
    return f"{role}{rng.randint(1, 200)}@jxedu.com"


def chinese_name(rng: random.Random) -> tuple[str, str, str]:
    surname = rng.choice(SURNAMES)
    given = rng.choice(GIVEN)
    name = surname + given
    phonetic = f"{PINYIN_MAP.get(surname, 'Zhang')} {GIVEN_PINYIN.get(given, 'Wei')}"
    english = rng.choice(ENGLISH_NAMES)
    return name, phonetic, english


def unix_ts(dt: datetime) -> int:
    return int(dt.timestamp())


def make_customers(rng: random.Random, count: int) -> list[dict]:
    base = datetime(2018, 1, 1)
    rows = []
    for i in range(1, count + 1):
        name, phonetic, english = chinese_name(rng)
        birthday_dt = datetime(rng.randint(1995, 2008), rng.randint(1, 12), rng.randint(1, 28))
        card_type = rng.choices([1, 2], weights=[85, 15])[0]
        card = rand_id_card(rng, birthday_dt) if card_type == 1 else None
        passport = rand_passport(rng) if card_type == 2 or rng.random() < 0.2 else None
        created = base + timedelta(days=rng.randint(0, 2500), hours=rng.randint(0, 23))
        updated = created + timedelta(days=rng.randint(0, 400))
        biz = created + timedelta(days=rng.randint(0, 60))
        last_login = updated - timedelta(days=rng.randint(0, 30)) if rng.random() < 0.7 else None
        mobile = rand_phone(rng, rng.choice(["138", "139", "186", "188", "150"]))
        parent = rand_phone(rng, rng.choice(["135", "136", "137", "159"]))
        contract_phone = mobile if rng.random() < 0.8 else rand_phone(rng, "133")
        branch_id = rng.choice(BRANCH_IDS)
        is_sign = rng.choices([10, 20], weights=[80, 20])[0]
        status = rng.choices([11, 88, 99], weights=[92, 5, 3])[0]
        server_porg = rng.choices([0, 1, 2, 3, 4], weights=[10, 50, 25, 10, 5])[0]
        rows.append(
            {
                "customer_id": i,
                "client_id": f"ERP{i:06d}",
                "open_id": f"ox{rng.randbytes(12).hex()}" if rng.random() < 0.6 else None,
                "nick_name": f"wx_{name}" if rng.random() < 0.5 else None,
                "head_img": f"https://cdn.example.com/avatar/{i}.jpg" if rng.random() < 0.5 else None,
                "name": name,
                "old_name": name if rng.random() < 0.1 else None,
                "mobile_phone": mobile,
                "nps_phone": mobile if rng.random() < 0.7 else "",
                "parent_phone": parent,
                "contract_phone": contract_phone,
                "card_type": card_type,
                "card": card,
                "passport": passport,
                "birthday": unix_ts(birthday_dt),
                "belong_branch_id": branch_id,
                "campuses_id": None,
                "edu_email": teacher_email(rng, "edu"),
                "edu_branch_id": branch_id,
                "first_tutor_email": teacher_email(rng, "tutor"),
                "second_tutor_email": teacher_email(rng, "tutor2") if rng.random() < 0.4 else "",
                "selection_email": teacher_email(rng, "select") if rng.random() < 0.7 else "",
                "document_email": teacher_email(rng, "doc"),
                "document_director_email": teacher_email(rng, "docdir"),
                "application_email": teacher_email(rng, "app"),
                "adviser_email": teacher_email(rng, "adv"),
                "second_adviser_email": teacher_email(rng, "adv2") if rng.random() < 0.3 else "",
                "course_email": teacher_email(rng, "course") if rng.random() < 0.5 else None,
                "teaching_email": teacher_email(rng, "teach") if rng.random() < 0.6 else None,
                "email": rand_email(rng, phonetic.split()[0].lower(), "student.jxedu.com"),
                "graduate_school": rng.choice(SCHOOLS),
                "graduate_major": rng.choice(MAJORS),
                "is_sign": is_sign,
                "status": status,
                "is_login": 1 if rng.random() < 0.65 else 0,
                "last_login_ip": f"1{rng.randint(0,9)}.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}"
                if last_login
                else None,
                "last_login_time": unix_ts(last_login) if last_login else None,
                "biz_time": unix_ts(biz),
                "oper_id": rng.randint(1, 50),
                "sex": rng.choice([1, 2]),
                "school_name": rng.choice(SCHOOLS),
                "course_set_id": rng.choice([0, 1, 2, 3, 5, 8]),
                "home_address": f"{rng.choice(['北京市', '上海市', '广州市', '深圳市', '杭州市', '成都市'])}"
                f"{rng.choice(['朝阳区', '海淀区', '浦东新区', '天河区', '南山区', '西湖区'])}"
                f"{rng.randint(1, 200)}号",
                "summer_school_id": rng.choice([0, 0, 0, 1, 2, 3]),
                "lang_score": rng.choice(["IELTS 6.5", "IELTS 7.0", "TOEFL 95", "TOEFL 105", ""]),
                "ielts_id": rng.choice([0, 0, 1, 2, 3]),
                "gpa_id": 0,
                "jlpt": rng.choice(["", "N1", "N2", "N3"]),
                "toefl": rng.choice(["", "90", "95", "100", "105", "110"]),
                "sat": rng.choice(["", "1200", "1350", "1450", "1500"]),
                "eju": rng.choice(["", "650", "700", "720", "750"]),
                "add_type": rng.choices([1, 2], weights=[70, 30])[0],
                "other_lang": rng.choice(["", "法语A2", "德语B1", "韩语TOPIK3"]),
                "server_porg": server_porg,
                "many_country": rng.choice(["", "115", "120", "125", "130"]),
                "edu_area": rng.choice(["华北", "华东", "华南", "西南", "华中"]),
                "is_change_school": rng.choices([1, 2], weights=[15, 85])[0],
                "style_end_time": unix_ts(updated + timedelta(days=rng.randint(30, 400)))
                if rng.random() < 0.5
                else None,
                "is_better": rng.choices([1, 2], weights=[20, 80])[0],
                "master_class": rng.choice(["", "大师课A", "大师课B", "海外教授工作坊"]),
                "is_better_coach": rng.choices([1, 2], weights=[15, 85])[0],
                "is_better_task": rng.choices([1, 2], weights=[15, 85])[0],
                "is_better_review": rng.choices([1, 2], weights=[10, 90])[0],
                "is_document": rng.choices([1, 2, 3, 4, 5], weights=[50, 30, 10, 5, 5])[0],
                "is_edition": rng.choices([1, 2], weights=[40, 60])[0],
                "remarks": rng.choice(["", "重点跟进", "家长要求更换顾问", "转校区中", "课时充足"]),
                "created_at": unix_ts(created),
                "updated_at": unix_ts(updated),
                "inter_course_subjects_and_grades": rng.choice(
                    ["", "A-Level: Math A, Physics B", "IB: 38/45", "AP: Calc 5, Physics 4"]
                ),
                "gpa": f"{rng.uniform(2.8, 4.0):.2f}",
                "phonetic_name": phonetic,
                "english_name": english,
                "student_number": f"S{created.year}{i:05d}",
                "customer_service_phone": rand_phone(rng, "400") if rng.random() < 0.3 else "",
                "service_contact_date": created + timedelta(days=rng.randint(0, 15)),
            }
        )
    return rows


def make_agreements(rng: random.Random, customers: list[dict], count: int) -> list[dict]:
    rows = []
    for i in range(1, count + 1):
        c = customers[(i - 1) % len(customers)]
        created_dt = datetime.fromtimestamp(c["created_at"]) + timedelta(days=rng.randint(0, 20))
        updated_dt = created_dt + timedelta(days=rng.randint(0, 300))
        biz_dt = created_dt + timedelta(days=rng.randint(0, 10))
        course_start = biz_dt + timedelta(days=rng.randint(7, 45))
        course_end = course_start + timedelta(days=rng.randint(180, 720))
        status, status_name = rng.choice(STATUS_AGREEMENT)
        money = round(rng.uniform(19800, 128000), 2)
        class_hour = rng.choice([40, 60, 80, 100, 120, 160, 200])
        give_hour = round(rng.uniform(0, 20), 2)
        choose_hour = round(rng.uniform(0, 30), 2)
        project = round(rng.uniform(1, 8), 2)
        ag_type = round(rng.uniform(0, 5), 2)
        be_class = round(min(class_hour, rng.uniform(0, class_hour)), 2)
        is_master = rng.choices([0, 1, 2, 3], weights=[10, 70, 10, 10])[0]
        rows.append(
            {
                "id": i,
                "contract_name": f"{c['name']}-{c['graduate_major'] or '综合'}-服务合同",
                "is_master": is_master,
                "contract_number": f"HT{created_dt.year}{i:06d}",
                "qiantu_id": f"QT{i:08d}" if rng.random() < 0.6 else None,
                "customer_name": c["name"],
                "card": c["card"],
                "card_type": c["card_type"] if c["card_type"] else 1,
                "phone": c["mobile_phone"],
                "address": c["home_address"],
                "email": c["email"],
                "school_year": rng.randint(2024, 2028),
                "country_name": rng.choice(COUNTRIES),
                "major_name": rng.choice(MAJORS),
                "subject_name": rng.choice(SUBJECTS),
                "degree": rng.choice(DEGREES),
                "file_time": unix_ts(biz_dt + timedelta(days=rng.randint(1, 30)))
                if rng.random() < 0.7
                else 0,
                "file_money": int(money * rng.uniform(0.6, 1.0)),
                "service_charge": rng.choice([3000, 5000, 8000, 10000, 15000]),
                "money": money,
                "campuses_id": c["belong_branch_id"] or 0,
                "edu_email": c["edu_email"][:50],
                "document_email": (c["document_email"] or "")[:50],
                "adviser_email": (c["adviser_email"] or "")[:50],
                "adviser_branch_id": c["belong_branch_id"] or 0,
                "start_adviser_email": teacher_email(rng, "sadv")[:50],
                "teaching_email": (c["teaching_email"] or teacher_email(rng, "teach"))[:50],
                "create_time": unix_ts(created_dt),
                "status": status,
                "pay_branch_name": rng.choice(["北京校区", "上海校区", "广州校区", "深圳校区", "杭州校区", ""]),
                "status_name": status_name,
                "class_hour": str(class_hour),
                "product_cate_id": rng.choice(PRODUCT_CATE),
                "service_status": rng.choices([0, 1, 2, 3], weights=[10, 50, 30, 10])[0],
                "budget": str(rng.choice([50000, 80000, 100000, 150000, 200000])),
                "ag_give_hour": give_hour,
                "ag_choose_hour": choose_hour,
                "ag_project": project,
                "ag_type": ag_type,
                "be_class_hour": be_class,
                "be_give_hour": round(min(give_hour, rng.uniform(0, give_hour + 0.01)), 2),
                "be_choose_hour": round(min(choose_hour, rng.uniform(0, choose_hour + 0.01)), 2),
                "be_project": round(min(project, rng.uniform(0, project)), 2),
                "be_project_modify": round(rng.uniform(-1, 1), 2),
                "be_type": round(min(ag_type, rng.uniform(0, ag_type + 0.01)), 2),
                "be_type_modify": round(rng.uniform(-1, 1), 2),
                "biz_time": unix_ts(biz_dt),
                "type": rng.choices([0, 1], weights=[75, 25])[0],
                "course_start_time": unix_ts(course_start),
                "course_end_time": unix_ts(course_end),
                "out_branch_id": 0 if rng.random() < 0.9 else rng.choice(BRANCH_IDS),
                "must_class_end_time": unix_ts(course_end - timedelta(days=30)),
                "type_end_time": unix_ts(course_end),
                "created_at": unix_ts(created_dt),
                "updated_at": unix_ts(updated_dt),
                "class_add_hours": rng.choice([None, 0, 4, 8, 10, 16]),
                "class_core_hours": rng.choice([None, 20, 40, 60, 80]),
                "value_add_hours": rng.choice([None, 0, 4, 8, 12]),
                "cf_gift": rng.choice([None, 0, 2, 4, 6]),
                "cf_lesson_times": rng.choice([None, "作品集辅导", "文书精修", "模拟面试", ""]),
                "cf_content": rng.choice([None, "赠送作品集点评2次", "延期服务30天", "更换授课老师一次"]),
                "has_add_contract": rng.choices([0, 1], weights=[80, 20])[0],
                "add_contract_status": rng.choices([0, 1], weights=[70, 30])[0],
                "pay_branch_id": rng.choice([0, 1, 2, 3, 5, 8]),
                "fid": f"FID{i:010d}" if rng.random() < 0.5 else None,
                "total_end_time": unix_ts(course_end + timedelta(days=rng.randint(0, 60))),
                "typeset_time": unix_ts(course_end - timedelta(days=rng.randint(10, 90)))
                if rng.random() < 0.6
                else None,
                "is_recommend": rng.choice(["0", "1"]),
                "is_assessed": rng.choice(["0", "1"]),
                "is_listened": rng.choice(["0", "1"]),
                "is_assisted": rng.choice(["0", "1"]),
                "goal_school": rng.choice(GOAL_SCHOOLS),
                "special_comment": rng.choice(
                    [None, "家长希望优先安排周末课程", "学生出国交换中，需线上授课", "对文书老师有指定要求"]
                ),
                "full_pay": 1 if rng.random() < 0.55 else 0,
                "payed_class_hour": int(be_class) if rng.random() < 0.8 else 0,
                "discount_content": rng.choice(
                    [None, "老带新减免3000", "早鸟优惠5000", "团报折扣8折", ""]
                ),
                "erp_have_class": float(class_hour),
                "erp_give_class": give_hour,
                "erp_chose_class": choose_hour,
                "erp_project_count": project,
                "erp_type_count": ag_type,
                "must_course_sum": '{"total":%d,"done":%.2f}' % (class_hour, be_class),
                "give_course_sum": '{"total":%.2f,"done":%.2f}' % (give_hour, min(give_hour, be_class / 10)),
                "is_count": rng.choice([0, 1]),
                "related_product": rng.choice([0, 1]),
                "school_edit_num": rng.randint(0, 5),
                "customer_id": c["customer_id"],
                "previous_master_id": 0 if is_master == 1 or i == 1 else max(0, i - rng.randint(1, 5)),
            }
        )
    return rows


CUSTOMER_COLS = [
    "customer_id", "client_id", "open_id", "nick_name", "head_img", "name", "old_name",
    "mobile_phone", "nps_phone", "parent_phone", "contract_phone", "card_type", "card",
    "passport", "birthday", "belong_branch_id", "campuses_id", "edu_email", "edu_branch_id",
    "first_tutor_email", "second_tutor_email", "selection_email", "document_email",
    "document_director_email", "application_email", "adviser_email", "second_adviser_email",
    "course_email", "teaching_email", "email", "graduate_school", "graduate_major",
    "is_sign", "status", "is_login", "last_login_ip", "last_login_time", "biz_time",
    "oper_id", "sex", "school_name", "course_set_id", "home_address", "summer_school_id",
    "lang_score", "ielts_id", "gpa_id", "jlpt", "toefl", "sat", "eju", "add_type",
    "other_lang", "server_porg", "many_country", "edu_area", "is_change_school",
    "style_end_time", "is_better", "master_class", "is_better_coach", "is_better_task",
    "is_better_review", "is_document", "is_edition", "remarks", "created_at", "updated_at",
    "inter_course_subjects_and_grades", "gpa", "phonetic_name", "english_name",
    "student_number", "customer_service_phone", "service_contact_date",
]

AGREEMENT_COLS = [
    "id", "contract_name", "is_master", "contract_number", "qiantu_id", "customer_name",
    "card", "card_type", "phone", "address", "email", "school_year", "country_name",
    "major_name", "subject_name", "degree", "file_time", "file_money", "service_charge",
    "money", "campuses_id", "edu_email", "document_email", "adviser_email",
    "adviser_branch_id", "start_adviser_email", "teaching_email", "create_time", "status",
    "pay_branch_name", "status_name", "class_hour", "product_cate_id", "service_status",
    "budget", "ag_give_hour", "ag_choose_hour", "ag_project", "ag_type", "be_class_hour",
    "be_give_hour", "be_choose_hour", "be_project", "be_project_modify", "be_type",
    "be_type_modify", "biz_time", "type", "course_start_time", "course_end_time",
    "out_branch_id", "must_class_end_time", "type_end_time", "created_at", "updated_at",
    "class_add_hours", "class_core_hours", "value_add_hours", "cf_gift", "cf_lesson_times",
    "cf_content", "has_add_contract", "add_contract_status", "pay_branch_id", "fid",
    "total_end_time", "typeset_time", "is_recommend", "is_assessed", "is_listened",
    "is_assisted", "goal_school", "special_comment", "full_pay", "payed_class_hour",
    "discount_content", "erp_have_class", "erp_give_class", "erp_chose_class",
    "erp_project_count", "erp_type_count", "must_course_sum", "give_course_sum",
    "is_count", "related_product", "school_edit_num", "customer_id", "previous_master_id",
]

STR_COLS_CUSTOMER = {
    "client_id", "open_id", "nick_name", "head_img", "name", "old_name", "mobile_phone",
    "nps_phone", "parent_phone", "contract_phone", "card", "passport", "edu_email",
    "first_tutor_email", "second_tutor_email", "selection_email", "document_email",
    "document_director_email", "application_email", "adviser_email", "second_adviser_email",
    "course_email", "teaching_email", "email", "graduate_school", "graduate_major",
    "last_login_ip", "school_name", "home_address", "lang_score", "jlpt", "toefl", "sat",
    "eju", "other_lang", "many_country", "edu_area", "master_class", "remarks",
    "inter_course_subjects_and_grades", "gpa", "phonetic_name", "english_name",
    "student_number", "customer_service_phone",
}
TS_COLS_CUSTOMER = {"service_contact_date"}

STR_COLS_AGREEMENT = {
    "contract_name", "contract_number", "qiantu_id", "customer_name", "card", "phone",
    "address", "email", "country_name", "major_name", "subject_name", "degree",
    "edu_email", "document_email", "adviser_email", "start_adviser_email", "teaching_email",
    "pay_branch_name", "status_name", "class_hour", "budget", "cf_lesson_times",
    "cf_content", "fid", "is_recommend", "is_assessed", "is_listened", "is_assisted",
    "goal_school", "special_comment", "discount_content", "must_course_sum",
    "give_course_sum",
}


def format_value(col: str, value, str_cols: set[str], ts_cols: set[str] | None = None) -> str:
    ts_cols = ts_cols or set()
    if value is None:
        return "NULL"
    if col in ts_cols:
        return sql_ts(value)
    if col in str_cols:
        return sql_str(str(value))
    if isinstance(value, float):
        return f"{value:.2f}"
    return sql_num(value)


def write_inserts(
    path: Path,
    table: str,
    cols: list[str],
    rows: list[dict],
    str_cols: set[str],
    ts_cols: set[str] | None = None,
    batch_size: int = 100,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    col_list = ", ".join(f"`{c}`" for c in cols)
    with path.open("w", encoding="utf-8") as f:
        f.write(f"-- Seed data for `{table}`: {len(rows)} rows\n")
        f.write("SET NAMES utf8mb4;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        for start in range(0, len(rows), batch_size):
            chunk = rows[start : start + batch_size]
            f.write(f"INSERT INTO `{table}` ({col_list}) VALUES\n")
            values = []
            for row in chunk:
                parts = [format_value(c, row[c], str_cols, ts_cols) for c in cols]
                values.append("(" + ", ".join(parts) + ")")
            f.write(",\n".join(values))
            f.write(";\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")


def write_schema(path: Path, ddl: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ddl.strip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=COUNT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--out-dir", type=Path, default=Path("/workspace/sql/seed"))
    args = parser.parse_args()

    rng = random.Random(args.seed)
    customers = make_customers(rng, args.count)
    agreements = make_agreements(rng, customers, args.count)

    out = args.out_dir
    write_inserts(
        out / "jx_p_customer_seed_1000.sql",
        "jx_p_customer",
        CUSTOMER_COLS,
        customers,
        STR_COLS_CUSTOMER,
        TS_COLS_CUSTOMER,
    )
    write_inserts(
        out / "jx_p_agreement_seed_1000.sql",
        "jx_p_agreement",
        AGREEMENT_COLS,
        agreements,
        STR_COLS_AGREEMENT,
    )

    summary = out / "README.md"
    summary.write_text(
        "\n".join(
            [
                "# 种子数据说明",
                "",
                f"- 生成时间种子: `{args.seed}`",
                f"- `jx_p_customer`: {len(customers)} 条 → `jx_p_customer_seed_1000.sql`",
                f"- `jx_p_agreement`: {len(agreements)} 条 → `jx_p_agreement_seed_1000.sql`",
                "- 合同表 `customer_id` 与客户表 `customer_id` 一一对应（第 i 条合同关联第 i 个客户，循环复用）",
                "- 重新生成: `python3 scripts/generate_seed_data.py`",
                "",
                "## 导入示例",
                "",
                "```bash",
                "mysql -uUSER -p DBNAME < sql/schema/jx_p_customer.sql",
                "mysql -uUSER -p DBNAME < sql/schema/jx_p_agreement.sql",
                "mysql -uUSER -p DBNAME < sql/seed/jx_p_customer_seed_1000.sql",
                "mysql -uUSER -p DBNAME < sql/seed/jx_p_agreement_seed_1000.sql",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Generated {len(customers)} customers and {len(agreements)} agreements into {out}")


if __name__ == "__main__":
    main()
