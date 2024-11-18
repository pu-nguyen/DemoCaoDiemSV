import requests
import json

#print(json.dumps(request.json(), ensure_ascii=False, indent=4))

API = 'https://onlineapi.hcmue.edu.vn/api'
API_KEY = 'hcmuepscRBF0zT2Mqo6vMw69YMOH43IrB2RtXBS0EHit2kzvL2auxaFJBvw=='
CLIENT_ID = 'hcmue'
ds_hb= []
sinh_vien = {}
def login():
    URL = f'{API}/authenticate/authpsc'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Apikey':API_KEY,
        'Clientid':CLIENT_ID,
        'Accept-Language':'vi-VN',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Content-Type':'application/json; charset=utf-8'
    }
    request = requests.post(
        url=URL,
        json={"username": "9111","password":"9111"},
        headers=header
    )
    # print(request.status_code)
    if request.status_code == 200:
        global TOKEN
        TOKEN = request.json()['Token']

def lay_diem_sinh_vien_theo_mssv_hk_nam(MaSV, Key, Nam, HocKi):

    URL = f'{API}/professor/GetAllMarkStudentByProgramID'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Apikey': API_KEY,
        'Clientid': CLIENT_ID,
        'Authorization': f'Bearer {TOKEN}',
        'Accept-Language': 'vi-VN,vi;q=0.9  ',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    request = requests.post(
        URL,
        json={"p1": MaSV, "p2": Key, "p3": Nam, "p4": HocKi},
        headers=header
    )
    #print(request.json())
    if len(request.json()) == 0 or len(request.json()[0]['DanhSachDiem']) == 0:
        return
    Diem_TB_4 = request.json()[0]['DanhSachDiem'][0]['DanhSachDiemHK'][0]['TB_HK_4']
    if Diem_TB_4 is None:
        return
    Diem_TB_10 = request.json()[0]['DanhSachDiem'][0]['DanhSachDiemHK'][0]['TB_HK_10']
    Ren_Luyen = request.json()[0]['DanhSachDiem'][0]['DanhSachDiemHK'][0]['DiemRenLuyenHK']
    Diem_HB = round((float(Diem_TB_4)*80+int(Ren_Luyen)/25*20)/100, 2)

    sinh_vien['Diem_TB_4'] = Diem_TB_4
    sinh_vien['Ren_Luyen'] = Ren_Luyen
    sinh_vien['Diem_HB'] = Diem_HB
    global ds_hb
    ds_hb.append(sinh_vien.copy())
    sinh_vien.clear()


def lay_danh_sach_sinh_vien_theo_lop(NamHoc,HocKi,MaLop):
    login()
    URL = f'{API}/professor/GetStudentInClassCVHT'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Apikey': API_KEY,
        'Clientid': CLIENT_ID,
        'Authorization': f'Bearer {TOKEN}',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    request = requests.post(
        URL,
        json={'YearStudy': NamHoc, 'TermId': HocKi, 'Id': MaLop},
        headers=header
    )
    #khắc phục khi lấy dữ liệu ensure_ascii=False tránh tự động giải mã unicode
    danh_sach = list(request.json())

    #Sắp xếp theo mã sinh viên
    danh_sach_sinh_vien = sorted(danh_sach,key=lambda People: People['StudentID'],reverse=False)

    #print(json.dumps(danh_sach_sinh_vien, indent=4,ensure_ascii=False))
    #Sau khi có được toàn bộ danh sách sinh viên theo lớp, thì ở dưới sẽ thực hiện cào điểm sinh viên theo từng lớp, học kì, năm học:
    for i in danh_sach_sinh_vien:
        sinh_vien['MaSV'] = i['StudentID']
        sinh_vien['TenSV'] = i['StudentNameWithoutID']
        lay_diem_sinh_vien_theo_mssv_hk_nam(i['StudentID'],'K487480201',NamHoc,HocKi)
    return ds_hb

#if __name__ == "__main__":
    # Lấy danh sách sinh viên theo lớp:
    # lay_danh_sach_sinh_vien_theo_lop("2023-2024",'HK01','48.01.CNTT.C')