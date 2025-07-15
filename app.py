import streamlit as st
import random

st.set_page_config(page_title="ランダム席替え", layout="centered")
st.title("🎯 完全ランダム席替えジェネレーター")

# 1. 初期設定（初回のみ）
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.remaining_ids = []
    st.session_state.remaining_seats = []
    st.session_state.assigned = {}
    st.session_state.current_student = None
    st.session_state.current_seat = None

# 2. 初期設定入力（未初期化時のみ）
if not st.session_state.initialized:
    with st.form("setup_form"):
        max_id = st.number_input("🧑‍🎓 出席番号の最大値", min_value=1, max_value=100, value=40)
        rows = st.number_input("🪑 行数（前から後ろ）", min_value=1, max_value=20, value=5)
        cols = st.number_input("🪑 列数（左から右）", min_value=1, max_value=20, value=8)
        submitted = st.form_submit_button("✅ 初期化して開始")

        if submitted:
            total_seats = rows * cols
            if max_id > total_seats:
                st.error(f"生徒数（{max_id}）が座席数（{total_seats}）を超えています")
            else:
                st.session_state.remaining_ids = list(range(1, max_id + 1))
                st.session_state.remaining_seats = [(r, c) for r in range(rows) for c in range(cols)]
                st.session_state.assigned = {}
                st.session_state.rows = rows
                st.session_state.cols = cols
                st.session_state.initialized = True
                st.rerun()

# 3. メイン処理
else:
    st.subheader("🎲 次の生徒をランダムに抽選")

    if st.button("🔔 次の生徒を抽選"):
        if st.session_state.remaining_ids and st.session_state.remaining_seats:
            sid = random.choice(st.session_state.remaining_ids)
            seat = random.choice(st.session_state.remaining_seats)

            st.session_state.remaining_ids.remove(sid)
            st.session_state.remaining_seats.remove(seat)
            st.session_state.assigned[sid] = seat
            st.session_state.current_student = sid
            st.session_state.current_seat = seat
        else:
            st.warning("すべての生徒に席が割り当てられました。")

    # 現在の抽選結果表示
    if st.session_state.current_student is not None:
        r, c = st.session_state.current_seat
        st.success(f"🧑‍🎓 {st.session_state.current_student} 番さんの席が決まりました → 位置: {r+1} 行 {c+1} 列")

    # 座席表の可視化
    st.subheader("🪑 現在の座席表")
    seat_grid = [["" for _ in range(st.session_state.cols)] for _ in range(st.session_state.rows)]
    for sid, (r, c) in st.session_state.assigned.items():
        icon = "🧑‍🎓" if sid % 2 == 1 else "👩‍🎓"
        seat_grid[r][c] = f"{icon}{sid}"

    for row in seat_grid:
        cols = st.columns(st.session_state.cols)
        for i, cell in enumerate(row):
            with cols[i]:
                st.markdown(cell or "　")

    # 完了メッセージ
    if not st.session_state.remaining_ids:
        st.success("🎉 全員の席が決まりました！")

    # リセット
    if st.button("🔁 やり直す（リセット）"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
