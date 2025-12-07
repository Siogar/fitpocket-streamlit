import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

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

# ---------------------------------------------------------------------
# 1) 資料載入：從 CSV 讀取 7-ELEVEN 食品清單
# ---------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "711_food_data.csv"


@st.cache_data
def load_food_df() -> pd.DataFrame:
    """讀取 CSV 並進行欄位清洗與欄位標準化。"""
    if not DATA_PATH.exists():
        st.error(f"找不到資料檔案：{DATA_PATH}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    if "食物名稱(name)" not in df.columns:
        st.error("CSV 欄位名稱不符合預期，請確認檔案格式。")
        return pd.DataFrame()

    df = df.dropna(subset=["食物名稱(name)"])

    def parse_list(val: Any) -> List[str]:
        if pd.isna(val):
            return []
        return [x.strip() for x in str(val).replace("，", ",").split(",") if x.strip()]

    df["meal_list"] = df["餐次規則(meal)"].apply(parse_list)
    df["category_list"] = df["食物六大類(category)"].apply(parse_list)
    df["has_veg"] = df["category_list"].apply(lambda x: "蔬菜類" in x)
    df["商店(shop)"] = df["商店(shop)"].fillna("7-ELEVEN")
    df["價格(price)"] = pd.to_numeric(df["價格(price)"], errors="coerce").fillna(0).astype(int)
    df["熱量(calories)"] = pd.to_numeric(df["熱量(calories)"], errors="coerce").fillna(0).astype(int)

    img_series = df["食物無片(image)"] if "食物無片(image)" in df.columns else pd.Series([None] * len(df))
    if "image" in df.columns:
        img_series = img_series.fillna(df["image"])
    df["img"] = img_series.fillna("").replace("", pd.NA)
    return df


FOOD_DF = load_food_df()
if FOOD_DF.empty:
    st.error("找不到有效的 7-ELEVEN 食物資料，請確認 711_food_data.csv 是否存在且格式正確。")


def row_to_item(row: pd.Series) -> MealItem:
    return {
        "store": row["商店(shop)"],
        "meal_time": row["meal_list"],
        "name": row["食物名稱(name)"],
        "type": row.get("餐點性質(type)", ""),
        "price": int(row["價格(price)"]),
        "cal": int(row["熱量(calories)"]),
        "cats": list(row["category_list"]),
        "img": row["img"] if isinstance(row["img"], str) and row["img"] else None,
    }

TARGET_TIERS = [1500, 1800, 2000, 2200, 2500, 2700]
FOOD_GROUPS = ["全穀雜糧類", "豆魚蛋肉類", "乳品類", "蔬菜類", "水果類", "油脂與堅果種子類"]
MAIN_DISH_CAT = "全穀雜糧類"
BUDGET_TOLERANCE = 50  # 總預算允許的浮動範圍
DEFAULT_SIMULATIONS = 50000


# ---------------------------------------------------------------------
# 2) 演算法：BMR / TDEE / 菜單生成
# ---------------------------------------------------------------------
def calculate_bmr(gender: str, age: int, height_cm: float, weight_kg: float) -> float:
    """依性別使用 Harris-Benedict 公式計算 BMR。"""
    if gender == "male":
        return 66.5 + (13.75 * weight_kg) + (5.003 * height_cm) - (6.755 * age)
    return 655.1 + (9.563 * weight_kg) + (1.850 * height_cm) - (4.676 * age)


def get_activity_multiplier(level: str) -> float:
    return {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }.get(level, 1.2)


def get_closest_tier(tdee: float) -> int:
    for tier in TARGET_TIERS:
        if tdee <= tier:
            return tier
    return TARGET_TIERS[-1]


class MenuOptimizer:
    """蒙地卡羅取樣，加入餐點性質（主食/副餐）組合規則與預算容忍。"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if "餐點性質(type)" not in self.df.columns:
            self.df["餐點性質(type)"] = "主食"
        if "categories_set" not in self.df.columns:
            self.df["categories_set"] = self.df["category_list"].apply(lambda x: set(x))

    def _parse_candidates(self, meal_type: str) -> List[List[MealItem]]:
        """依餐次生成候選組合，遵循主/副餐規則。"""
        valid = self.df[self.df["meal_list"].apply(lambda x: meal_type in x)]
        mains = valid[valid["餐點性質(type)"] == "主食"].to_dict("records")
        sides = valid[valid["餐點性質(type)"] == "副餐"].to_dict("records")

        main_items = [row_to_item(pd.Series(r)) for r in mains]
        side_items = [row_to_item(pd.Series(r)) for r in sides]

        candidates: List[List[MealItem]] = []

        for m in main_items:
            candidates.append([m])  # 單點主食（預算低時備案）

        for m in main_items:
            for s in side_items:
                candidates.append([m, s])  # 主食 + 副餐

        if meal_type == "早餐":
            for s in side_items:
                candidates.append([s])  # 單點副餐
            for i in range(len(side_items)):
                for j in range(i + 1, len(side_items)):
                    candidates.append([side_items[i], side_items[j]])  # 副餐 + 副餐

        return candidates

    @staticmethod
    def _combo_summary(combo: List[MealItem]) -> Combo:
        cats = set(cat for item in combo for cat in item["cats"])
        return {
            "items": combo,
            "cal": float(sum(item["cal"] for item in combo)),
            "price": float(sum(item["price"] for item in combo)),
            "categories": cats,
        }

    def generate_plans(
        self,
        user_cal: float,
        user_budget: float,
        max_plans: int = 3,
        simulations: int = DEFAULT_SIMULATIONS,
    ) -> List[Plan]:
        pools = {
            "早餐": self._parse_candidates("早餐"),
            "午餐": self._parse_candidates("午餐"),
            "晚餐": self._parse_candidates("晚餐"),
        }
        if any(len(pool) == 0 for pool in pools.values()):
            return []

        valid_plans: List[Plan] = []

        for _ in range(simulations):
            cb = random.choice(pools["早餐"])
            cl = random.choice(pools["午餐"])
            cd = random.choice(pools["晚餐"])

            all_items = cb + cl + cd
            names = [i["name"] for i in all_items]
            if len(names) != len(set(names)):
                continue

            total_cost = sum(i["price"] for i in all_items)
            # 只檢查不超支，允許低於預算（避免資料集價格偏低時無解）
            if total_cost > user_budget + BUDGET_TOLERANCE:
                continue

            total_cal = sum(i["cal"] for i in all_items)
            cal_diff = abs(total_cal - user_cal)

            cats: Set[str] = set()
            for item in all_items:
                cats.update(item["cats"])

            plan_record: Plan = {
                "menu": [
                    {"meal": "早餐", **self._combo_summary(cb)},
                    {"meal": "午餐", **self._combo_summary(cl)},
                    {"meal": "晚餐", **self._combo_summary(cd)},
                ],
                "total_cal": float(total_cal),
                "total_cost": float(total_cost),
                "diversity": list(cats),
                "cat_count": len(cats),
                "cal_diff": float(cal_diff),
            }
            valid_plans.append(plan_record)

        valid_plans.sort(key=lambda x: (-x["cat_count"], x["cal_diff"]))

        unique_plans: List[Plan] = []
        seen: Set[tuple] = set()
        for p in valid_plans:
            sig = (int(p["total_cost"]), int(p["total_cal"]))
            if sig in seen:
                continue
            seen.add(sig)
            unique_plans.append(p)
            if len(unique_plans) >= max_plans:
                break

        return unique_plans


def budget_level(total_price: float) -> str:
    if total_price <= 499:
        return "低預算"
    if total_price <= 800:
        return "中預算"
    return "高預算"


def budget_cap(budget_type: str) -> float:
    if budget_type == "低預算":
        return 499
    if budget_type == "中預算":
        return 800
    return 1200


def build_plans(target_calories: float, budget_type: str) -> List[Plan]:
    """使用核心演算法生成最多三套可行方案（可能少於三套）。"""
    if FOOD_DF.empty:
        return []

    optimizer = MenuOptimizer(FOOD_DF)
    daily_budget = budget_cap(budget_type)
    raw_plans = optimizer.generate_plans(user_cal=target_calories, user_budget=daily_budget, max_plans=3)
    if not raw_plans:
        return []

    tags = [("營養師推薦", "⭐"), ("精省首選", "💰"), ("均衡美味", "👍")]
    plans: List[Plan] = []

    for plan, (tag, icon) in zip(raw_plans, tags):
        meal_map = {"早餐": [], "午餐": [], "晚餐": []}
        for meal in plan["menu"]:
            meal_map[meal["meal"]].extend(meal["items"])

        categories = set(plan.get("diversity", []))
        plans.append(
            {
                "breakfast": meal_map["早餐"],
                "lunch": meal_map["午餐"],
                "dinner": meal_map["晚餐"],
                "totalCal": int(plan["total_cal"]),
                "totalPrice": int(plan["total_cost"]),
                "budgetLevel": budget_level(plan["total_cost"]),
                "missingCategories": [c for c in FOOD_GROUPS if c not in categories],
                "tag": tag,
                "tagIcon": icon,
            }
        )
    return plans


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
                    <div class="fp-badge">FitPocket · Earth Tone</div>
                    <h1 style="margin:12px 0 10px; font-size:32px; font-weight:900; letter-spacing:-0.4px; color: var(--brand-text); line-height:1.2;">
                        美味、均衡、剛剛好 —— 7-ELEVEN 一日三餐精選
                    </h1>
                    <p style="margin:6px 0 0; color: var(--brand-muted); font-size:15px; font-weight:700; line-height:1.6;">
                        依你的 BMR / TDEE 與預算，秒產最多三套餐單，讓營養與荷包同時兼顧。
                    </p>
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:14px;">
                        <span class="fp-pill">大地色系介面</span>
                        <span class="fp-pill">營養師級邏輯</span>
                        <span class="fp-pill">隨時調整預算</span>
                    </div>
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



def render_metric_cards(bmr: float, tdee: float, tier: int, activity_label: str) -> None:
    """Display BMR/TDEE/recommendation summary cards."""
    st.markdown(
        f"""
        <div class="fp-card" style="margin-top:18px; background:linear-gradient(120deg, rgba(247,241,232,0.7), #fff);">
            <div style="display:flex; gap:16px; flex-wrap:wrap;">
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(216,116,76,0.12), #fff);">
                    <div class="fp-pill">BMR</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{bmr:.0f} kcal / 天</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">Harris-Benedict 公式估算</div>
                </div>
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(110,139,61,0.12), #fff);">
                    <div class="fp-pill">TDEE</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{tdee:.0f} kcal / 天</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">活動係數：{activity_label}</div>
                </div>
                <div class="fp-card" style="flex:1; min-width:220px; background:linear-gradient(150deg, rgba(242,197,124,0.16), #fff);">
                    <div class="fp-pill">建議目標</div>
                    <div style="font-size:26px; font-weight:900; margin-top:6px;">{tier} kcal / 天</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">以熱量級距協助找餐單</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_meal_block(title: str, items: List[MealItem]) -> None:
    st.markdown(f"<div class='fp-section-title'>{title}</div>", unsafe_allow_html=True)
    st.caption(
        f"總熱量 {sum(i['cal'] for i in items)} kcal · 合作通路：7-ELEVEN · 共 {len(items)} 道餐點"
    )
    for item in items:
        cats = "、".join(item["cats"])
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
                        <span>·</span>
                        <span>{cats}</span>
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
    """Header bar for each plan tab."""
    stats_html = "".join(
        [
            render_stat_chip(f"總熱量 {plan['totalCal']} kcal"),
            render_stat_chip(f"總花費 NT${plan['totalPrice']}"),
            render_stat_chip(f"預算 {plan['budgetLevel']}"),
        ]
    )
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div class="fp-logo-icon" style="width:34px; height:34px; box-shadow:none;">
                    <span style="position:relative; z-index:1; font-size:16px;">{plan['tagIcon']}</span>
                </div>
                <div>
                    <div style="font-weight:900; color:var(--brand-text);">{label}</div>
                    <div style="color:var(--brand-muted); font-weight:700; font-size:12px;">{plan['tag']} · {plan['budgetLevel']}</div>
                </div>
            </div>
            <div style="display:flex; gap:12px; flex-wrap:wrap;">
                {stats_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


render_hero()


with st.form("user_input"):
    st.markdown('<div class="fp-card">', unsafe_allow_html=True)
    st.markdown('<div class="fp-section-title">你的基礎資料</div>', unsafe_allow_html=True)
    st.caption("輸入身體資訊與活動量，系統將計算 BMR / TDEE 並生成最多 3 套餐單。")
    col1, col2, col3 = st.columns([1.2, 1.2, 1])
    with col1:
        gender = st.radio("生理性別", ["male", "female"], format_func=lambda v: "男性" if v == "male" else "女性")
        age = st.number_input("年齡", min_value=15, max_value=80, value=25, step=1)
    with col2:
        height = st.number_input("身高（公分）", min_value=130, max_value=220, value=170, step=1)
        weight = st.number_input("體重（公斤）", min_value=30.0, max_value=200.0, value=65.0, step=0.5)
    with col3:
        budget_type = st.radio("預算偏好", ["低預算", "中預算", "高預算"], horizontal=True)
        activity = st.selectbox(
            "日常活動量",
            options=[
                ("sedentary", "久坐 / 辦公室 (×1.2)"),
                ("light", "輕度活動：每週運動 1-3 天 (×1.375)"),
                ("moderate", "中度活動：每週運動 3-5 天 (×1.55)"),
                ("active", "高度活動：每週運動 6-7 天 (×1.725)"),
                ("very_active", "超高活動：勞力工作或重度訓練 (×1.9)"),
            ],
            format_func=lambda t: t[1],
        )
    submitted = st.form_submit_button("計算並生成餐單方案", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


if submitted:
    bmr = calculate_bmr(gender, age, height, weight)
    tdee = bmr * get_activity_multiplier(activity[0])
    tier = get_closest_tier(tdee)
    plans = build_plans(tier, budget_type)
    if not plans:
        st.error("目前無法生成餐單，請確認資料是否完整。")
        st.stop()

    render_metric_cards(bmr, tdee, tier, activity[1])

    labels = [f"方案{chr(65 + i)}" for i in range(len(plans))]
    tab_titles = labels
    tabs = st.tabs(tab_titles)

    for tab, label, plan in zip(tabs, labels, plans):
        with tab:
            st.markdown('<div class="fp-card">', unsafe_allow_html=True)
            render_plan_header(plan, label)

            if plan["missingCategories"]:
                st.warning("缺少的食物類別：" + "、".join(plan["missingCategories"]))
            else:
                st.success("已涵蓋六大食物類別 ✅")

            st.divider()
            render_meal_block("早餐", plan["breakfast"])
            render_meal_block("午餐", plan["lunch"])
            render_meal_block("晚餐", plan["dinner"])
            st.markdown("</div>", unsafe_allow_html=True)
