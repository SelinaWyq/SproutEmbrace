import streamlit as st
import time
from coze_agent import ask_coze

def query_answer(question):
    """调用coze接口查询答案和后续问题"""
    answer, follow_up_questions = ask_coze(question)
    
    # 如果获得了新的后续问题，更新列表
    if follow_up_questions:
        st.session_state.follow_up_questions = follow_up_questions
    
    # 返回答案，如果答案为空则返回默认提示
    return answer if answer else "未获取到答复"

def main():
    # 设置页面标题
    st.title("Selina的智能助手")
    
    # 初始化后续问题列表
    if 'follow_up_questions' not in st.session_state:
        st.session_state.follow_up_questions = [
            "青少年女性胸部发育过程中会遇到哪些疾病？",
            "挑选内衣的注意事项",
            "胸部发育有哪些阶段？"
        ]
    
    # 初始化选中的问题
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = ""
    
    # 创建问题输入区域
    col1, col2 = st.columns([4, 1])
    with col1:
        question = st.text_input("请输入您的问题：", value=st.session_state.selected_question)
    with col2:
        submit = st.button("提交")

    # 显示后续问题
    st.write("您可能感兴趣的问题：")
    for q in st.session_state.follow_up_questions:
        if st.button(q, key=q):
            st.session_state.selected_question = q
            st.rerun()

    # 处理问题提交
    if submit or (question and st.session_state.get('_last_question') != question):
        if question:
            st.session_state._last_question = question
            with st.spinner('正在思考中...'):
                answer = query_answer(question)
            
            # 显示问答结果
            st.write("---")
            st.write("**问题：**", question)
            st.write("**回答：**", answer)

if __name__ == "__main__":
    main()
