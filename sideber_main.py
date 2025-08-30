import streamlit as st
import csv
from datetime import datetime
from PIL import Image

# ====背景色（変更）====
# ページの設定（タイトルなど）
st.set_page_config(page_title="背景色変更サンプル")

# CSS を書いて背景色を設定
page_bg = """
<style>
/* 全体の背景色 */
.stApp {
    background-color:#AEC6CF;  /* パステルブルー */
    color: black; /* 文字色を黒に指定 */
}

/* サイドバーの背景色 */
[data-testid="stSidebar"] {
    background-color: #FFFFF0;  /* アイボリー */
}
</style>
"""

# CSS を反映
st.markdown(page_bg, unsafe_allow_html=True)


# 定数・設定
FOOD_MENU_FILE = "food_menu.csv"
FOOD_ORDER_FILE = "order_history.csv"

# ====セッション状態====
# 追加注文-画面状態管理-A
if "step_order_add" not in st.session_state:
    st.session_state["step_order_add"] = 1

# 店員呼出-画面状態管理-C
if "step_callclerk" not in st.session_state:
    st.session_state["step_callclerk"] = 1

# お会計-画面状態管理-D
if "step_checkout" not in st.session_state:
    st.session_state["step_checkout"] = 1

# サイドバー状態管理
if "page" not in st.session_state:
    st.session_state["page"] = None

# フードID管理
if "food_id" not in st.session_state:
    st.session_state["food_id"] = 0


# 数量データ管理
if "f_q" not in st.session_state:
    st.session_state["f_q"] = 0


# ====関数管理=====
# ページ管理(追加注文）
def next_to_step_order_add(num):
    st.session_state["step_order_add"] = num


# ページ管理（店員呼出）
def next_to_step_callclerk(num):
    st.session_state["step_callclerk"] = num


# ページ管理（お会計）
def next_to_step_checkout(num):
    st.session_state["step_checkout"] = num


# ページ管理（メインプログラム）
def next_to_page(page):
    st.session_state["page"] = page


# フードid
def food_id_add(num_id):
    st.session_state["food_id"] = num_id


# 数量管理
def quantity_add(num_q):
    st.session_state["f_q"] = num_q


# フードメニュー表示
def show_food_menu(new_reader):
    food_image = Image.open("Carbonara.jpg")
    for key, el in new_reader.items():
        food_image = f"{el['画像']}"
        st.image(food_image, width=100)
        st.text(f"{key}[{el['商品名']}:{el['価格']}円]")


# CSV→辞書形式で読み込み
def foodmenu_to_dict(filename):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        new_reader = {}
        start_num = 1001  # キーの開始番号
        for i, row in enumerate(reader):
            key = start_num + i
            new_reader[key] = row
    return new_reader


# "注文履歴.csv"ファイル読み込み
def foodorder_reading(filname):
    with open(filname, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        order_list = []
        for row in reader:
            order_list.append(row)
        return order_list


# 注文商品を"注文履歴.csv"に保存
def orderfood_to_keepcsv(date, datetime, foodname, food_qauntity, food_price):
    with open(FOOD_ORDER_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, datetime, foodname, food_qauntity, food_price])


# 金額計算(各注文毎)
def calcu_order_history(order_list):
    calcu_result = []
    for element in order_list:
        calcu_mult = int(element["数量"]) * int(element["価格"])
        calcu_result.append(calcu_mult)
    return calcu_result


# 合計金額計算
def sum_calcu(calcu_result):
    sum_result = sum(calcu_result)
    return sum_result


# ユーザー入力数字
def num4_input():
    num_input = st.number_input(
        label="数字4桁を入力してください", value=1001, min_value=1001, max_value=1019
    )
    return num_input


# ====メインプログラム====
# サイドバー
st.sidebar.text("【操作バー】")
select_page = st.sidebar.selectbox(
    "選択", ["メニュー", "追加注文", "注文履歴", "お会計", "店員呼出"]
)

st.session_state["page"] = select_page


# 画面構成-メニュー操作-(メインプログラム)
if select_page == "メニュー":
    st.title("メニュー")
    st.text(
        "■左の操作バーから「追加注文」「注文履歴」「お会計」「店員呼出」のいずれかを選択してください。\n(スマートフォンの場合「＞＞」を押してください。\n押した後画面の真ん中を再度押してください)"
    )

# 画面構成【A】-追加注文-（メインプログラム）
elif select_page == "追加注文":
    st.title("-注文追加-")

    if st.session_state["step_order_add"] == 1:
        col1, col2 = st.columns([1, 2])
        with col1:
            num_input = num4_input()

            if st.button("次へ"):
                found = False  # 入力されたidがあるか探している
                food_menu = foodmenu_to_dict(FOOD_MENU_FILE)
                for k in food_menu:
                    if num_input == k:
                        found = True
                        food_id_add(num_input)
                        next_to_step_order_add(2)
                        st.rerun()

                if not found:
                    st.error("フードメニューに存在しない番号です")

        with col2:
            food_menu = foodmenu_to_dict(FOOD_MENU_FILE)
            show_menu = show_food_menu(food_menu)

    # サブ画面構成【2】-数量画面-
    elif st.session_state["step_order_add"] == 2:

        with st.form(key="food_quantity"):
            food_quantity = st.number_input(label="数量を入力してください", value=1)
            user_select = st.selectbox("選択してください", ("追加", "キャンセル"))

            user_st_pd = st.form_submit_button("次へ")

        if user_st_pd:
            if user_select == "追加":
                quantity_add(food_quantity)
                next_to_step_order_add(3)
                st.rerun()

            elif user_select == "キャンセル":
                next_to_step_order_add(1)
                st.rerun()

    # サブ画面構成【3】-注文カゴ-
    elif st.session_state["step_order_add"] == 3:
        st.text("注文内容を確認してください")

        with st.form(key="order_basket"):
            session_food_id = st.session_state["food_id"]
            session_food_quantity = st.session_state["f_q"]
            food_menu = foodmenu_to_dict(FOOD_MENU_FILE)
            food_num1 = st.number_input(
                label=f"{food_menu[session_food_id]['商品名']}",
                value=session_food_quantity,
                step=1,
            )
            user_select = st.selectbox("選択してください", ("注文", "キャンセル"))

            user_st_pd = st.form_submit_button("次へ")

        if user_st_pd:
            if user_select == "注文":
                next_to_step_order_add(4)
                st.rerun()

            elif user_select == "キャンセル":
                next_to_step_order_add(1)
                st.rerun()

    # サブ画面構成【4】-注文完了画面-
    elif st.session_state["step_order_add"] == 4:
        session_food_quantity = st.session_state["f_q"]
        session_food_id = st.session_state["food_id"]
        food_menu = foodmenu_to_dict(FOOD_MENU_FILE)
        st.text("注文完了しました")
        st.text(
            f"・{food_menu[session_food_id]['商品名']}:{food_menu[session_food_id]['価格']}円×{session_food_quantity}個\n上記のメニューを注文完了しました"
        )
        order_time = datetime.now().strftime("%H時%M分")
        order_day = datetime.now().strftime("%Y年%m月%d日")

        keep_order_csv = orderfood_to_keepcsv(
            order_day,
            order_time,
            food_menu[session_food_id]["商品名"],
            session_food_quantity,
            food_menu[session_food_id]["価格"],
        )

        user_st_pd = st.button("追加画面へ戻る")
        next_to_step_order_add(1)
        st.rerun()


# 画面構成【B】-注文履歴-（メインプログラム）
elif select_page == "注文履歴":
    st.text("【注文履歴】")

    order_history = foodorder_reading(FOOD_ORDER_FILE)
    calcu_result = calcu_order_history(order_history)
    sum_result = sum_calcu(calcu_result)
    for x in order_history:
        st.text(f"{x['商品名']}:{x['数量']}個:{x['価格']}円")
    st.text(f"【合計金額】:{sum_result}円")


# 画面構成【C】-店員呼び出し-(メインプログラム)
elif select_page == "店員呼出":
    st.header("店員呼出")

    # サブ画面構成【1】-店員呼出-
    if st.session_state["step_callclerk"] == 1:
        clerk_call_op = st.radio("店員を呼び出しますか？", ("はい"))
        if st.button("次へ"):
            if clerk_call_op == "はい":
                next_to_step_callclerk(2)
                st.rerun()

    # サブ画面構成【2】-店員呼出確認-
    elif st.session_state["step_callclerk"] == 2:
        st.text("店員が来るまで少々お待ちください。")
        next_to_step_callclerk(1)


# 画面構成【D】-お会計-
elif select_page == "お会計":
    st.title("お会計")

    # サブ画面構成【7】-お会計選択-
    if st.session_state["step_checkout"] == 1:
        checkput_op = st.radio("お会計しますか？", ("はい"))

        user_st_pd = st.button("次へ")

        if user_st_pd:
            if checkput_op == "はい":
                next_to_step_checkout(2)
                st.rerun()

    # サブ画面構成【8】-お会計確認画面-
    elif st.session_state["step_checkout"] == 2:
        order_history = foodorder_reading(FOOD_ORDER_FILE)
        calcu_result = calcu_order_history(order_history)
        sum_result = sum_calcu(calcu_result)

        st.text("-お会計確認-")
        st.text(f"【合計金額】:{sum_result}円")
        st.text(
            "金額ご確認の上、レジにて以下のQRコードを読み取りお支払いしてください。"
        )

        QR_image = Image.open("qrcode.png")
        st.image(QR_image, width=200)

        next_to_step_checkout(1)
