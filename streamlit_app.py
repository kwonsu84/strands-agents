import streamlit as st
from strands import Agent
from strands_tools import calculator, current_time

st.title("🧠 Strands Agent Demo")

user_input = st.text_input("무엇을 계산하거나 알고 싶나요?", "서울의 현재 시간은?")

@st.cache_resource
def load_agent():
    # OpenAI 모델 프로바이더로 변경
    return Agent(
        name="openai_agent",
        system_prompt="You are a helpful assistant that can calculate and tell the time.",
        tools=[calculator, current_time],
        model_provider={
            "provider": "openai",
            "model": "gpt-4o-mini",  # gpt-4o 또는 gpt-4-turbo 가능
            "api_key": st.secrets.get("OPENAI_API_KEY")
        },
    )

agent = load_agent()

if st.button("에이전트 실행"):
    with st.spinner("에이전트가 생각 중입니다..."):
        try:
            result = agent(user_input)
            st.success("✅ 에이전트의 응답:")
            st.write(result.message)
        except Exception as e:
            st.error(f"오류 발생: {e}")

if st.checkbox("대화 내역 보기"):
    for msg in agent.messages:
        role = msg.get("role", "")
        content = ""
        if msg.get("content"):
            block = msg["content"][0]
            content = block.get("text") or str(block)
        st.markdown(f"**{role.upper()}**: {content}")
