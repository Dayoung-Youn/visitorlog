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
tab1, tab2, tab3, tab4 = st.tabs(["✍️ 작성하기", "📋 목록보기", "♻️ 베르데비보란?", "👚 의류 교환 파티란?"])

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
    st.title("🌱 VerdeVivo베르데비보")

    # 1. 브랜드 Hero Section
    col1, col2 = st.columns([1, 4])

    col2_text = """
    ### 지속가능한 팝업스토어 경험을 설계합니다.

    <div style="background-color:#e6f9ec; padding:16px;">
        <b>베르데비보(VerdeVivo)</b>는 ‘녹색’(Verde)과 ‘삶’(Vivo)의 스페인어 합성어로, 친환경적 삶을 지향하는 팀의 방향성을 담았습니다.<br>
        또한, ‘Ver de Vivo’(사는 것을 보다)라는 의미처럼, 일상에서 환경 문제를 직접 바라보고 해결하고자 합니다.
    </div>
    """

    text_length = len(col2_text)
    # 텍스트 길이에 따른 이미지 너비 대략 계산 (너무 커지지 않게 제한)
    image_width = min(max(100, text_length // 3), 300)

    with col1:
        st.image(
            ["./Profile Ver White.png", "./Profile Verde White.png"],
            width=image_width
        )
    with col2:
        st.markdown(col2_text, unsafe_allow_html=True)

    st.divider()
    

    # 2. 미션 & 비전
    st.subheader("🎯 우리의 미션")

    mv_col1, mv_col2 = st.columns(2)
    with mv_col1:
        st.markdown("### Mission")
        st.caption("팝업스토어 폐기물을 줄여 브랜드와 소비자가 함께 친환경 팝업스토어를 만들어갑니다")
    with mv_col2:
        st.markdown("### Vision")
        st.caption("일회성 이벤트를 넘어 지속가능한 소비 문화를 확산하고 정착합니다")

    st.markdown("---")

    # 프로젝트 3개
    st.subheader("🌍 프로젝트")

    projects = [
        (" EcoScore에코스코어",
        "국내 친환경 팝업스토어 사례 연구, 친환경성 평가 지표 개발"),

        (" EcoPop에코팝",
        "학교·기관·브랜드와 협업하여 에코스코어를 현장에 적용, 실효성 평가 및 개선책 탐색, 친환경 운영지침 제작"),

        (" EcoP!ck에코픽",
        "웹진과 인스타그램 매거진 운영을 통해 2030 세대에게 환경 영향 정보 제공 및 인식 제고")
        
    ]

    for title, desc in projects:
        st.markdown(f"### {title}")
        st.markdown(desc)

    st.divider()

    # 3. 핵심 역량
    st.subheader("💪 핵심 역량")
    cap_cols = st.columns(3)
    capabilities = [
        ("📊 데이터 분석", "소비/폐기물 데이터 기반 인사이트"),
        ("🌎 환경/ESG", "UNFPA 요르단 국가사무소, 국회기후변화포럼, 고려대학교 지속가능원, 국사봉중학교 사회적협동조합 등 다양한 학내외 기관에서 환경 문제 해결을 위해 고민한 경험이 있는 학생들의 조합"),
        ("📽️ 촬영/기사작성, SNS 운영", "Fashion&Film 매거진, NERD 매거진과 국회기후변화포럼, NERD, 고려대학교 극예술연구회 SNS 운영")
    ]
    for col, (title, desc) in zip(cap_cols, capabilities):
        with col:
            st.markdown(f"### {title}")
            st.markdown(desc)


    st.divider()

    # 5. 팀원 요약 (Optional)
    st.subheader("👥 팀원들")
    st.markdown("환경 문제와 촬영/기사작성, SNS 운영 등 다양한 경험과 관심사를 가진 6명이 모였습니다.")
    team_members = ["이혜린(팀장)", "김유하", "박진영", "윤다영", "이수아", "정예린"]
    member_select = st.selectbox("팀원을 선택하세요:", team_members)
    # st.image(f"member_{member_select}.png", use_column_width=True, caption=member_select)

    st.divider()

    # 6. Contact
    st.subheader("📬 Get in Touch")
    st.markdown("""
    - 📧 Email: **verdevivo@naver.com**  
    - 🔗 [Instagram](https://instagram.com/ecopick.mag) | [Webzine](https://ecopickmag.cargo.site) | [LinkTree](https://linktr.ee/verdeviv)
    """)

with tab4:
    st.subheader("의류 교환 파티")
