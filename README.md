# BSI Learning Content

Workspace này phục vụ việc dịch slide đào tạo BIM / ISO 19650 sang tiếng Việt theo `AGENTS.md` và `glossary.md`.

## Nguồn Quyết Định

Khi dịch, chỉ dùng thứ tự ưu tiên sau:

1. `glossary.md`
2. `AGENTS.md`
3. `Example/`
4. `References/`

`Example/` là mẫu văn phong và cách xử lý thuật ngữ đã được duyệt. `References/` chỉ dùng để kiểm tra nghĩa nguồn hoặc bối cảnh tiêu chuẩn. Không dùng cache, bản dịch trung gian cũ, override cũ, hoặc cấu trúc workspace cũ để quyết định văn phong hay thuật ngữ.

Các file và thư mục chính:

- `AGENTS.md`: quy tắc dịch, cấu trúc đầu ra và checklist chất lượng.
- `glossary.md`: thuật ngữ bắt buộc dùng khi dịch.
- `vi_translation.md`: bản dịch tiếng Việt theo cấu trúc slide/note.
- `translation_issues.md`: nhật ký các điểm OCR, nguồn hoặc thuật ngữ cần kiểm tra.
- `slides/`: deck nguồn đang xử lý, text trích xuất và ảnh slide.
- `References/`: tài liệu tham chiếu, tiêu chuẩn, ví dụ gốc.
- `Example/`: deck ví dụ nhanh, giữ nguyên để đối chiếu.

## Cấu trúc dịch slide hiện tại

```text
project-root/
├─ AGENTS.md
├─ glossary.md
├─ vi_translation.md
├─ translation_issues.md
├─ slides/
│  ├─ source.pptx
│  ├─ exported_text/
│  └─ images/
```

Ghi chú: `slides/source.pptx` là vị trí dành cho deck nguồn đang dịch. Các thư mục `References/` và `Example/` được giữ nguyên ở gốc workspace để tiện đối chiếu.

## Quy ước làm việc

- Đọc `AGENTS.md` và `glossary.md` trước khi dịch.
- Đặt deck nguồn đang xử lý tại `slides/source.pptx`.
- Đặt text trích xuất tại `slides/exported_text/`.
- Đặt ảnh slide tại `slides/images/`.
- Ghi bản dịch vào `vi_translation.md`.
- Ghi mọi điểm chưa chắc chắn vào `translation_issues.md`.
- Không dùng lại cấu hình dịch tự động, override cũ hoặc cache dịch máy để quyết định thuật ngữ.
- Không dùng `_work/`, `translation/`, `authoring/`, `courses/`, `tools/`, hoặc config workspace cũ làm nguồn tham khảo nếu chúng xuất hiện lại.

## Ghi chú

- Pipeline dịch tự động cũ đã được loại bỏ vì có thuật ngữ xung đột với `glossary.md`.
- Workspace hiện được giữ tối giản để tránh mọi bias từ pipeline hoặc cấu hình cũ.
