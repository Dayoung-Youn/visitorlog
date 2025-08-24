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
st.sidebar.caption("'📋 목록보기' 탭을 누르고 이름을 검색하면, 작성자명에 해당하는 방명록을 찾을 수 있어요.")

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
                
                ✅  저장하기 버튼을 누른 후, 저장 완료 메시지가 나타나면 '목록보기'에서 작성한 내용을 확인할 수 있어요.
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

    cards_per_row = 3
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


    if "show_admin_input" not in st.session_state:
        st.session_state.show_admin_input = False

    if st.checkbox("관리자 모드", value=False):
        st.session_state.show_admin_input = True
    else:
        st.session_state.show_admin_input = False

    # 관리자 모드일 때만 비밀번호 입력창과 엑셀 다운로드 버튼 노출
    if st.session_state.show_admin_input:
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
                file_name="방명록.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab3:
    st.title("🌱 VerdeVivo베르데비보")

    # 1. 브랜드 Hero Section
    col1, col2 = st.columns([1, 4])

    col2_text = """
        ### 지속가능한 팝업스토어 경험을 설계합니다.

        <div style="background-color:#e6f9ec; padding:16px;">
            <b>팀명 베르데비보(VerdeVivo)</b>에는 ‘녹색’(Verde)과 ‘삶’(Vivo)의 스페인어 합성어로, 친환경적 삶을 지향하는 팀의 방향성을 담겨 있습니다.<br>
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
        st.markdown("팝업스토어 폐기물을 줄여 브랜드와 소비자가 함께 친환경 팝업스토어를 만들어갑니다")
    with mv_col2:
        st.markdown("### Vision")
        st.markdown("일회성 이벤트를 넘어 지속가능한 소비 문화를 확산하고 정착합니다")

    st.markdown("---")

    # 프로젝트 3개
    st.subheader("🌍 프로젝트")

    projects = [
        (" EcoScore에코스코어",
        "국내 친환경 팝업스토어 사례 연구, 친환경성 평가 지표 개발"),

        (" EcoPop에코팝",
        "교내외 단체와 협업하여 에코스코어를 현장에 적용, 실효성 평가 및 개선책 탐색, 친환경 운영지침 제작"),

        (" EcoP!ck에코픽",
        "웹진과 인스타그램 매거진 운영을 통해 2030 세대에게 환경 영향 정보 제공 및 인식 제고")
        
    ]

    for title, desc in projects:
        st.markdown(f"### {title}")
        st.markdown(desc)

    st.divider()

    # 3. 핵심 역량
    st.subheader("💪 핵심 역량")
    cap_cols = st.columns(2)
    capabilities = [
        ("환경/ESG", "UNFPA 요르단 국가사무소, 국회기후변화포럼, 고려대학교 지속가능원, 국사봉중학교 사회적협동조합 등 다양한 학내외 기관에서 환경 문제 해결을 위해 고민한 경험이 있는 학생들의 조합"),
        ("촬영/기사작성, SNS 운영", "Fashion&Film 매거진, NERD 매거진과 국회기후변화포럼, NERD, 고려대학교 극예술연구회 SNS 운영")
    ]
    for col, (title, desc) in zip(cap_cols, capabilities):
        with col:
            st.markdown(f"### {title}")
            st.markdown(desc)


    st.divider()

    # 5. 팀원 요약 (Optional)
    st.subheader("👥 팀원들")
    st.markdown("환경 문제와 촬영/기사작성, SNS 운영 등 다양한 경험과 관심사를 가진 고려대학교 서어서문학과 6명이 모였습니다.")
    team_members = ["김유하", "박진영", "윤다영", "이수아", "이혜린", "정예린"]

    # 팀원 데이터 (사진 경로와 이력 포함)
    team_data = {
        "김유하": {
            "img": "./김유하.jpg",
            "bio": """**고려대학교 서어서문학과(제1전공)･Emerging Market & Latin America(제2전공), 학부 재학**
                    - **환경단체 ‘성대골 사람들’과 협업, 국사봉중학교 사회적 협동조합 운영(2015.08.-2016.12.)**
                        - 사회적 협동조합 발기인(2015.08.)
                        - 사회적 협동조합 발족(2016.02.)
                        - 조합원으로서 교내 생태에너지 전환 카페 ‘그냥가게’에서 지역사회와 연계한 친환경 식품 판매
                        - 북카페 ‘라온’ 운영
                        - 소외가정 김치 나눔 행사(2016.12.)
                    - **국사봉중학교 생태축제 기획·운영 (2016.07.)**
                        - 환경보호를 주제로 한 학급별 부스 예산안 심사 및 운영 총괄
                    - **적정기술 하우스 만들기 사업 참여 (2014-2015)**
                        - 압전소자, 얼음 에어컨 등 적정기술을 활용한 집 짓기"""

        },
        "박진영": {
            "img": "./박진영.png",
            "bio": """**고려대학교 서어서문학과(제1전공)･환경생태공학부(제2전공), 학부 재학**
                    - **국회기후변화포럼 청년위원 (2025.03.-현재)**
                    - **한국지속가능발전해법네트워크 청년위원 (2025.02.-현재)**
                        - Planet Team(SDGs Planet Pillar 관련 업무), Archive Team(회원 조직 IR 제작), Assembly Team(정기총회 개최) 소속
                    - **국회기후변화포럼 서포터즈 7기 우수 수료 (2024.07.-2025.01.)**
                        - 국회기후변화포럼 블로그 포스팅 작성
                        - 국회기후변화포럼 인스타그램 콘텐츠 제작
                        - 국회기후변화포럼 유튜브 콘텐츠 기획 및 제작
                    - **국회기후변화포럼 COP29 대학생 참관단 (2024.07.-2025.01.)**
                        - COP29·INC-5 참관
                        - COP29 한국 파빌리온 세미나 기획 및 참여
                        - COP29 참관기 블로그 포스팅 작성
                        - COP29 브이로그·코멘터리 영상 기획 및 제작
                    - **국회기후변화포럼 제14기 대학생 기후변화 아카데미 수료 (2024.07.)**
                        - 대상 수상
                    - **'아모레퍼시픽과 시세이도의 비교를 기반으로 한 ESG 경영 재고 및 실천 방안 도출' 프로젝트 진행 (2024.03.-2024.07.)**
                    - **고려대학교 제13대 서어서문학과/반 집행부 행사기획국장 (2023.11.-2024.11.)**"""
        },
        "윤다영": {
            "img": "./윤다영.jpg",
            "bio": """**고려대학교 서어서문학과, 학부 재학**
                    - **고려대학교 지속가능원 지속가능대사 1기(2024.08.-2025.02.)**
                        - 지속가능원 뉴스레터(2025 겨울호) 제작
                        - 지속가능주간 지속가능대사부스 기획 및 운영
                        - 세계대학평가에 반영되는 KU 지속가능성 문해력 조사 문항 제작･검수"""
        },
        "이수아": {
            "img": "./이수아.jpg",
            "bio": """**고려대학교 서어서문학과(제1전공)･미디어학부(제2전공), 학부 재학**
                    - **대학생기후행동 고대지부원 활동 (2024.09.-현재)**
                        - 캠페인 굿즈 제작 및 행사 진행
                        - 회지 기획 및 디자인
                    - **국내 문구 브랜드 모나미 서포터즈 “모나미 펜클럽 7기” 활동 (2024.09.-2025.02.)**
                    - **대학생기후행동 운영 <기후정의페스티벌> 서포터즈 활동 (2024.06.-2024.07.)**
                        - 카드뉴스 및 행사 굿즈 디자인 및 제작
                    - **Fashion & Film 매거진 <NERD> 패션팀원으로 잡지 제작 참여 (2024.03.-현재)**
                        - 에디터로 활동하며 다양한 콘텐츠 기획 및 작성
                        - 아트팀장으로서 SNS 콘텐츠 게시물 제작 및 실물 종이 잡지 디자인 (2024.08.-현재)
                        - 실물 잡지 텀블벅 후원금액 목표 달성 경험
                        - 매거진 자체 전시 및 팝업스토어 기획 및 운영
                    - **한국문화예술위원회 운영 아르코·대학로예술극장 관객안내원 수료 (2023.02.-2023.12.)**
                        - 베리어프리 환경 조성 지원 및 접근성 향상 역할 수행
                    - **청년 문화예술 기획 단체 “주식회사 메리한 사람들” 전략기획팀원 (2023.03.- 2023.09.)**
                        - 서울시 도심 플로깅 행사 ‘운줍깅’ 기획 및 진행
                        - 웹 TF 팀원 소속으로 웹페이지 디자인 및 제작
                    - **고려대학교 중앙동아리 "극예술연구회" 활동 (2021.09.-2023.12.)**
                        - 연극 포스터 디자인 및 굿즈 제작, 공연 프로필 촬영, 팀 인스타그램 계정 운영"""
        },
        "이혜린": {
            "img": "./이혜린.jpg",
            "bio": """**고려대학교 서어서문학과(제1전공)･환경생태공학부(제2전공), 학부 재학**
                    - **유엔인구기금(UNFPA) 요르단 국가사무소, Climate Change Junior Officer 근무 (2024.09.-2025.02.)**
                        - 2024 Regional Conference of Youth MENA 내 UNFPA 파빌리온 기획 및 운영
                        - 제29회 기후변화협약 당사국총회(The 29th Conference of Parties, COP29) 참가
                        - UNFPA Jordan Climate Change 인포그래픽 제작
                    - **한국국제협력단(KOICA) 세네갈 사무소, Young Professional 근무 (2023.12.-2024.08.)**
                        - 농업 및 보건 국별 협력 사업 지원
                        - 국별 연수･석･박사 학위 연수 프로그램 및 KOICA-세네갈 연수생 알럼나이(ALASCO) 운영 지원
                        - 서아프리카 개발협력동향 리서치
                    - **제6회 모의 아프리카연합 총회 (2023.08.)**
                        - 케냐 대표단으로 참가하여 ‘기후금융을 활용한 아프리카 내 녹색 에너지 전환 및 보편적 에너지 접근 촉진’ 의제 논의 및 결정문 도출
                        - 외교부장관상 수상
                    - **Universidad Pompeu Fabra, 가을학기 수료 (2022.09.-2022.12.)**
                        - 비건화장품 기업 ETINA 설립 모의 기획 및 런칭 프로젝트 참여"""
        },
        "정예린": {
            "img": "./정예린.jpg",
            "bio": """**고려대학교 서어서문학과(제1전공)･Emerging Market & Latin America(제2전공), 학부 재학** 
                    - **교촌치킨 서포터즈 K-스피커스 7기 (2025.01.-현재)**
                    - **2024 아시아 대학생 청년작가 미술축제 아시아프(ASYAAF) 학생아트매니저(SAM) (2024.08.)**
                        - 전시장 운영 및 작품 동선 안내를 통해 공간 기획과 효율적 운영에 대한 이해 확보
                        - 작품 홍보 및 방문객 응대(도슨트): 대중과의 소통 및 문화 경험 설계 경험
                        - 예술 공간에서 친환경적 전시 방식 및 운영 개선 가능성 탐색 경험 축적
                    - **2023 조선일보 아시안 리더십 컨퍼런스(ALC) 서포터즈 (2023.05.)**
                    - **고려대학교 중앙동아리 "극예술연구회" 기획부 (2022)**
                        - 다수의 연극 무대 제작 및 해체 경험: 일시적 공간의 자재 활용 및 폐기물 문제에 대한 이해 보유
                        - 동아리 행사 및 외부 단체와의 다양한 협업 프로젝트 기획･운영 경험
                        - 공식 SNS 운영: 디지털 홍보 및 콘텐츠 제작 경험 축적
                    - **국제신문 중고생 명예기자 (2017-2018)**"""
        }
    }

    # 토글박스(expander)로 표시
    for member, info in team_data.items():
        with st.expander(member, expanded=False):
            col1, col2 = st.columns([1, 3])  # 좌측: 사진, 우측: 이력
            with col1:
                st.image(info["img"], use_column_width=True)
            with col2:
                st.markdown(f"**이력**  \n{info['bio']}")

    member_select = st.selectbox("팀원을 선택하세요:", team_members)

    st.divider()

    # 6. Contact
    st.subheader("📬 Get in Touch")
    st.markdown("""
    - 📧 Email: **verdevivo@naver.com**  
    - 🔗 [Instagram](https://instagram.com/ecopick.mag) | [Webzine](https://ecopickmag.cargo.site) | [LinkTree](https://linktr.ee/verdeviv)
    """)

with tab4:
    st.subheader("의류 교환 파티")
