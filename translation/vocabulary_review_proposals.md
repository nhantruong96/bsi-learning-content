# De xuat cap nhat tu vung dich ISO 19650/BIM

Nguon so sanh: cac cap file co va khong co hau to `_VN` trong `References/Example`.

Huong dan sua:
- Cot `Phe duyet`: dien `Yes`, `No`, hoac `Modify`.
- Neu chon `Modify`, sua truc tiep cot `De xuat tieng Viet`.
- Cot `Ghi chu`: ghi quy tac rieng, boi canh khong ap dung, hoac cach viet mong muon.
- File nay chi la danh sach review, chua duoc ap dung vao `translation/config/base_vi.json`.

## Thuat ngu chinh

| ID | Uu tien | English | De xuat tieng Viet | Ly do / vi du | Phe duyet | Ghi chu |
|---|---|---|---|---|---|---|
| T001 | Cao | appointing party | ben giao nhiem vu | Mot so cho con de `appointing party`, `Appointing Party`. |  |  |
| T002 | Cao | lead appointed party | ben duoc giao nhiem vu chinh | Mot so slide con nguyen `Lead appointed party`. |  |  |
| T003 | Cao | appointed party | ben duoc giao nhiem vu | Nen khoa ca dang viet hoa `Appointed Party`. |  |  |
| T004 | Cao | appointment | viec giao nhiem vu | Co loi dich thanh `cuoc hen`; de xuat nay khop voi cap `appointing/appointed party`. | bo nhiem | Neu muon giu `bo nhiem`, sua o day. |
| T005 | Cao | appointments | cac giao nhiem vu | Tranh loi `cac cuoc hen`. | cac bo nhiem | Co the sua thanh `cac quan he giao nhiem vu`. |
| T006 | Cao | pre-appointment | truoc khi giao nhiem vu | Dung cho `pre-appointment BEP`. | truoc bo nhiem |  |
| T007 | Cao | post-appointment | sau khi giao nhiem vu | Dung cho `post-appointment BEP`. | sau bo nhiem |  |
| T008 | Cao | delivery team | nhom trien khai | Hien dang lan `nhom trien khai`, `nhom ban giao`, va co cho con tieng Anh. |  |  |
| T009 | Cao | task team | nhom nhiem vu | Co cho dich thanh `nhom cong viec`; nen chuan hoa. | nhom nhiem vu |  |
| T010 | Cao | information container | container thong tin | Hien lan `container thong tin`, `thung chua thong tin`, va `information containers`. |  |  |
| T011 | Cao | information delivery | ban giao thong tin | Nen dung nhat quan cho IDC, MIDP, TIDP. | chuyen giao |  |
| T012 | Cao | Information Delivery Cycle (IDC) | Chu trinh ban giao thong tin (IDC) | Hien co cho con `The Information Delivery Cycle`. | Chu trinh chuyen giao thong tin |  |
| T013 | Cao | information exchange | trao doi thong tin | Khac voi `information delivery`; `EIR` da dich theo huong nay. |  |  |
| T014 | Cao | Exchange Information Requirements (EIR) | Yeu cau trao doi thong tin (EIR) | Dang dung tuong doi tot; nen khoa de tranh bien the. |  |  |
| T015 | Trung binh | information requirements | yeu cau thong tin | Nen dung thong nhat, tranh `nhu cau thong tin` khi dang noi ve requirements. |  |  |
| T016 | Trung binh | level of information need | muc do thong tin can thiet (LOIN) | Ban hien tai `muc do nhu cau thong tin` hoi kho hieu. |  | Neu muon bam sat ban cu, sua lai. |
| T017 | Trung binh | information production | tao lap thong tin | Co cho la `san xuat thong tin`, nghe may moc. |  |  |
| T018 | Trung binh | produce information | tao lap thong tin | Dong bo voi `information production`. |  |  |
| T019 | Trung binh | information production methods and procedures | phuong phap va quy trinh tao lap thong tin | Ban hien tai da dung o nhieu cho; nen khoa. |  |  |
| T020 | Trung binh | reference information and shared resources | thong tin tham chieu va tai nguyen dung chung | Hien lan `nguon luc dung chung` va `tai nguyen dung chung`. |  |  |
| T021 | Trung binh | shared resources | tai nguyen dung chung | Trong ngu canh mau, quy tac, tai lieu dung chung, `tai nguyen` ro hon `nguon luc`. |  |  |
| T022 | Trung binh | authorization for release | cho phep phat hanh | Co cho con nguyen `CDE prior to authorization for release`. |  | Co the sua thanh `phe duyet phat hanh`. |
| T023 | Trung binh | acceptance criteria | tieu chi chap nhan | Mot o trong BIM713 con nguyen `Acceptance criteria`. |  |  |
| T024 | Trung binh | status code(s) | ma trang thai | Co tieu de con nguyen `Status codes in BS EN...`. |  |  |
| T025 | Thap | revision code(s) | ma phien ban sua doi | Ro nghia hon `ma phien ban` khi doi chieu `revision`. |  |  |
| T026 | Thap | revision | phien ban sua doi | Tranh nham voi version thong thuong neu ngu canh la CDE metadata. |  |  |
| T027 | Thap | facility management | quan ly co so vat chat | Co cho dung `quan ly tai san/co so`; `co so` hoi cut nghia. |  |  |
| T028 | Thap | Information Protocol | Giao thuc thong tin | Mot so ten/tieu de con nguyen tieng Anh. |  | Neu la ten tai lieu rieng, co the giu English kem dich. |
| T029 | Thap | responsibility matrix | ma tran phan cong trach nhiem | Ban hien tai kha on; nen khoa de giu nhat quan. |  |  |
| T030 | Thap | federation strategy | chien luoc lien hop mo hinh | Ban hien tai kha on; nen khoa de giu nhat quan. |  |  |
| T031 | Thap | information management function | chuc nang quan ly thong tin | Ban hien tai kha on; nen khoa de giu nhat quan. |  |  |
| T032 | Thap | trigger event | su kien kich hoat | Ban hien tai kha on; nen khoa de giu nhat quan. |  |  |
| T033 | Thap | information management risk register | so dang ky rui ro quan ly thong tin | Co noi dung lien quan den ISO 19650-2/3. |  |  |
| T034 | Thap | capability and capacity | nang luc va nguon luc | Ban hien tai dang dung nhieu; can quyet dinh co giu hay sua thanh `nang luc va kha nang dap ung`. |  |  |

## De xuat global replacements

| ID | Hien tai | Thay bang | Ly do | Phe duyet | Ghi chu |
|---|---|---|---|---|---|
| R001 | cuoc hen | viec giao nhiem vu | Sua loi dich `appointment`. | bo nhiem |  |
| R002 | cac cuoc hen | cac giao nhiem vu | Sua loi dich `appointments`. | cac bo nhiem |  |
| R003 | nhom cong viec | nhom nhiem vu | Chuan hoa `task team`. |  |  |
| R004 | nhom ban giao | nhom trien khai | Chuan hoa `delivery team`. |  |  |
| R005 | thung chua thong tin | container thong tin | Chuan hoa `information container`. |  |  |
| R006 | information containers | cac container thong tin | Sua tieng Anh con sot. |  |  |
| R007 | san xuat thong tin | tao lap thong tin | Chuan hoa `information production`. |  |  |
| R008 | Acceptance criteria | Tieu chi chap nhan | Sua tieng Anh con sot. |  |  |
| R009 | Status codes | Ma trang thai | Sua tieng Anh con sot. |  |  |
| R010 | CDE prior to authorization for release | CDE truoc khi duoc cho phep phat hanh | Sua cum tieng Anh con sot trong notes. |  |  |

## Cau hoi can quyet dinh

| ID | Van de | Phuong an de xuat | Phe duyet / Sua |
|---|---|---|---|
| Q001 | Nen dich `appointment` la gi? | Uu tien `viec giao nhiem vu`; chi dung `bo nhiem` neu anh muon bam cach dich hien tai. | bo nhiem |
| Q002 | Nen dich `delivery team` la gi? | Uu tien `nhom trien khai`; khong dung `nhom ban giao` de tranh nham voi hanh dong ban giao. |  |
| Q003 | Nen dich `level of information need` la gi? | Uu tien `muc do thong tin can thiet (LOIN)`; ban cu la `muc do nhu cau thong tin`. |  |
| Q004 | Nen dich `shared resources` la gi? | Uu tien `tai nguyen dung chung`; ban cu co luc la `nguon luc dung chung`. |  |
