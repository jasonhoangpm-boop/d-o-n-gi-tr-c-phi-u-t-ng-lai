import streamlit as st
import bcrypt
from project.database.user_db import add_user, get_user

# =========================
# CUSTOM CSS
# =========================
# CSS được chuyển sang hàm inject_styles() trong streamlit_app.py
# để quản lý tập trung và tránh gọi st.set_page_config() nhiều lần.



# =========================
# PASSWORD FUNCTIONS
# =========================
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


# =========================
# LOGIN FORM
# =========================
def login_form():

    st.markdown("""
    <div class="auth-card">
    <div class="main-title">📈 STOCK AI</div>
    <div class="subtitle">
        Hệ thống phân tích chứng khoán thông minh
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔐 Đăng Nhập")

    with st.form("login_form"):

        username = st.text_input(
            "Tên đăng nhập",
            placeholder="Nhập username..."
        ).lower()

        password = st.text_input(
            "Mật khẩu",
            type="password",
            placeholder="••••••••"
        )

        submitted = st.form_submit_button("Đăng nhập")

        if submitted:

            if not username or not password:
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
                return

            user = get_user(username)

            if user and check_password(
                password,
                user.password_hash.encode('utf-8')
            ):

                st.session_state['logged_in'] = True
                st.session_state['username'] = username

                st.success("✅ Đăng nhập thành công!")
                st.rerun()

            else:
                st.error("❌ Sai tài khoản hoặc mật khẩu.")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# REGISTER FORM
# =========================
def registration_form():

    st.markdown("""
    <div class="auth-card">
    <div class="main-title">📊 STOCK AI</div>
    <div class="subtitle">
        Tạo tài khoản đầu tư thông minh
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📝 Đăng Ký")

    with st.form("registration_form"):

        new_username = st.text_input(
            "Tên đăng nhập mới",
            placeholder="Username..."
        ).lower()

        new_password = st.text_input(
            "Mật khẩu mới",
            type="password",
            placeholder="••••••••"
        )

        confirm_password = st.text_input(
            "Xác nhận mật khẩu",
            type="password",
            placeholder="••••••••"
        )

        submitted = st.form_submit_button("Tạo tài khoản")

        if submitted:

            if not new_username or not new_password or not confirm_password:
                st.warning("⚠️ Vui lòng điền đầy đủ thông tin.")
                return

            if new_password != confirm_password:
                st.error("❌ Mật khẩu không khớp.")
                return

            hashed_password = hash_password(new_password)

            success, message = add_user(
                new_username,
                hashed_password.decode('utf-8')
            )

            if success:
                st.success("🎉 Đăng ký thành công!")
            else:
                st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN AUTH PAGE
# =========================
def show_auth_pages():

    st.sidebar.title("📈 STOCK AI")

    page = st.sidebar.radio(
        "Điều hướng",
        ["Đăng Nhập", "Đăng Ký"]
    )

    if page == "Đăng Nhập":
        login_form()
    else:
        registration_form()

