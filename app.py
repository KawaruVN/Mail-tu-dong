import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ======================== CONFIG ========================
SENDER_EMAIL = "huuphuc1208vn@gmail.com"
APP_PASSWORD = "xjxaybjrgnxsngad"  # Đã bỏ khoảng trắng

EMAILS = {
    "cat_lai": "cbkh.cl@saigonnewport.com.vn",
    "phu_huu": "chuyenbaikiemhoa.tcph@saigonnewport.com.vn",
    "giang_nam": "kiemhoa@terminalclgn.com",
}

# ======================== FUNCTIONS ========================
def send_email(receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        return True
    except Exception as e:
        return str(e)

# ======================== STREAMLIT UI ========================
st.title("📦 Auto Send Mail Thông Báo Kiểm Dịch")

with st.form("form"):
    cong_ty = st.text_input("Tên công ty", "CÔNG TY TNHH NGUYÊN LIỆU THUỶ SẢN")
    dia_chi = st.text_input("Địa chỉ công ty", "2bis-4-6 Lê Thánh Tôn, Bến Nghé, Quận 1, TP HCM")
    mst = st.text_input("Mã số thuế", "0316841383")
    ten_hang = st.text_input("Tên hàng", "Bột thịt xương")
    ngay_den = st.date_input("Ngày đến")
    ngay_kiem = st.date_input("Ngày kiểm dịch")
    so_luong = st.text_input("Số lượng cont", "03*20")
    so_dien_thoai = st.text_input("SĐT liên hệ", "0337702251 (MR. Phúc)")
    danh_sach_cont = st.text_area("Danh sách container (mỗi cont cách nhau bởi dấu phẩy hoặc xuống dòng)")
    submitted = st.form_submit_button("Gửi Email")

if submitted:
    list_cont = [c.strip() for c in danh_sach_cont.replace('\n', ',').split(',') if c.strip()]
    cont_str = ",  ".join(list_cont)

    body = f"""
Dear Anh chị
Thông tin công ty:
{cong_ty}
Đc: {dia_chi}

Mst: {mst}

HÀNG LẤY MẪU KIỂM DỊCH ĐỘNG VẬT: {ngay_kiem.strftime('%d/%m/%Y')}

TÊN HÀNG: {ten_hang}

Ngày đến: {ngay_den.strftime('%d/%m/%Y')}
Số lượng cont: {so_luong}

SĐT: {so_dien_thoai}

Vui lòng đưa cont về BÃI KIỂM HÓA HẠ CÙNG 1 LINE, để Doanh Nghiệp tiến hành lấy mẫu kiểm dịch động vật. Vì quy trình mới của kiểm dịch rất khắt khe nên xin QUÝ CẢNG hỗ trợ cho lô hàng để tiện cho việc cắt seal cũng như lấy mẫu kiểm dịch động vật.

CONT / SEAL:
{cont_str}
"""

    # TEST - Chỉ gửi đến cả 3 email để thử
    for key, email in EMAILS.items():
        result = send_email(email, "[THÔNG BÁO KIỂM DỊCH] Lô hàng cần hỗ trợ kiểm hoá", body)
        if result is True:
            st.success(f"✅ Đã gửi email đến {key.upper()} thành công")
        else:
            st.error(f"❌ Gửi email đến {key.upper()} lỗi: {result}")
