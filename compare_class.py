import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="210124",
    database="sinhvien_db"
)


def lay_du_lieu_lop(nam_hoc, hoc_ky):
    query = """
    SELECT lop, AVG(diem_tbm) AS diem_tb_lop
    FROM sinhvien
    WHERE nam_hoc = %s AND hoc_ky = %s
    GROUP BY lop
    """
    cursor = conn.cursor()
    cursor.execute(query, (nam_hoc, hoc_ky))

    # Lấy kết quả từ truy vấn
    result = cursor.fetchall()
    cursor.close()

    # Chuyển đổi dữ liệu thành danh sách các từ điển
    lop_data = [{"lop": row[0], "diem_tb_lop": row[1]} for row in result]
    return lop_data


def sap_xep_sinh_vien_hoc_bong(nam_hoc, hoc_ky):
    query = """
    SELECT masv, ten_sv, lop, diem_hoc_bong
    FROM sinhvien
    WHERE nam_hoc = %s AND hoc_ky = %s
    ORDER BY diem_hoc_bong DESC
    """
    cursor = conn.cursor()
    cursor.execute(query, (nam_hoc, hoc_ky))

    # Lấy kết quả từ truy vấn
    result = cursor.fetchall()
    cursor.close()

    # In danh sách sinh viên
    print(f"\nDanh sách sinh viên có điểm học bổng từ cao xuống thấp trong học kỳ {hoc_ky}:")
    for row in result:
        print(f"MSSV: {row[0]}, Tên: {row[1]}, Lớp: {row[2]}, Điểm học bổng: {row[3]:.2f}")


def so_sanh_diem_tb(nam_hoc):
    for hoc_ky in [1, 2]:
        print(f"\nHọc kỳ {hoc_ky}:")
        data = lay_du_lieu_lop(nam_hoc, f"HK0{hoc_ky}")

        # In dữ liệu điểm trung bình
        for record in data:
            print(f"Lớp: {record['lop']}, Điểm TB: {record['diem_tb_lop']:.2f}")

        # Tìm lớp có điểm trung bình cao nhất
        lop_tot_nhat = max(data, key=lambda x: x["diem_tb_lop"])
        print(
            f"Lớp có điểm trung bình cao nhất trong học kỳ {hoc_ky}: {lop_tot_nhat['lop']} với điểm TB: {lop_tot_nhat['diem_tb_lop']:.2f}")

        # Gọi hàm sắp xếp sinh viên theo điểm học bổng
        sap_xep_sinh_vien_hoc_bong(nam_hoc, f"HK0{hoc_ky}")


if __name__ == "__main__":
    nam_hoc = input("Nhập năm học (xxxx-yyyy): ")
    so_sanh_diem_tb(nam_hoc)

# Đóng kết nối MySQL sau khi chạy xong
conn.close()
