import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Dashboard งบประมาณ", layout="wide")

# (ตัวอย่าง CSS สำหรับรองรับภาษาไทย)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun&display=swap');
html, body, [class*="css"] {
    font-family: 'Sarabun', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ✅ เมนู Slide Bar
selected_menus = st.sidebar.multiselect("📌 เลือกหัวข้อ Dashboard", [
    "1️⃣ ภาพรวมทั้งประเทศ/กระทรวงหรือเทียบเท่ากระทรวง",
    "2️⃣ หน่วยงาน (แยกตามกระทรวง)",
    "3️⃣ งบกลาง",
    "4️⃣ แผนบูรณาการ",
    "5️⃣ จังหวัดและกลุ่มจังหวัด",
    "6️⃣ หน่วยงานของรัฐสภา",
    "7️⃣ ผลผลิต/โครงการ (ค้นหาชื่อ)",
    "8️⃣ ผลผลิต/โครงการ (ติดตามรายหน่วยงาน)",
    "9️⃣ ลักษณะงาน"  # 
])



# โหลดข้อมูล
@st.cache_data
def load_data():
    file_path = "q2-69 Feb.xlsx"
    df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
    num_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')
    df["พรบ."] = df["พรบ."] / 1_000_000
    df["งบฯ หลังโอน"] = df["งบฯ หลังโอน"] / 1_000_000
    df["เบิกจ่าย"] = df["เบิกจ่าย"] / 1_000_000
    df["ใช้จ่าย"] = df["ใช้จ่าย"] / 1_000_000
    return df

df = load_data()
if df.empty:
    st.error("❌ ไม่พบข้อมูลในไฟล์ Excel")
    st.stop()

# ส่วนหัว (ใช้สีที่ดูดีทั้ง dark และ light mode)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }
    .header-main {
        background-color: #AC1B1F;
        color: white;
        text-align: center;
        padding: 1rem;
        font-size: 30px;
        font-weight: 700;
        border-radius: 6px;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .header-sub {
        text-align: center;
        color: #AC1B1F;
        font-weight: 600;
        font-size: 25px;
        margin-bottom: 1.5rem;
    }
    .metric-label {
        font-size: 16px;
        color: gray;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 600;
    }
    </style>
    <div class='header-main'>ผลการเบิกจ่ายงบประมาณและการใช้จ่ายภาครัฐ ณ สิ้นสุดเดือนกุมภาพันธ์ ปีงบประมาณ พ.ศ. 2569</div>
""", unsafe_allow_html=True)
#-----------------------------


st.markdown(
    """
    <div style="text-align: right;">
        <a href="https://docs.google.com/forms/d/1Kt45668xXpCx07o_k_VuSK3uG7YejpQfyKhNIuOry8M/edit" target="_blank">
            <div style="display:inline-block; padding:0.3em 1em; background-color:#4CAF50; color:white; border-radius:8px; text-decoration:none; font-weight:normal;">
                คลิก เพื่อให้ความเห็นต่อการปรับปรุงระบบฯ
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
 🔵 หมายเหตุประกอบการอ่านข้อมูล
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
1. ข้อมูลผลการเบิกจ่ายงบประมาณและการใช้จ่ายของรัฐ จากระบบ New GFMIS Thai กรมบัญชีกลาง | แสดงข้อมูล ณ ตั้งแต่ต้นปี งปม. ถึงสิ้นเดือนกุมภาพันธ์ ปี งปม. 2569 | เรียกข้อมูล ณ วันที่ 9 มีนาคม 2569
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
2. เบิกจ่าย คือ มูลค่าการเบิกจ่ายทั้งสิ้นที่ส่วนราชการเบิกจ่ายเองและส่วนราชการอื่นเบิกแทนให้ 
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
3. ใช้จ่าย คือ มูลค่าการเบิกจ่ายทั้งสิ้น รวม PO รวมสำรองเงินแบบมีหนี้ (เบิกจ่าย+PO+สำรองเงินแบบมีหนี้)
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
4. สีของค่า %เบิกจ่าย และ %ใช้จ่าย ประกอบด้วย "สีแดง" หมายถึง ต่ำกว่าเป้าหมาย และ "สีเขียว" หมายถึง เกินกว่าเป้าหมาย
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# ส่วนหัวข้อความ
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
 🔵 มาตรการเร่งรัดการเบิกจ่ายงบประมาณและการใช้จ่ายภาครัฐ ประจำปีงบประมาณ พ.ศ. 2569 (ค่าเป้าหมาย)
</div>
""", unsafe_allow_html=True)

html_table = """
<style>
table {
    border-collapse: collapse;
    width: 100%;
    font-size: 16px;
    margin: auto;
    text-align: center;
}
th, td {
    border: 1px solid black;
    padding: 8px;
    vertical-align: middle;
}
.green-text {
    color: green;
    font-weight: bold;
}
</style>

<table>
    <tr>
        <th>รายการ</th>
        <th>ต.ค.-68</th><th>พ.ย.-68</th><th>ธ.ค.-68</th>
        <th>ม.ค.-69</th><th class="green-text">ก.พ.-69</th><th>มี.ค.-69</th>
        <th>เม.ย.-69</th><th>พ.ค.-69</th><th>มิ.ย.-69</th>
        <th>ก.ค.-69</th><th>ส.ค.-69</th><th>ก.ย.-69</th>
    </tr>
    <tr>
        <td>ภาพรวม_เบิกจ่าย</td>
        <td>11.00</td><td>22.00</td><td >33.00</td>
        <td>40.33</td><td class="green-text">47.66</td><td>55.00</td>
        <td>62.00</td><td>69.00</td><td>76.00</td>
        <td>81.67</td><td>87.34</td><td>93.00</td>
    </tr>
    <tr>
        <td>ภาพรวม_ใช้จ่าย</td>
        <td>12.67</td><td>25.34</td><td>38.00</td>
        <td>45.67</td><td class="green-text">53.34</td><td>61.00</td>
        <td>67.67</td><td>74.34</td><td>81.00</td>
        <td>87.33</td><td>93.66</td><td>100.00</td>
    </tr>
    <tr>
        <td>ประจำ_เบิกจ่าย</td>
        <td>12.33</td><td>24.66</td><td>37.00</td>
        <td>44.67</td><td class="green-text">52.34</td><td>60.00</td>
        <td>67.67</td><td>75.34</td><td>83.00</td>
        <td>88.00</td><td>93.00</td><td>98.00</td>
    </tr>
    <tr>
        <td>ประจำ_ใช้จ่าย</td>
        <td>12.67</td><td>25.34</td><td>38.00</td>
        <td>45.67</td><td class="green-text">53.34</td><td>61.00</td>
        <td>68.67</td><td>76.34</td><td>84.00</td>
        <td>89.33</td><td>94.66</td><td>100.00</td>
    </tr>
    <tr>
        <td>ลงทุน_เบิกจ่าย</td>
        <td>6.67</td><td>13.34</td><td>20.00</td>
        <td>26.00</td><td class="green-text">32.00</td><td>38.00</td>
        <td>43.67</td><td>49.34</td><td>55.00</td>
        <td>61.67</td><td>68.34</td><td>75.00</td>
    </tr>
    <tr>
        <td>ลงทุน_ใช้จ่าย</td>
        <td>112.00</td><td>24.00</td><td>36.00</td>
        <td>43.67</td><td class="green-text">51.34</td><td>59.00</td>
        <td>62.33</td><td>65.66</td><td>69.00</td>
        <td>79.33</td><td>89.66</td><td>100.00</td>
    </tr>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
ที่มา: หนังสือสำนักเลขาธิการคณะรัฐมนตรี ด่วนที่สุด นร 0505/ว 426 ลงวันที่ 24 ตุลาคม 2568
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
หมายเหตุ: ค่าเป้าหมายรายเดือน คำนวณจากค่าเป้าหมายรายไตรมาส
</div>
""", unsafe_allow_html=True)

#--------------------------*************--------------------------
st.markdown("<br>", unsafe_allow_html=True)
import streamlit as st

st.markdown("""
<style>
.blink {
  animation: blinker 1s linear infinite;
}
@keyframes blinker {
  50% { opacity: 0; }
}
</style>

<div style='text-align: left; font-size: 24px; font-weight: bold; margin-bottom: 10px; color: red;'>
  <span class="blink">⬅ </span>กรุณาเลือกหัวข้อจากแท็บด้านซ้าย
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: bold; margin-bottom: 12px;'>
⚙️ ตั้งค่าสีพื้นหลังจอแสดงผล
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
1. คลิกที่จุดสามจุดมุมบนขวา&nbsp;&nbsp;&nbsp;|&nbsp; 2. เลือก "Settings"&nbsp;&nbsp;&nbsp;|&nbsp; 3. เลือก "Choose app theme, colors and fronts"&nbsp;&nbsp;&nbsp;หรือตั้งค่าสีเองโดยเลือก "Edit active theme"
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

#--------------------------------------------------------------
# 🔧 ฟังก์ชันคำนวณภาพรวม
def compute_summary(df):
    total_prb = round(df["พรบ."].sum(), 4)
    total_after = round(df["งบฯ หลังโอน"].sum(), 4)
    total_disb = round(df["เบิกจ่าย"].sum(), 4)
    total_spend = round(df["ใช้จ่าย"].sum(), 4)
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
    return total_prb, total_after, total_disb, percent_disb, total_spend, percent_spend

# 🔧 ฟังก์ชันแสดงผล metric พร้อมเงื่อนไขสีแยกตามกลุ่ม
def show_metrics(data, title):
    prb, after, disb, per_disb, spend, per_spend = data
    st.markdown(f"### {title}")
    col1, col2, col3 = st.columns(3)

    # ✅ เกณฑ์สีตามกลุ่ม 🟥🟥🟥
    if title == "📊 ภาพรวม":
        disb_threshold = 47.66
        spend_threshold = 53.34
    elif title == "🏢 รายจ่ายประจำ":
        disb_threshold = 52.34
        spend_threshold = 53.34
    elif title == "🏗️ รายจ่ายลงทุน":
        disb_threshold = 32.00
        spend_threshold = 51.34
    else:
        disb_threshold = spend_threshold = 0

    def small_metric(label, value, is_percent=False, threshold=None):
        formatted = f"{value:,.2f}%" if is_percent else f"{value:,.4f}"
        color = (
            "#00FF9F" if is_percent and value >= threshold
            else "#FF4B4B" if is_percent
            else "inherit"
        )
        return f"""
            <div style='margin-bottom: 0.75rem;'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value' style='color: {color};'>{formatted}</div>
            </div>
        """

    with col1:
        st.markdown(small_metric("พ.ร.บ.", prb), unsafe_allow_html=True)
        st.markdown(small_metric("งบฯ หลังโอน", after), unsafe_allow_html=True)
    with col2:
        st.markdown(small_metric("เบิกจ่าย", disb), unsafe_allow_html=True)
        st.markdown(small_metric("%เบิกจ่าย", per_disb, is_percent=True, threshold=disb_threshold), unsafe_allow_html=True)
    with col3:
        st.markdown(small_metric("ใช้จ่าย", spend), unsafe_allow_html=True)
        st.markdown(small_metric("%ใช้จ่าย", per_spend, is_percent=True, threshold=spend_threshold), unsafe_allow_html=True)

#-----*********************************************************

# 🔧 ฟังก์ชันจัดการตารางพร้อมไฮไลต์
def prepare_table(df_part, category="ภาพรวม"):
    df_part = df_part.groupby("หน่วยงาน")[["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]].sum().reset_index()
    df_part["%เบิกจ่าย"] = (df_part["เบิกจ่าย"] / df_part["งบฯ หลังโอน"]) * 100
    df_part["%ใช้จ่าย"] = (df_part["ใช้จ่าย"] / df_part["งบฯ หลังโอน"]) * 100
    cols = ["หน่วยงาน", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
    df_part = df_part[cols]

    def highlight(row):
        color_disb = get_color(row["%เบิกจ่าย"], category, "เบิกจ่าย")
        color_spend = get_color(row["%ใช้จ่าย"], category, "ใช้จ่าย")
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    styled_df = df_part.style.format({
        "พรบ.": "{:,.4f}",
        "งบฯ หลังโอน": "{:,.4f}",
        "เบิกจ่าย": "{:,.4f}",
        "ใช้จ่าย": "{:,.4f}",
        "%เบิกจ่าย": "{:,.2f}%",
        "%ใช้จ่าย": "{:,.2f}%"
    }).apply(highlight, axis=1)

    return styled_df


# 🔧 ฟังก์ชันสรุปค่าตาม DataFrame
def compute_summary(df):
    total_prb = df["พรบ."].sum()
    total_after = df["งบฯ หลังโอน"].sum()
    total_disb = df["เบิกจ่าย"].sum()
    total_spend = df["ใช้จ่าย"].sum()
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
    return total_prb, total_after, total_disb, percent_disb, total_spend, percent_spend

#---------------------------------------------------------------------------
# 🔧 ฟังก์ชันกำหนดสีตามประเภทรายจ่าย 🟥🟥🟥
def get_color(value, category, target_type):
    """
    category: 'ภาพรวม', 'รายจ่ายประจำ', 'รายจ่ายลงทุน'
    target_type: 'เบิกจ่าย' หรือ 'ใช้จ่าย'
    """
    thresholds = {
        "ภาพรวม": {"เบิกจ่าย": 47.66, "ใช้จ่าย": 53.34},
        "รายจ่ายประจำ": {"เบิกจ่าย": 52.34, "ใช้จ่าย": 53.34},
        "รายจ่ายลงทุน": {"เบิกจ่าย": 32.00, "ใช้จ่าย": 51.34},
    }
    threshold = thresholds.get(category, {}).get(target_type, 0)
    return "#00FF9F" if value >= threshold else "#FF4B4B"
 
# 🔹 ฟังก์ชันแสดงตารางรายกระทรวง
def show_ministry_table(df_subset, title, category):
    if df_subset.empty:
        st.info(f"ไม่มีข้อมูลสำหรับ {title}")
        return

    df_grouped = df_subset.groupby("กระทรวง", as_index=False)[
        ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
    ].sum(numeric_only=True)

    df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
    df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

    display_cols = ["กระทรวง", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

    # ✅ ใส่สีตาม threshold
    def highlight(row):
        c1 = get_color(row["%เบิกจ่าย"], category, "เบิกจ่าย")
        c2 = get_color(row["%ใช้จ่าย"], category, "ใช้จ่าย")
        return ["", "", "", "", f"color:{c1}", "", f"color:{c2}"]

    styled = df_grouped[display_cols].style.format({
        "พรบ.": "{:,.4f}",
        "งบฯ หลังโอน": "{:,.4f}",
        "เบิกจ่าย": "{:,.4f}",
        "ใช้จ่าย": "{:,.4f}",
        "%เบิกจ่าย": "{:,.2f}%",
        "%ใช้จ่าย": "{:,.2f}%"
    }).apply(highlight, axis=1)

    st.markdown(f"### {title}")
    st.dataframe(styled, use_container_width=True)

#-----*********************************************************
# ✅ ส่วนแสดงผลตามเมนู
if "1️⃣ ภาพรวมทั้งประเทศ/กระทรวงหรือเทียบเท่ากระทรวง" in selected_menus:
    st.markdown("## 1️⃣ภาพรวมทั้งประเทศ")

    # สรุปภาพรวม
    total_all = compute_summary(df)
    total_regular = compute_summary(df[df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"])
    total_invest = compute_summary(df[df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"])

    # แสดง Metric
    show_metrics(total_all, "📊 ภาพรวม")
    show_metrics(total_regular, "🏢 รายจ่ายประจำ")
    show_metrics(total_invest, "🏗️ รายจ่ายลงทุน")
    st.markdown("<br>", unsafe_allow_html=True)

    
    # ----- แสดงหัวข้อ -----
    st.markdown("## 🔵ติดตามผลการเบิกจ่ายและใช้จ่ายงบประมาณรายจ่ายลงทุน")

    # ======================== 🔢 รวมยอดงบประมาณ ======================== #
    total_prb    = float(df["พรบ."].sum() or 0.0)                                # รวมงบประมาณ พ.ร.บ.
    total_trans  = float(df["งบฯ หลังโอน"].sum() or 0.0)                         # รวมงบฯ หลังโอน
    total_invest = float(
        df.loc[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน", "พรบ."].sum() or 0.0
    )                                                                             # รวมงบลงทุน

    # รวมยอดเบิกจ่ายและใช้จ่าย เฉพาะหมวดลงทุน
    total_invest_disb = float(
        df.loc[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน", "เบิกจ่าย"].sum() or 0.0
    )
    total_invest_spend = float(
        df.loc[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน", "ใช้จ่าย"].sum() or 0.0
    )

    # ======================== 🎯 ปัดเศษสำหรับแสดงผล ======================== #
    total_prb_disp          = round(total_prb, 4)
    total_trans_disp        = round(total_trans, 4)
    total_invest_disp       = round(total_invest, 4)
    total_invest_disb_disp  = round(total_invest_disb, 4)
    total_invest_spend_disp = round(total_invest_spend, 4)

    # ======================== 📊 คำนวณสัดส่วน (%) ======================== #
    ratio_invest_disb_prb    = round((total_invest_disb  / total_prb)   * 100, 2) if total_prb   else 0.0
    ratio_invest_disb_trans  = round((total_invest_disb  / total_trans) * 100, 2) if total_trans else 0.0
    ratio_invest_spend_prb   = round((total_invest_spend / total_prb)   * 100, 2) if total_prb   else 0.0
    ratio_invest_spend_trans = round((total_invest_spend / total_trans) * 100, 2) if total_trans else 0.0
    ratio_invest_prb         = round((total_invest       / total_prb)   * 100, 2) if total_prb   else 0.0
    
        # ======================== 📝 ข้อความสรุป (Custom Font Size) ======================== #
    st.markdown("""
    <style>
      .summary-text {
        font-size:18px;        /* ขนาดฟอนต์ใหญ่ขึ้น */
        line-height:1.7;       /* ระยะบรรทัดอ่านง่าย */
      }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="summary-text">
        ในปีงบประมาณ พ.ศ. 2569 มีการจัดสรรงบประมาณรวมทั้งสิ้น {total_prb_disp:,.4f} ล้านบาท 
        มีงบประมาณหลังโอนเปลี่ยนแปลงทั้งสิ้น {total_trans_disp:,.4f} ล้านบาท
        มีงบประมาณรายจ่ายลงทุนรวมทั้งสิ้น {total_invest_disp:,.4f} ล้านบาท
        คิดเป็น {ratio_invest_prb:,.2f}% ของงบประมาณรายจ่ายทั้งสิ้น ซึ่งเป็นไปตามมาตรา 20 (1) แห่งพระราชบัญญัติวินัยการเงินการคลังของรัฐ พ.ศ. 2561
        ที่กำหนดให้รัฐบาลตั้งงบประมาณรายจ่ายลงทุนไม่น้อยกว่าร้อยละ 20
        โดยมีผลการเบิกจ่ายและใช้จ่ายดังนี้
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================== 📑 สร้างตาราง 3 แถว x 2 คอลัมน์ ======================== #
    import pandas as pd

    display_df = pd.DataFrame(
        {
            "ผลการเบิกจ่าย": [
                f"{total_invest_disb:,.4f}",
                f"{ratio_invest_disb_prb:.2f}%",
                f"{ratio_invest_disb_trans:.2f}%",
            ],
            "ผลการใช้จ่าย": [
                f"{total_invest_spend:,.4f}",
                f"{ratio_invest_spend_prb:.2f}%",
                f"{ratio_invest_spend_trans:.2f}%",
            ],
        },
        index=[
            "งบประมาณรายจ่ายลงทุน (ล้านบาท)",
            "% ต่อ พ.ร.บ.",
            "% ต่อ งบฯ หลังโอน",
        ],
    )

    # ใช้ st.table เพื่อการนำเสนอแบบคงที่ (ไม่เลื่อน/ไม่แก้ไข)
    #st.table(display_df)
    
    # ======================== 🌟 KPI CARDS (Large & Stylish) ======================== #
    # วาง CSS แค่ครั้งเดียวพอ (รองรับ Light/Dark)
    st.markdown("""
    <style>
      @media (prefers-color-scheme: light) {
        .kpi-card { background:#ffffff; color:#000; box-shadow:0 2px 6px rgba(0,0,0,0.08); }
      }
      @media (prefers-color-scheme: dark) {
        .kpi-card { background:#2b2b2b; color:#fff; box-shadow:0 2px 6px rgba(255,255,255,0.05); }
      }
      .kpi-card{
        padding:22px; border-radius:14px; border:1px solid rgba(128,128,128,.18);
        margin-bottom:16px; text-align:center;
      }
      .kpi-label{
        font-size:16px; font-weight:700; margin-bottom:8px; color:#8a8a8a;
        text-transform:uppercase; letter-spacing:.4px;
      }
      .kpi-value{ font-size:30px; font-weight:800; margin-bottom:10px; color:#00b4d8; }
      .kpi-sub{ font-size:15px; opacity:.95; }
    </style>
    """, unsafe_allow_html=True)

    # === การ์ด KPI: เบิกจ่าย / ใช้จ่าย (ลงทุน) ===
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class='kpi-card'>
              <div class='kpi-label'>เบิกจ่ายงบประมาณรายจ่ายลงทุน</div>
              <div class='kpi-value'>{total_invest_disb_disp:,.4f} ล้านบาท</div>
              <div class='kpi-sub'>
                % ต่อ พ.ร.บ.: <b>{ratio_invest_disb_prb:.2f}%</b> •
                % ต่อ งบฯ หลังโอน: <b>{ratio_invest_disb_trans:.2f}%</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(int(ratio_invest_disb_prb), 100))

    with c2:
        st.markdown(
            f"""
            <div class='kpi-card'>
              <div class='kpi-label'>ใช้จ่ายงบประมาณรายจ่ายลงทุน</div>
              <div class='kpi-value'>{total_invest_spend_disp:,.4f} ล้านบาท</div>
              <div class='kpi-sub'>
                % ต่อ พ.ร.บ.: <b>{ratio_invest_spend_prb:.2f}%</b> •
                % ต่อ งบฯ หลังโอน: <b>{ratio_invest_spend_trans:.2f}%</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(int(ratio_invest_spend_prb), 100))

    # ======================== 📝 ข้อความสรุป (Custom Font Size) ======================== #
    st.markdown("""
    <style>
      .summary-text {
        font-size:18px;        /* ขนาดฟอนต์ใหญ่ขึ้น */
        line-height:1.7;       /* ระยะบรรทัดอ่านง่าย */
      }

    </style>
    """, unsafe_allow_html=True)


    
    # 🔵 กระทรวง/เทียบเท่ากระทรวง
    st.markdown("## 🔵 กระทรวง/เทียบเท่ากระทรวง")

    # ======================== 🔵 ฟังก์ชันสรุปผล ======================== #
    def summarize_ministry_text(df_subset, disb_thres, spend_thres):
        group_cols = ["กระทรวง"]
        sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        df_grouped = df_subset.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        low_disb = df_grouped[df_grouped["%เบิกจ่าย"] < disb_thres]["กระทรวง"].tolist()
        low_spend = df_grouped[df_grouped["%ใช้จ่าย"] < spend_thres]["กระทรวง"].tolist()

        return len(df_grouped), len(low_disb), low_disb, len(low_spend), low_spend

    # 📊 ภาพรวม  🟥🟥🟥
    total_all, num_low_disb_all, low_disb_all, num_low_spend_all, low_spend_all = summarize_ministry_text(
        df, disb_thres=47.66, spend_thres=53.34
    )

    # 🏢 รายจ่ายประจำ 🟥🟥🟥
    df_regular = df[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    total_reg, num_low_disb_reg, low_disb_reg, num_low_spend_reg, low_spend_reg = summarize_ministry_text(
        df_regular, disb_thres=52.34, spend_thres=53.34
    )

    # 🏗️ รายจ่ายลงทุน  🟥🟥🟥
    df_invest = df[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
    total_inv, num_low_disb_inv, low_disb_inv, num_low_spend_inv, low_spend_inv = summarize_ministry_text(
        df_invest, disb_thres=32.00, spend_thres=51.34
    )

    # ======================== 🔵 แสดงผลสรุปเป็นข้อความ (รองรับ Dark/Light) ======================== #
    st.markdown("""
    <style>
    /* Light mode */
    @media (prefers-color-scheme: light) {
        .summary-box {
            background-color: #f9f9f9;
            color: #000000;
        }
        .recommend-box {
            background-color: #eaeaea;
            color: #000000;
        }
    }
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        .summary-box {
            background-color: #1E1E1E;
            color: #ffffff;
        }
        .recommend-box {
            background-color: #262626;
            color: #ffffff;
        }
    }
    .summary-box, .recommend-box {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======================== 🔵 หัวข้อหลัก ======================== #
    st.markdown(f"""
    <div style='font-size:22px; font-weight:bold; margin-bottom:15px;'>
    📊 สรุปผลการติดตามการเบิกจ่ายและการใช้จ่ายงบประมาณของรัฐ  
    จำนวน {total_all} กระทรวง/เทียบเท่ากระทรวง จำแนกตามประเภทงบประมาณรายจ่าย
    </div>
    """, unsafe_allow_html=True)

    # ---- Block 1: ภาพรวม ----
    st.markdown(f"""
    <div class='summary-box'>
        <h3>📊 ในภาพรวม</h3>
        <ul>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_disb_all}</b> กระทรวง</span> 
                ที่เบิกจ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_disb_all) if low_disb_all else "-"}</li>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_spend_all}</b> กระทรวง</span> 
                ที่ใช้จ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_spend_all) if low_spend_all else "-"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---- Block 2: รายจ่ายประจำ ----
    st.markdown(f"""
    <div class='summary-box'>
        <h3>🏢 รายจ่ายประจำ</h3>
        <ul>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_disb_reg}</b> กระทรวง</span> 
                ที่เบิกจ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_disb_reg) if low_disb_reg else "-"}</li>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_spend_reg}</b> กระทรวง</span> 
                ที่ใช้จ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_spend_reg) if low_spend_reg else "-"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---- Block 3: รายจ่ายลงทุน ----
    st.markdown(f"""
    <div class='summary-box'>
        <h3>🏗️ รายจ่ายลงทุน</h3>
        <ul>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_disb_inv}</b> กระทรวง</span> 
                ที่เบิกจ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_disb_inv) if low_disb_inv else "-"}</li>
            <li><span style='color:red;'>มีกระทรวงทั้งหมด <b>{num_low_spend_inv}</b> กระทรวง</span> 
                ที่ใช้จ่ายต่ำกว่าค่าเป้าหมาย ได้แก่ {", ".join(low_spend_inv) if low_spend_inv else "-"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---- Block 4: ข้อเสนอแนะ ----
    st.markdown("""
    <div class='recommend-box'>
        ✨ <b>ข้อเสนอแนะ:</b>  
        กระทรวง/เทียบเท่ากระทรวง ที่มีผลการเบิกจ่ายงบประมาณและมีผลการใช้จ่ายเงินของรัฐต่ำกว่าเป้าหมาย 
        ควรเร่งรัดให้มีการเบิกจ่ายและใช้จ่ายให้เป็นไปตามค่าเป้าหมายตามมาตรการฯ 
        เพื่อให้การใช้จ่ายงบประมาณเป็นไปตามวัตถุประสงค์ของการขอรับจัดสรรงบประมาณ 
        ทั้งในด้านการพัฒนาประเทศ การแก้ไขปัญหาความเดือดร้อนให้กับประชาชน และการยกระดับความเป็นอยู่ของประชาชน
    </div>
    """, unsafe_allow_html=True)


    # ✅ ปุ่ม Tab 3 ปุ่ม
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])
    with tab1:
        show_ministry_table(df, "📊 ภาพรวม", "ภาพรวม")

    with tab2:
        df_regular = df[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
        show_ministry_table(df_regular, "🏢 รายจ่ายประจำ", "รายจ่ายประจำ")

    with tab3:
        df_invest = df[df["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
        show_ministry_table(df_invest, "🏗️ รายจ่ายลงทุน", "รายจ่ายลงทุน")

#-----*********************************************************
#-----*********************************************************
# ✅ SECTION 2: กระทรวง/หน่วยงาน
if "2️⃣ หน่วยงาน (แยกตามกระทรวง)" in selected_menus:
    st.markdown("## 2️⃣ หน่วยงาน")

    # 🔹 Dropdown สำหรับเลือกกระทรวง
    ministry_list = df["กระทรวง"].dropna().unique()
    selected_ministry = st.selectbox("เลือกกระทรวง", sorted(ministry_list), key="ministry_section2")

    # 🔹 Filter ข้อมูล
    df_min = df[df["กระทรวง"] == selected_ministry]
    df_reg = df_min[df_min["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    df_inv = df_min[df_min["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

    # 🔹 สรุปภาพรวม
    total_all = compute_summary(df_min)
    total_regular = compute_summary(df_reg)
    total_invest = compute_summary(df_inv)

    prb, after, disb, per_disb, spend, per_spend = total_all
    color_disb = get_color(per_disb, "ภาพรวม", "เบิกจ่าย")
    color_spend = get_color(per_spend, "ภาพรวม", "ใช้จ่าย")

    # 📝 คำบรรยายด้านบน (อยู่นอก Tabs)
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ในภาพรวม **📍{selected_ministry}** ได้รับจัดสรรงบประมาณ **{prb:,.4f} ล้านบาท** มีงบประมาณหลังโอนเปลี่ยนแปลง **{after:,.4f} ล้านบาท**  มีการเบิกจ่าย **{disb:,.4f} ล้านบาท**  (<span style="color:{color_disb}; font-weight:bold;">{per_disb:.2f}%</span> ของงบฯ หลังโอน)  และมีการใช้จ่าย **{spend:,.4f} ล้านบาท**  (<span style="color:{color_spend}; font-weight:bold;">{per_spend:.2f}%</span> ของงบฯ หลังโอน) ทั้งนี้ สามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้
""", unsafe_allow_html=True)

    # 🔹 รายจ่ายประจำ
    if not df_reg.empty:
        prb_r, after_r, disb_r, per_disb_r, spend_r, per_spend_r = total_regular
        color_disb_r = get_color(per_disb_r, "รายจ่ายประจำ", "เบิกจ่าย")
        color_spend_r = get_color(per_spend_r, "รายจ่ายประจำ", "ใช้จ่าย")
        st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ **{prb_r:,.4f} ล้านบาท**  งบประมาณหลังโอนเปลี่ยนแปลง **{after_r:,.4f} ล้านบาท**  เบิกจ่าย **{disb_r:,.4f} ล้านบาท** (<span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span>)  ใช้จ่าย **{spend_r:,.4f} ล้านบาท** (<span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span>)
""", unsafe_allow_html=True)

    # 🔹 รายจ่ายลงทุน
    if not df_inv.empty:
        prb_i, after_i, disb_i, per_disb_i, spend_i, per_spend_i = total_invest
        color_disb_i = get_color(per_disb_i, "รายจ่ายลงทุน", "เบิกจ่าย")
        color_spend_i = get_color(per_spend_i, "รายจ่ายลงทุน", "ใช้จ่าย")
        st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **{prb_i:,.4f} ล้านบาท**  งบประมาณหลังโอนเปลี่ยนแปลง **{after_i:,.4f} ล้านบาท**  เบิกจ่าย **{disb_i:,.4f} ล้านบาท** (<span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span>)  ใช้จ่าย **{spend_i:,.4f} ล้านบาท** (<span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span>)
""", unsafe_allow_html=True)

    # 🔹 Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    with tab1:
        st.dataframe(prepare_table(df_min, category="ภาพรวม"), use_container_width=True)

    with tab2:
        if not df_reg.empty:
            st.dataframe(prepare_table(df_reg, category="รายจ่ายประจำ"), use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลสำหรับรายจ่ายประจำ")

    with tab3:
        if not df_inv.empty:
            st.dataframe(prepare_table(df_inv, category="รายจ่ายลงทุน"), use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลสำหรับรายจ่ายลงทุน")


#--------------------------------------------------------------
# ✅ SECTION 3: งบกลาง (รองรับ sidebar)
if "3️⃣ งบกลาง" in selected_menus:
    st.markdown("## 3️⃣ งบกลาง")

    # 🔹 Filter เฉพาะกระทรวง "งบกลาง"
    df_central = df[df["กระทรวง"] == "งบกลาง"].copy()

    # 🔹 ฟังก์ชันใส่สีในตาราง
    def highlight_central(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    # 🔹 ฟังก์ชันแสดงตารางและสรุปผล
    def show_central_table(df_subset, disb_thres, spend_thres):
        df_grouped = df_subset.groupby("ผลผลิต/โครงการ", as_index=False)[
            ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        ].sum(numeric_only=True)

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["ผลผลิต/โครงการ", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_central(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

        # 🔸 รวมยอด
        total_prb = df_grouped["พรบ."].sum()
        total_after = df_grouped["งบฯ หลังโอน"].sum()
        total_disb = df_grouped["เบิกจ่าย"].sum()
        total_spend = df_grouped["ใช้จ่าย"].sum()
        percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
        percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

        color_disb_text = "#00FF9F" if percent_disb >= disb_thres else "#FF4B4B"
        color_spend_text = "#00FF9F" if percent_spend >= spend_thres else "#FF4B4B"

        st.markdown(f"""
**รวมทั้งสิ้น** | พรบ.: **{total_prb:,.4f}** | หลังโอน: **{total_after:,.4f}** | 
เบิกจ่าย: **{total_disb:,.4f}** | <span style='color:{color_disb_text}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
ใช้จ่าย: **{total_spend:,.4f}** | <span style='color:{color_spend_text}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
""", unsafe_allow_html=True)

    # 🔹 Tabs สำหรับตาราง 🟥🟥🟥
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    with tab1:
        show_central_table(df_central, disb_thres=47.66, spend_thres=53.34)

    with tab2:
        df_central_reg = df_central[df_central["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
        if not df_central_reg.empty:
            show_central_table(df_central_reg, disb_thres=52.34, spend_thres=53.34)
        else:
            st.info("ไม่มีข้อมูลสำหรับรายจ่ายประจำ")

    with tab3:
        df_central_inv = df_central[df_central["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
        if not df_central_inv.empty:
            show_central_table(df_central_inv, disb_thres=32.00, spend_thres=51.34)
        else:
            st.info("ไม่มีข้อมูลสำหรับรายจ่ายลงทุน")

    st.markdown("<br>", unsafe_allow_html=True)


#--------------------------------------------------------------
# ✅ SECTION 4: แผนบูรณาการ
if "4️⃣ แผนบูรณาการ" in selected_menus:
    st.markdown("## 4️⃣ แผนบูรณาการ")

    # 🔹 Filter เฉพาะแผนงานบูรณาการ
    df_plan = df[df["กลุ่มแผนงาน"] == "แผนงานบูรณาการ"]
    df_reg = df_plan[df_plan["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    df_inv = df_plan[df_plan["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

    # 🔹 คำนวณภาพรวม 🟥🟥🟥
    total_prb = df_plan["พรบ."].sum()
    total_after = df_plan["งบฯ หลังโอน"].sum()
    total_disb = df_plan["เบิกจ่าย"].sum()
    total_spend = df_plan["ใช้จ่าย"].sum()
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
    color_disb = "#00FF9F" if percent_disb >= 47.66 else "#FF4B4B"
    color_spend = "#00FF9F" if percent_spend >= 53.34 else "#FF4B4B"

    # 🔹 ประจำ 🟥🟥🟥
    prb_r = df_reg["พรบ."].sum()
    after_r = df_reg["งบฯ หลังโอน"].sum()
    disb_r = df_reg["เบิกจ่าย"].sum()
    spend_r = df_reg["ใช้จ่าย"].sum()
    per_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
    per_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0
    color_disb_r = "#00FF9F" if per_disb_r >= 52.34 else "#FF4B4B"
    color_spend_r = "#00FF9F" if per_spend_r >= 53.34 else "#FF4B4B"

    # 🔹 ลงทุน 🟥🟥🟥
    prb_i = df_inv["พรบ."].sum()
    after_i = df_inv["งบฯ หลังโอน"].sum()
    disb_i = df_inv["เบิกจ่าย"].sum()
    spend_i = df_inv["ใช้จ่าย"].sum()
    per_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
    per_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0
    color_disb_i = "#00FF9F" if per_disb_i >= 32.00 else "#FF4B4B"
    color_spend_i = "#00FF9F" if per_spend_i >= 51.34 else "#FF4B4B"

    st.markdown("""<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>🔵 ภาพรวมทุกแผนงานบูรณาการ</div>""", unsafe_allow_html=True)

    st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ในปีงบประมาณ พ.ศ. 2568 มีการจัดสรรงบประมาณสำหรับ**📍แผนงานบูรณาการ รวมทั้งสิ้น {total_prb:,.4f} ล้านบาท** มีงบประมาณหลังโอนเปลี่ยนแปลง **จำนวน {total_after:,.4f} ล้านบาท**  โดยมีการเบิกจ่าย **จำนวน {total_disb:,.4f} ล้านบาท** (คิดเป็น <span style="color:{color_disb}; font-weight:bold;">{percent_disb:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย **จำนวน {total_spend:,.4f} ล้านบาท** (คิดเป็น <span style="color:{color_spend}; font-weight:bold;">{percent_spend:.2f}%</span> ของ งบฯ หลังโอน) ทั้งนี้ สามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้""", unsafe_allow_html=True)

    if not df_reg.empty:
        st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ จำนวน **{prb_r:,.4f}** ล้านบาท มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_r:,.4f}** ล้านบาท โดยมีการเบิกจ่าย  **{disb_r:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย จำนวน **{spend_r:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span> ของ งบฯ หลังโอน)""", unsafe_allow_html=True)

    if not df_inv.empty:
        st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **{prb_i:,.4f}** ล้านบาท มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_i:,.4f}** ล้านบาท โดยมีการเบิกจ่าย จำนวน **{disb_i:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย จำนวน **{spend_i:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span> ของ งบฯ หลังโอน)""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================== ตาราง: แผนงานบูรณาการ ======================== #
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """<div style='text-align: left; font-size: 18px; font-weight: bold; margin: 10px 0;'>
        🔵 สรุปผลการเบิกจ่ายและใช้จ่ายงบประมาณแยกรายแผนงานบูรณาการ
        </div>""",
        unsafe_allow_html=True
    )

    # ---------- Tabs ----------
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    # ---------- ฟังก์ชันคำนวณตาราง ----------
    def build_plan_table(df_src, disb_th, spend_th):
        g = (
            df_src.groupby("แผนงาน", as_index=False)
            [["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]]
            .sum(numeric_only=True)
        )
        g["%เบิกจ่าย"] = round((g["เบิกจ่าย"] / g["งบฯ หลังโอน"]) * 100, 2)
        g["%ใช้จ่าย"] = round((g["ใช้จ่าย"] / g["งบฯ หลังโอน"]) * 100, 2)

        def _style(row):
            return [
                "",
                "",
                "",
                "",
                f"color:#00FF9F;" if row["%เบิกจ่าย"] >= disb_th else "color:#FF4B4B;",
                "",
                f"color:#00FF9F;" if row["%ใช้จ่าย"] >= spend_th else "color:#FF4B4B;",
            ]

        return (
            g[["แผนงาน","พรบ.","งบฯ หลังโอน","เบิกจ่าย","%เบิกจ่าย","ใช้จ่าย","%ใช้จ่าย"]]
            .style
            .format({
                "พรบ.":"{:,.4f}",
                "งบฯ หลังโอน":"{:,.4f}",
                "เบิกจ่าย":"{:,.4f}",
                "ใช้จ่าย":"{:,.4f}",
                "%เบิกจ่าย":"{:,.2f}%",
                "%ใช้จ่าย":"{:,.2f}%"
            })
            .apply(_style, axis=1)
        )

    # ================= TAB 1 : ภาพรวม =================🟥🟥🟥
    with tab1:
        st.dataframe(
            build_plan_table(df_plan, 47.66, 53.34),
            use_container_width=True
        )

    # ================= TAB 2 : รายจ่ายประจำ =================🟥🟥🟥
    with tab2:
        if not df_reg.empty:
            st.dataframe(
                build_plan_table(df_reg, 52.34, 53.34),
                use_container_width=True
            )
        else:
            st.info("ไม่มีข้อมูลรายจ่ายประจำ")

    # ================= TAB 3 : รายจ่ายลงทุน =================🟥🟥🟥
    with tab3:
        if not df_inv.empty:
            st.dataframe(
                build_plan_table(df_inv, 32.00, 51.34),
                use_container_width=True
            )
        else:
            st.info("ไม่มีข้อมูลรายจ่ายลงทุน")


    
    #--------------------------- แผนงานย่อย ---------------------------#
    st.markdown("""<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>🔵 แยกตามรายแผนงานบูรณาการ</div>""", unsafe_allow_html=True)

    df_plan = df[df["กลุ่มแผนงาน"] == "แผนงานบูรณาการ"].copy()
    plan_options = df_plan["แผนงาน"].dropna().unique()
    selected_plan = st.selectbox("🔍เลือกแผนงาน", sorted(plan_options))

    df_plan_selected = df_plan[df_plan["แผนงาน"] == selected_plan]
    df_plan_reg = df_plan_selected[df_plan_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    df_plan_inv = df_plan_selected[df_plan_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

    def highlight_plan(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    def show_plan_table(df_subset, title, disb_thres, spend_thres):
        group_cols = ["หน่วยงาน"]
        sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        df_grouped = df_subset.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)
        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        display_cols = ["หน่วยงาน", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_plan(row, disb_thres, spend_thres), axis=1)
        st.markdown(f"### {title}")
        st.dataframe(styled, use_container_width=True)

    # คำนวณรวม 🟥🟥🟥
    total_prb = df_plan_selected["พรบ."].sum()
    total_after = df_plan_selected["งบฯ หลังโอน"].sum()
    total_disb = df_plan_selected["เบิกจ่าย"].sum()
    total_spend = df_plan_selected["ใช้จ่าย"].sum()
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
    color_disb = "#00FF9F" if percent_disb >= 47.66 else "#FF4B4B"
    color_spend = "#00FF9F" if percent_spend >= 53.34 else "#FF4B4B"

    st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; มีการจัดสรรงบประมาณสำหรับ**📝{selected_plan}**  จำนวน **{total_prb:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{total_after:,.4f} ล้านบาท**  มีการเบิกจ่าย จำนวน **{total_disb:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb}; font-weight:bold;">{percent_disb:.2f}%</span> ของ งบฯ หลังโอน)  และมีการใช้จ่าย จำนวน **{total_spend:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend}; font-weight:bold;">{percent_spend:.2f}%</span> ของ งบฯ หลังโอน) ทั้งนี้ สามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้""", unsafe_allow_html=True)
    # รายจ่ายประจำ 🟥🟥🟥
    if not df_plan_reg.empty:
        prb_r = df_plan_reg["พรบ."].sum()
        after_r = df_plan_reg["งบฯ หลังโอน"].sum()
        disb_r = df_plan_reg["เบิกจ่าย"].sum()
        spend_r = df_plan_reg["ใช้จ่าย"].sum()
        per_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
        per_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0
        color_disb_r = "#00FF9F" if per_disb_r >= 52.34 else "#FF4B4B"
        color_spend_r = "#00FF9F" if per_spend_r >= 53.34 else "#FF4B4B"
        st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ **{prb_r:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_r:,.4f} ล้านบาท**  เบิกจ่าย **{disb_r:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span> ของ งบฯ หลังโอน)  ใช้จ่าย **{spend_r:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span> ของ งบฯ หลังโอน)""", unsafe_allow_html=True)

    # รายจ่ายลงทุน 🟥🟥🟥
    if not df_plan_inv.empty:
        prb_i = df_plan_inv["พรบ."].sum()
        after_i = df_plan_inv["งบฯ หลังโอน"].sum()
        disb_i = df_plan_inv["เบิกจ่าย"].sum()
        spend_i = df_plan_inv["ใช้จ่าย"].sum()
        per_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
        per_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0
        color_disb_i = "#00FF9F" if per_disb_i >= 32.00 else "#FF4B4B"
        color_spend_i = "#00FF9F" if per_spend_i >= 51.34 else "#FF4B4B"
        st.markdown(f"""&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **{prb_i:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_i:,.4f} ล้านบาท**  เบิกจ่าย **{disb_i:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span> ของ งบฯ หลังโอน)  ใช้จ่าย **{spend_i:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span> ของ งบฯ หลังโอน)""", unsafe_allow_html=True)

    # ✅ Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    # ฟังก์ชันแสดงตาราง
    def show_plan_table(df_subset, disb_thres, spend_thres):
        group_cols = ["หน่วยงาน"]
        sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        df_grouped = df_subset.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)
        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["หน่วยงาน", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_plan(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

    # 📊 Tab 1: ภาพรวม 🟥🟥🟥
    with tab1:
        show_plan_table(df_plan_selected, disb_thres=47.66, spend_thres=53.34)

    # 🏢 Tab 2: รายจ่ายประจำ 🟥🟥🟥
    with tab2:
        if not df_plan_reg.empty:
            show_plan_table(df_plan_reg, disb_thres=52.34, spend_thres=53.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายประจำ")

    # 🏗️ Tab 3: รายจ่ายลงทุน 🟥🟥🟥
    with tab3:
        if not df_plan_inv.empty:
            show_plan_table(df_plan_inv, disb_thres=32.00, spend_thres=51.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายลงทุน")

#--------------------------------------------------------------

# ✅ SECTION 5: จังหวัดและกลุ่มจังหวัด (รองรับ sidebar)
if "5️⃣ จังหวัดและกลุ่มจังหวัด" in selected_menus:
    st.markdown("## 5️⃣ จังหวัดและกลุ่มจังหวัด")

    # 🔹 Dropdown 1: จังหวัด/กลุ่มจังหวัด
    province_options = df["จังหวัด/กลุ่มจังหวัด"].dropna().unique()
    selected_province = st.selectbox("🔍เลือกจังหวัด/กลุ่มจังหวัด", sorted(province_options))

    # 🔹 Filter ตามจังหวัด
    df_province = df[df["จังหวัด/กลุ่มจังหวัด"] == selected_province]

    # 🔹 Dropdown 2: หน่วยงาน
    agency_options = df_province["หน่วยงาน"].dropna().unique()
    selected_agency = st.selectbox("🔍เลือกหน่วยงาน", sorted(agency_options))

    # 🔹 Filter ตามหน่วยงาน
    df_agency = df_province[df_province["หน่วยงาน"] == selected_agency]

    # 🔹 Dropdown 3: ผลผลิต/โครงการ
    project_options = df_agency["ผลผลิต/โครงการ"].dropna().unique()
    selected_project = st.selectbox("🔍เลือกผลผลิต/โครงการ", sorted(project_options))

    # 🔹 Filter ตามผลผลิต/โครงการ
    df_selected = df_agency[df_agency["ผลผลิต/โครงการ"] == selected_project]

    # 🔹 ฟังก์ชันใส่สี
    def highlight_local(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    # 🔹 ฟังก์ชันแสดงตาราง
    def show_local_table(df_subset, disb_thres, spend_thres):
        group_cols = ["ชื่อรหัสงบประมาณ"]
        sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]

        df_grouped = df_subset.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)
        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["ชื่อรหัสงบประมาณ", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_local(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

    # ✅ Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    # 📊 Tab 1: ภาพรวม 🟥🟥🟥
    with tab1:
        show_local_table(df_selected, disb_thres=47.66, spend_thres=53.34)

    # 🏢 Tab 2: รายจ่ายประจำ 🟥🟥🟥
    with tab2:
        df_reg = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
        if not df_reg.empty:
            show_local_table(df_reg, disb_thres=52.34, spend_thres=53.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายประจำ")

    # 🏗️ Tab 3: รายจ่ายลงทุน 🟥🟥🟥
    with tab3:
        df_inv = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
        if not df_inv.empty:
            show_local_table(df_inv, disb_thres=32.00, spend_thres=51.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายลงทุน")

    st.markdown("<br>", unsafe_allow_html=True)


#--------------------------------------------------------------

# ✅ SECTION 6: หน่วยงานของรัฐสภา (รองรับ sidebar)
if "6️⃣ หน่วยงานของรัฐสภา" in selected_menus:
    st.markdown("## 6️⃣ หน่วยงานของรัฐสภา")

    # 🔹 Filter ข้อมูลเฉพาะหน่วยงานของรัฐสภา
    df_parliament = df[df["กระทรวง"] == "หน่วยงานของรัฐสภา"].copy()

    # 🔹 Dropdown เลือกหน่วยงาน
    agency_options = df_parliament["หน่วยงาน"].dropna().unique()
    selected_agency = st.selectbox("🔍เลือกหน่วยงาน", sorted(agency_options))

    # 🔹 Filter ข้อมูลเฉพาะหน่วยงานที่เลือก
    df_selected = df_parliament[df_parliament["หน่วยงาน"] == selected_agency]

    # 🔹 ฟังก์ชันสำหรับใส่สีตาม threshold
    def highlight_parliament(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    # 🔹 ฟังก์ชันแสดงตารางและสรุปผล
    def show_parliament_table(df_subset, disb_thres, spend_thres):
        df_grouped = df_subset.groupby("ผลผลิต/โครงการ", as_index=False)[
            ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        ].sum(numeric_only=True)

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["ผลผลิต/โครงการ", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_parliament(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

        # 🔸 รวมยอด
        total_prb = df_grouped["พรบ."].sum()
        total_after = df_grouped["งบฯ หลังโอน"].sum()
        total_disb = df_grouped["เบิกจ่าย"].sum()
        total_spend = df_grouped["ใช้จ่าย"].sum()
        percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
        percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

        color_disb_text = "#00FF9F" if percent_disb >= disb_thres else "#FF4B4B"
        color_spend_text = "#00FF9F" if percent_spend >= spend_thres else "#FF4B4B"

        st.markdown(f"""
**รวมทั้งสิ้น** | พรบ.: **{total_prb:,.4f}** | หลังโอน: **{total_after:,.4f}** | 
เบิกจ่าย: **{total_disb:,.4f}** | <span style='color:{color_disb_text}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
ใช้จ่าย: **{total_spend:,.4f}** | <span style='color:{color_spend_text}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
""", unsafe_allow_html=True)

    # ✅ Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    # 📊 Tab 1: ภาพรวม 🟥🟥🟥
    with tab1:
        show_parliament_table(df_selected, disb_thres=47.66, spend_thres=53.34)

    # 🏢 Tab 2: รายจ่ายประจำ 🟥🟥🟥
    with tab2:
        df_par_reg = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
        if not df_par_reg.empty:
            show_parliament_table(df_par_reg, disb_thres=52.34, spend_thres=53.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายประจำ")

    # 🏗️ Tab 3: รายจ่ายลงทุน 🟥🟥🟥
    with tab3:
        df_par_inv = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
        if not df_par_inv.empty:
            show_parliament_table(df_par_inv, disb_thres=32.00, spend_thres=51.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายลงทุน")

    st.markdown("<br>", unsafe_allow_html=True)


#--------------------------------------------------------------
# ✅ SECTION 7: ผลผลิต/โครงการ (รองรับ slide bar)
if "7️⃣ ผลผลิต/โครงการ (ค้นหาชื่อ)" in selected_menus:
    st.markdown("## 7️⃣ ผลผลิต/โครงการ (ค้นหาชื่อผลผลิต/โครงการ)")

    # 🔍 ช่องค้นหาชื่อโครงการ
    search_text = st.text_input("🔍ค้นหาชื่อผลผลิต/โครงการ", "", key="search_project_section7")

    # 🔎 กรองข้อมูลตามคำค้นหา
    df_search = df[df["ผลผลิต/โครงการ"].str.contains(search_text, case=False, na=False)] if search_text else df

    # 🧩 สร้าง project_key เพื่อใช้ตัดซ้ำเฉพาะภายในหน่วยงาน
    df_search["project_key"] = df_search["ผลผลิต/โครงการ"] + " | " + df_search["หน่วยงาน"]

    # ✅ แสดงเฉพาะ project_key ที่ไม่ซ้ำ
    project_options = df_search.drop_duplicates(subset=["project_key"])[["ผลผลิต/โครงการ", "หน่วยงาน"]]
    project_options["label"] = project_options["ผลผลิต/โครงการ"] + " | " + project_options["หน่วยงาน"]

    # 🔽 Dropdown ให้ผู้ใช้เลือก
    selected_label = st.selectbox("🔍เลือกผลผลิต/โครงการ", project_options["label"].tolist())

    # 🔎 แยกชื่อโครงการและหน่วยงานที่เลือก
    selected_project, selected_agency = selected_label.split(" | ", 1)

    # 🔄 Filter ข้อมูลตรงกับที่เลือก
    df_project = df[
        (df["ผลผลิต/โครงการ"] == selected_project) &
        (df["หน่วยงาน"] == selected_agency)
    ].copy()

    # 🔢 คำนวณ %เบิกจ่าย และ %ใช้จ่าย
    df_project["%เบิกจ่าย"] = round((df_project["เบิกจ่าย"] / df_project["งบฯ หลังโอน"]) * 100, 2)
    df_project["%ใช้จ่าย"] = round((df_project["ใช้จ่าย"] / df_project["งบฯ หลังโอน"]) * 100, 2)

    # 📌 แสดงกระทรวง หน่วยงาน และงบประมาณรวม
    if not df_project.empty:
        ministry_of_project = df_project["กระทรวง"].iloc[0]
        total_prb_all = df_project["พรบ."].sum()
        total_after_all = df_project["งบฯ หลังโอน"].sum()

        st.markdown(f"""
        📌 โครงการนี้อยู่ภายใต้ กระทรวง: <span style='color:green; font-weight:bold;'>{ministry_of_project}</span> | หน่วยงาน: <span style='color:green; font-weight:bold;'>{selected_agency}</span>  
        ได้รับจัดสรรงบประมาณทั้งสิ้น <span style='font-weight:bold;'>{total_prb_all:,.4f}</span> ล้านบาท และมีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน <span style='font-weight:bold;'>{total_after_all:,.4f}</span> ล้านบาท
        """, unsafe_allow_html=True)

    # 🎨 ฟังก์ชันใส่สี
    def highlight_project(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    # 📋 ฟังก์ชันแสดงตาราง + สรุปยอด
    def show_project_table(df_sub, disb_thres, spend_thres):
        df_grouped = df_sub.groupby("ชื่อรหัสงบประมาณ", as_index=False).agg({
            "พรบ.": "sum",
            "งบฯ หลังโอน": "sum",
            "เบิกจ่าย": "sum",
            "ใช้จ่าย": "sum"
        })

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["ชื่อรหัสงบประมาณ", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]

        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_project(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

        # 🔢 รวมยอด
        total_prb = df_grouped["พรบ."].sum()
        total_after = df_grouped["งบฯ หลังโอน"].sum()
        total_disb = df_grouped["เบิกจ่าย"].sum()
        total_spend = df_grouped["ใช้จ่าย"].sum()
        percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
        percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

        color_disb = "#00FF9F" if percent_disb >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if percent_spend >= spend_thres else "#FF4B4B"

        st.markdown(f"""
        **รวมทั้งสิ้น** | พรบ.: **{total_prb:,.4f}** | หลังโอน: **{total_after:,.4f}** | 
        เบิกจ่าย: **{total_disb:,.4f}** | <span style='color:{color_disb}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
        ใช้จ่าย: **{total_spend:,.4f}** | <span style='color:{color_spend}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
        """, unsafe_allow_html=True)

    # ✅ Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    # 📊 Tab 1: ภาพรวม 🟥🟥🟥
    with tab1:
        show_project_table(df_project, disb_thres=47.66, spend_thres=53.34)

    # 🏢 Tab 2: รายจ่ายประจำ 🟥🟥🟥
    with tab2:
        df_reg = df_project[df_project["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
        if not df_reg.empty:
            show_project_table(df_reg, disb_thres=52.34, spend_thres=53.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายประจำ")

    # 🏗️ Tab 3: รายจ่ายลงทุน 🟥🟥🟥
    with tab3:
        df_inv = df_project[df_project["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
        if not df_inv.empty:
            show_project_table(df_inv, disb_thres=32.00, spend_thres=51.34)
        else:
            st.info("ไม่มีข้อมูลรายจ่ายลงทุน")

    st.markdown("<br>", unsafe_allow_html=True)

#--------------------------------------------------------------
# ✅ SECTION 8: ผลผลิต/โครงการ (ติดตามรายหน่วยงาน)
if "8️⃣ ผลผลิต/โครงการ (ติดตามรายหน่วยงาน)" in selected_menus:
    st.markdown("## 8️⃣ ผลผลิต/โครงการ (ติดตามรายหน่วยงาน)")

    # 🔹 เลือกกระทรวง
    ministry_options = df["กระทรวง"].dropna().unique()
    selected_ministry = st.selectbox("เลือกกระทรวง", sorted(ministry_options), key="ministry_section8")

    # 🔹 เลือกหน่วยงาน
    df_min = df[df["กระทรวง"] == selected_ministry]
    agency_options = df_min["หน่วยงาน"].dropna().unique()
    selected_agency = st.selectbox("เลือกหน่วยงาน", sorted(agency_options))

    # 🔹 กรองข้อมูลตามหน่วยงาน
    df_agency = df_min[df_min["หน่วยงาน"] == selected_agency]

    # 🔹 ฟังก์ชันใส่สี
    def highlight_proj_detail(row, category):
        c1 = get_color(row["%เบิกจ่าย"], category, "เบิกจ่าย")
        c2 = get_color(row["%ใช้จ่าย"], category, "ใช้จ่าย")
        return ["", "", "", "", f"color: {c1}", "", f"color: {c2}"]

    # 🔹 ฟังก์ชันแสดงตาราง
    def show_proj_by_agency(df_sub, category):
        if df_sub.empty:
            st.info("ไม่มีข้อมูล")
            return

        df_grouped = df_sub.groupby("ผลผลิต/โครงการ", as_index=False)[
            ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        ].sum(numeric_only=True)

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["ผลผลิต/โครงการ", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_proj_detail(row, category), axis=1)

        st.dataframe(styled, use_container_width=True)

    # 🔹 แยกข้อมูล
    df_all = df_agency.copy()
    df_reg = df_agency[df_agency["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    df_inv = df_agency[df_agency["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

    # ✅ Tabs สำหรับตาราง
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    with tab1:
        show_proj_by_agency(df_all, "ภาพรวม")

    with tab2:
        show_proj_by_agency(df_reg, "รายจ่ายประจำ")

    with tab3:
        show_proj_by_agency(df_inv, "รายจ่ายลงทุน")

    st.markdown("<br>", unsafe_allow_html=True)



#--------------------------------------------------------------
# --- SECTION 9: ลักษณะงาน ---
if "9️⃣ ลักษณะงาน" in selected_menus:
    st.markdown("## 9️⃣ ลักษณะงาน")

    selected_dimension = st.selectbox(
        "🔍 เลือกด้านลักษณะงาน",
        sorted(df["ด้าน_ลักษณะงาน"].dropna().unique()),
        key="main_dimension"
    )

    df_dim = df[df["ด้าน_ลักษณะงาน"] == selected_dimension].copy()
    df_dim["%เบิกจ่าย"] = round((df_dim["เบิกจ่าย"] / df_dim["งบฯ หลังโอน"]) * 100, 2)
    df_dim["%ใช้จ่าย"] = round((df_dim["ใช้จ่าย"] / df_dim["งบฯ หลังโอน"]) * 100, 2)

    def highlight_table(row, disb_thres, spend_thres):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
        return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

    def show_dimension_table(df_sub, disb_thres, spend_thres, category):
        if df_sub.empty:
            st.info("ไม่มีข้อมูล")
            return

        group_cols = ["หน่วยงาน"]
        sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]
        df_grouped = df_sub.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)

        df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
        df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

        display_cols = ["หน่วยงาน", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
        styled = df_grouped[display_cols].style.format({
            "พรบ.": "{:,.4f}",
            "งบฯ หลังโอน": "{:,.4f}",
            "เบิกจ่าย": "{:,.4f}",
            "ใช้จ่าย": "{:,.4f}",
            "%เบิกจ่าย": "{:,.2f}%",
            "%ใช้จ่าย": "{:,.2f}%"
        }).apply(lambda row: highlight_table(row, disb_thres, spend_thres), axis=1)

        st.dataframe(styled, use_container_width=True)

        # 🔸 รวมยอด
        total_prb = df_grouped["พรบ."].sum()
        total_after = df_grouped["งบฯ หลังโอน"].sum()
        total_disb = df_grouped["เบิกจ่าย"].sum()
        total_spend = df_grouped["ใช้จ่าย"].sum()
        percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
        percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

        color_disb_text = "#00FF9F" if percent_disb >= disb_thres else "#FF4B4B"
        color_spend_text = "#00FF9F" if percent_spend >= spend_thres else "#FF4B4B"

        st.markdown(f"""
**รวมทั้งสิ้น** | พรบ.: **{total_prb:,.4f}** | หลังโอน: **{total_after:,.4f}** | 
เบิกจ่าย: **{total_disb:,.4f}** | <span style='color:{color_disb_text}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
ใช้จ่าย: **{total_spend:,.4f}** | <span style='color:{color_spend_text}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
""", unsafe_allow_html=True)

    # 🔹 แยกข้อมูล
    df_dim_reg = df_dim[df_dim["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
    df_dim_inv = df_dim[df_dim["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

    # ✅ Tabs สำหรับตาราง 🟥🟥🟥
    tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", "🏢 รายจ่ายประจำ", "🏗️ รายจ่ายลงทุน"])

    with tab1:
        show_dimension_table(df_dim, disb_thres=47.66, spend_thres=53.34, category="ภาพรวม")

    with tab2:
        show_dimension_table(df_dim_reg, disb_thres=52.34, spend_thres=53.34, category="รายจ่ายประจำ")

    with tab3:
        show_dimension_table(df_dim_inv, disb_thres=32.00, spend_thres=51.34, category="รายจ่ายลงทุน")


#--------------------------------------------------------------

# --- Section: Footer Contact and Credits ---

# 🔹 สร้างตัวเลือกใน Sidebar เพื่อเปิด/ปิดการแสดงผล
with st.sidebar:
    show_footer = st.checkbox("📞ติดต่อ / Contact", value=True)

# 🔹 แสดง footer เฉพาะเมื่อผู้ใช้เลือก
if show_footer:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### Contact us  
        📞 **Call**: +66 2 242 5900 ext. 4121  
        📧 **Email**: [pbo@parliament.go.th](mailto:pbo@parliament.go.th)  
        💬 **LINE ID**: @thaipbo
        """)

    with col2:
        st.markdown("""
        #### สอบถามเพิ่มเติม  
        📞 **ติดต่อ**: +66 2 242 5900 ต่อ 4121  
        📧 **Email**: [pbo@parliament.go.th](mailto:pbo@parliament.go.th)  
        💬 **LINE ID**: @thaipbo
        """)

    with col3:
        st.markdown("""
        #### เจ้าของผลงานและผู้รับผิดชอบ  
        🔹 ลิขสิทธิ์: สำนักงบประมาณของรัฐสภา (PBO)  
        🔹 ผู้รับผิดชอบ: **กุลธิดา สมศรี** และ **ศุภิกา ตรีรัตนไพบูลย์**  
        🔹 Code writer: **กุลธิดา สมศรี (70%)** และ **ChatGPT (30%)**  
        🔹 ค่าใช้จ่าย: ระบบไม่ได้ใช้งบประมาณแผ่นดิน ค่า chatGPT ผู้เขียนโค้ดออกค่าใช้จ่ายเอง
        """)
