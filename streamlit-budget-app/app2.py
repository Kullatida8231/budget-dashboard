import streamlit as st
import pandas as pd
#from IPython.display import display, Markdown
    
#-------------------------------------------------------------------------------

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Dashboard งบประมาณ", layout="wide")

# --- โหลดข้อมูลจาก Excel ---
@st.cache_data
def load_data():
    file_path = "q1-68.xlsx"
    df = pd.read_excel(file_path, dtype=str, engine="openpyxl")

    # แปลงคอลัมน์ตัวเลข
    num_cols = ["พรบ.", "งบฯ หลังโอน", "เบิกจ่าย", "%เบิกจ่าย", "ใช้จ่าย", "%ใช้จ่าย"]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

    # แปลงหน่วยจากบาทเป็นล้านบาท
    df["พรบ.(ล้านบาท)"] = df["พรบ."] / 1_000_000
    df["งบฯ หลังโอน(ล้านบาท)"] = df["งบฯ หลังโอน"] / 1_000_000
    df["เบิกจ่าย(ล้านบาท)"] = df["เบิกจ่าย"] / 1_000_000
    df["ใช้จ่าย(ล้านบาท)"] = df["ใช้จ่าย"] / 1_000_000

    return df

df1 = load_data()

# --- ตรวจสอบว่ามีข้อมูลก่อน ---
if df1.empty:
    st.error("❌ ไม่พบข้อมูลในไฟล์ Excel")
    st.stop()

st.markdown("""
    <div style='
        background-color: #AC1B1F;
        color: black;
        text-align: center;
        padding: 1rem;
        font-size: 30px;
        font-weight: 700;
        border-radius: 6px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    '>
        ผลการเบิกจ่ายและใช้จ่ายงบประมาณ ณ สิ้นสุดไตรมาสที่ 1 ปีงบประมาณ พ.ศ. 2568
    </div>
""", unsafe_allow_html=True)

#----------------------------------------------------------------------------------
# 🟠 ส่วนที่ 1: ผลการเบิกจ่ายภาพรวม/ประจำ/ลงทุน
st.markdown("""
    <style>
    * {
        font-family: "Segoe UI", sans-serif !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    .uniform-font {
        font-size: 35px;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 27px;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .uniform-percent {
        font-size: 37px;
        font-weight: bold;
    }
    .metric-label {
        font-size: 16px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='uniform-font'>1️⃣🟠ภาพรวมทั้งประเทศ</div>", unsafe_allow_html=True)

def colored_text(value, color):
    return f"<span class='uniform-percent' style='color:{color}'>{value:.2f} %</span>"

# --- ภาพรวม ---
st.markdown("<div class='sub-header'>🏛️ ผลการเบิกจ่ายงบประมาณรายจ่ายภาพรวม</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

total_prb = round(df1['พรบ.(ล้านบาท)'].sum(), 4)
total_after = round(df1['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
total_disb = round(df1['เบิกจ่าย(ล้านบาท)'].sum(), 4)
total_spend = round(df1['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb = round((total_disb / total_after) * 100, 2) if total_after else 0
percent_spend = round((total_spend / total_after) * 100, 2) if total_after else 0

color_disb = "green" if percent_disb > 27 else "red"
color_spend = "green" if percent_spend > 37 else "red"

with col1:
    st.metric("พรบ.", f"{total_prb:,.4f}")
    st.metric("ใช้จ่าย", f"{total_spend:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{total_after:,.4f}")
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb, color_disb), unsafe_allow_html=True)
with col3:
    st.metric("เบิกจ่าย", f"{total_disb:,.4f}")
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend, color_spend), unsafe_allow_html=True)

# --- รายจ่ายประจำ ---
st.markdown("<div class='sub-header'>📜 ผลการเบิกจ่ายงบประมาณรายจ่ายประจำ</div>", unsafe_allow_html=True)
df_regular = df1[df1['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
prb_r = round(df_regular['พรบ.(ล้านบาท)'].sum(), 4)
after_r = round(df_regular['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_r = round(df_regular['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_r = round(df_regular['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
percent_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0

color_disb_r = "green" if percent_disb_r > 35 else "red"
color_spend_r = "green" if percent_spend_r > 36 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ประจำ)", f"{prb_r:,.4f}")
    st.metric("ใช้จ่าย", f"{spend_r:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_r:,.4f}")
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_r, color_disb_r), unsafe_allow_html=True)
with col3:
    st.metric("เบิกจ่าย", f"{disb_r:,.4f}")
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_r, color_spend_r), unsafe_allow_html=True)

# --- รายจ่ายลงทุน ---
st.markdown("<div class='sub-header'>🏗️ ผลการเบิกจ่ายงบประมาณรายจ่ายลงทุน</div>", unsafe_allow_html=True)
df_invest = df1[df1['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
prb_i = round(df_invest['พรบ.(ล้านบาท)'].sum(), 4)
after_i = round(df_invest['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_i = round(df_invest['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_i = round(df_invest['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
percent_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0

color_disb_i = "green" if percent_disb_i > 17 else "red"
color_spend_i = "green" if percent_spend_i > 39 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ลงทุน)", f"{prb_i:,.4f}")
    st.metric("ใช้จ่าย", f"{spend_i:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_i:,.4f}")
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_i, color_disb_i), unsafe_allow_html=True)
with col3:
    st.metric("เบิกจ่าย", f"{disb_i:,.4f}")
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_i, color_spend_i), unsafe_allow_html=True)



#----------------------------------------------------------------------------------

# 🔹 ส่วนที่ 2: Interactive dropdown
st.divider()
st.markdown("<div class='uniform-font'>2️⃣ รายกระทรวง</div>", unsafe_allow_html=True)

ministries = df1['กระทรวง'].dropna().unique()
selected_ministry = st.selectbox("เลือกกระทรวง", ministries)
filtered_df = df1[df1['กระทรวง'] == selected_ministry]

st.markdown(f"<div class='sub-header'> ผลการเบิกจ่ายของกระทรวง: <code>{selected_ministry}</code></div>", unsafe_allow_html=True)

st.markdown("<div class='sub-header'>🏛️ ผลการเบิกจ่ายงบประมาณรายจ่ายภาพรวม</div>", unsafe_allow_html=True)

sum_prb = round(filtered_df['พรบ.(ล้านบาท)'].sum(), 4)
sum_after = round(filtered_df['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
sum_disb = round(filtered_df['เบิกจ่าย(ล้านบาท)'].sum(), 4)
sum_spend = round(filtered_df['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb = round((sum_disb / sum_after) * 100, 2) if sum_after else 0
percent_spend = round((sum_spend / sum_after) * 100, 2) if sum_after else 0

color_disb = "green" if percent_disb > 27 else "red"
color_spend = "green" if percent_spend > 37 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ.", f"{sum_prb:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{sum_after:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{sum_disb:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{sum_spend:,.4f}")
with col5:
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb, color_disb), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend, color_spend), unsafe_allow_html=True)

# --- รายจ่ายประจำ ---
st.markdown("<div class='sub-header'>📜 ผลการเบิกจ่ายรายจ่ายประจำ</div>", unsafe_allow_html=True)
df_r = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
prb_r = round(df_r['พรบ.(ล้านบาท)'].sum(), 4)
after_r = round(df_r['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_r = round(df_r['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_r = round(df_r['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
percent_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0

color_disb_r = "green" if percent_disb_r > 35 else "red"
color_spend_r = "green" if percent_spend_r > 36 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ประจำ)", f"{prb_r:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_r:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{disb_r:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{spend_r:,.4f}")
with col5:
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_r, color_disb_r), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_r, color_spend_r), unsafe_allow_html=True)

# --- รายจ่ายลงทุน ---
st.markdown("<div class='sub-header'>🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน</div>", unsafe_allow_html=True)
df_i = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
prb_i = round(df_i['พรบ.(ล้านบาท)'].sum(), 4)
after_i = round(df_i['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_i = round(df_i['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_i = round(df_i['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
percent_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0

color_disb_i = "green" if percent_disb_i > 17 else "red"
color_spend_i = "green" if percent_spend_i > 39 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ลงทุน)", f"{prb_i:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_i:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{disb_i:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{spend_i:,.4f}")
with col5:
    st.markdown("<div class='metric-label'>%เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_i, color_disb_i), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_i, color_spend_i), unsafe_allow_html=True)
    
#----------------------------------------------------------------------------------

# 🔹 ส่วนที่ 3: ตารางสรุปผลเบิกจ่ายรายหน่วยงานแบบแยก 3 ส่วน 
st.divider()
st.markdown("<div class='uniform-font'>3️⃣รายหน่วยงาน</div>", unsafe_allow_html=True)

# --- Dropdown เลือกกระทรวง ---
selected_ministry = st.selectbox("เลือกกระทรวง (ตารางหน่วยงาน)", df1['กระทรวง'].dropna().unique())
filtered_df_all = df1[df1['กระทรวง'] == selected_ministry].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('หน่วยงาน').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    # เรียงคอลัมน์ใหม่
    ordered_cols = [
        'หน่วยงาน', 
        'พรบ.(ล้านบาท)', 
        'งบฯ หลังโอน(ล้านบาท)', 
        'เบิกจ่าย(ล้านบาท)', 
        '%เบิกจ่าย', 
        'ใช้จ่าย(ล้านบาท)', 
        '%ใช้จ่าย',
        'ประเภท'
    ]
    return group[ordered_cols]

# --- ฟังก์ชันจัดสีในตาราง ---
def highlight_cells(row):
    style = [''] * len(row)
    disb = row['%เบิกจ่าย']
    spend = row['%ใช้จ่าย']
    exp_type = row.get('ประเภท', '')

    # %เบิกจ่าย
    if exp_type == "รายจ่ายประจำ":
        style[4] = 'background-color: lightgreen' if disb > 35 else ('background-color: salmon' if disb < 35 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[4] = 'background-color: lightgreen' if disb > 17 else ('background-color: salmon' if disb < 17 else '')
    else:
        style[4] = 'background-color: lightgreen' if disb > 27 else ('background-color: salmon' if disb < 27 else '')

    # %ใช้จ่าย
    if exp_type == "รายจ่ายประจำ":
        style[6] = 'background-color: lightgreen' if spend > 36 else ('background-color: salmon' if spend < 36 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[6] = 'background-color: lightgreen' if spend > 39 else ('background-color: salmon' if spend < 39 else '')
    else:
        style[6] = 'background-color: lightgreen' if spend > 27 else ('background-color: salmon' if spend < 27 else '')

    return style

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)

#----------------------------------------------------------------------------------

# 🔹 ส่วนที่ 4: ผลการเบิกจ่ายรายยุทธศาสตร์
st.divider()
st.markdown("<div class='uniform-font'>4️⃣ รายยุทธศาสตร์</div>", unsafe_allow_html=True)

# Dropdown รายยุทธศาสตร์
strategy_list = df1['ยุทธศาสตร์การจัดสรร'].dropna().unique()
selected_strategy = st.selectbox("เลือกยุทธศาสตร์", strategy_list)
filtered_df = df1[df1['ยุทธศาสตร์การจัดสรร'] == selected_strategy]

# ชื่อยุทธศาสตร์ที่เลือก
st.markdown(f"<div class='sub-header'> ผลการเบิกจ่ายของยุทธศาสตร์: <code>{selected_strategy}</code></div>", unsafe_allow_html=True)

# ฟังก์ชันแสดงผลแต่ละหมวด
def display_budget_section(title, df, disb_threshold, spend_threshold):
    prb = round(df['พรบ.(ล้านบาท)'].sum(), 4)
    after = round(df['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
    disb = round(df['เบิกจ่าย(ล้านบาท)'].sum(), 4)
    spend = round(df['ใช้จ่าย(ล้านบาท)'].sum(), 4)
    percent_disb = round((disb / after) * 100, 2) if after else 0
    percent_spend = round((spend / after) * 100, 2) if after else 0

    st.markdown(f"<div class='sub-header'>{title}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("พรบ.", f"{prb:,.4f}")
    with col2:
        st.metric("งบฯ หลังโอน", f"{after:,.4f}")
    with col3:
        st.metric("เบิกจ่าย", f"{disb:,.4f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("ใช้จ่าย", f"{spend:,.4f}")
    with col5:
        st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
        st.markdown(colored_text(percent_disb, 'green' if percent_disb > disb_threshold else 'red'), unsafe_allow_html=True)
    with col6:
        st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
        st.markdown(colored_text(percent_spend, 'green' if percent_spend > spend_threshold else 'red'), unsafe_allow_html=True)

# แสดงกลุ่มที่ 1: ภาพรวม
st.markdown("<div class='sub-header'>🏛️ ผลการเบิกจ่ายงบประมาณรายจ่ายภาพรวม</div>", unsafe_allow_html=True)
display_budget_section("ภาพรวม", filtered_df, disb_threshold=27, spend_threshold=37)

# กลุ่มที่ 2: รายจ่ายประจำ
df_r = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
st.markdown("<div class='sub-header'>📜 ผลการเบิกจ่ายรายจ่ายประจำ</div>", unsafe_allow_html=True)
display_budget_section("รายจ่ายประจำ", df_r, disb_threshold=35, spend_threshold=36)

# กลุ่มที่ 3: รายจ่ายลงทุน
df_i = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
st.markdown("<div class='sub-header'>🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน</div>", unsafe_allow_html=True)
display_budget_section("รายจ่ายลงทุน", df_i, disb_threshold=17, spend_threshold=39)


#----------------------------------------------------------------------------------

# 🔹 ส่วนที่ 5: ผลการเบิกจ่ายงบประมาณ จำแนกรายด้าน
st.divider()
st.markdown("<div class='uniform-font'>5️⃣ งบประมาณรายด้าน</div>", unsafe_allow_html=True)

# Dropdown รายด้าน
dimension_list = df1['ด้าน_ลักษณะงาน'].dropna().unique()
selected_dimension = st.selectbox("เลือกด้าน/ลักษณะงาน", dimension_list)
filtered_df = df1[df1['ด้าน_ลักษณะงาน'] == selected_dimension]

# ชื่อด้านที่เลือก
st.markdown(f"<div class='sub-header'> ผลการเบิกจ่ายของด้าน: <code>{selected_dimension}</code></div>", unsafe_allow_html=True)

st.markdown("<div class='sub-header'>🏛️ ผลการเบิกจ่ายงบประมาณรายจ่ายภาพรวม</div>", unsafe_allow_html=True)

sum_prb = round(filtered_df['พรบ.(ล้านบาท)'].sum(), 4)
sum_after = round(filtered_df['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
sum_disb = round(filtered_df['เบิกจ่าย(ล้านบาท)'].sum(), 4)
sum_spend = round(filtered_df['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb = round((sum_disb / sum_after) * 100, 2) if sum_after else 0
percent_spend = round((sum_spend / sum_after) * 100, 2) if sum_after else 0

color_disb = "green" if percent_disb > 27 else "red"
color_spend = "green" if percent_spend > 37 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ.", f"{sum_prb:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{sum_after:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{sum_disb:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{sum_spend:,.4f}")
with col5:
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb, color_disb), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend, color_spend), unsafe_allow_html=True)

# --- รายจ่ายประจำ ---
st.markdown("<div class='sub-header'>📜 ผลการเบิกจ่ายรายจ่ายประจำ</div>", unsafe_allow_html=True)
df_r = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
prb_r = round(df_r['พรบ.(ล้านบาท)'].sum(), 4)
after_r = round(df_r['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_r = round(df_r['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_r = round(df_r['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_r = round((disb_r / after_r) * 100, 2) if after_r else 0
percent_spend_r = round((spend_r / after_r) * 100, 2) if after_r else 0

color_disb_r = "green" if percent_disb_r > 35 else "red"
color_spend_r = "green" if percent_spend_r > 36 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ประจำ)", f"{prb_r:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_r:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{disb_r:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{spend_r:,.4f}")
with col5:
    st.markdown("<div class='metric-label'> %เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_r, color_disb_r), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_r, color_spend_r), unsafe_allow_html=True)

# --- รายจ่ายลงทุน ---
st.markdown("<div class='sub-header'>🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน</div>", unsafe_allow_html=True)
df_i = filtered_df[filtered_df['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
prb_i = round(df_i['พรบ.(ล้านบาท)'].sum(), 4)
after_i = round(df_i['งบฯ หลังโอน(ล้านบาท)'].sum(), 4)
disb_i = round(df_i['เบิกจ่าย(ล้านบาท)'].sum(), 4)
spend_i = round(df_i['ใช้จ่าย(ล้านบาท)'].sum(), 4)
percent_disb_i = round((disb_i / after_i) * 100, 2) if after_i else 0
percent_spend_i = round((spend_i / after_i) * 100, 2) if after_i else 0

color_disb_i = "green" if percent_disb_i > 17 else "red"
color_spend_i = "green" if percent_spend_i > 39 else "red"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("พรบ. (ลงทุน)", f"{prb_i:,.4f}")
with col2:
    st.metric("งบฯ หลังโอน", f"{after_i:,.4f}")
with col3:
    st.metric("เบิกจ่าย", f"{disb_i:,.4f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("ใช้จ่าย", f"{spend_i:,.4f}")
with col5:
    st.markdown("<div class='metric-label'>%เบิกจ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_disb_i, color_disb_i), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='metric-label'> %ใช้จ่าย</div>", unsafe_allow_html=True)
    st.markdown(colored_text(percent_spend_i, color_spend_i), unsafe_allow_html=True)

#----------------------------------------------------------------------------------
# 🔹 ส่วนที่ 6: ผลการเบิกจ่ายงบประมาณรายจ่ายงบกลาง
st.divider()
st.markdown("<div class='uniform-font'>6️⃣ รายจ่ายงบกลาง</div>", unsafe_allow_html=True)

# --- กรองเฉพาะกระทรวงงบกลาง ---
filtered_df_all = df1[df1['กระทรวง'] == "งบกลาง"].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('ผลผลิต/โครงการ').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    ordered_cols = [
        'ผลผลิต/โครงการ',
        'พรบ.(ล้านบาท)',
        'งบฯ หลังโอน(ล้านบาท)',
        'เบิกจ่าย(ล้านบาท)',
        '%เบิกจ่าย',
        'ใช้จ่าย(ล้านบาท)',
        '%ใช้จ่าย',
        'ประเภท'
    ]
    return group[ordered_cols].sort_values(by='%เบิกจ่าย', ascending=True)

# --- ฟังก์ชันจัดสีในตาราง ---
def highlight_cells(row):
    style = [''] * len(row)
    disb = row['%เบิกจ่าย']
    spend = row['%ใช้จ่าย']
    exp_type = row.get('ประเภท', '')

    if exp_type == "รายจ่ายประจำ":
        style[4] = 'background-color: lightgreen' if disb > 35 else ('background-color: salmon' if disb < 35 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[4] = 'background-color: lightgreen' if disb > 17 else ('background-color: salmon' if disb < 17 else '')
    else:
        style[4] = 'background-color: lightgreen' if disb > 27 else ('background-color: salmon' if disb < 27 else '')

    if exp_type == "รายจ่ายประจำ":
        style[6] = 'background-color: lightgreen' if spend > 36 else ('background-color: salmon' if spend < 36 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[6] = 'background-color: lightgreen' if spend > 39 else ('background-color: salmon' if spend < 39 else '')
    else:
        style[6] = 'background-color: lightgreen' if spend > 27 else ('background-color: salmon' if spend < 27 else '')

    return style

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)

#----------------------------------------------------------------------------------

# 🔹 ส่วนที่ 7: ผลการเบิกจ่ายงบประมาณตามกลุ่มแผนงาน
st.divider()
st.markdown("<div class='uniform-font'>7️⃣ กลุ่มแผนงาน</div>", unsafe_allow_html=True)

# --- Dropdown เลือกกลุ่มแผนงาน ---
selected_group = st.selectbox("เลือกกลุ่มแผนงาน", df1['กลุ่มแผนงาน'].dropna().unique())
filtered_df_all = df1[df1['กลุ่มแผนงาน'] == selected_group].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('แผนงาน').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    ordered_cols = [
        'แผนงาน',
        'พรบ.(ล้านบาท)',
        'งบฯ หลังโอน(ล้านบาท)',
        'เบิกจ่าย(ล้านบาท)',
        '%เบิกจ่าย',
        'ใช้จ่าย(ล้านบาท)',
        '%ใช้จ่าย',
        'ประเภท'
    ]
    group = group[ordered_cols]
    group = group.sort_values(by='%เบิกจ่าย', ascending=True)
    return group

# --- ฟังก์ชันจัดสีในตาราง ---
def highlight_cells(row):
    style = [''] * len(row)
    disb = row['%เบิกจ่าย']
    spend = row['%ใช้จ่าย']
    exp_type = row.get('ประเภท', '')

    if exp_type == "รายจ่ายประจำ":
        style[4] = 'background-color: lightgreen' if disb > 35 else ('background-color: salmon' if disb < 35 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[4] = 'background-color: lightgreen' if disb > 17 else ('background-color: salmon' if disb < 17 else '')
    else:
        style[4] = 'background-color: lightgreen' if disb > 27 else ('background-color: salmon' if disb < 27 else '')

    if exp_type == "รายจ่ายประจำ":
        style[6] = 'background-color: lightgreen' if spend > 36 else ('background-color: salmon' if spend < 36 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[6] = 'background-color: lightgreen' if spend > 39 else ('background-color: salmon' if spend < 39 else '')
    else:
        style[6] = 'background-color: lightgreen' if spend > 27 else ('background-color: salmon' if spend < 27 else '')

    return style

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)

#----------------------------------------------------------------------------------
# 🔹 ส่วนที่ 8: ผลการเบิกจ่ายงบประมาณรายจังหวัด
st.divider()
st.markdown("<div class='uniform-font'>8️⃣ รายจังหวัด</div>", unsafe_allow_html=True)

# --- Dropdown เลือกจังหวัด ---
selected_province = st.selectbox("เลือกจังหวัด/กลุ่มจังหวัด", df1['จังหวัด/กลุ่มจังหวัด'].dropna().unique())
filtered_df_all = df1[df1['จังหวัด/กลุ่มจังหวัด'] == selected_province].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('หน่วยงาน').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    ordered_cols = [
        'หน่วยงาน',
        'พรบ.(ล้านบาท)',
        'งบฯ หลังโอน(ล้านบาท)',
        'เบิกจ่าย(ล้านบาท)',
        '%เบิกจ่าย',
        'ใช้จ่าย(ล้านบาท)',
        '%ใช้จ่าย',
        'ประเภท'
    ]
    return group[ordered_cols].sort_values(by='%เบิกจ่าย', ascending=True)

# --- ฟังก์ชันจัดสีในตาราง ---
def highlight_cells(row):
    style = [''] * len(row)
    disb = row['%เบิกจ่าย']
    spend = row['%ใช้จ่าย']
    exp_type = row.get('ประเภท', '')

    if exp_type == "รายจ่ายประจำ":
        style[4] = 'background-color: lightgreen' if disb > 35 else ('background-color: salmon' if disb < 35 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[4] = 'background-color: lightgreen' if disb > 17 else ('background-color: salmon' if disb < 17 else '')
    else:
        style[4] = 'background-color: lightgreen' if disb > 27 else ('background-color: salmon' if disb < 27 else '')

    if exp_type == "รายจ่ายประจำ":
        style[6] = 'background-color: lightgreen' if spend > 36 else ('background-color: salmon' if spend < 36 else '')
    elif exp_type == "รายจ่ายลงทุน":
        style[6] = 'background-color: lightgreen' if spend > 39 else ('background-color: salmon' if spend < 39 else '')
    else:
        style[6] = 'background-color: lightgreen' if spend > 27 else ('background-color: salmon' if spend < 27 else '')

    return style

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)
#----------------------------------------------------------------------------------
# 🔹 ส่วนที่ 9: ผลการเบิกจ่ายงบประมาณของหน่วยงานรัฐสภา
st.divider()
st.markdown("<div class='uniform-font'>9️⃣ หน่วยงานของรัฐสภา</div>", unsafe_allow_html=True)

# --- Dropdown เลือกหน่วยงาน ---
filtered_df_base = df1[df1['กระทรวง'] == "หน่วยงานของรัฐสภา"]
selected_agency = st.selectbox("เลือกหน่วยงาน", filtered_df_base['หน่วยงาน'].dropna().unique())
filtered_df_all = filtered_df_base[filtered_df_base['หน่วยงาน'] == selected_agency].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('ผลผลิต/โครงการ').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    ordered_cols = [
        'ผลผลิต/โครงการ',
        'พรบ.(ล้านบาท)',
        'งบฯ หลังโอน(ล้านบาท)',
        'เบิกจ่าย(ล้านบาท)',
        '%เบิกจ่าย',
        'ใช้จ่าย(ล้านบาท)',
        '%ใช้จ่าย',
        'ประเภท'
    ]
    return group[ordered_cols].sort_values(by='%เบิกจ่าย', ascending=True)

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)

#----------------------------------------------------------------------------------
# 🔹 ส่วนที่ 10: ผลการเบิกจ่ายรายรหัสงบประมาณ (เลือกจากชื่อโครงการ)
st.divider()
st.markdown("<div class='uniform-font'>🔟 ผลการเบิกจ่ายรายรหัสงบประมาณ (เลือกจากชื่อโครงการ)</div>", unsafe_allow_html=True)

# --- ช่องกรอกข้อความเพื่อกรองชื่อโครงการ ---
search_text = st.text_input("🔍 พิมพ์คำค้นหาเพื่อเลือกชื่อโครงการ")

# --- กรองชื่อโครงการตามข้อความที่ค้นหา ---
project_options = df1['ผลผลิต/โครงการ'].dropna().unique()
filtered_options = [proj for proj in project_options if search_text.lower() in proj.lower()]
selected_project = st.selectbox("เลือกชื่อโครงการที่ต้องการดูข้อมูล", filtered_options)

# --- กรองข้อมูลตามโครงการที่เลือก ---
filtered_df_all = df1[df1['ผลผลิต/โครงการ'] == selected_project].copy()

# --- ฟังก์ชันรวมข้อมูล ---
def aggregate_table(df, exp_type_label):
    group = df.groupby('ชื่อรหัสงบประมาณ').agg({
        'พรบ.(ล้านบาท)': 'sum',
        'งบฯ หลังโอน(ล้านบาท)': 'sum',
        'เบิกจ่าย(ล้านบาท)': 'sum',
        'ใช้จ่าย(ล้านบาท)': 'sum'
    }).reset_index()

    group['%เบิกจ่าย'] = (group['เบิกจ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['%ใช้จ่าย'] = (group['ใช้จ่าย(ล้านบาท)'] / group['งบฯ หลังโอน(ล้านบาท)']) * 100
    group['ประเภท'] = exp_type_label

    return group[[
        'ชื่อรหัสงบประมาณ',
        'พรบ.(ล้านบาท)',
        'งบฯ หลังโอน(ล้านบาท)',
        'เบิกจ่าย(ล้านบาท)',
        '%เบิกจ่าย',
        'ใช้จ่าย(ล้านบาท)',
        '%ใช้จ่าย',
        'ประเภท'
    ]]

# --- ฟังก์ชันไฮไลต์ ---
def highlight_cells(row):
    style = [''] * len(row)
    disb = row['%เบิกจ่าย']
    spend = row['%ใช้จ่าย']
    exp_type = row.get('ประเภท', '')

    if exp_type == "รายจ่ายประจำ":
        style[4] = 'background-color: lightgreen' if disb > 35 else 'background-color: salmon'
        style[6] = 'background-color: lightgreen' if spend > 36 else 'background-color: salmon'
    elif exp_type == "รายจ่ายลงทุน":
        style[4] = 'background-color: lightgreen' if disb > 17 else 'background-color: salmon'
        style[6] = 'background-color: lightgreen' if spend > 39 else 'background-color: salmon'
    else:
        style[4] = 'background-color: lightgreen' if disb > 27 else 'background-color: salmon'
        style[6] = 'background-color: lightgreen' if spend > 27 else 'background-color: salmon'

    return style

# --- กลุ่มที่ 1: ภาพรวม ---
st.subheader("🏛️ ผลการเบิกจ่ายรายจ่ายภาพรวม")
df_all = aggregate_table(filtered_df_all, "ภาพรวม")
styled_all = (
    df_all.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_all, use_container_width=True)

# --- กลุ่มที่ 2: รายจ่ายประจำ ---
st.subheader("📜 ผลการเบิกจ่ายรายจ่ายประจำ")
df_regular = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายประจำ"]
df_grouped_regular = aggregate_table(df_regular, "รายจ่ายประจำ")
styled_regular = (
    df_grouped_regular.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_regular, use_container_width=True)

# --- กลุ่มที่ 3: รายจ่ายลงทุน ---
st.subheader("🏗️ ผลการเบิกจ่ายรายจ่ายลงทุน")
df_invest = filtered_df_all[filtered_df_all['รายจ่ายประจำ/ลงทุน'] == "รายจ่ายลงทุน"]
df_grouped_invest = aggregate_table(df_invest, "รายจ่ายลงทุน")
styled_invest = (
    df_grouped_invest.drop(columns=['ประเภท'])
    .style
    .format({
        'พรบ.(ล้านบาท)': '{:,.4f}',
        'งบฯ หลังโอน(ล้านบาท)': '{:,.4f}',
        'เบิกจ่าย(ล้านบาท)': '{:,.4f}',
        'ใช้จ่าย(ล้านบาท)': '{:,.4f}',
        '%เบิกจ่าย': '{:.2f}',
        '%ใช้จ่าย': '{:.2f}'
    })
    .apply(highlight_cells, axis=1)
)
st.dataframe(styled_invest, use_container_width=True)



#----------------------------------------------------------------------------------