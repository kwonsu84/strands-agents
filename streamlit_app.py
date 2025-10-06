import streamlit as st
from strands import Agent
from strands.tools import calculator, current_time

# 페이지 제목
st.title("🧠 Strands Agent Demo - Streamlit")

# 사용자 입력
user_input = st.text_input("무엇을 계산하거나 알고 싶나요?", "3 + 5")

# 에이전트 초기화
@st.cache_resource
def load_agent():
    # 기본 도구(calculator, current_time) 등록
    return Agent(
        name="demo_agent",
        system_prompt="You are a helpful assistant that can calculate and tell the time.",
        tools=[calculator, current_time],
    )

agent = load_agent()

# 실행 버튼
if st.button("에이전트 실행"):
    with st.spinner("에이전트가 생각 중입니다..."):
        try:
            response = agent.run(user_input)
            st.success("✅ 에이전트의 응답:")
            st.write(response.output)
        except Exception as e:
            st.error(f"오류 발생: {e}")

# 대화 기록 표시
if st.checkbox("대화 내역 보기"):
    for msg in agent.messages:
        role = msg["role"]
        content = msg["content"][0]["text"] if msg["content"] else ""
        st.markdown(f"**{role.upper()}:** {content}")
