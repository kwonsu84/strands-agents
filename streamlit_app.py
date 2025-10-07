# 📦 필요한 도구 불러오기
import os                    # 컴퓨터 안의 환경변수를 사용할 때 필요
import streamlit as st        # 화면에 버튼, 입력창 등을 만들기 위한 도구
from strands import Agent     # 인공지능(에이전트)을 만들기 위한 Strands의 핵심 도구
from strands.models.openai import OpenAIModel  # OpenAI 모델을 쓰기 위한 클래스
from strands_tools import calculator           # 계산 도구 (에이전트가 계산할 수 있게 함)


# 🧰 에이전트를 미리 만들어서 저장해 두는 함수
@st.cache_resource  # Streamlit이 한 번 만든 에이전트를 계속 재사용하게 해줌
def load_agent():
    # 🔑 OpenAI API 키 불러오기 (비밀번호처럼 중요한 열쇠)
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        # 키가 없을 때 오류를 띄우기
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
        
    # 🧩 OpenAI 모델 만들기 (여기서는 gpt-5-nano 사용)
    model = OpenAIModel(
        client_args={"api_key": api_key},  # 내 OpenAI 열쇠 사용
        model_id="gpt-5-nano",             # 사용할 모델 이름
        streaming=False,                   # 천천히 말하기(스트리밍) 끔
        params={
            "max_completion_tokens": 4444,  # 최대 대답 길이 (단어 수 제한)
        },
    )

    # 🧠 에이전트 만들기: 모델 + 계산기 도구를 합쳐서 "도와주는 친구" 완성
    return Agent(
        model=model, 
        tools=[calculator],
        system_prompt="너는 친절히 정답만 이야기한다. 답하기 어렵거나 모르는 질문에 대해선 '모릅니다.'라고 해라. 질문에 대한 답변은 3~4문장 수준으로 짧게 답한다."  #  예르 들어 '3 더하기 3은?' 이라고 질문하면 '6' 이라고만 답한다.
    )


# 에이전트 실제로 만들기
agent = load_agent()


# 🧠 화면 제목 쓰기
st.title("🧠 Strands Agent With OpenAI")

# ✏️ 입력창과 실행 버튼을 폼으로 묶어 Enter 제출 지원
with st.form("qa_form", clear_on_submit=False):
    user_input = st.text_input("무엇을 물어볼까요?", "42^5 계산하면?", key="user_input")
    submitted = st.form_submit_button("에이전트 실행")

# ▶️ Enter 또는 버튼으로 제출되면 실행
if submitted:
    with st.spinner("생각 중..."):  # 에이전트가 답을 만드는 동안 표시되는 문구
        try:
            result = agent(user_input)      # 사용자가 입력한 문장을 에이전트에게 전달
            st.success("응답을 받았습니다")              # 성공 메시지

            # 에이전트 응답을 채팅 버블로 표시 + 마크다운 렌더링
            msg = result.message
            with st.chat_message("assistant"):
                if isinstance(msg, dict):
                    content = msg.get("content", [])
                    texts = [
                        block["text"] for block in content
                        if isinstance(block, dict) and "text" in block
                    ]
                    if texts:
                        st.markdown("\n\n".join(texts))
                    else:
                        st.info("출력할 텍스트가 없습니다.")

            st.toast("완료되었습니다 ✅", icon="✅")

        except Exception as e:
            st.error(f"오류: {e}")          # 문제가 생기면 오류 표시

st.write("❤️ 최근 대화 히스토리")

# 📜 이전 대화 내용을 화면에 보여줌
for msg in agent.messages:              # 대화 기록을 하나씩 읽어오기
    role = msg.get("role", "assistant")
    role_for_ui = role if role in ("user", "assistant") else "assistant"

    # 모든 블록의 텍스트를 합쳐서 표시
    content_text = ""
    if msg.get("content"):
        blocks = msg["content"]
        texts = [
            (b.get("text") if isinstance(b, dict) else str(b))
            for b in blocks
        ]
        texts = [t for t in texts if t]
        content_text = "\n\n".join(texts) if texts else str(blocks)

    with st.chat_message(role_for_ui):
        if content_text:
            st.markdown(content_text)
        else:
            st.markdown(f"_{role.upper()} 메시지 내용이 없습니다._")
