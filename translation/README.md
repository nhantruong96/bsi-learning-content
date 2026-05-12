# Translation Pipeline

Thư mục này chứa cấu hình và tài liệu cho luồng dịch/bản địa hóa học liệu.

Trong workspace hiện tại, `translation/` là một nhánh chức năng của hệ thống học liệu rộng hơn, không còn là mục đích duy nhất của toàn bộ môi trường.

Xem thêm:

- `README.md` ở thư mục gốc để nắm cấu trúc tổng thể workspace.
- `authoring/` nếu cần biên soạn mới thay vì chỉ dịch.
- `courses/` nếu muốn tổ chức tài liệu theo từng mã khóa học.

## Cấu trúc

- `config/base_vi.json`
  Cấu hình dịch nền cho tiếng Việt:
  glossary, protected terms, keep patterns, override câu ngắn, override đoạn đầy đủ, global replacements.

- `config/template.deck_overrides.vi.json`
  Mẫu override cho từng deck.
  Dùng khi một bộ slide có:
  từ phải giữ nguyên,
  cách dịch riêng,
  hoặc một số notes/shape cần sửa theo `slide|path`.

## Cách dùng

### 1. Dịch từ đầu sang file mới

```powershell
powershell -ExecutionPolicy Bypass -File tools\translate-ppt.ps1 `
  -InputPath "References\Example\BIM71401ENGX_v3_Jul2025\Delegate Workbook\01 Slides_BIM71401ENGX_v3_Jul2025.pptx" `
  -OutputPath "courses\BIM71401\04_translation\01 Slides_BIM71401ENGX_v3_Jul2025_VN.pptx"
```

### 2. Dịch tiếp trên một bản VN đã có sẵn

```powershell
powershell -ExecutionPolicy Bypass -File tools\translate-ppt.ps1 `
  -InputPath "References\Example\BIM71201ENGX_v4_Jul2025\Delegate Workbook\01 Slides BIM71201ENGX_v4_Jul2025.pptx" `
  -DraftPath "courses\BIM71201\04_translation\01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx" `
  -OutputPath "courses\BIM71201\04_translation\01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx"
```

### 3. Dùng thêm override riêng cho từng deck

```powershell
Copy-Item translation\config\template.deck_overrides.vi.json translation\config\BIM71201.overrides.vi.json
```

Sau đó sửa file override và chạy:

```powershell
powershell -ExecutionPolicy Bypass -File tools\translate-ppt.ps1 `
  -InputPath "References\Example\BIM71201ENGX_v4_Jul2025\Delegate Workbook\01 Slides BIM71201ENGX_v4_Jul2025.pptx" `
  -DraftPath "courses\BIM71201\04_translation\01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx" `
  -OutputPath "courses\BIM71201\04_translation\01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx" `
  -OverridePath "translation\config\BIM71201.overrides.vi.json"
```

## Cách hiểu thư mục Example mới

`References/Example/` hiện là thư viện package khóa học mẫu.

Mỗi thư mục con tương ứng một khóa học và thường có:

- `Delegate Workbook/`: slide, workbook, reference handout để dịch hoặc trích xuất.
- `Tutor Guide/`: tài liệu cho giảng viên.
- `Certificate Sample/`: mẫu chứng chỉ.
- `Version Control/`: lịch sử thay đổi, proposal, record.
- file root như `Build List_...` và `Important Course Info(rmation)_...`.

Khuyến nghị: lấy input từ `References/Example/.../Delegate Workbook/` và ghi đầu ra sang `courses/<code>/04_translation/` thay vì ghi đè vào thư mục mẫu.

## Ý nghĩa các block config

- `protected_terms`
  Các thuật ngữ sẽ được khóa trước khi dịch để tránh bị dịch sai.

- `keep_patterns`
  Các pattern cần giữ nguyên như mã tiêu chuẩn, mã trạng thái, email, URL, mã tài liệu.

- `text_overrides`
  Override theo câu/đoạn ngắn, dùng khi nội dung lặp lại nhiều lần.

- `full_overrides`
  Override cho các đoạn dài lặp lại nguyên văn, thường là phần note mở đầu hoặc hướng dẫn lớp học.

- `global_replacements`
  Hậu xử lý để chuẩn hóa cách dịch, ví dụ `thùng chứa thông tin` -> `container thông tin`.

- `path_overrides`
  Sửa đúng một vị trí cụ thể theo khóa `slide|path`.
  Ví dụ: `10|notes:3`

## File work tạm

Script sẽ tạo các file `.source.json`, `.draft.json`, `.translations.json` trong `_work`.
Cache dịch được tái sử dụng tại:

`_work/cache/google_vi_cache.json`

## Phụ thuộc

Script Python cần package:

```powershell
pip install deep-translator
```
