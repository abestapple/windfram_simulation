import hmac  
import streamlit as st  
def check_password(): 
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
	.e8zbici0{visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>""", unsafe_allow_html=True)
    def login_form(): 
	#st.set_page_config(page_title="风电场计算",layout="wide")
	col0,col1, col2 = st.columns([0.25,0.5,0.25]) 
	with col1: 
        	with st.form("Credentials"):  
            		col0,col1, col2 = st.columns([0.6,0.4, 2])
            		with col0:  
                		st.write("  ")  
            		with col1:  
                		st.image("login_logo.png",  width=75)  
            		with col2:  
                		st.markdown("WINDFARM ANALYSIS")  
            		st.text_input("Username", key="username")  
            		st.text_input("Password", type="password", key="password")  
            		# 将按钮靠右放置  
            		cols = st.columns([4, 1])  
            		cols[1].form_submit_button("Login", on_click=password_entered)  
            		# st.form_submit_button("登录", on_click=password_entered)   
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if st.session_state["username"] in st.secrets[  
            "passwords"  
        ] and hmac.compare_digest(  
            st.session_state["password"],  
            st.secrets.passwords[st.session_state["username"]],  
        ):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  
            del st.session_state["username"]  
        else:  
            st.session_state["password_correct"] = False  
    if st.session_state.get("password_correct", False):  
        # st.success("登录成功！")  
        return True  
    # Show inputs for username + password.  
    login_form()  
    if "password_correct" in st.session_state:  
        st.error("😕 账号不存在或者密码不正确")  
    return False   
