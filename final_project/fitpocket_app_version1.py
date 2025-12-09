import random
from pathlib import Path
from typing import Any, Dict, List, Set

import pandas as pd
import streamlit as st

# Streamlit page setup（保留頁籤標題即可）
st.set_page_config(page_title="FitPocket | Fit Your Body, Fit Your Budget", layout="wide")

# ---------------------------------------------------------------------
# Global style: brand system & layout polish (warm, appetizing palette)
# ---------------------------------------------------------------------
BRAND_COLORS = {
    "primary": "#d8744c",  # terracotta
    "secondary": "#6e8b3d",  # olive sage
    "accent": "#f2c57c",  # sandstone
    "bg": "#f7f1e8",  # clay dust
    "text_main": "#2f261b",
    "text_muted": "#6d5c4a",
    "card": "#ffffff",
    "stroke": "#e4d6c2",
}

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Space+Grotesk:wght@500;600&display=swap');
      :root {{
        --brand-primary: {BRAND_COLORS['primary']};
        --brand-secondary: {BRAND_COLORS['secondary']};
        --brand-accent: {BRAND_COLORS['accent']};
        --brand-bg: {BRAND_COLORS['bg']};
        --brand-text: {BRAND_COLORS['text_main']};
        --brand-muted: {BRAND_COLORS['text_muted']};
        --brand-card: {BRAND_COLORS['card']};
        --brand-stroke: {BRAND_COLORS['stroke']};
      }}
      html, body, [class*="css"]  {{
        font-family: 'Manrope', 'Space Grotesk', 'Segoe UI', system-ui, -apple-system, sans-serif;
        background: var(--brand-bg);
        color: var(--brand-text);
      }}
      body:before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
          radial-gradient(120% 120% at 15% 15%, rgba(216,116,76,0.12), transparent),
          radial-gradient(120% 120% at 85% 8%, rgba(110,139,61,0.12), transparent),
          radial-gradient(120% 120% at 50% 0%, rgba(242,197,124,0.18), transparent);
        opacity: 0.9;
        mix-blend-mode: multiply;
        z-index: -1;
      }}
      .appview-container .main .block-container {{
        padding: 2.6rem 2.6rem 2.2rem 2.6rem;
        max-width: 1240px;
      }}
      h1, h2, h3 {{
        color: var(--brand-text);
      }}
      .fp-hero {{
        background: linear-gradient(125deg, rgba(216,116,76,0.08), rgba(242,197,124,0.16)), #fdf9f2;
        border: 1px solid var(--brand-stroke);
        box-shadow: 0 24px 60px rgba(47,38,27,0.08);
        border-radius: 24px;
        padding: 26px 28px;
        position: relative;
        overflow: hidden;
      }}
      .fp-hero:before {{
        content: "";
        position: absolute;
        width: 420px; height: 420px;
        background: radial-gradient(circle, rgba(110,139,61,0.16) 0%, transparent 60%);
        top: -160px; left: -120px;
      }}
      .fp-hero:after {{
        content: "";
        position: absolute;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(47,38,27,0.06) 0%, transparent 60%);
        bottom: -140px; right: -120px;
        filter: blur(1px);
      }}
      .fp-hero-illo {{
        width: 230px; height: 230px;
        border-radius: 28px;
        background: linear-gradient(145deg, rgba(216,116,76,0.18), rgba(110,139,61,0.18));
        border: 1px solid var(--brand-stroke);
        display: grid; place-items: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(47,38,27,0.12);
      }}
      .fp-hero-illo:after {{
        content: "";
        position: absolute;
        inset: 12px;
        border-radius: 24px;
        background: linear-gradient(160deg, rgba(255,255,255,0.35), rgba(255,255,255,0));
        opacity: 0.75;
        pointer-events: none;
      }}
      .fp-hero-illo .fp-floating {{
        position: absolute;
        inset: 0;
        background-image:
          radial-gradient(circle at 20% 30%, rgba(255,255,255,0.18) 0, transparent 40%),
          radial-gradient(circle at 80% 20%, rgba(255,255,255,0.14) 0, transparent 34%),
          radial-gradient(circle at 50% 70%, rgba(47,38,27,0.07) 0, transparent 55%);
        mix-blend-mode: soft-light;
      }}
      .fp-badge {{
        display: inline-flex; align-items: center; gap: 8px;
        padding: 7px 14px;
        background: rgba(110,139,61,0.12);
        border: 1px solid rgba(110,139,61,0.2);
        color: var(--brand-secondary);
        font-weight: 800;
        border-radius: 999px;
        letter-spacing: 0.8px;
        font-size: 12px;
      }}
      .fp-logo {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 999px;
        background: #fffdf9;
        border: 1px solid rgba(47,38,27,0.08);
        box-shadow: 0 12px 30px rgba(216,116,76,0.16);
      }}
      .fp-logo-icon {{
        width: 42px; height: 42px;
        border-radius: 12px;
        background: linear-gradient(145deg, var(--brand-primary), #e79870);
        display: grid; place-items: center;
        position: relative;
        overflow: hidden;
      }}
      .fp-logo-icon:before {{
        content: "";
        position: absolute;
        width: 120%; height: 120%;
        top: -50%; left: -10%;
        background: radial-gradient(circle, rgba(255,255,255,0.45) 0%, transparent 55%);
        transform: rotate(-8deg);
      }}
      .fp-card {{
        background: var(--brand-card);
        border: 1px solid var(--brand-stroke);
        border-radius: 16px;
        padding: 18px 18px;
        box-shadow: 0 16px 36px rgba(47,38,27,0.08);
        background-image: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.9));
      }}
      .fp-section-title {{
        font-weight: 800;
        font-size: 21px;
        color: var(--brand-text);
        letter-spacing: -0.3px;
        margin-bottom: 8px;
      }}
      .fp-pill {{
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(47,38,27,0.06);
        color: var(--brand-muted);
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 0.4px;
      }}
      .fp-meal-card {{
        border: 1px solid var(--brand-stroke);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        background: linear-gradient(150deg, rgba(247,241,232,0.7), #fff);
        box-shadow: 0 12px 24px rgba(47,38,27,0.05);
        transition: transform 0.08s ease, box-shadow 0.12s ease;
      }}
      .fp-meal-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 18px 30px rgba(47,38,27,0.08);
      }}
      .fp-meal-title {{
        font-weight: 900;
        color: var(--brand-text);
      }}
      .fp-chip {{
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        color: var(--brand-secondary);
        background: rgba(110,139,61,0.12);
        border: 1px solid rgba(110,139,61,0.22);
      }}
      .fp-chip.neutral {{
        color: var(--brand-text);
        background: rgba(47,38,27,0.05);
        border: 1px solid var(--brand-stroke);
      }}
      .stButton>button, .stForm button {{
        background: linear-gradient(135deg, var(--brand-primary), #e79870);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 11px 18px;
        font-weight: 800;
        letter-spacing: 0.3px;
        box-shadow: 0 14px 26px rgba(216,116,76,0.25);
        transition: transform 0.08s ease, box-shadow 0.12s ease;
      }}
      .stButton>button:hover, .stForm button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 16px 30px rgba(216,116,76,0.3);
      }}
      div[data-baseweb="tab-list"] button {{
        border-radius: 12px 12px 0 0 !important;
        background: rgba(47,38,27,0.04);
        color: var(--brand-muted);
        border: 1px solid var(--brand-stroke);
        padding: 12px 18px;
        font-weight: 800;
      }}
      div[data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: #fff;
        color: var(--brand-text);
        box-shadow: 0 12px 20px rgba(47,38,27,0.06);
      }}
      label, .stRadio legend {{
        font-weight: 800 !important;
        color: var(--brand-text);
      }}
      .stNumberInput input, .stTextInput input, .stSelectbox div[role="combobox"] {{
        border-radius: 12px !important;
        border: 1px solid var(--brand-stroke) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
      }}
      .stAlert > div {{
        border-radius: 12px;
        border: 1px solid var(--brand-stroke);
      }}
      /* Hide Streamlit default footer */
      footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# Brand headline（頁面主標題，避免重複 slogan）
st.title("FitPocket 智慧膳食 預算管家")

STAT_CHIP_STYLE = (
    "padding:8px 14px; font-size:13px; box-shadow:0 10px 20px rgba(47,38,27,0.12); "
    "background:rgba(47,38,27,0.04); border:1px solid var(--brand-stroke); color:var(--brand-text);"
)

# Type aliases for readability
MealItem = Dict[str, Any]
DailyMenu = Dict[str, Any]
Plan = Dict[str, Any]
Combo = Dict[str, Any]

# Display labels for meal sections
MEAL_DISPLAY_NAMES = {
    "breakfast": "早餐時光",
    "lunch": "午間補給",
    "dinner": "晚餐饗宴",
}

# ---------------------------------------------------------------------
# 1) 資料載入與全域設定
# ---------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "711_food_data.csv"

CONSTANTS = {
    "BUDGET_TOLERANCE": 50,
    "SIMULATION_COUNT": 20000,
    "TARGET_Categories": 6,
    "MAX_BUDGET_OVERRUN": 100,  # 最多只接受超出預算 100 元內的方案
    "CALORIE_RANGE": (0.9, 1.1),  # 總熱量需落在 TDEE 的 90%~110%
    "CAL_DIFF_WARN_RATIO": 0.05,  # 超支保留時允許的熱量相對誤差
}

ACTIVITY_MULTIPLIERS = {
    "久坐": 1.2,
    "輕強度": 1.4,
    "中強度": 1.6,
    "高強度": 1.8,
    "超高強度": 2.0,
}

FOOD_GROUPS = ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"]


def parse_list(val: Any) -> List[str]:
    """將 CSV 欄位轉為乾淨的列表。"""
    if pd.isna(val):
        return []
    normalized = (
        str(val)
        .replace('"', "")
        .replace("，", ",")
        .replace("、", ",")
        .replace("/", ",")
        .replace("／", ",")
        .replace("|", ",")
    )
    return [x.strip() for x in normalized.split(",") if x.strip()]


@st.cache_data
def load_and_prep_data(filepath: Path) -> tuple[pd.DataFrame, str]:
    """依據最新防呆規則讀取並清洗 7-ELEVEN 食品資料。"""
    if not filepath.exists():
        return pd.DataFrame(), "錯誤：找不到檔案，請確認檔名是否正確。"

    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="utf-8-sig")
    except FileNotFoundError:
        return pd.DataFrame(), "錯誤：找不到檔案，請確認檔名是否正確。"

    # 自動去除欄位名稱前後空白
    df.columns = df.columns.str.strip()

    required_cols = [
        "價格(price)",
        "熱量(calories)",
        "餐次規則(meal)",
        "餐點性質(type)",
        "食物六大類(category)",
        "食物名稱(name)",
    ]
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame(), f"錯誤：資料庫缺漏必要欄位，請檢查 CSV 表頭是否包含: {required_cols}"

    # 轉型失敗強制 NaN，以便後續清除
    df["價格(price)"] = pd.to_numeric(df["價格(price)"], errors="coerce")
    df["熱量(calories)"] = pd.to_numeric(df["熱量(calories)"], errors="coerce")

    # 關鍵欄位不得為空
    df = df.dropna(subset=required_cols)
    if df.empty:
        return pd.DataFrame(), "錯誤：資料庫中沒有有效資料 (所有資料均含有空值)。"

    df["meal_list"] = df["餐次規則(meal)"].apply(parse_list)
    df["category_list"] = df["食物六大類(category)"].apply(parse_list)
    df["categories_set"] = df["category_list"].apply(set)

    def normalize_type(row: pd.Series) -> str:
        raw_type = str(row["餐點性質(type)"]).strip()
        if raw_type in ["主餐", "主食"]:
            return "主食"
        return "副餐"

    df["normalized_type"] = df.apply(normalize_type, axis=1)

    def is_beverage(row: pd.Series) -> bool:
        raw_type = str(row["餐點性質(type)"]).strip()
        if raw_type == "飲料":
            return True

        name = str(row["食物名稱(name)"])
        cat = str(row["食物六大類(category)"])

        if "乳品類" in cat:
            return True
        keywords = ["拿鐵", "美式", "咖啡", "茶", "豆漿", "鮮奶", "牛奶", "飲", "汁"]
        for k in keywords:
            if k in name and "沙茶" not in name and "茶葉蛋" not in name:
                return True
        return False

    df["is_drink"] = df.apply(is_beverage, axis=1)

    # 補齊店家、圖片欄位，避免渲染錯誤
    if "商店(shop)" in df.columns:
        df["商店(shop)"] = df["商店(shop)"].fillna("7-ELEVEN")
    else:
        df["商店(shop)"] = "7-ELEVEN"

    img_series = df["食物無片(image)"] if "食物無片(image)" in df.columns else pd.Series([None] * len(df), index=df.index)
    if "image" in df.columns:
        img_series = img_series.fillna(df["image"])
    df["img"] = img_series.fillna("").replace("", pd.NA)

    # 與舊版欄位名稱保持兼容
    df["type_norm"] = df["normalized_type"]
    return df, "OK"


FOOD_DF, LOAD_STATUS = load_and_prep_data(DATA_PATH)
if LOAD_STATUS != "OK":
    st.error(LOAD_STATUS)
    st.stop()


def record_to_item(record: Dict[str, Any]) -> MealItem:
    """將原始記錄轉為前端渲染需要的格式。"""
    cats_val = record.get("categories_set") or set()
    if not isinstance(cats_val, set):
        try:
            cats_val = set(cats_val)
        except TypeError:
            cats_val = set()
    img_val = record.get("img")
    img_val = img_val if isinstance(img_val, str) and img_val else None
    return {
        "store": record.get("商店(shop)", "7-ELEVEN"),
        "meal_time": record.get("meal_list", []),
        "name": record.get("食物名稱(name)", ""),
        "type": record.get("normalized_type") or record.get("type_norm", ""),
        "price": int(record.get("價格(price)", 0)),
        "cal": int(record.get("熱量(calories)", 0)),
        "cats": list(cats_val),
        "img": img_val,
        "is_drink": bool(record.get("is_drink", False)),
    }


def calculate_bmr(gender: str, age: int, height_cm: float, weight_kg: float) -> float:
    """依新版公式計算 BMR。"""
    if gender == "male":
        return 5.0 * height_cm + 13.7 * weight_kg - 6.8 * age + 66
    return 1.8 * height_cm + 9.6 * weight_kg - 4.7 * age + 655


def calculate_tdee(user_profile: Dict[str, Any]) -> float:
    """依據活動係數計算 TDEE。"""
    bmr = calculate_bmr(
        gender=user_profile["gender"],
        age=user_profile["age"],
        height_cm=user_profile["height"],
        weight_kg=user_profile["weight"],
    )
    return bmr * ACTIVITY_MULTIPLIERS.get(user_profile["activity_level"], 1.2)


def bmi_category(bmi: float) -> str:
    """成人 BMI 分類（台灣標準）。"""
    if bmi < 18.5:
        return "體重過輕"
    if bmi < 24:
        return "健康體位"
    if bmi < 27:
        return "體重過重"
    if bmi < 30:
        return "輕度肥胖"
    if bmi < 35:
        return "中度肥胖"
    return "重度肥胖"


def get_meal_candidates(df: pd.DataFrame, meal_tag: str) -> List[List[Dict[str, Any]]]:
    """依主/副餐規則生成候選餐點組合。"""
    valid_df = df[df["meal_list"].apply(lambda x: meal_tag in x)].copy()
    if valid_df.empty:
        return []

    mains = valid_df[valid_df["normalized_type"] == "主食"].to_dict("records")
    sides = valid_df[valid_df["normalized_type"] == "副餐"].to_dict("records")
    candidates: List[List[Dict[str, Any]]] = []

    def check_drink_limit(items: List[Dict[str, Any]]) -> bool:
        return sum(1 for x in items if x.get("is_drink")) <= 1

    if meal_tag in ["午餐", "晚餐"]:
        for m in mains:
            for s in sides:
                combo = [m, s]
                if check_drink_limit(combo):
                    candidates.append(combo)
        for m in mains:
            if check_drink_limit([m]):
                candidates.append([m])
    else:
        for m in mains:
            for s in sides:
                combo = [m, s]
                if check_drink_limit(combo):
                    candidates.append(combo)
        for m in mains:
            if check_drink_limit([m]):
                candidates.append([m])
        for i in range(len(sides)):
            for j in range(i + 1, len(sides)):
                combo = [sides[i], sides[j]]
                if check_drink_limit(combo):
                    candidates.append(combo)
        for s in sides:
            if check_drink_limit([s]):
                candidates.append([s])
    return candidates


def run_simulation(user_profile: Dict[str, Any], df_data: pd.DataFrame) -> tuple[List[Dict[str, Any]], str]:
    """蒙地卡羅模擬：挑選符合預算/熱量/類別廣度的餐單。"""
    tdee = calculate_tdee(user_profile)
    budget = user_profile["budget"]
    b_min, b_max = budget - CONSTANTS["BUDGET_TOLERANCE"], budget + CONSTANTS["BUDGET_TOLERANCE"]
    cal_min_ratio, cal_max_ratio = CONSTANTS["CALORIE_RANGE"]
    min_cal, max_cal = tdee * cal_min_ratio, tdee * cal_max_ratio

    pool_b = get_meal_candidates(df_data, "早餐")
    pool_l = get_meal_candidates(df_data, "午餐")
    pool_d = get_meal_candidates(df_data, "晚餐")

    if not pool_b:
        return [], "錯誤：資料庫中沒有適合的「早餐」資料。"
    if not pool_l:
        return [], "錯誤：資料庫中沒有適合的「午餐主食」。"
    if not pool_d:
        return [], "錯誤：資料庫中沒有適合的「晚餐主食」。"

    valid_plans: List[Dict[str, Any]] = []
    for _ in range(CONSTANTS["SIMULATION_COUNT"]):
        mb = random.choice(pool_b)
        ml = random.choice(pool_l)
        md = random.choice(pool_d)
        all_items = mb + ml + md

        names = [x["食物名稱(name)"] for x in all_items]
        if len(names) != len(set(names)):
            continue

        cost = sum(x["價格(price)"] for x in all_items)
        cal = sum(x["熱量(calories)"] for x in all_items)
        if not (min_cal <= cal <= max_cal):
            continue
        diff = abs(cal - tdee)

        # 僅保留超支 100 元以內的組合
        if cost > budget + CONSTANTS["MAX_BUDGET_OVERRUN"]:
            continue

        status = "Valid"
        if cost > b_max:
            if (diff / tdee) < CONSTANTS["CAL_DIFF_WARN_RATIO"]:
                status = "OverBudgetWarning"  # 超出容忍度也給警示
            else:
                continue
        elif cost > budget:
            status = "OverBudgetWarning"  # 任何超支都提示
        # 若低於下限容忍則直接接受，不警示

        cats: Set[str] = set()
        for x in all_items:
            cats.update(x["categories_set"])

        # 需要涵蓋六大食物類別才視為有效方案
        if not cats.issuperset(FOOD_GROUPS):
            continue

        valid_plans.append(
            {
                "plan_content": {"早餐": mb, "午餐": ml, "晚餐": md},
                "metrics": {
                    "cost": cost,
                    "cal": cal,
                    "diff": diff,
                    "cat_count": len(cats),
                    "categories": list(cats),
                    "status": status,
                },
            }
        )

    return valid_plans, "Success"


def select_top_plans(valid_plans: List[Dict[str, Any]], num_plans: int = 3) -> tuple[List[Dict[str, Any]], bool]:
    """依類別廣度與熱量誤差排序，取唯一解。"""
    if not valid_plans:
        return [], False

    valid_plans.sort(key=lambda x: (-x["metrics"]["cat_count"], x["metrics"]["diff"]))

    unique: List[Dict[str, Any]] = []
    seen: Set[tuple] = set()
    has_warning = False

    for p in valid_plans:
        sig = (p["metrics"]["cost"], p["metrics"]["cal"])
        if sig in seen:
            continue
        seen.add(sig)
        unique.append(p)
        if p["metrics"]["status"] == "OverBudgetWarning":
            has_warning = True
        if len(unique) >= num_plans:
            break
    return unique, has_warning


def budget_level(total_price: float) -> str:
    if total_price <= 499:
        return "低預算"
    if total_price <= 800:
        return "中預算"
    return "高預算"


def build_plans(user_profile: Dict[str, Any], df_data: pd.DataFrame) -> tuple[List[Plan], str, bool]:
    """使用最新蒙地卡羅演算法生成最多三套可行方案。"""
    if df_data.empty:
        return [], "錯誤：資料庫為空，請確認 711_food_data.csv 是否存在。", False

    valid_plans, status = run_simulation(user_profile, df_data)
    if status != "Success":
        return [], status, False
    if not valid_plans:
        no_plan_msg = (
            "⚠️ 搜尋結果：找不到符合條件的組合。\n"
            "原因可能是：\n"
            "1. 預算過低 (午晚餐強制主食 + 早餐，建議預算 > 250元)\n"
            "2. 資料庫食物選擇不足或無法同時涵蓋六大食物類別\n"
        )
        return [], no_plan_msg, False

    top_plans, has_warning = select_top_plans(valid_plans, num_plans=3)
    if not top_plans:
        return [], "⚠️ 搜尋結果：找不到符合條件的組合。", has_warning

    tags = [("營養師推薦", "⭐"), ("精省首選", "💰"), ("均衡美味", "👍")]
    plans: List[Plan] = []
    for plan_data, (tag, icon) in zip(top_plans, tags):
        metrics = plan_data["metrics"]
        meal_map = {k: [record_to_item(item) for item in v] for k, v in plan_data["plan_content"].items()}
        categories = set(metrics.get("categories", []))
        plans.append(
            {
                "breakfast": meal_map.get("早餐", []),
                "lunch": meal_map.get("午餐", []),
                "dinner": meal_map.get("晚餐", []),
                "totalCal": int(metrics["cal"]),
                "totalPrice": int(metrics["cost"]),
                "budgetLevel": budget_level(metrics["cost"]),
                "missingCategories": [c for c in FOOD_GROUPS if c not in categories],
                "userBudget": int(user_profile["budget"]),
                "tag": tag,
                "tagIcon": icon,
                "status": metrics.get("status", "Valid"),
            }
        )
    return plans, "Success", has_warning


# ---------------------------------------------------------------------
# 3) UI：Streamlit 互動介面
# ---------------------------------------------------------------------
def render_logo() -> None:
    st.markdown(
        """
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Top hero section with brand badge and logo."""
    st.markdown(
        """
        <div class="fp-hero">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap; margin-top:4px;">
                <div style="max-width:580px; min-width:280px;">
                    <h2 style="margin:0 0 10px; font-size:36px; font-weight:900; color:#1f2937; line-height:1.1; letter-spacing:-0.3px;">
                        量身打造<br/>
                        <span style="color:transparent; background:linear-gradient(90deg, #f59e0b, #f97316); -webkit-background-clip:text; background-clip:text;">
                            您的專屬菜單
                        </span>
                    </h2>
                    <p style="margin:0; color:#6b7280; font-size:16px; font-weight:700; line-height:1.6;">
                        FitPocket 結合營養科學與美味演算法。輸入您的身體數值，我們將為您計算最精準的熱量需求，並嚴格把關您的餐食預算。
                    </p>
                </div>
                <div class="fp-hero-illo">
                    <div class="fp-floating"></div>
                    <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="plate" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#fef6ea"/>
                                <stop offset="100%" stop-color="#f5e2c7"/>
                            </linearGradient>
                            <linearGradient id="bowl" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#d8744c"/>
                                <stop offset="100%" stop-color="#e8a072"/>
                            </linearGradient>
                            <linearGradient id="leaf" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#6e8b3d"/>
                                <stop offset="100%" stop-color="#89a85a"/>
                            </linearGradient>
                        </defs>
                        <rect x="18" y="20" width="184" height="180" rx="34" fill="url(#plate)" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
                        <circle cx="74" cy="74" r="34" fill="rgba(242,197,124,0.32)" />
                        <path d="M48 118h124c0 32-34 58-62 58s-62-26-62-58Z" fill="url(#bowl)" stroke="rgba(255,255,255,0.8)" stroke-width="4" stroke-linejoin="round"/>
                        <path d="M82 118c2 10 9 20 26 20s24-10 26-20" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="3" stroke-linecap="round"/>
                        <path d="M110 78c12-10 24-10 32-2" fill="none" stroke="url(#leaf)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M116 74c-4-12-1-22 8-30" fill="none" stroke="url(#leaf)" stroke-width="6" stroke-linecap="round"/>
                        <path d="M134 68c10-3 18-12 20-22" fill="none" stroke="url(#leaf)" stroke-width="6" stroke-linecap="round"/>
                        <circle cx="82" cy="102" r="10" fill="#f2c57c" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
                        <circle cx="136" cy="98" r="9" fill="#6e8b3d" opacity="0.85" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
                        <circle cx="110" cy="100" r="7" fill="#ffe6c1" opacity="0.9" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
                        <path d="M74 140c8 10 22 18 36 18s28-8 36-18" fill="none" stroke="rgba(46,38,27,0.12)" stroke-width="8" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_logo()



def render_metric_cards(
    bmr: float, tdee: float, bmi_value: float, activity_label: str, activity_multiplier: float
) -> None:
    """Display BMR/TDEE/recommendation summary cards."""
    bmi_status = bmi_category(bmi_value)
    st.markdown(
        f"""
        <div class="fp-card" style="margin-top:18px; margin-bottom:26px; background:linear-gradient(120deg, rgba(247,241,232,0.7), #fff);">
            <div style="display:flex; gap:16px; flex-wrap:wrap;">
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(216,116,76,0.12), #fff);">
                    <div class="fp-pill">BMR</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{bmr:.0f} kcal / 天</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">BMR 指靜止時維持生命的最低熱量。</div>
                </div>
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(110,139,61,0.12), #fff);">
                    <div class="fp-pill">TDEE</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{tdee:.0f} kcal / 天</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px; margin-top:4px; line-height:1.5;">
                        TDEE 為單日總消耗熱量，含基礎代謝、活動及飲食。\
                    </div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">
                        = BMR x {activity_multiplier:.3g} （{activity_label}）
                    </div>
                </div>
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(242,197,124,0.16), #fff);">
                    <div class="fp-pill">BMI</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{bmi_value:.1f} {bmi_status}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_meal_block(title: str, items: List[MealItem]) -> None:
    st.markdown(f"<div class='fp-section-title'>{title}</div>", unsafe_allow_html=True)
    st.caption(
        f"總熱量 {sum(i['cal'] for i in items)} kcal · 共 {len(items)} 道餐點"
    )
    for item in items:
        if item.get("img"):
            img_tag = f"<img src='{item['img']}' alt='{item['name']}' style='width:72px;height:72px;object-fit:cover;border-radius:10px;border:1px solid var(--brand-stroke);background:#fff;' onerror=\"this.style.display='none'\"/>"
        else:
            img_tag = (
                "<div style='width:72px;height:72px;border-radius:10px;"
                "border:1px dashed var(--brand-stroke);display:grid;place-items:center;"
                "color:var(--brand-muted);font-weight:800;'>🌿</div>"
            )
        st.markdown(
            f"""
            <div class="fp-meal-card" style="display:flex; gap:12px; align-items:center;">
                {img_tag}
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                        <div class="fp-meal-title">{item['name']}</div>
                        <div class="fp-chip neutral">NT${item['price']}</div>
                    </div>
                    <div style="display:flex; gap:10px; margin-top:6px; color: var(--brand-muted); font-weight:700; font-size:12px; align-items:center; flex-wrap:wrap;">
                        <span>{item['store']}</span>
                        <span>·</span>
                        <span>{item['cal']} kcal</span>
                    </div>
                    <div style="margin-top:6px; display:flex; flex-wrap:wrap; gap:8px;">
                        {"".join([f"<span class='fp-pill'>{c}</span>" for c in item["cats"]])}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_stat_chip(text: str) -> str:
    """Reusable chip HTML for plan header stats."""
    return f'<div class="fp-chip" style="{STAT_CHIP_STYLE}">{text}</div>'


def render_plan_header(plan: Plan, label: str) -> None:
    """Header bar for each plan tab (只顯示統計區域)，重新美化並合併六大類狀態。"""
    missing = plan.get("missingCategories", [])
    if missing:
        cat_text = f"缺少：{'、'.join(missing)}"
        cat_class = "warn"
    else:
        cat_text = "已涵蓋六大食物類別 ✅"
        cat_class = "ok"

    budget = int(plan.get("userBudget", 0))
    cost = int(plan.get("totalPrice", 0))
    balance = budget - cost
    if balance >= 0:
        balance_icon, balance_text = "💡", f"省下 NT${balance}"
    else:
        balance_icon, balance_text = "⚠️", f"超支 NT${abs(balance)}"

    metrics = [
        ("🔥", f"總熱量 {plan['totalCal']} kcal"),
        ("💰", f"總花費 NT${plan['totalPrice']}"),
        (balance_icon, balance_text),
    ]
    metric_html = "".join(
        [f"<div class='fp-metric-chip'><span class='icon'>{ico}</span><span>{txt}</span></div>" for ico, txt in metrics]
    )

    st.markdown(
        f"""
        <div class="fp-plan-bar">
          <div class="fp-plan-bar__badge fp-plan-bar__badge-{cat_class}">
            <span class="icon">{'✅' if cat_class == 'ok' else '⚠️'}</span>
            <span>{cat_text}</span>
          </div>
          <div class="fp-plan-bar__metrics">{metric_html}</div>
        </div>
        <style>
          .fp-plan-bar {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 10px;
            padding: 12px 14px;
            border-radius: 14px;
            background: #ffffff;
            border: 1px solid rgba(47,38,27,0.08);
            box-shadow: 0 10px 20px rgba(47,38,27,0.06);
          }}
          .fp-plan-bar__badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 12px;
            font-weight: 800;
            letter-spacing: 0.2px;
            border: 1px solid transparent;
          }}
          .fp-plan-bar__badge-ok {{
            background: rgba(110,139,61,0.12);
            border-color: rgba(110,139,61,0.2);
            color: var(--brand-secondary);
          }}
          .fp-plan-bar__badge-warn {{
            background: rgba(216,116,76,0.12);
            border-color: rgba(216,116,76,0.22);
            color: var(--brand-primary);
          }}
          .fp-plan-bar__metrics {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
          }}
          .fp-metric-chip {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border-radius: 12px;
            background: #f8f5f0;
            border: 1px solid rgba(47,38,27,0.08);
            box-shadow: none;
            font-weight: 800;
            color: var(--brand-text);
          }}
          .fp-metric-chip .icon {{
            font-size: 14px;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )


render_hero()


with st.form("user_input"):
    st.markdown('<div class="fp-section-title">你的基礎資料</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1.2, 1])
    with col1:
        gender = st.radio("生理性別", ["male", "female"], format_func=lambda v: "男性" if v == "male" else "女性")
        age = st.number_input("年齡", min_value=15, max_value=80, value=25, step=1)
    with col2:
        height = st.number_input("身高（公分）", min_value=130, max_value=220, value=170, step=1)
        weight = st.number_input("體重（公斤）", min_value=30.0, max_value=200.0, value=65.0, step=0.5)
    with col3:
        budget_value = st.slider("每日預算上限 (NTD)", min_value=200, max_value=1200, value=600, step=10)
        activity = st.selectbox(
            "日常活動量",
            options=[
                ("久坐", "久坐 / 辦公室"),
                ("輕強度", "輕度活動：每週運動 1-3 天"),
                ("中強度", "中度活動：每週運動 3-5 天"),
                ("高強度", "高度活動：每週運動 6-7 天"),
                ("超高強度", "超高活動：勞力工作或重度訓練"),
            ],
            format_func=lambda t: t[1],
        )
    submitted = st.form_submit_button("計算並生成餐單方案", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


if submitted:
    activity_level, activity_label = activity
    activity_multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    bmr = calculate_bmr(gender, age, height, weight)
    tdee = bmr * activity_multiplier
    bmi_value = weight / ((height / 100) ** 2)

    user_profile = {
        "age": int(age),
        "gender": gender,
        "height": float(height),
        "weight": float(weight),
        "activity_level": activity_level,
        "budget": float(budget_value),
    }

    plans, status_msg, has_warning = build_plans(user_profile, FOOD_DF)

    render_metric_cards(bmr, tdee, bmi_value, activity_label, activity_multiplier)

    if not plans:
        st.warning(status_msg)
        st.stop()

    labels = [f"方案{chr(65 + i)}" for i in range(len(plans))]
    tab_titles = labels
    tabs = st.tabs(tab_titles)

    for tab, label, plan in zip(tabs, labels, plans):
        with tab:
            render_plan_header(plan, label)

            if plan.get("status") == "OverBudgetWarning":
                st.warning("為了貼近熱量目標，部分組合略微超出預算上限。")
            elif plan.get("status") == "CalorieShortfall":
                st.warning(
                    "目前無法找到達到目標熱量 90%~110% 的組合，以下為最接近的方案，"
                    "建議提高預算或放寬熱量條件。"
                )

            st.divider()
            render_meal_block(MEAL_DISPLAY_NAMES["breakfast"], plan["breakfast"])
            render_meal_block(MEAL_DISPLAY_NAMES["lunch"], plan["lunch"])
            render_meal_block(MEAL_DISPLAY_NAMES["dinner"], plan["dinner"])
