import streamlit as st
from strands import Agent
# FROM 이 부분을 바꿔야 한다
from strands_tools import calculator, current_time

# 페이지 제목
st.title("🧠 Strands Agent 샘플 테스트")

# 사용자 입력 받기
user_input = st.text_input("무엇을 계산하거나 알고 싶나요?", "7 * 9")

@st.cache_resource
def load_agent():
    return Agent(
        name="demo_agent",
        system_prompt="You are a helpful assistant that can calculate and tell current time.",
        tools=[calculator, current_time],
    )

agent = load_agent()

if st.button("에이전트 실행"):
    with st.spinner("생각 중..."):
        try:
            resp = agent.run(user_input)
            st.success("에이전트 응답:")
            st.write(resp.output)
        except Exception as e:
            st.error(f"오류 발생: {e}")

if st.checkbox("대화 내역 보기"):
    for msg in agent.messages:
        role = msg["role"]
        # 메시지 내용 구조가 여러 block일 수 있으니 간단하게 꺼내본다
        content = ""
        if msg.get("content"):
            # content는 리스트 안에 dict 형식일 수 있음
            try:
                content = msg["content"][0].get("text", "")
            except Exception:
                content = str(msg["content"])
        st.markdown(f"**{role.upper()}**: {content}")
