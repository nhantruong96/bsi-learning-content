# De xuat chinh sua ban dich ISO 19650 Part 2

Nguon kiem tra:
- EN: `_work/compare_example/01 Slides BIM71201ENGX_v4_Jul2025.json`
- VN: `_work/compare_example/01 Slides BIM71201ENGX_v4_Jul2025_VN.json`
- PPT dich: `References/Example/01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx`

Pham vi: 76 slides, 1028 text entries trong ban VN.

## Ket luan nhanh

Ban dich Part 2 la ban cu hon bo tri thuc hien tai. Nen uu tien sua theo cach tai su dung `translation/config/base_vi.json`, khong tao override rieng cho Part 2.

Cac nhom loi chinh:
- Con sot cac doan tieng Anh trong notes va mot so text tren slide.
- Thuat ngu `delivery team`, `task team`, `information delivery`, `information production`, `level of information need` chua dong nhat voi tri thuc chung hien tai.
- Mot so tieu de/tieu muc cua tieu chuan ISO/UK BIM Framework con giu English trong khi nen dich phan mo ta.
- Slide 50 can doi chieu truc quan vi title cua EN/VN/context khong khop hoan toan.

## Uu tien cao

| Slide | Path | Hien tai | De xuat | Ly do |
|---:|---|---|---|---|
| 8 | notes:3 | Doan notes con nguyen tieng Anh bat dau `BIM according to ISO 19650...` | Dich toan bo notes sang tieng Viet | Notes giang vien quan trong, khong nen de EN dai. |
| 9 | notes:3 | Doan notes con nguyen tieng Anh bat dau `UK: In the UK...` | Dich toan bo notes sang tieng Viet | Noi dung UK BIM Framework la boi canh chinh cua module. |
| 19 | notes:3 | Doan notes con nguyen tieng Anh bat dau `Delivery of information during a project...` | Dich toan bo notes sang tieng Viet | Noi dung giai thich Project Delivery Cycle dang bo trong. |
| 75 | notes:3 | Doan tong ket con nguyen tieng Anh `You should now be able to...` | `Anh/chị bây giờ có thể: ...` | Slide tong ket khoa hoc nen Viet hoa. |
| 1-76 | notes footer | `ISO 19650 Part 2: Building Information Modelling (BIM) Project Delivery Phase Training Course` | `Khóa đào tạo ISO 19650 Phần 2: Mô hình thông tin công trình (BIM) - Giai đoạn triển khai dự án` | Lap lai 75+ lan trong notes. Nen them vao `text_overrides`/`full_overrides` chung. |

## Chuan hoa thuat ngu

| Nhom | So lan thay trong ban VN | Hien tai | De xuat |
|---|---:|---|---|
| `delivery team` | 26 | `nhóm bàn giao` | `nhóm triển khai` |
| `task team` | 30+ | `nhóm công việc` | `nhóm nhiệm vụ` |
| `information delivery` | 32 | `bàn giao thông tin` | `chuyển giao thông tin` |
| `information production` | 11 | `sản xuất thông tin` | `tạo lập thông tin` |
| `level of information need` | 14 | `mức độ nhu cầu thông tin (LOIN)` | `mức độ thông tin cần thiết (LOIN)` |
| `information containers` | 2 | `information containers` | `các container thông tin` |
| `lead appointed party` | 4 | `Lead appointed party` | `bên được giao nhiệm vụ chính` |
| `appointing party / appointed party` | 5 | con sot English | `bên giao nhiệm vụ` / `bên được giao nhiệm vụ` |

Vi du can sua:
- Slide 14 `59/65`: `(Các) nhóm công việc` -> `(Các) nhóm nhiệm vụ`
- Slide 14 `121/120`: `Bên được giao nhiệm vụ / nhóm công việc` -> `Bên được giao nhiệm vụ / nhóm nhiệm vụ`
- Slide 34 `2`: `Yêu cầu thông tin được phân tầng xuống và xuyên suốt các nhóm bàn giao` -> `Yêu cầu thông tin được phân tầng xuống và xuyên suốt các nhóm triển khai`
- Slide 43 `5`: `Kế hoạch huy động của nhóm bàn giao...` -> `Kế hoạch huy động của nhóm triển khai...`
- Slide 50 `4`: `Kế hoạch bàn giao thông tin của nhóm nhiệm vụ (TIDP)` -> `Kế hoạch chuyển giao thông tin của nhóm nhiệm vụ (TIDP)`
- Slide 52 `5`: `Kế hoạch bàn giao thông tin tổng thể (MIDP)` -> `Kế hoạch tổng thể chuyển giao thông tin (MIDP)`

## Tieng Anh con sot tren slide

| Slide | Path | Hien tai | De xuat |
|---:|---|---|---|
| 8 | 18/13 | `ISO 19650-1:2018 Concepts and principles` | `ISO 19650-1:2018 Khái niệm và nguyên tắc` |
| 8 | 45/46 | `ISO 19650-3:2020 Operational phase` | `ISO 19650-3:2020 Giai đoạn vận hành` |
| 8 | 55/56 | `ISO 19650-5:2020 Security` | `ISO 19650-5:2020 An ninh` |
| 8 | 61/62 | `ISO 19650-2:2018 Delivery phase` | `ISO 19650-2:2018 Giai đoạn triển khai` |
| 8 | 66/67 | `ISO 19650-4:2022 Information exchange` | `ISO 19650-4:2022 Trao đổi thông tin` |
| 9 | 21/22 | `BS 8536:2022 Design, manufacture and construction for operability` | `BS 8536:2022 Thiết kế, chế tạo và thi công phục vụ khả năng vận hành` |
| 10 | 15 | `... information containers` | `... các container thông tin` |
| 11 | 5 | `Bao gồm UK National Annex` | `Bao gồm Phụ lục quốc gia của Vương quốc Anh` |
| 16 | notes:6\|cell:1,1 | `Concepts and principles from ISO 19650 Part 2: Project Delivery Phase` | `Khái niệm và nguyên tắc từ ISO 19650 Phần 2: Giai đoạn triển khai dự án` |
| 30 | 6 | `= Appointing Party, Lead Appointed Party hoặc Appointed Party...` | `= bên giao nhiệm vụ, bên được giao nhiệm vụ chính hoặc bên được giao nhiệm vụ...` |
| 34 | 75 | `1 delivery team appointed parties` | `1 nhóm triển khai / các bên được giao nhiệm vụ` |
| 34 | 77 | `Appointing party 4 delivery teams with lead appointed parties` | `Bên giao nhiệm vụ; 4 nhóm triển khai có bên được giao nhiệm vụ chính` |
| 57 | 47/48 | `Work in Progress Information being developed...` | `WIP - Thông tin đang được bên tạo lập hoặc nhóm nhiệm vụ phát triển...` |
| 61 | 2 | `Status codes in BS EN ISO 19650-2 National Annex` | `Mã trạng thái trong Phụ lục quốc gia của BS EN ISO 19650-2` |

## Diem can doi chieu thu cong

| Slide | Path | Van de | De xuat xu ly |
|---:|---|---|---|
| 50 | 4 | EN JSON ghi `Physical controls (Annex B.2)`, trong khi context slide/notes dang noi ve TIDP va muc do thong tin. Ban VN hien la `Kế hoạch bàn giao thông tin của nhóm nhiệm vụ (TIDP)`. | Can mo PPT de doi chieu hinh thuc. Kha nang cao title dung nen la `Kế hoạch chuyển giao thông tin của nhóm nhiệm vụ (TIDP)`, khong phai `Physical controls`. |
| 11 | 14, 26/13-26/24 | Cac doan tren bia tieu chuan EN/FR/DE/CEN con nguyen. | Neu day la anh/cover cua tieu chuan thi co the giu. Neu la text editable, chi nen dich caption/chuc nang, khong can dich toan bo noi dung phap ly tren bia. |
| 57 | Shared/Published/Archive/WIP | Dang vua giu English label vua dich mo ta. | Chap nhan duoc neu coi day la ten trang thai CDE; can thong nhat format: `Shared - ...`, `Published - ...`, `Archive - ...`, `WIP - ...`. |

## De xuat cach sua

1. Khong tao file override Part 2.
2. Bo sung cac override chung vao `base_vi.json` cho:
   - Tieu de khoa hoc Part 2.
   - Ten cac phan ISO 19650: Concepts and principles, Delivery phase, Operational phase, Information exchange, Security, Health & Safety.
   - `UK National Annex` -> `Phụ lục quốc gia của Vương quốc Anh`.
   - `Status codes in BS EN ISO 19650-2 National Annex`.
3. Chay lai script voi source EN va draft VN, khong truyen `-OverridePath`, de ap dung tri thuc chung hien tai:

```powershell
powershell -ExecutionPolicy Bypass -File tools\translate-ppt.ps1 `
  -InputPath "References\Example\01 Slides BIM71201ENGX_v4_Jul2025.pptx" `
  -DraftPath "References\Example\01 Slides BIM71201ENGX_v4_Jul2025_VN.pptx" `
  -OutputPath "References\Example\01 Slides BIM71201ENGX_v4_Jul2025_VN.reviewed.pptx"
```

4. Sau khi sinh file reviewed, can kiem tra lai cac slide: 8, 9, 10, 14, 17-21, 30, 34, 43, 50-53, 57, 61, 75.
