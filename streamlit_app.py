import os
import streamlit as st
from strands import Agent
from strands.models.openai import OpenAIModel  # ← 정확한 경로
from strands_tools import calculator           # 기본 도구 예시

st.title("🧠 Strands Agent Demo (OpenAI)")

user_input = st.text_input("무엇을 계산하거나 물어볼까요?", "What is 42^5?")

@st.cache_resource
def load_agent():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
    model = OpenAIModel(
        client_args={  # OpenAI 클라이언트 설정
            "api_key": api_key,
            # "base_url": "https://api.openai.com/v1",  # (필요 시 커스텀/호환 API 엔드포인트)
        },
        model_id="gpt-5-mini",            # 모델 ID
        params={"max_completion_tokens": 800, "temperature": 0.3},  # 모델 파라미터
    )
    return Agent(model=model, tools=[calculator],
                 system_prompt="You are a helpful assistant.")

agent = load_agent()

if st.button("에이전트 실행"):
    with st.spinner("생각 중..."):
        try:
            result = agent(user_input)      # run() 아님
            st.success("응답")
            st.write(result.message)        # 최종 메시지
        except Exception as e:
            st.error(f"오류: {e}")

if st.checkbox("대화 내역 보기"):
    for msg in agent.messages:
        role = msg.get("role", "")
        content = ""
        if msg.get("content"):
            block0 = msg["content"][0]
            content = block0.get("text") or str(block0)
        st.markdown(f"**{role.upper()}**: {content}")
