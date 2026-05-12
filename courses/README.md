# Courses

Thư mục này chứa workspace riêng cho từng khóa học hoặc từng bộ nội dung.

## Naming

Khuyến nghị dùng mã khóa hoặc mã nội bộ làm tên thư mục:

- `BIM70001`
- `BIM71501`
- `ISO19650-Intro`

## Standard Structure

Mỗi khóa học nên có các thư mục:

- `01_brief`
- `02_source`
- `03_authoring`
- `04_translation`
- `05_review`
- `06_delivery`

Trong `02_source/`, nếu khóa học đi theo package BSI chuẩn thì nên giữ các thành phần:

- `Delegate Workbook/`
- `Tutor Guide/`
- `Certificate Sample/`
- `Version Control/`

Và các file cấp package như:

- `Build List_...`
- `Important Course Info_...` hoặc `Important Course Information_...`

## Starter

Dùng script sau để tạo nhanh:

```powershell
powershell -ExecutionPolicy Bypass -File tools\new-course-workspace.ps1 `
  -CourseCode "BIM70001" `
  -CourseTitle "BIM Awareness"
```
