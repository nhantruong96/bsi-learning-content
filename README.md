# BSI Learning Content

Workspace này phục vụ nhiều mục đích liên quan đến học liệu BSI, không chỉ dịch workbook.

Các luồng công việc chính:

- `translation/`: dịch và bản địa hóa slide, workbook, DOCX, PPTX.
- `authoring/`: biên soạn giáo trình mới, cấu trúc buổi học, hoạt động, đánh giá.
- `courses/`: nơi tổ chức từng khóa học hoặc từng bộ nội dung theo mã khóa.
- `References/`: tài liệu tham chiếu, tiêu chuẩn, ví dụ gốc.
- `References/Example/`: thư viện hồ sơ khóa học mẫu, mỗi thư mục con là một bộ hồ sơ hoàn chỉnh của một khóa.
- `tools/`: script hỗ trợ trích xuất, dịch, đóng gói và scaffold workspace.
- `_work/`: file trung gian, cache, JSON extract, bản build tạm.

## Định hướng sử dụng

Workspace này phù hợp cho:

- dịch học liệu hiện có sang tiếng Việt;
- biên soạn mới từ tài liệu chuẩn hoặc ghi chú nội bộ;
- xây dựng outline khóa học, lesson plan, activity sheet, assessment;
- chuẩn hóa đầu ra cho review và đóng gói phát hành nội bộ.

## Cấu trúc hồ sơ khóa học mẫu

Trong `References/Example/`, mỗi thư mục khóa học hiện được xem là một package chuẩn. Bên trong thường có:

- `Delegate Workbook/`
- `Tutor Guide/` hoặc `Tutor guide/`
- `Certificate Sample/` hoặc `Certificate sample/`
- `Version Control/` hoặc `Version control/`
- file gốc cấp package như `Build List_...` và `Important Course Info(rmation)_...`

Các biến thể chữ hoa/chữ thường và cách viết `Info`/`Information` đều được xem là hợp lệ trong config mới.

## Cấu trúc đề xuất cho khóa học mới

Mỗi khóa học nên có một thư mục riêng trong `courses/`, ví dụ:

```text
courses/
  BIM70001/
    01_brief/
    02_source/
      Delegate Workbook/
      Tutor Guide/
      Certificate Sample/
      Version Control/
    03_authoring/
    04_translation/
    05_review/
    06_delivery/
```

## Khởi tạo nhanh một khóa học mới

```powershell
powershell -ExecutionPolicy Bypass -File tools\new-course-workspace.ps1 `
  -CourseCode "BIM99999" `
  -CourseTitle "Sample Course"
```

## Quy ước làm việc

- Nguồn gốc tài liệu gốc đặt ở `References/` hoặc `courses/<code>/02_source/`.
- Nếu dùng package kiểu BSI, nên giữ nguyên cấu trúc hồ sơ như trong `References/Example/<course-package>/`.
- Nội dung đang biên soạn đặt ở `courses/<code>/03_authoring/`.
- Bản dịch và override đặt ở `courses/<code>/04_translation/` hoặc `translation/config/` nếu dùng chung.
- Tài liệu chờ rà soát đặt ở `courses/<code>/05_review/`.
- Bản giao cuối cùng đặt ở `courses/<code>/06_delivery/`.

## Ghi chú

- Các script dịch hiện tại vẫn được giữ nguyên để đảm bảo tương thích ngược.
- Tên khuyến nghị cho thư mục gốc trên máy là `BSI Learning Content` để đồng bộ với scope và cấu hình hiện tại.
