import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart CRM - Dashboard Phan Khuc KH", layout="wide")
st.title("SMART CRM - MEKONG MOBILE (LUONG L1)")
st.subheader("Bao cao Phan bo Phan khuc va Danh sach Tiep thi Muc tieu")

def get_connection():
    return sqlite3.connect("dwh.db")

try:
    conn = get_connection()
    query = """
    SELECT 
        c.customer_id, 
        c.full_name, 
        c.mask_phone, 
        f.total_spent_12m, 
        f.total_orders_12m, 
        f.segment_code 
    FROM dim_customer c 
    JOIN fact_customer_segment f ON c.customer_key = f.customer_key 
    WHERE c.is_deleted = 0
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        st.warning("Chua co du lieu trong Kho du lieu. Vui long chay python pipeline.py truoc!")
    else:
        st.markdown("### 1. Phan bo Phan khuc Khach hang (QT-12)")
        col1, col2 = st.columns([1, 2])

        segment_counts = df["segment_code"].value_counts()

        with col1:
            st.metric("Tong so khach hang sach", len(df))
            st.dataframe(
                segment_counts.reset_index().rename(
                    columns={"segment_code": "Phan khuc", "count": "So luong"}
                )
            )

        with col2:
            fig, ax = plt.subplots(figsize=(6, 3))
            colors = {
                "VIP": "#E53E3E",
                "REGULAR": "#3182CE",
                "NEW": "#38A169",
                "DORMANT": "#718096",
            }
            bar_colors = [colors.get(x, "#A0AEC0") for x in segment_counts.index]
            ax.bar(segment_counts.index, segment_counts.values, color=bar_colors)
            ax.set_ylabel("So luong KH")
            ax.set_title("Bieu do Phan bo Phan khuc Khach hang")
            st.pyplot(fig)

        st.divider()

        st.markdown("### 2. Loc va Xuat Danh sach Tiep thi Muc tieu (Che SDT QT-15)")

        selected_segment = st.selectbox(
            "Loc theo Phan khuc:", ["TAT CA"] + list(df["segment_code"].unique())
        )

        if selected_segment != "TAT CA":
            df_filtered = df[df["segment_code"] == selected_segment]
        else:
            df_filtered = df.copy()

        st.write(f"Tim thay {len(df_filtered)} khach hang phu hop:")
        st.dataframe(
            df_filtered[[
                "customer_id",
                "full_name",
                "mask_phone",
                "total_spent_12m",
                "total_orders_12m",
                "segment_code",
            ]]
        )

        csv_data = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Xuat danh sach CSV (Che SDT QT-15)",
            data=csv_data,
            file_name=f"danh_sach_kh_{selected_segment.lower()}.csv",
            mime="text/csv",
        )

except Exception as e:
    st.error(f"Loi ket noi CSDL hoac truy van: {e}")