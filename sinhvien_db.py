import mysql.connector
import Request

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="210124",
    database="sinhvien_db"
)

# Tạo cursor
cursor = conn.cursor()
if __name__ == "__main__":
        NamHoc = input("Nhập năm học theo xxxx-yyyy: ")
        HocKi = input("Nhập học kì: ")
        MaLop = input('Nhập mã lớp: ')
        sinh_vien_data = Request.lay_danh_sach_sinh_vien_theo_lop(NamHoc, HocKi, MaLop)
        print("Dữ liệu sinh viên từ API:", sinh_vien_data)
        if sinh_vien_data is None:
            print("Không lấy được dữ liệu sinh viên!")
        else:
            sql = """
            INSERT INTO sinhvien (masv, ten_sv, lop, nam_hoc, hoc_ky, diem_tbm, diem_ren_luyen, diem_hoc_bong) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Chèn từng sinh viên vào bảng
            for sv in sinh_vien_data:
                diem_tbm = sv.get("Diem_TB_4", 0.0)
                diem_ren_luyen = sv.get("Ren_Luyen", 0.0)
                diem_hoc_bong = sv.get("Diem_HB", 0.0)

                values = (sv["MaSV"], sv["TenSV"], MaLop, NamHoc, HocKi, diem_tbm, diem_ren_luyen, diem_hoc_bong)
                cursor.execute(sql, values)

            conn.commit()
            cursor.close()
            conn.close()
            print("Dữ liệu sinh viên đã được lưu thành công!")