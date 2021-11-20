from question import Question
import streamlit as st


class Page():
    def __init__(self):
        func_list = ["Simple Question", "Complex Question"]
        function = st.sidebar.selectbox("Ask a Question", func_list)
        self.qa = Question("")
        if function == func_list[0]:
            self.simple_page()
        else:
            self.complex_page()

    def simple_page(self):
        st.header("This part supports the user to ask a simple question or a combinaiton of simple questions")
        num = st.number_input("Select the number of conditions for your question", value=1, step=1, format="%d")
        sq_ls = [""]*num
        for i in range(num):
            st.write("Question " + str(i + 1))
            sq_ls[i] = st.text_input("", key=i)
        if st.button("Confirm all the questions"):
            for i in range(num):
                self.qa.sent = sq_ls[i]
                result = self.qa.run_simple()
            st.write(result)

    
    def complex_page(self):
        st.header("This part supports the user to ask a complex question")
        cq = st.text_area("Please input your complex question")


if __name__ == "__main__":
    Page()
