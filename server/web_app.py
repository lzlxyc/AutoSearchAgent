import streamlit as st
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append('../')

from auto_search import AutoSearchAgent


class ChatApp:
    def __init__(self):
        self.agent = AutoSearchAgent()
        self.setup_page()

    def setup_page(self):
        """设置页面布局和样式"""
        st.set_page_config(
            page_title="智能问答助手",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

        # 自定义CSS样式
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .analysis-box {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border-left: 5px solid #1f77b4;
        }
        .answer-box {
            background-color: #e6f3ff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border-left: 5px solid #4CAF50;
        }
        .user-message {
            background-color: #d4edda;
            border-radius: 10px;
            padding: 15px;
            margin: 5px 0;
            text-align: right;
        }
        .bot-message {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)

    def display_chat_history(self):
        """显示聊天历史"""
        if "chat_history" in st.session_state:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 您:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="bot-message">
                        <strong>🤖 助手:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

    def run(self):
        """运行主应用"""
        st.markdown('<h1 class="main-header">🤖 智能百科问答助手</h1>', unsafe_allow_html=True)

        # 初始化session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "processing" not in st.session_state:
            st.session_state.processing = False

        # 创建两列布局
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("💬 对话界面")

            # 显示聊天历史
            self.display_chat_history()

            # 输入区域
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_area(
                    "请输入您的问题:",
                    placeholder="例如：请帮我介绍一下PPO算法的相关知识",
                    height=100
                )

                submit_button = st.form_submit_button("发送问题")

                if submit_button and user_input.strip():
                    st.session_state.processing = True
                    st.session_state.current_question = user_input.strip()

                    # 添加用户消息到历史
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_input.strip()
                    })

                    # 重新运行以更新界面
                    st.rerun()

        with col2:
            st.subheader("🔍 分析过程")

            if st.session_state.processing:
                # 显示分析过程
                analysis_placeholder = st.empty()
                analysis_container = analysis_placeholder.container()

                with analysis_container:
                    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                    st.write("**分析过程:**")

                    # 模拟分析过程
                    analysis_steps = [
                        "🔍 分析问题结构...",
                        "📚 搜索相关知识...",
                        "💡 理解核心概念...",
                        "📝 组织回答内容...",
                        "✨ 生成最终答案..."
                    ]

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i, step in enumerate(analysis_steps):
                        progress = (i + 1) / len(analysis_steps)
                        progress_bar.progress(progress)
                        status_text.text(step)
                        time.sleep(1)  # 模拟处理时间

                    # 获取最终答案
                    final_answer = self.agent.sample_run(
                        st.session_state.current_question
                    )

                    # 添加助手消息到历史
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": final_answer
                    })

                    st.markdown('</div>', unsafe_allow_html=True)

                    # 显示最终答案预览
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.write("**最终答案预览:**")
                    st.text(final_answer[:200] + "..." if len(final_answer) > 200 else final_answer)
                    st.markdown('</div>', unsafe_allow_html=True)

                # 完成处理
                st.session_state.processing = False
                analysis_placeholder.empty()

                # 显示完成消息
                st.success("✅ 分析完成！答案已显示在对话界面。")

                # 重新运行以更新界面
                st.rerun()
            else:
                st.info("💡 请输入问题并发送，这里将显示分析过程")

        # 侧边栏功能
        with st.sidebar:
            st.header("设置")

            # 清空聊天历史
            if st.button("清空聊天记录"):
                st.session_state.chat_history = []
                st.rerun()

            # 显示统计信息
            st.subheader("统计信息")
            st.write(f"对话轮数: {len([m for m in st.session_state.chat_history if m['role'] == 'user'])}")

            # 示例问题
            st.subheader("示例问题")
            example_questions = [
                "请帮我介绍一下PPO算法的相关知识",
                "什么是机器学习？",
                "解释一下深度学习的基本原理",
                "强化学习有哪些应用场景？"
            ]

            for question in example_questions:
                if st.button(question, key=f"example_{question}"):
                    st.session_state.current_question = question
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    st.session_state.processing = True
                    st.rerun()


def main():
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    main()