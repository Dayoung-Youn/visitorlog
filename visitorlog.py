import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 저장할 엑셀 파일 이름
FILE_NAME = "guestbook.xlsx"

# 기존 데이터 불러오기
if os.path.exists(FILE_NAME):
    df = pd.read_excel(FILE_NAME)
else:
    df = pd.DataFrame(columns=["이름", "메시지", "날짜"])

st.title("📖 VerdeVivo와 함께하는 의류 교환 파티 온라인 방명록")
st.sidebar.title("방명록 찾기")

# 사이드바에서 이름 입력
search_name = st.sidebar.text_input("이름을 입력하세요", value="")

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["✍️ 작성하기", "📋 목록보기", "👚 의류 교환 파티란?", "♻️ 베르데비보란?"])

with tab1:  # 방명록 작성 탭
    with st.form("guest_form"):
        name = st.text_input("이름을 입력하세요")
        message = st.text_area("메시지를 남겨주세요")
        submitted = st.form_submit_button("저장하기")

        # 안내 카드: 세련되게, 글자 크기 조절
        st.markdown(
            """
                <div style="
                    color: #f8f9fa;              /* 연한 회색 글자 */
                
                ✅  저장하기 버튼을 누른 후, 저장 완료 메시지가 나타나면 '목록보기'에서 작성한 내용을 확인할 수 있어요.<br>🔍  좌측 칼럼을 통해 작성자명을 기준으로 방명록을 검색할 수 있어요.
                </div>
                """,
                unsafe_allow_html=True
            )

        if submitted:
            if name and message:
                new_entry = pd.DataFrame({
                    "이름": [name],
                    "메시지": [message],
                    "날짜": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")]
                    })
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_excel(FILE_NAME, index=False)
                st.success("방명록에 저장되었습니다! ✅")
            else:
                st.warning("이름과 메시지를 모두 입력해주세요.")

    with tab2:  # 방명록 목록 탭
        st.subheader("📋 방명록 목록")

        # 이름으로 필터링
        if search_name:
            filtered_df = df[df["이름"].str.contains(search_name)]
            if filtered_df.empty:
                st.info(f"'{search_name}' 이름의 방명록이 없습니다.")
        else:
            filtered_df = df

        cards_per_row = 3  # 한 줄에 보여줄 카드 수
        for i in range(0, len(filtered_df), cards_per_row):
            cols = st.columns(cards_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered_df):
                    row = filtered_df.iloc[i + j]
                    with col:
                        st.markdown(
                            f"""
                        <div style="
                            background-color:#f8f9fa;
                            padding:15px;
                            margin-bottom:10px;
                            border-radius:12px;
                            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                            height:auto;
                        ">
                            <p style="font-size:15px; color:#333;">{row['메시지']}</p>
                            <p style="font-size:13px; color:gray; text-align:right;">- {row['이름']} ({row['날짜']})</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # 관리자 전용 다운로드 기능
        st.write("---")
        admin_pw = st.text_input("🔑 관리자 비밀번호 입력", type="password")
        if admin_pw == "admin123":  # 원하는 비밀번호로 변경하세요
            st.success("관리자 인증 성공 ✅")

            def convert_df_to_excel(dataframe):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    dataframe.to_excel(writer, index=False, sheet_name="방명록")
                return output.getvalue()

            excel_data = convert_df_to_excel(df)

            st.download_button(
                label="📥 방명록 엑셀 다운로드",
                data=excel_data,
                file_name=FILE_NAME,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
with tab3:
    st.subheader("의류 교환 파티")

with tab4:
    st.subheader("베르데비보에 대하여")

