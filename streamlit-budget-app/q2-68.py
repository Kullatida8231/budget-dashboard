import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Dashboard งบประมาณ", layout="wide")

# 🔤 เพิ่ม CSS เพื่อให้รองรับฟอนต์ภาษาไทย
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Sarabun', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)
# โหลดข้อมูล
@st.cache_data
def load_data():
    file_path = "q2-68.xlsx"
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
    <div class='header-main'>ผลการเบิกจ่ายและใช้จ่ายงบประมาณ ณ สิ้นสุดไตรมาสที่ 2 ปีงบประมาณ พ.ศ. 2568</div>
    <div class='header-sub'>⚠️ อยู่ระหว่างการพัฒนาระบบ (Under development) ⚠️</div>
""", unsafe_allow_html=True)
#-----------------------------
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
 🔵 หมายเหตุประกอบการอ่านข้อมูล
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
1. ข้อมูลผลการเบิกจ่ายงบประมาณและการใช้จ่ายของรัฐ จากระบบ New GFMIS Thai กรมบัญชีกลาง | แสดงข้อมูล ณ ตั้งแต่ต้นปี งปม. ถึงสิ้นเดือนมีนาคม ปี งปม. 2568 | เรียกข้อมูล ณ วันที่ 28 เมษายน 2568 เวลา 12.02 น.
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
2. เบิกจ่าย คือ มูลลค่าการเบิกจ่ายทั้งสิ้นที่ส่วนราชการเบิกจ่ายเองและส่วนราชการอื่นเบิกแทนให้ 
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
3. ใช้จ่าย คือ มูลค่าการเบิกจ่ายทั้งสิ้นรวม PO รวมสำรองเงินแบบมีหนี้ (เบิกจ่าย+PO+สำรองเงินแบบมีหนี้)
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
4. สีของค่า %เบิกจ่าย และ %ใช้จ่าย ประกอบด้วย "สีแดง" หมายถึง ต่ำกว่าเป้าหมาย และ "สีเขียว" หมายถึง เกินกว่าเป้าหมาย
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ส่วนหัวข้อความแบบจัดกึ่งกลาง
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
 🔵 มาตรการเร่งรัดการเบิกจ่ายงบประมาณและการใช้จ่ายภาครัฐ ประจำปีงบประมาณ พ.ศ. 2568 (ค่าเป้าหมาย)
</div>
""", unsafe_allow_html=True)

# ตาราง HTML พร้อมจัดกึ่งกลางทุกเซลล์
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
    text-align: center;
    vertical-align: middle;
}
</style>

<table>
    <tr>
        <th rowspan="2">รายการ</th>
        <th colspan="2">รวม</th>
        <th colspan="2">ไตรมาสที่ 1</th>
        <th colspan="2">ไตรมาสที่ 2</th>
        <th colspan="2">ไตรมาสที่ 3</th>
        <th colspan="2">ไตรมาสที่ 4</th>
    </tr>
    <tr>
        <th>เบิกจ่าย</th><th>ใช้จ่าย</th>
        <th>เบิกจ่าย</th><th>ใช้จ่าย</th>
        <th>เบิกจ่าย</th><th>ใช้จ่าย</th>
        <th>เบิกจ่าย</th><th>ใช้จ่าย</th>
        <th>เบิกจ่าย</th><th>ใช้จ่าย</th>
    </tr>
    <tr>
        <td>ภาพรวม</td><td>94</td><td>100</td><td>27</td><td>37</td><td>53</td><td>61</td><td>75</td><td>80</td><td>94</td><td>100</td>
    </tr>
    <tr>
        <td>ประจำ</td><td>98</td><td>100</td><td>35</td><td>36</td><td>57</td><td>58</td><td>80</td><td>81</td><td>98</td><td>100</td>
    </tr>
    <tr>
        <td>ลงทุน</td><td>80</td><td>100</td><td>17</td><td>39</td><td>35</td><td>66</td><td>54</td><td>77</td><td>80</td><td>100</td>
    </tr>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)
st.markdown("""
<div style='text-align: left; font-size: 14px; font-weight: normal; margin-bottom: 10px;'>
ที่มา : มาตรการเร่งรัดการเบิกจ่ายงบประมาณและการใช้จ่ายภาครัฐ ประจำปีงบประมาณ พ.ศ. 2568 (ตามหนังสือสำนักเลขาธิการคณะรัฐมนตรี ด่วนที่สุด นร 0505/ว 466 ลงวันที่ 25 ตุลาคม 2567
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#-----------------------------
# ส่วนที่ 1 ภาพรวมทั้งประเทศ
# ฟังก์ชันรวมข้อมูล
def compute_summary(df):
    total_prb = round(df["พรบ."].sum(), 4)
    total_after = round(df["งบฯ หลังโอน"].sum(), 4)
    total_disb = round(df["เบิกจ่าย"].sum(), 4)
    total_spend = round(df["ใช้จ่าย"].sum(), 4)
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
    return total_prb, total_after, total_disb, percent_disb, total_spend, percent_spend

# สรุปแต่ละประเภท
total_all = compute_summary(df)
total_regular = compute_summary(df[df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"])
total_invest = compute_summary(df[df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"])

# ฟังก์ชันแสดงผล
def show_metrics(data, title):
    prb, after, disb, per_disb, spend, per_spend = data
    st.markdown(f"### {title}")
    col1, col2, col3 = st.columns(3)

    if "ภาพรวม" in title:
        disb_threshold = 53
        spend_threshold = 61
    elif "ประจำ" in title:
        disb_threshold = 57
        spend_threshold = 58
    elif "ลงทุน" in title:
        disb_threshold = 35
        spend_threshold = 66
    else:
        disb_threshold = spend_threshold = 0

    def small_metric(label, value, is_percent=False, threshold=None):
        formatted = f"{value:,.2f}%" if is_percent else f"{value:,.4f}"
        color = "#00FF9F" if is_percent and value >= threshold else "#FF4B4B" if is_percent else "inherit"
        return f"""
            <div style='margin-bottom: 0.75rem;'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value' style='color: {color};'>{formatted}</div>
            </div>
        """

    with col1:
        st.markdown(small_metric("พ.ร.บ.", prb), unsafe_allow_html=True)
        st.markdown(small_metric("งบฯ หลังโอนฯ", after), unsafe_allow_html=True)
    with col2:
        st.markdown(small_metric("เบิกจ่าย", disb), unsafe_allow_html=True)
        st.markdown(small_metric("%เบิกจ่าย", per_disb, is_percent=True, threshold=disb_threshold), unsafe_allow_html=True)
    with col3:
        st.markdown(small_metric("ใช้จ่าย", spend), unsafe_allow_html=True)
        st.markdown(small_metric("%ใช้จ่าย", per_spend, is_percent=True, threshold=spend_threshold), unsafe_allow_html=True)

# แสดงผล
st.markdown("## 1️⃣ภาพรวมทั้งประเทศ")
show_metrics(total_all, "📊 ภาพรวม")
show_metrics(total_regular, "🏢 รายจ่ายประจำ")
show_metrics(total_invest, "🏗️ รายจ่ายลงทุน")
st.markdown("<br>", unsafe_allow_html=True)

#--------------------------------------
# --- SECTION 2: ผลการเบิกจ่ายและใช้จ่ายรายหน่วยงาน ---
st.markdown("## 2️⃣กระทรวง/หน่วยงาน")

# 🔹 Dropdown สำหรับเลือกกระทรวง
ministry_list = df["กระทรวง"].dropna().unique()
selected_ministry = st.selectbox("เลือกกระทรวง", sorted(ministry_list))

# 🔹 Filter ข้อมูลเฉพาะกระทรวงที่เลือก
df_filtered = df[df["กระทรวง"] == selected_ministry]

# 🔹 ฟังก์ชันจัดการตารางและใส่สี
def prepare_table(df_part):
    # รวมข้อมูลตาม 'หน่วยงาน'
    df_part = df_part.groupby("หน่วยงาน")[["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]].sum().reset_index()

    # คำนวณ %เบิกจ่าย และ %ใช้จ่าย
    df_part["%เบิกจ่าย"] = (df_part["เบิกจ่าย"] / df_part["งบฯ หลังโอน"]) * 100
    df_part["%ใช้จ่าย"] = (df_part["ใช้จ่าย"] / df_part["งบฯ หลังโอน"]) * 100

    # เรียงลำดับคอลัมน์
    cols = ["หน่วยงาน", "พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
    df_part = df_part[cols]

    # ใส่สีตาม threshold
    def highlight(row):
        color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= 53 else "#FF4B4B"
        color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= 61 else "#FF4B4B"
        return [
            "", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"
        ]

    styled_df = df_part.style.format({
        "พรบ.": "{:,.4f}",
        "งบฯ หลังโอน": "{:,.4f}",
        "เบิกจ่าย": "{:,.4f}",
        "ใช้จ่าย": "{:,.4f}",
        "%เบิกจ่าย": "{:,.2f}%",
        "%ใช้จ่าย": "{:,.2f}%"
    }).apply(highlight, axis=1)

    return styled_df

# 🔹 Filter ข้อมูลเฉพาะกระทรวงที่เลือก
df_min = df[df["กระทรวง"] == selected_ministry]
df_reg = df_min[df_min["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
df_inv = df_min[df_min["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

# 🔹 คำนวณภาพรวม
total_prb = df_min["พรบ."].sum()
total_after = df_min["งบฯ หลังโอน"].sum()
total_disb = df_min["เบิกจ่าย"].sum()
total_spend = df_min["ใช้จ่าย"].sum()
percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
color_disb = "#00FF9F" if percent_disb >= 53 else "#FF4B4B"
color_spend = "#00FF9F" if percent_spend >= 61 else "#FF4B4B"

# 🔹 รายจ่ายประจำ
prb_r = df_reg["พรบ."].sum()
after_r = df_reg["งบฯ หลังโอน"].sum()
disb_r = df_reg["เบิกจ่าย"].sum()
spend_r = df_reg["ใช้จ่าย"].sum()
per_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
per_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0
color_disb_r = "#00FF9F" if per_disb_r >= 57 else "#FF4B4B"
color_spend_r = "#00FF9F" if per_spend_r >= 58 else "#FF4B4B"

# 🔹 รายจ่ายลงทุน
prb_i = df_inv["พรบ."].sum()
after_i = df_inv["งบฯ หลังโอน"].sum()
disb_i = df_inv["เบิกจ่าย"].sum()
spend_i = df_inv["ใช้จ่าย"].sum()
per_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
per_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0
color_disb_i = "#00FF9F" if per_disb_i >= 35 else "#FF4B4B"
color_spend_i = "#00FF9F" if per_spend_i >= 66 else "#FF4B4B"

# 🔹 แสดงผล
st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ในภาพรวม **📍{selected_ministry}** ได้รับจัดสรรงบประมาณ **จำนวน {total_prb:,.4f} ล้านบาท** มีงบประมาณหลังโอนเปลี่ยนแปลง **จำนวน {total_after:,.4f} ล้านบาท**  มีการเบิกจ่าย **จำนวน {total_disb:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb}; font-weight:bold;">{percent_disb:.2f}%</span> ของงบฯ หลังโอน)  และมีการใช้จ่าย **จำนวน {total_spend:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend}; font-weight:bold;">{percent_spend:.2f}%</span> ของงบฯ หลังโอน)
""", unsafe_allow_html=True)

st.markdown(f"""
โดยสามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้ 
""", unsafe_allow_html=True)

if not df_reg.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ **จำนวน {prb_r:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง **จำนวน {after_r:,.4f} ล้านบาท** โดยมีการเบิกจ่าย **จำนวน {disb_r:,.4f} ล้านบาท**  (<span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span> ของงบฯ หลังโอน) และมีการใช้จ่าย **จำนวน {spend_r:,.4f} ล้านบาท**  (<span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span> ของงบฯ หลังโอน)
""", unsafe_allow_html=True)

if not df_inv.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **จำนวน {prb_i:,.4f} ล้านบาท** มีงบประมาณหลังโอนเปลี่ยนแปลง **จำนวน {after_i:,.4f} ล้านบาท** โดยมีการเบิกจ่าย **จำนวน {disb_i:,.4f} ล้านบาท**  (<span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span> ของงบฯ หลังโอน) และมีการใช้จ่าย **จำนวน {spend_i:,.4f} ล้านบาท**  (<span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span> ของงบฯ หลังโอน)
""", unsafe_allow_html=True)

# 🔸 แสดงตารางภาพรวม
st.markdown("### ภาพรวม")
st.dataframe(prepare_table(df_filtered), use_container_width=True)

# 🔸 รายจ่ายประจำ
df_reg = df_filtered[df_filtered["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_reg.empty:
    st.markdown("### รายจ่ายประจำ")
    st.dataframe(prepare_table(df_reg), use_container_width=True)

# 🔸 รายจ่ายลงทุน
df_inv = df_filtered[df_filtered["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_inv.empty:
    st.markdown("### รายจ่ายลงทุน")
    st.dataframe(prepare_table(df_inv), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
#---------------------------------------
# --- SECTION 3: งบกลาง ---
st.markdown("## 3️⃣ งบกลาง")

# 🔹 Filter เฉพาะกระทรวง "งบกลาง"
df_central = df[df["กระทรวง"] == "งบกลาง"].copy()

# 🔹 ฟังก์ชันใส่สีในตาราง
def highlight_central(row, disb_thres, spend_thres):
    color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
    color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
    return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

# 🔹 ฟังก์ชันแสดงตารางและสรุปผล
def show_central_table(df_subset, title, disb_thres, spend_thres):
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

    st.markdown(f"### {title}")
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

    # 🔸 สรุปผลล่างตารางพร้อมใส่สี
    st.markdown(f"""
รวมทั้งสิ้น | พรบ.: {total_prb:,.4f} | หลังโอน: {total_after:,.4f} | 
เบิกจ่าย: {total_disb:,.4f} | <span style='color:{color_disb_text}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
ใช้จ่าย: {total_spend:,.4f} | <span style='color:{color_spend_text}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
""", unsafe_allow_html=True)

# 🔸 ภาพรวม
show_central_table(df_central, "ภาพรวม", disb_thres=53, spend_thres=61)

# 🔸 รายจ่ายประจำ
df_central_reg = df_central[df_central["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_central_reg.empty:
    show_central_table(df_central_reg, "รายจ่ายประจำ", disb_thres=57, spend_thres=58)

# 🔸 รายจ่ายลงทุน
df_central_inv = df_central[df_central["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_central_inv.empty:
    show_central_table(df_central_inv, "รายจ่ายลงทุน", disb_thres=35, spend_thres=66)

st.markdown("<br>", unsafe_allow_html=True)
#--------------------------------------
# SECTION 4: แผนบูรณาการ
st.markdown("## 4️⃣ แผนบูรณาการ")
# 🔹 Filter เฉพาะแผนงานบูรณาการ
df_plan = df[df["กลุ่มแผนงาน"] == "แผนงานบูรณาการ"]
df_reg = df_plan[df_plan["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
df_inv = df_plan[df_plan["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

# 🔹 คำนวณภาพรวม
total_prb = df_plan["พรบ."].sum()
total_after = df_plan["งบฯ หลังโอน"].sum()
total_disb = df_plan["เบิกจ่าย"].sum()
total_spend = df_plan["ใช้จ่าย"].sum()
percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
color_disb = "#00FF9F" if percent_disb >= 53 else "#FF4B4B"
color_spend = "#00FF9F" if percent_spend >= 61 else "#FF4B4B"

# 🔹 ประจำ
prb_r = df_reg["พรบ."].sum()
after_r = df_reg["งบฯ หลังโอน"].sum()
disb_r = df_reg["เบิกจ่าย"].sum()
spend_r = df_reg["ใช้จ่าย"].sum()
per_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
per_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0
color_disb_r = "#00FF9F" if per_disb_r >= 57 else "#FF4B4B"
color_spend_r = "#00FF9F" if per_spend_r >= 58 else "#FF4B4B"

# 🔹 ลงทุน
prb_i = df_inv["พรบ."].sum()
after_i = df_inv["งบฯ หลังโอน"].sum()
disb_i = df_inv["เบิกจ่าย"].sum()
spend_i = df_inv["ใช้จ่าย"].sum()
per_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
per_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0
color_disb_i = "#00FF9F" if per_disb_i >= 35 else "#FF4B4B"
color_spend_i = "#00FF9F" if per_spend_i >= 66 else "#FF4B4B"

# 🔸 แสดงผล
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
🔵 ภาพรวมทุกแผนงานบูรณาการ
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ในปีงบประมาณ พ.ศ. 2568 มีการจัดสรรงบประมาณสำหรับ**📍แผนงานบูรณาการ รวมทั้งสิ้น {total_prb:,.4f} ล้านบาท** มีงบประมาณหลังโอนเปลี่ยนแปลง **จำนวน {total_after:,.4f} ล้านบาท**  โดยมีการเบิกจ่าย **จำนวน {total_disb:,.4f} ล้านบาท** (คิดเป็น <span style="color:{color_disb}; font-weight:bold;">{percent_disb:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย **จำนวน {total_spend:,.4f} ล้านบาท** (คิดเป็น <span style="color:{color_spend}; font-weight:bold;">{percent_spend:.2f}%</span> ของ งบฯ หลังโอน) ทั้งนี้ สามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้
""", unsafe_allow_html=True)

if not df_reg.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ จำนวน **{prb_r:,.4f}** ล้านบาท มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_r:,.4f}** ล้านบาท โดยมีการเบิกจ่าย  **{disb_r:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย จำนวน **{spend_r:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span> ของ งบฯ หลังโอน)
""", unsafe_allow_html=True)

if not df_inv.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **{prb_i:,.4f}** ล้านบาท มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_i:,.4f}** ล้านบาท 
โดยมีการเบิกจ่าย จำนวน **{disb_i:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span> ของ งบฯ หลังโอน) และมีการใช้จ่าย จำนวน **{spend_i:,.4f}** ล้านบาท (คิดเป็น <span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span> ของ งบฯ หลังโอน)
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


#------------------------------------
st.markdown("""
<div style='text-align: left; font-size: 18px; font-weight: bold; margin-bottom: 10px;'>
🔵 แยกตามรายแผนงานบูรณาการ
</div>
""", unsafe_allow_html=True)

# 🔹 Filter เฉพาะกลุ่มแผนงาน "แผนงานบูรณาการ"
df_plan = df[df["กลุ่มแผนงาน"] == "แผนงานบูรณาการ"].copy()

# 🔹 Dropdown สำหรับเลือกแผนงาน
plan_options = df_plan["แผนงาน"].dropna().unique()
selected_plan = st.selectbox("🔍เลือกแผนงาน", sorted(plan_options))

# 🔹 Filter เฉพาะแผนงานที่เลือก
df_plan_selected = df_plan[df_plan["แผนงาน"] == selected_plan]

# 🔹 รายจ่ายประจำและลงทุน
df_plan_reg = df_plan_selected[df_plan_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
df_plan_inv = df_plan_selected[df_plan_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]

# 🔹 ฟังก์ชันใส่สีตาม threshold
def highlight_plan(row, disb_thres, spend_thres):
    color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
    color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
    return [
        "", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"
    ]

# 🔹 ฟังก์ชันแสดงตารางแบบมีสี
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

# 🔹 สรุปภาพรวม
total_prb = df_plan_selected["พรบ."].sum()
total_after = df_plan_selected["งบฯ หลังโอน"].sum()
total_disb = df_plan_selected["เบิกจ่าย"].sum()
total_spend = df_plan_selected["ใช้จ่าย"].sum()
percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0
color_disb = "#00FF9F" if percent_disb >= 53 else "#FF4B4B"
color_spend = "#00FF9F" if percent_spend >= 61 else "#FF4B4B"

# 🔹 ประเภท: รายจ่ายประจำ
prb_r = df_plan_reg["พรบ."].sum()
after_r = df_plan_reg["งบฯ หลังโอน"].sum()
disb_r = df_plan_reg["เบิกจ่าย"].sum()
spend_r = df_plan_reg["ใช้จ่าย"].sum()
per_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
per_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0
color_disb_r = "#00FF9F" if per_disb_r >= 57 else "#FF4B4B"
color_spend_r = "#00FF9F" if per_spend_r >= 58 else "#FF4B4B"

# 🔹 ประเภท: รายจ่ายลงทุน
prb_i = df_plan_inv["พรบ."].sum()
after_i = df_plan_inv["งบฯ หลังโอน"].sum()
disb_i = df_plan_inv["เบิกจ่าย"].sum()
spend_i = df_plan_inv["ใช้จ่าย"].sum()
per_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
per_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0
color_disb_i = "#00FF9F" if per_disb_i >= 35 else "#FF4B4B"
color_spend_i = "#00FF9F" if per_spend_i >= 66 else "#FF4B4B"

# 🔸 แสดงผล
st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; มีการจัดสรรงบประมาณสำหรับ**📝{selected_plan}**  จำนวน **{total_prb:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{total_after:,.4f} ล้านบาท**  มีการเบิกจ่าย จำนวน **{total_disb:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb}; font-weight:bold;">{percent_disb:.2f}%</span> ของ งบฯ หลังโอน)  และมีการใช้จ่าย จำนวน **{total_spend:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend}; font-weight:bold;">{percent_spend:.2f}%</span> ของ งบฯ หลังโอน) ทั้งนี้ สามารถจำแนกงบประมาณรายจ่ายออกเป็น 2 ประเภท ดังนี้
""", unsafe_allow_html=True)

if not df_plan_reg.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1. รายจ่ายประจำ** ได้รับจัดสรรงบประมาณ **{prb_r:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_r:,.4f} ล้านบาท**  เบิกจ่าย **{disb_r:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb_r}; font-weight:bold;">{per_disb_r:.2f}%</span> ของ งบฯ หลังโอน)  ใช้จ่าย **{spend_r:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend_r}; font-weight:bold;">{per_spend_r:.2f}%</span> ของ งบฯ หลังโอน)
""", unsafe_allow_html=True)

if not df_plan_inv.empty:
    st.markdown(f"""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2. รายจ่ายลงทุน** ได้รับจัดสรรงบประมาณ **{prb_i:,.4f} ล้านบาท**  มีงบประมาณหลังโอนเปลี่ยนแปลง จำนวน **{after_i:,.4f} ล้านบาท**  เบิกจ่าย **{disb_i:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_disb_i}; font-weight:bold;">{per_disb_i:.2f}%</span> ของ งบฯ หลังโอน)  ใช้จ่าย **{spend_i:,.4f} ล้านบาท**  (คิดเป็น <span style="color:{color_spend_i}; font-weight:bold;">{per_spend_i:.2f}%</span> ของ งบฯ หลังโอน)
""", unsafe_allow_html=True)

# 🔸 ตารางภาพรวม
show_plan_table(df_plan_selected, "ภาพรวม", disb_thres=53, spend_thres=61)

# 🔸 ตารางรายจ่ายประจำ
if not df_plan_reg.empty:
    show_plan_table(df_plan_reg, "รายจ่ายประจำ", disb_thres=57, spend_thres=58)

# 🔸 ตารางรายจ่ายลงทุน
if not df_plan_inv.empty:
    show_plan_table(df_plan_inv, "รายจ่ายลงทุน", disb_thres=35, spend_thres=66)

st.markdown("<br>", unsafe_allow_html=True)
#-------------------------------------------


# --- SECTION 5: จังหวัดและกลุ่มจังหวัด ---
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
def show_local_table(df_subset, title, disb_thres, spend_thres):
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

    st.markdown(f"### {title}")
    st.dataframe(styled, use_container_width=True)

# 🔸 แสดงตาราง
show_local_table(df_selected, "ภาพรวมชื่อรหัสงบประมาณ", disb_thres=53, spend_thres=61)

# 🔸 Filter และแสดง รายจ่ายประจำ
df_reg = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_reg.empty:
    show_local_table(df_reg, "รายจ่ายประจำ", disb_thres=57, spend_thres=58)

# 🔸 Filter และแสดง รายจ่ายลงทุน
df_inv = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_inv.empty:
    show_local_table(df_inv, "รายจ่ายลงทุน", disb_thres=35, spend_thres=66)

st.markdown("<br>", unsafe_allow_html=True)
#-------------------------------------------

# --- SECTION 6: หน่วยงานของรัฐสภา ---
st.markdown("## 6️⃣ หน่วยงานของรัฐสภา")

# 🔹 Filter ข้อมูลเฉพาะหน่วยงานของรัฐสภา
df_parliament = df[df["กระทรวง"] == "หน่วยงานของรัฐสภา"].copy()

# 🔹 Dropdown เลือกหน่วยงาน
agency_options = df_parliament["หน่วยงาน"].dropna().unique()
selected_agency = st.selectbox("🔍เลือกหน่วยงาน", sorted(agency_options))

# 🔹 Filter ข้อมูลเฉพาะหน่วยงานที่เลือก
df_selected = df_parliament[df_parliament["หน่วยงาน"] == selected_agency]

# 🔹 ใช้ 'ผลผลิต/โครงการ' สำหรับ grouping
group_cols = ["ผลผลิต/โครงการ"]
sum_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "ใช้จ่าย"]

# 🔹 ฟังก์ชันสำหรับใส่สีตาม threshold
def highlight_parliament(row, disb_thres, spend_thres):
    color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
    color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
    return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

# 🔹 ฟังก์ชันแสดงตารางพร้อมสี
def show_parliament_table(df_subset, title, disb_thres, spend_thres):
    df_grouped = df_subset.groupby(group_cols, as_index=False)[sum_cols].sum(numeric_only=True)
    df_grouped["%เบิกจ่าย"] = round((df_grouped["เบิกจ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)
    df_grouped["%ใช้จ่าย"] = round((df_grouped["ใช้จ่าย"] / df_grouped["งบฯ หลังโอน"]) * 100, 2)

    display_cols = group_cols + ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
    styled = df_grouped[display_cols].style.format({
        "พรบ.": "{:,.4f}",
        "งบฯ หลังโอน": "{:,.4f}",
        "เบิกจ่าย": "{:,.4f}",
        "ใช้จ่าย": "{:,.4f}",
        "%เบิกจ่าย": "{:,.2f}%",
        "%ใช้จ่าย": "{:,.2f}%"
    }).apply(lambda row: highlight_parliament(row, disb_thres, spend_thres), axis=1)

    st.markdown(f"### {title}")
    st.dataframe(styled, use_container_width=True)

# 🔸 ภาพรวม
show_parliament_table(df_selected, "ภาพรวม", disb_thres=53, spend_thres=61)

# 🔸 รายจ่ายประจำ
df_par_reg = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_par_reg.empty:
    show_parliament_table(df_par_reg, "รายจ่ายประจำ", disb_thres=57, spend_thres=58)

# 🔸 รายจ่ายลงทุน
df_par_inv = df_selected[df_selected["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_par_inv.empty:
    show_parliament_table(df_par_inv, "รายจ่ายลงทุน", disb_thres=35, spend_thres=66)

st.markdown("<br>", unsafe_allow_html=True)
#------------------------------------
# --- SECTION 7: ผลผลิต/โครงการ ---
st.markdown("## 7️⃣ ผลผลิต/โครงการ")

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
def show_project_table(df_sub, title, disb_thres, spend_thres):
    # 🧮 รวมชื่อรหัสงบประมาณที่ซ้ำ
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

    # 🔢 รวมยอด
    total_prb = df_grouped["พรบ."].sum()
    total_after = df_grouped["งบฯ หลังโอน"].sum()
    total_disb = df_grouped["เบิกจ่าย"].sum()
    total_spend = df_grouped["ใช้จ่าย"].sum()
    percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
    percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

    color_disb = "#00FF9F" if percent_disb >= disb_thres else "#FF4B4B"
    color_spend = "#00FF9F" if percent_spend >= spend_thres else "#FF4B4B"

    # 📊 แสดงผล
    st.markdown(f"### {title}")
    st.dataframe(styled, use_container_width=True)

    st.markdown(f"""
    **รวมทั้งสิ้น** | พรบ.: **{total_prb:,.4f}** | หลังโอน: **{total_after:,.4f}** | 
    เบิกจ่าย: **{total_disb:,.4f}** | <span style='color:{color_disb}; font-weight:bold;'>%เบิกจ่าย: {percent_disb:.2f}%</span> | 
    ใช้จ่าย: **{total_spend:,.4f}** | <span style='color:{color_spend}; font-weight:bold;'>%ใช้จ่าย: {percent_spend:.2f}%</span>
    """, unsafe_allow_html=True)

# ✅ ตาราง: ภาพรวม
show_project_table(df_project, "ภาพรวม", disb_thres=53, spend_thres=61)

# ✅ ตาราง: รายจ่ายประจำ
df_reg = df_project[df_project["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_reg.empty:
    show_project_table(df_reg, "จ่ายรายจ่ายประจำ", disb_thres=57, spend_thres=58)

# ✅ ตาราง: รายจ่ายลงทุน
df_inv = df_project[df_project["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_inv.empty:
    show_project_table(df_inv, "จ่ายรายจ่ายลงทุน", disb_thres=35, spend_thres=66)

st.markdown("<br>", unsafe_allow_html=True)
#--------------------------------------

# --- SECTION 8: ลักษณะงาน ---
st.markdown("## 8️⃣ ลักษณะงาน")

# 🔽 สร้าง dropdown จาก 'ด้าน_ลักษณะงาน'
selected_dimension = st.selectbox("🔍เลือกด้านลักษณะงาน", sorted(df["ด้าน_ลักษณะงาน"].dropna().unique()))

# 🔎 กรองข้อมูลตามลักษณะงานที่เลือก
df_dim = df[df["ด้าน_ลักษณะงาน"] == selected_dimension].copy()

# 🔢 คำนวณ %เบิกจ่าย และ %ใช้จ่าย ใหม่
df_dim["%เบิกจ่าย"] = round((df_dim["เบิกจ่าย"] / df_dim["งบฯ หลังโอน"]) * 100, 2)
df_dim["%ใช้จ่าย"] = round((df_dim["ใช้จ่าย"] / df_dim["งบฯ หลังโอน"]) * 100, 2)

# 🎨 ฟังก์ชันใส่สี
def highlight_table(row, disb_thres, spend_thres):
    color_disb = "#00FF9F" if row["%เบิกจ่าย"] >= disb_thres else "#FF4B4B"
    color_spend = "#00FF9F" if row["%ใช้จ่าย"] >= spend_thres else "#FF4B4B"
    return ["", "", "", "", f"color: {color_disb}", "", f"color: {color_spend}"]

# 📋 ฟังก์ชันแสดงตาราง + สรุปยอด
def show_dimension_table(df_sub, title, disb_thres, spend_thres):
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

    st.markdown(f"### {title}")
    st.dataframe(styled, use_container_width=True)

# ✅ ตาราง: ภาพรวม
show_dimension_table(df_dim, "ภาพรวม", disb_thres=53, spend_thres=61)

# ✅ ตาราง: รายจ่ายประจำ
df_dim_reg = df_dim[df_dim["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายประจำ"]
if not df_dim_reg.empty:
    show_dimension_table(df_dim_reg, "รายจ่ายประจำ", disb_thres=57, spend_thres=58)

# ✅ ตาราง: รายจ่ายลงทุน
df_dim_inv = df_dim[df_dim["รายจ่ายประจำ/ลงทุน"] == "รายจ่ายลงทุน"]
if not df_dim_inv.empty:
    show_dimension_table(df_dim_inv, "รายจ่ายลงทุน", disb_thres=35, spend_thres=66)

#----------------------------------------
# --- Section: Footer Contact and Credits ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### Need help? Contact us!  
    📞 **Call**: +66 2 242 5900 ext. 7420  
    📧 **Email**: [pbo@parliament.go.th](mailto:pbo@parliament.go.th)  
    💬 **LINE ID**: @thaipbo
    """)

with col2:
    st.markdown("""
    #### สอบถามเพิ่มเติม  
    📞 **ติดต่อ**: +66 2 242 5900 ต่อ 7420  
    📧 **Email**: [pbo@parliament.go.th](mailto:pbo@parliament.go.th)  
    💬 **LINE ID**: @thaipbo
    """)

with col3:
    st.markdown("""
    #### เจ้าของผลงานและผู้รับผิดชอบ 
    🔹 ลิขสิทธิ์: สำนักงบประมาณของรัฐสภา (PBO)  
    🔹 ผู้รับผิดชอบ: **กุลธิดา สมศรี** และ **ศุภิกา ตรีรัตนไพบูลย์**  
    🔹 Coding writer: **กุลธิดา สมศรี**
    """)
