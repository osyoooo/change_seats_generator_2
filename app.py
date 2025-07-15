import streamlit as st
import random

st.set_page_config(page_title="ランダム席決め", layout="centered")
st.title("🎯 ステップ式ランダム席替えアプリ")

# 初期化
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.remaining_ids = []
    st.session_state.remaining_seats = []
    st.session_state.assigned = {}
    st.session_state.current_student = None
    st.session_state.current_seat = None

# 初期設定（フォーム）
if not st.session_state.initialized:
    with st.form("setup_form"):
        max_id = st.number_input("🧑‍🎓 出席番号の最大値", 1, 100, 40)
        rows = st.number_input("🪑 行数（前から後ろ）", 1, 20, 5)
        cols = st.number_input("🪑 列数（左から右）", 1, 20, 8)
        submitted = st.form_submit_button("✅ 初期化して開始")

        if submitted:
            total_seats = rows * cols
            if max_id > total_seats:
                st.error("座席数より生徒数が多いです。")
            else:
                st.session_state.remaining_ids = list(range(1, max_id + 1))
                st.session_state.remaining_seats = [(r, c) for r in range(rows) for c in range(cols)]
                st.session_state.assigned = {}
                st.session_state.rows = rows
                st.session_state.cols = cols
                st.session_state.initialized = True
                st.rerun()

else:
    st.subheader("👤 現在の状態")

    if not st.session_state.remaining_ids:
        st.success("🎉 全員の席が決まりました！")
    else:
        # Step 1: 出席番号の抽選
        if st.session_state.current_student is None:
            if st.button("🎲 出席番号をランダムに抽選"):
                sid = random.choice(st.session_state.remaining_ids)
                st.session_state.current_student = sid
                st.rerun()
        else:
            st.info(f"✅ {st.session_state.current_student} 番さんが選ばれました")

            # Step 2: 座席決定（ボタン押下）
            if st.button("📍 空いている席をランダムに割り当て"):
                seat = random.choice(st.session_state.remaining_seats)
                st.session_state.assigned[st.session_state.current_student] = seat
                st.session_state.remaining_ids.remove(st.session_state.current_student)
                st.session_state.remaining_seats.remove(seat)
                st.success(f"{st.session_state.current_student} 番さんの席：{seat[0]+1} 行 {seat[1]+1} 列に決定！")
                st.session_state.current_student = None
                st.rerun()

    # 座席表の表示
    st.subheader("🪑 現在の座席表")

    seat_grid = [["" for _ in range(st.session_state.cols)] for _ in range(st.session_state.rows)]
    for sid, (r, c) in st.session_state.assigned.items():
        icon = "🧑‍🎓" if sid % 2 == 1 else "👩‍🎓"
        seat_grid[r][c] = f"{icon}{sid}"

    # 表形式で表示
    table_html = "<table style='border-collapse: collapse;'>"
    for row in seat_grid:
        table_html += "<tr>"
        for cell in row:
            table_html += f"<td style='border: 1px solid gray; padding: 8px; text-align: center; width: 50px; height: 50px;'>{cell or ' '}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # リセット
    if st.button("🔁 リセットしてやり直す"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
