CREATE DATABASE sinhvien_db;
-- DROP DATABASE sinhvien_db;

USE sinhvien_db;

-- DROP TABLE IF EXISTS sinhvien;
CREATE TABLE sinhvien (
    masv VARCHAR(13),                   -- Mã sinh viên
    ten_sv VARCHAR(255),                -- Tên sinh viên
    lop VARCHAR(13),                    -- Lớp học (48.01.CNTT.A, 48.01.CNTT.B, 48.01.CNTT.C)
    nam_hoc VARCHAR(9),                 -- Năm học (xxxx-yyyy)
    hoc_ky VARCHAR(5),                  -- Học kỳ (HK01, HK02)
    diem_tbm FLOAT,                     -- Điểm trung bình môn
    diem_ren_luyen FLOAT,               -- Điểm rèn luyện
    diem_hoc_bong FLOAT,                -- Điểm học bổng
    PRIMARY KEY (masv, nam_hoc, hoc_ky) -- Khóa chính bao gồm mã sinh viên, năm học và học kỳ
);
-- SELECT*FROM sinhvien
-- SET SQL_SAFE_UPDATES = 0;
-- DELETE FROM sinhvien WHERE lop = '48.01.CNTT.A';
-- DELETE FROM sinhvien WHERE lop = '48.01.CNTT.B';
-- DELETE FROM sinhvien WHERE lop = '48.01.CNTT.C';

select*from sinhvien
where lop = '48.01.CNTT.B';

--  Truy vấn toàn bộ sinh viên của các lớp cụ thể theo điểm học bổng giảm dần trong từng học kỳ
SELECT hoc_ky, masv, ten_sv, lop, diem_tbm, diem_ren_luyen, diem_hoc_bong
FROM sinhvien
WHERE lop IN ('48.01.CNTT.A', '48.01.CNTT.B', '48.01.CNTT.C')
AND nam_hoc = '2023-2024'  -- Thay đổi theo năm học bạn muốn
ORDER BY hoc_ky, diem_hoc_bong DESC;

-- Truy vấn sinh viên có điểm học bổng cao nhất trong mỗi lớp theo từng học kỳ
SELECT s1.hoc_ky, s1.lop, s1.masv, s1.ten_sv, s1.diem_hoc_bong
FROM sinhvien s1
WHERE s1.lop IN ('48.01.CNTT.A', '48.01.CNTT.B', '48.01.CNTT.C')
AND s1.nam_hoc = '2023-2024'
AND s1.diem_hoc_bong = (
    SELECT MAX(s2.diem_hoc_bong)
    FROM sinhvien s2
    WHERE s2.lop = s1.lop AND s2.hoc_ky = s1.hoc_ky AND s2.nam_hoc = '2023-2024'
)
ORDER BY s1.hoc_ky, s1.lop;

-- Truy vấn sinh viên có điểm trung bình môn (diem_tbm) cao nhất trong mỗi lớp theo từng học kỳ
SELECT s1.hoc_ky, s1.lop, s1.masv, s1.ten_sv, s1.diem_tbm
FROM sinhvien s1
WHERE s1.lop IN ('48.01.CNTT.A', '48.01.CNTT.B', '48.01.CNTT.C')
AND s1.nam_hoc = '2023-2024'
AND s1.diem_tbm = (
    SELECT MAX(s2.diem_tbm)
    FROM sinhvien s2
    WHERE s2.lop = s1.lop AND s2.hoc_ky = s1.hoc_ky AND s2.nam_hoc = '2023-2024'
)
ORDER BY s1.hoc_ky, s1.lop;

--  Truy vấn sinh viên có điểm rèn luyện cao nhất trong từng học kỳ
SELECT s1.hoc_ky, s1.lop, s1.masv, s1.ten_sv, s1.diem_ren_luyen
FROM sinhvien s1
WHERE s1.lop IN ('48.01.CNTT.A', '48.01.CNTT.B', '48.01.CNTT.C')
AND s1.nam_hoc = '2023-2024'
AND s1.diem_ren_luyen = (
    SELECT MAX(s2.diem_ren_luyen)
    FROM sinhvien s2
    WHERE s2.hoc_ky = s1.hoc_ky AND s2.lop = s1.lop AND s2.nam_hoc = '2023-2024'
)
ORDER BY s1.hoc_ky, s1.lop;