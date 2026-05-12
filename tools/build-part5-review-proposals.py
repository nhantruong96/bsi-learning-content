from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]

SOURCE_JSON = ROOT / "_work" / "part5_source_en.json"
BASE_CONFIG_JSON = ROOT / "translation" / "config" / "base_vi.json"
PART2_EN_JSON = ROOT / "_work" / "compare_example" / "01 Slides BIM71201ENGX_v4_Jul2025.json"
PART2_VN_JSON = ROOT / "_work" / "compare_example" / "01 Slides BIM71201ENGX_v4_Jul2025_VN.json"
PART4_EN_JSON = ROOT / "_work" / "compare_example" / "01 Slides_BIM71401ENGX_v3_Jul2025.json"
PART4_VN_JSON = ROOT / "_work" / "compare_example" / "01 Slides_BIM71401ENGX_v3_Jul2025_VN.json"
OUTPUT_JSON = ROOT / "_work" / "part5_review_proposals_curated.json"
LATEST_PROPOSAL_JSON = OUTPUT_JSON


def normalize_text(text: str | None) -> str:
    if text is None:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\u000b", "").strip("\n")


def finalize_text(text: str) -> str:
    return normalize_text(text).replace("\n", "\r")


def cleanup_translation(text: str) -> str:
    cleaned = normalize_text(text)

    literal_replacements = (
        ("Phần 2 Giai đoạn bàn giao", "Phần 2 Giai đoạn triển khai"),
        ("Giai đoạn bàn giao", "Giai đoạn triển khai"),
        ("\nSlide\n", "\nTrang trình bày\n"),
        ("bao gồm slide,", "bao gồm các trang trình bày,"),
        ("bao gồm slides,", "bao gồm các trang trình bày,"),
        ("các slide trước", "các trang trình bày trước đó"),
        ("slide tiếp theo", "trang trình bày tiếp theo"),
        ("bổ nhiệm riêng một người cụ thể", "chỉ định riêng một người cụ thể"),
    )
    for source_text, target_text in literal_replacements:
        cleaned = cleaned.replace(source_text, target_text)

    cleaned = re.sub(r"\bSlides\b", "Trang trình bày", cleaned)

    return cleaned


def key_for(slide: int, path: str) -> str:
    return f"{slide}|{path}"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_optional_json(path: Path):
    if not path.exists():
        return None
    return load_json(path)


def load_bilingual_memory(en_path: Path, vn_path: Path) -> dict[str, str]:
    en_deck = load_json(en_path)
    vn_deck = load_json(vn_path)

    en_map = {
        key_for(entry["slide"], entry["path"]): normalize_text(entry.get("text", ""))
        for slide in en_deck["slides"]
        for entry in slide["entries"]
    }
    vn_map = {
        key_for(entry["slide"], entry["path"]): normalize_text(entry.get("text", ""))
        for slide in vn_deck["slides"]
        for entry in slide["entries"]
    }

    memory: dict[str, str] = {}
    for entry_key, english in en_map.items():
        vietnamese = vn_map.get(entry_key, "")
        if english and vietnamese and vietnamese != english:
            memory.setdefault(english, vietnamese)
    return memory


MANUAL_PATH_OVERRIDES = {
    "1|notes:8": """
        Tài liệu này chỉ dành cho mục đích sử dụng cá nhân của học viên tham dự khóa học do BSI tổ chức.
        Không phần nào của tài liệu này được phép sao chép, lưu trữ điện tử hoặc truyền tải dưới bất kỳ hình thức hay phương tiện nào nếu chưa có sự đồng ý trước bằng văn bản của BSI.
    """,
    "3|6": """
        Tài liệu:
        Trang trình bày
        Tài liệu tham khảo
    """,
    "3|notes:3": """
        Giảng viên sẽ giới thiệu bố cục và cách triển khai của khóa học.

        Khóa học này gồm phần trình bày, các hoạt động dành cho học viên và thảo luận.

        Sổ tay học viên tập hợp toàn bộ tài liệu liên quan đến khóa học, bao gồm các trang trình bày, hoạt động và tài liệu tham khảo. Đáp án mẫu cho các hoạt động cũng nằm trong phần tài liệu tham khảo. Vui lòng chỉ xem đáp án sau khi đã hoàn thành từng hoạt động, hoặc khi anh/chị thực sự bị vướng.

        Anh/chị sẽ thu được nhiều giá trị nhất từ khóa học khi tham gia tích cực, đặt câu hỏi và trao đổi trong các phần thảo luận cũng như hoạt động. Không có câu hỏi nào là ngớ ngẩn; hãy chủ động nhờ giảng viên hỗ trợ khi cần.
    """,
    "6|notes:3": """
        Mục tiêu khóa học
        Trang bị cho những người phụ trách quản lý công việc cộng tác và quản lý dự án hoặc tài sản BIM những kiến thức và kỹ năng cốt lõi cần thiết để hiểu và triển khai quản lý an ninh.

        Sau khi hoàn thành khóa học này, anh/chị sẽ có thể:
        Giải thích các loại mối đe dọa an ninh đối với tài sản xây dựng và thông tin liên quan
        Nhận biết các vấn đề an ninh liên quan đến ISO 19650, Môi trường dữ liệu chung (CDE) và BIM
        Xác định vai trò của người quản lý an ninh
        Giải thích các tài liệu và cách triển khai những chính sách cần thiết cho tư duy an ninh
    """,
    "7|notes:2": """
        Cấu trúc của khóa học này nhìn chung bám theo cấu trúc của tiêu chuẩn ISO, đồng thời đưa thêm các phụ lục ở những chỗ phù hợp.

        Phiên đầu tiên tập trung vào tổng quan các cân nhắc an ninh liên quan đến tài sản xây dựng và thông tin dự án/tài sản. Phần này bao gồm việc xem xét một số định nghĩa và một số gợi ý mang tính định hướng về những gì cần được bảo vệ, cũng như cần bảo vệ trước những mối đe dọa nào.

        Phiên thứ hai xem xét các cân nhắc chiến lược đối với việc quản lý tài sản và thông tin theo hướng chú trọng an ninh, cũng như cách xây dựng chiến lược an ninh. Các yêu cầu cho nội dung này nằm trong Điều 4, 5 và 6.

        Phiên thứ ba xem xét các vấn đề quản lý, tức cách quản lý tư duy an ninh ở cấp độ dự án hoặc tài sản. Phần này liên quan đến việc chuyển chiến lược thành kế hoạch quản lý, bao gồm cả cách xử lý các vi phạm an ninh. Các yêu cầu tương ứng nằm trong Điều 7 và 8, cùng các loại biện pháp kiểm soát trong Phụ lục B.

        Phiên cuối cùng xem xét các vấn đề vận hành, tức cách triển khai tư duy an ninh ở cấp độ dự án hoặc tài sản. Phần này liên quan đến việc chuyển kế hoạch quản lý thành các biện pháp kiểm soát cụ thể, bao gồm đánh giá bên thứ ba và thiết lập các thỏa thuận chính thức, như nêu trong Điều 9, Phụ lục C và D, để anh/chị bắt đầu xác định các bước tiếp theo cho việc triển khai tư duy an ninh.

        Tổng quan
        Lời nói đầu, giới thiệu và 
        1. Phạm vi
        2. Tài liệu tham khảo
        3. Thuật ngữ và định nghĩa
        Chiến lược
        4. Nhu cầu
        5. Cách tiếp cận
        6. Chiến lược
        Quản lý
        7. Quản lý
        8. Quản lý vi phạm
        Triển khai
        9. Làm việc với các bên được giao nhiệm vụ
        C. Đánh giá bên thứ ba
        D. Thỏa thuận chia sẻ thông tin
    """,
    "10|notes:3": """
        Điểm cốt lõi của ISO 19650-5 là tư duy an ninh phải xuyên suốt toàn bộ tổ chức khách hàng và mọi hoạt động cộng tác liên quan đến dự án cũng như quản lý tài sản. Kinh nghiệm và bài học rút ra cần được đưa ngược trở lại để duy trì mức độ tư duy an ninh phù hợp.
    """,
    "11|notes:3": """
        An ninh là mối quan tâm đối với cả tài sản vật chất lẫn tài sản thông tin. Các mối đe dọa có nhiều dạng khác nhau, bao gồm xâm nhập vật lý để lấy cắp hàng hóa có giá trị (kho lưu giữ an toàn), gây hư hỏng bằng phương tiện giao thông hoặc giành quyền truy cập trái phép (hàng rào an ninh). Các mối đe dọa mạng cũng liên quan đến truy cập trái phép (để phá hoại hệ thống máy tính) hoặc đánh cắp thông tin số. Hành vi đánh cắp có thể diễn ra công khai (kẻ xâm nhập vật lý sao chép thông tin từ máy tính) hoặc bí mật (chặn dữ liệu/thông tin trong quá trình truyền từ địa điểm này sang địa điểm khác).

        Cần lưu ý rằng vi phạm an ninh mạng có thể mở đường tiếp cận tài sản vật chất, và vi phạm an ninh vật lý có thể mở đường tiếp cận dữ liệu. Đây là một trong những lý do khiến các mối đe dọa đối với chính tài sản xây dựng và thông tin liên quan đến chúng cần được xem xét một cách tổng thể.
        Điều quan trọng là phải nắm những khái niệm nền tảng về an ninh và hiểu vì sao khái niệm này là một phần cốt yếu của “BIM cộng tác”.

        Sơ đồ này sắp xếp các khái niệm trong Phụ lục B.3.3 của ISO 19650-5.

        Tính bảo mật - Kiểm soát quyền truy cập và ngăn chặn việc truy cập trái phép vào thông tin có thể nhạy cảm khi xét riêng lẻ hoặc khi tổng hợp
        Sự chiếm hữu - Bảo đảm việc ngăn chặn hành vi kiểm soát, thao túng hoặc can thiệp trái phép luôn được duy trì
        Tính toàn vẹn - Duy trì tính nhất quán, mạch lạc và cấu hình của thông tin và hệ thống, đồng thời ngăn chặn các thay đổi trái phép
        Tính hữu dụng - Bảo đảm thông tin và hệ thống tài sản vẫn hữu dụng, có thể sử dụng được trong suốt vòng đời của tài sản xây dựng
        Tính xác thực - Bảo đảm các đầu vào và đầu ra của hệ thống tài sản xây dựng là xác thực và không bị can thiệp
        Tính sẵn sàng - Bảo đảm thông tin tài sản có thể truy cập được và đáng tin cậy
        An toàn - Ngăn ngừa các trạng thái nguy hại có thể dẫn đến chấn thương hoặc tử vong trong quá trình thiết kế, triển khai, vận hành và bảo trì hệ thống tài sản xây dựng
        Khả năng chống chịu - Khả năng của thông tin và hệ thống tài sản trong việc chuyển đổi, phục hồi và tái tạo kịp thời để ứng phó với các sự kiện bất lợi
    """,
    "14|notes:3": """
        Các mối đe dọa an ninh có thể xuất hiện dưới nhiều hình thức. ISO 19650-5 không nhằm liệt kê đầy đủ mọi loại mối đe dọa có thể có, nhưng nêu bật những vấn đề quan trọng nhất.

        Các hành vi cố ý gây hại có thể đến từ nhiều nguồn khác nhau, như mã độc cài cắm, vi phạm từ bên ngoài, hoặc vi phạm do nhân viên nội bộ hay nhà thầu gây ra hoặc tiếp tay.

        Việc lộ dữ liệu cá nhân hiện phải tuân thủ các yêu cầu nghiêm ngặt hơn nhiều theo Quy định chung về bảo vệ dữ liệu (GDPR) có hiệu lực từ tháng 5 năm 2018. Các quy định liên quan khác còn bao gồm bảo vệ môi trường và quyền yêu cầu tiếp cận thông tin.

        Việc mất mát hoặc tiết lộ tài sản trí tuệ có thể bao gồm nhiều loại tài liệu khác nhau, như thiết kế, bí mật thương mại, quy trình độc quyền và nguyên mẫu vật lý.

        Việc mất mát hoặc tiết lộ tài liệu nhạy cảm về thương mại có thể bao gồm các thông tin tài chính, đặc biệt là giá hàng hóa và dịch vụ. Trong môi trường thương mại, một số thông tin về giá vẫn cần được chuyển cho tổ chức khách hàng tiềm năng; vì vậy nhà cung cấp phải tin tưởng rằng khách hàng có thể và sẽ bảo vệ an toàn thông tin đó.
    """,
    "27|notes:3": """
        Ví dụ về “tổ chức khác” có thể là các tài sản xây dựng ở khu vực lân cận của tài sản đang được xem xét:
        Có chung ranh giới (kể cả bên dưới hoặc bên trên)
        Bị ngăn cách về mặt vật lý
        Bởi đường phố công cộng hoặc tư nhân
        Không gian mở thuộc sở hữu công hoặc tư
        Hoặc đặc điểm tương tự
        Ngoài ra còn có “phạm vi ảnh hưởng” của tư duy an ninh xung quanh một tài sản
        Bán kính mà vấn đề an ninh cần được quan tâm sẽ phụ thuộc vào tính chất của một hoặc cả hai tài sản

        Một mối quan ngại cụ thể là việc lộ lọt thông tin liên quan đến tài sản xây dựng lân cận. Điều này đặc biệt đúng với cơ sở hạ tầng nhưng cũng áp dụng với các tòa nhà.

        Thông tin về một tài sản lân cận có thể bị thu thập ngoài ý muốn, ví dụ qua khảo sát dự án phục vụ kết nối hạ tầng kỹ thuật, lối tiếp cận hoặc bố trí mặt bằng, và sau đó cũng có thể vô tình được chia sẻ trong nhóm dự án. Cũng có thể xảy ra việc công bố ngoài ý muốn trên các tài liệu như hồ sơ xin quy hoạch.

        Điều quan trọng cần nhớ là ranh giới tài sản có thể theo phương ngang, phương đứng hoặc băng qua không gian công cộng.

        Trong trường hợp sau, có thể không có một “tài sản” lân cận cụ thể nào, nhưng phạm vi ảnh hưởng về an ninh có thể mở rộng đáng kể vượt ra ngoài bất kỳ hàng rào vật lý hoặc ranh giới tài sản nào. Ví dụ như các cuộc thảo luận về vùng cấm máy bay không người lái quanh sân bay, hoặc khu vực an ninh quanh các cơ sở quân sự như trường bắn hoặc bãi tập.
    """,
    "28|32": "Cách thức (Khoản 5)",
    "28|36": "Góc nhìn tổng thể về mối đe dọa mạng/số ",
    "28|37": "Hướng dẫn ứng phó",
    "28|40": "Xin ý kiến tư vấn",
    "28|41": "Triển khai xuống bên thứ ba và chuỗi cung ứng",
    "28|42": "Lồng ghép vào hồ sơ mua sắm và hồ sơ giao nhiệm vụ",
    "9|5": """
        ISO 19650
        Phần 2 Giai đoạn triển khai
    """,
    "28|notes:3": """
        Trách nhiệm giải trình nằm trong phạm vi của chủ sở hữu tài sản hoặc khách hàng dự án. Trách nhiệm giải trình cuối cùng phải thuộc về chủ sở hữu/đơn vị vận hành tài sản hoặc khách hàng dự án. Trách nhiệm đối với một số hoạt động an ninh cụ thể có thể được ủy quyền ra ngoài chủ sở hữu/khách hàng.

        Trách nhiệm đối với các chính sách cụ thể có thể được giao; việc này có thể diễn ra trong nội bộ chủ sở hữu/khách hàng hoặc trong chuỗi cung ứng. Các dự án lớn hoặc tài sản phức tạp có thể hưởng lợi từ một ủy ban an ninh.

        Vương quốc Anh: CPNI có hướng dẫn về việc tuyển dụng nhân sự hợp đồng theo hướng chú trọng an ninh.
    """,
    "39|4": "Triển khai cách tiếp cận chú trọng an ninh",
    "39|12": "Đối với chủ đầu tư",
    "39|notes:3": """
        Hoạt động được xác định trong ISO 19650-5 là quản lý an ninh. Cần lưu ý rằng đây là một vai trò, không phải chức danh công việc, nên không nhất thiết phải chỉ định riêng một người cụ thể để thực hiện vai trò này. Với dự án hoặc tài sản lớn, phức tạp, hoặc trên cả danh mục dự án/tài sản, có thể cần một nguồn lực hoặc một nhóm chuyên trách để dẫn dắt công việc này.

        Tương tự sức khỏe và an toàn cũng như nhiều chức năng quản lý khác, an ninh thực chất là trách nhiệm của mọi người. Tổ chức cần tránh tình trạng khi đã chỉ định một nguồn lực cụ thể thì những người còn lại cho rằng đây không còn là trách nhiệm của mình.

        Nhiệm vụ chính của người quản lý an ninh là đại diện cho chủ sở hữu tài sản hoặc chủ đầu tư, tùy theo ISO 19650-5 đang được áp dụng cho quản lý tài sản hiện hữu hay cho thiết kế và xây dựng tài sản mới.

        Ba khía cạnh chính của vai trò này gồm:
        Hướng dẫn và chỉ đạo việc xử lý các rủi ro liên quan đến an ninh
        Thúc đẩy văn hóa chú trọng an ninh trong toàn tổ chức
        Theo dõi các vấn đề và mối đe dọa an ninh
        Xử lý rủi ro
        Chịu trách nhiệm đầu mối và trách nhiệm quản lý đối với việc triển khai chiến lược an ninh (trang trình bày tiếp theo), các kế hoạch quản lý an ninh/sự cố và các yêu cầu thông tin
        Chiến lược an ninh
        Kế hoạch quản lý vi phạm/sự cố
        Yêu cầu thông tin về an ninh
        Tài liệu hỗ trợ, chính sách, quy trình và thủ tục
        Hỗ trợ triển khai các quy trình chủ chốt, bao gồm đóng góp cho PIR/AIR, đấu thầu, lập kế hoạch dự án, v.v.
    """,
    "40|1046": "Chính sách cụ thể hóa",
    "40|1050": "Quy trình cụ thể hóa",
    "40|1126/1076": "Làm cơ sở cho",
    "40|1078": "Yêu cầu thông tin của dự án và tài sản",
    "40|1081": "Nguồn lực quản lý thông tin",
    "40|1074/1072": "Kế hoạch quản lý an ninh cho tài sản xây dựng",
    "40|notes:3": """
        Kế hoạch quản lý an ninh được xây dựng dựa trên chiến lược an ninh và bao gồm các nội dung sau:
        Các chính sách thể hiện chiến lược an ninh
        Các quy trình mô tả công việc chi tiết và hướng dẫn cho việc triển khai, vận hành các quy trình trong chiến lược an ninh
        Các thủ tục được xây dựng từ chính sách an ninh trong suốt vòng đời tài sản
        Các phương thức xử lý thông tin được chia sẻ
        Các biện pháp phòng ngừa cần áp dụng khi lưu trữ và bảo vệ thông tin
        Cách xử lý mọi vi phạm an ninh hoặc sự cố tương tự
        Cách triển khai tư duy an ninh xuống các nhà cung cấp thông qua các thỏa thuận hợp đồng

        Các mối quan hệ với bên thứ ba, chẳng hạn các cơ quan chính phủ, và kế hoạch ứng phó sự cố sẽ được xem xét chi tiết hơn ở phần sau.

        An ninh hậu cần áp dụng cho mọi thiết bị nhạy cảm về an ninh và có thể bị xâm phạm trước khi lắp đặt, chạy thử.

        Các nội dung chi tiết trong Kế hoạch quản lý an ninh sau đó sẽ được chuyển hóa thành các yêu cầu thông tin và nguồn lực quản lý thông tin cụ thể của dự án và tài sản (chẳng hạn tiêu chuẩn thông tin hoặc các phương pháp và quy trình tạo lập thông tin).
    """,
    "41|13/50": "Cơ sở dữ liệu, hệ thống xử lý và lưu trữ trên nền tảng đám mây, truy cập qua web",
    "41|13/51": "Hệ thống lưu trữ và xử lý trên nền tảng đám mây",
    "41|13/52": "Hệ thống lưu trữ thuê ngoài (hosted)",
    "41|13/53": "Hệ thống lưu trữ tệp cục bộ dùng chung",
    "41|13/54": "Thiết bị lưu trữ di động",
    "43|41/5": "Kiểm soát tính bảo mật và quyền nắm giữ",
    "43|41/26": "Quyền truy cập vào thông tin và mô hình thông tin",
    "43|41/27": "Thẩm tra",
    "43|41/28": "Đào tạo hội nhập cho nhân sự và tổ chức mới",
    "43|41/29": "Đào tạo chuyên biệt theo vai trò",
    "43|41/30": "Rút nhân sự",
    "45|10": "Kiểm soát tính bảo mật và quyền nắm giữ",
    "43|notes:3": """
        Nhân sự là một trong bốn khía cạnh cần xem xét khi xây dựng các chính sách, quy trình và thủ tục trong kế hoạch quản lý an ninh.

        Các vấn đề liên quan đến nhân sự bao gồm:
        Xác định những vị trí có rủi ro cao trong tổ chức, kể cả ở các tổ chức liên quan như nhà thầu và nhà cung cấp
        Xác định yêu cầu sàng lọc và thẩm tra phù hợp, cả ở cấp dự án/tài sản lẫn cho từng vai trò cụ thể
        Vương quốc Anh: BS 7858 về sàng lọc an ninh đối với những người làm việc trong môi trường an ninh có thể hữu ích
        Yêu cầu đào tạo để hỗ trợ tư duy an ninh, bao gồm cả việc tham gia các khóa học như khóa học này
        Đào tạo hội nhập cho nhân sự mới; một phần sẽ là đào tạo riêng cho dự án/tài sản, một phần là các nguyên tắc chung như thực hành an ninh mạng tốt
        Yêu cầu về đào tạo và quyền truy cập đối với thông tin dự án/tài sản, bao gồm cách các quy tắc của CDE vận hành và được thực thi
        Kế hoạch rút nhân sự khi họ rời tổ chức/dự án hoặc khi dự án kết thúc
    """,
    "46|8": "Bảo vệ khỏi mất mát, sao chép hoặc hư hỏng ",
    "46|9": "Lồng ghép các yêu cầu",
    "46|10": "Kiểm soát tính bảo mật và quyền nắm giữ",
    "46|15": "Lượng thông tin được lưu giữ tối đa ",
    "46|notes:3": """
        Khía cạnh thông tin là góc nhìn thứ tư cần được xem xét trong kế hoạch quản lý an ninh.

        Hai chủ đề chính vẫn là kiểm soát tính bảo mật và tính sẵn sàng.
        Cân nhắc lượng thông tin tối đa cần được lưu giữ. Ở giai đoạn đầu của dự án hoặc chu kỳ vận hành, thông tin được lưu giữ có thể trông còn đơn giản và trùng lặp với thông tin đang được lưu ở nơi khác. Theo thời gian, thông tin sẽ đầy đủ hơn, cụ thể hơn và có giá trị hơn.
        Cân nhắc liệu thông tin có thể hoặc nên bị hủy, hoặc chuyển sang kho lưu trữ ngoại tuyến an toàn hay không.
    """,
    "47|4": "Hoạt động 3: Triển khai thực tế tư duy an ninh ",
    "47|15|cell:1,1": "Khía cạnh",
    "47|15|cell:1,2": "Rủi ro an ninh đã xác định",
    "47|15|cell:1,3": "Biện pháp\rgiảm thiểu",
    "47|15|cell:1,4": "Điểm cần\rlưu ý",
    "47|15|cell:2,1": "Nhân sự",
    "48|notes:6|cell:1,1": "Khía cạnh",
    "48|notes:6|cell:1,2": "Rủi ro an ninh đã xác định",
    "48|notes:6|cell:1,3": "Biện pháp\rgiảm thiểu",
    "48|notes:6|cell:1,4": "Điểm cần\rlưu ý",
    "48|notes:6|cell:2,1": "Nhân sự",
    "49|3/8": "Bước 1:\r\rDanh mục rủi ro tiềm ẩn do vi phạm/sự cố",
    "49|12/17": "Bước 3:\r\rHành động ngay khi phát hiện",
    "49|21/26": "Bước 5:\r\rRà soát",
    "49|39/44": "Bước 4:\r\rCác hành động bảo đảm liên tục kinh doanh và phục hồi",
    "49|notes:3": """
        Việc vi phạm và sự cố an ninh có lẽ sẽ không xảy ra, nhưng không thể chỉ dựa vào hy vọng đó. Cần xây dựng sẵn kế hoạch quản lý vi phạm để có thể triển khai ngay khi xảy ra bất kỳ vi phạm hoặc sự cố nào.

        ISO 19650-5 nêu ra một số chủ đề cấp cao cần được đưa vào kế hoạch này. Kế hoạch phải bao quát phạm vi có thể dự liệu của các vi phạm/sự cố vật lý và mạng. Đồng thời, đây cũng nên là điểm khởi đầu tốt cho hành động ứng phó khi xảy ra vi phạm/sự cố ngoài dự kiến, vì các tình huống đó vẫn phải được xử lý và có thể cần được đưa vào bản cập nhật của kế hoạch.

        Các quy trình áp dụng sau khi xảy ra vi phạm/sự cố bao gồm:
        Cần liên hệ ngay với ai khi phát hiện vi phạm/sự cố và liên hệ bằng cách nào
        Cách xác định những gì đã bị mất, hư hỏng hoặc bị xâm phạm
        Cách xác định những bên nào có liên quan, chẳng hạn những cá nhân có dữ liệu cá nhân có thể đã bị xâm phạm hoặc những người có thể đối mặt với rủi ro cao hơn do sự cố
        Cách phối hợp với các bên thứ ba liên quan, chẳng hạn cơ quan quản lý hoặc truyền thông
        Cách liên hệ với công chúng, nếu xét thấy phù hợp
    """,
    "53|6": "Tư duy an ninh khi làm việc với nhà cung cấp (Khoản 9)",
    "53|25/11": "Các điều khoản trong hợp đồng",
    "53|25/13": "Trong giai đoạn mua sắm/đấu thầu",
    "53|25/14": "Trong thời gian thực hiện hợp đồng",
    "53|25/15": "Phương pháp và quy trình\rtạo lập thông tin",
    "53|25/16": "Các đơn vị dự thầu không thành công",
    "53|notes:3": """
        Tư duy an ninh là yêu cầu cần có trong mối quan hệ giữa khách hàng dự án hoặc chủ sở hữu/đơn vị vận hành tài sản và bất kỳ nhà cung cấp nào được giao nhiệm vụ thực hiện công việc trên tài sản/dự án hoặc liên quan đến tài sản/dự án.

        Tư duy an ninh này cần chi phối hoạt động mua sắm, các hợp đồng được thiết lập, công việc của nhà cung cấp trong thời gian thực hiện hợp đồng và giai đoạn kết thúc khi hợp đồng chấm dứt.

        Nội dung này được đề cập trong Điều 9 của ISO 19650-5.

        Một số điểm cần lưu ý chính là:
        Bảo đảm rằng các nhà cung cấp đồng ý hành động theo hướng chú trọng an ninh (và biết các thủ tục phù hợp) trước khi được cấp quyền truy cập vào bất kỳ thông tin nhạy cảm nào trong quá trình mua sắm/đấu thầu
        Bảo đảm rằng các đơn vị dự thầu không thành công thực hiện các bước cần thiết để hoàn trả/hủy/xóa dữ liệu và thông tin liên quan mà họ đã được cấp quyền truy cập
        Đưa các điều khoản phù hợp vào hợp đồng, chẳng hạn quyền của chủ đầu tư trong việc kiểm tra các biện pháp an ninh của nhà cung cấp và mức độ tuân thủ các yêu cầu
        Kiểm tra xem tư duy an ninh đã được phản ánh phù hợp trong tiêu chuẩn thông tin của tài sản hoặc dự án và/hoặc trong các phương pháp và quy trình tạo lập thông tin của tài sản hoặc dự án hay chưa
        Kiểm tra xem các nhóm triển khai dự án và tài sản có đủ nguồn lực (vai trò) phù hợp và hiểu rõ trách nhiệm của mình hay không
        Bảo đảm rằng dữ liệu và thông tin nhạy cảm được xóa/hủy hoặc lưu trữ an toàn khi kết thúc hợp đồng, như một phần của quy trình kết thúc chính thức

        Một lĩnh vực mà tư duy an ninh có thể ảnh hưởng đến công tác quản lý thiết kế là thông qua chiến lược liên hợp mô hình để xác định “các khu vực hạn chế” trong mô hình thông tin dựa trên mức phân quyền an ninh thông tin. Điều này có nghĩa là chỉ những thành viên được lựa chọn của nhóm dự án hoặc nhóm tài sản mới có quyền cần thiết để xem thông tin trong một phần cụ thể của mô hình thông tin.
    """,
    "54|5": "Làm việc trước khi giao nhiệm vụ (Khoản 9.1)",
    "54|48": "Thỏa thuận chia sẻ thông tin (ngoài các giao nhiệm vụ chính thức)",
    "54|49": "Xử lý\rthông tin",
    "54|52": "Đánh giá\rnăng lực",
    "54|notes:3": """
        An ninh cần được thiết lập trước khi thực hiện việc giao nhiệm vụ, đặc biệt trong giai đoạn mời thầu/đấu thầu.

        Cần có thỏa thuận chia sẻ thông tin trước khi bất kỳ thông tin nhạy cảm nào, hoặc khả năng tồn tại thông tin nhạy cảm, được chia sẻ.

        Thỏa thuận này cần bao quát cách xử lý và tiêu hủy phù hợp.

        Vì vậy, một phần của quy trình mời thầu/đấu thầu phải là việc đánh giá năng lực của họ.
    """,
    "55|48": "Chuỗi ràng buộc hợp đồng",
    "55|49": "Quyền rà soát và kiểm tra",
    "55|52": "Quyền yêu cầu và\rxác minh việc tiêu hủy/\rđánh giá",
    "55|notes:3": """
        Chuỗi ràng buộc hợp đồng phải bảo đảm rằng các nhà cung cấp bị ràng buộc bởi những khía cạnh phù hợp của chiến lược an ninh. Ngoài ra, khách hàng/chủ sở hữu có thể cần có quyền rà soát và kiểm tra cả các khía cạnh trên môi trường số lẫn khía cạnh vật lý của các biện pháp an ninh đang được áp dụng. Cũng có thể cần tinh chỉnh hoặc điều chỉnh chiến lược trước các thay đổi từ bên ngoài. Cuối cùng, có thể cần có quyền yêu cầu và xác minh việc tiêu hủy mọi thông tin sau khi việc giao nhiệm vụ kết thúc. Dĩ nhiên, các kỳ vọng này phải “phù hợp và tương xứng”.

        Phụ lục C nêu ra một số điểm về việc đánh giá bên thứ ba. Điều quan trọng là phải xem xét hệ quả của việc không chia sẻ.

        Một khó khăn cụ thể có thể là việc xử lý các quy trình quản lý nhà nước và quy định pháp luật, vốn có thể hàm ý mức độ công khai rất lớn.

        Một số quốc gia có luật “Tự do Thông tin” (FoI), có thể là một phần của cách tiếp cận minh bạch hoặc dân chủ. Khi đó có thể cần tách riêng và thương lượng phạm vi của thông tin mở.

        Cuối cùng, các phần trình bày trước công chúng có thể vô tình làm gia tăng lượng thông tin được công khai rộng rãi, đặc biệt khi dự án có mức độ quan tâm cao của công chúng, là niềm tự hào hoặc mang tính đổi mới.

        Vương quốc Anh: Các mẫu UK BIM Framework cho Giao thức Thông tin có bao gồm các điều khoản hợp đồng để tích hợp tất cả các cân nhắc này vào hợp đồng dự án hoặc hợp đồng tài sản.
    """,
    "56|76": "Đánh giá bên thứ ba (Phụ lục C)",
    "56|7": "Trình bày và công bố trước công chúng\r\rYêu cầu về phê duyệt\r",
    "56|9": "Quy trình theo quy định pháp luật\r\rCơ chế bảo đảm tuân thủ và an ninh",
    "56|notes:3": """
        Phụ lục C đưa ra một số điểm cần lưu ý khi đánh giá bên thứ ba. Điều quan trọng là phải xem xét hệ quả của việc không chia sẻ thông tin.

        Một khó khăn cụ thể có thể nằm ở việc xử lý các quy trình theo quy định pháp luật, vốn có thể đòi hỏi mức độ công khai cao.

        Một số quốc gia có luật “Tự do Thông tin” (FoI), như một phần của cách tiếp cận minh bạch hoặc dân chủ. Khi đó, có thể cần tách riêng và thương lượng phạm vi của thông tin mở.

        Cuối cùng, các bài trình bày và ấn phẩm công khai có thể vô tình làm tăng tổng lượng thông tin sẵn có công khai, đặc biệt khi dự án nhận được nhiều quan tâm, là niềm tự hào hoặc mang tính đổi mới.

        Đánh giá thông tin
        Việc đánh giá thông tin cần xác định ai được phép truy cập thông tin được chia sẻ, liệu có cần tham vấn các bên liên quan trước khi chia sẻ hoặc công bố hay không, và lý do hay căn cứ cụ thể cho việc chia sẻ hoặc công bố đó. Điều này giúp bảo đảm dữ liệu được sử dụng và bảo vệ phù hợp trong suốt quá trình.

        Quyền tiếp cận thông tin của công chúng
        Kế hoạch quản lý an ninh cần nêu rõ cách bảo vệ thông tin nhạy cảm khi tổ chức nhận được yêu cầu theo luật tiếp cận thông tin công cộng hoặc luật minh bạch. Kế hoạch cũng cần xem xét các rủi ro do tổng hợp dữ liệu và xử lý các tác động tiềm ẩn để bảo đảm việc quản lý thông tin được an toàn và có trách nhiệm.

        Trình bày và công bố trước công chúng
        Kế hoạch quản lý an ninh cần xác định yêu cầu phê duyệt đối với mọi tài liệu về sáng kiến, dự án, tài sản, sản phẩm hoặc dịch vụ sẽ được trình bày tại sự kiện công cộng, trưng bày ở khu vực công cộng, chia sẻ với bên thứ ba hoặc công bố trên website, trong ấn phẩm học thuật/kỹ thuật hoặc tài liệu tiếp thị.

        Quy trình theo quy định pháp luật
        Kế hoạch quản lý an ninh cần nêu rõ cách chia sẻ thông tin một cách an toàn với bên thứ ba trong khi vẫn đáp ứng yêu cầu pháp lý. Dữ liệu nhạy cảm cần được bảo vệ bằng các biện pháp như biên tập/che mờ, định dạng thay thế hoặc thỏa thuận trước về biện pháp bảo vệ, đặc biệt khi xử lý các luật về tiếp cận thông tin công cộng, để bảo đảm rủi ro vẫn nằm trong mức chấp nhận được của tổ chức.
    """,
    "57|notes:3": """
        Phụ lục D đưa ra một dàn ý cho thỏa thuận chia sẻ thông tin (hoặc phụ lục kèm theo một thỏa thuận chính).

        Thỏa thuận này cần xác định rõ các mục đích đã được thống nhất và được phép khi chia sẻ thông tin, đồng thời có thể loại trừ các mục đích sử dụng khác.

        Sau đó, thỏa thuận sẽ đóng vai trò chuyển tải các điểm chính của kế hoạch quản lý an ninh và kế hoạch quản lý sự cố.
    """,
    "58|14|cell:1,2": "Mức độ sẵn sàng đến đâu?\r(1-10)",
    "58|14|cell:1,4": "Làm sao biết việc này đã hoàn thành?",
    "59|notes:6|cell:1,2": "Mức độ sẵn sàng đến đâu?\r(1-10)",
    "59|notes:6|cell:1,4": "Làm sao biết việc này đã hoàn thành?",
    "59|notes:6|cell:5,1": "Xây dựng hoặc phản hồi đối với chiến lược an ninh ",
    "59|notes:6|cell:6,1": "Soạn thảo hoặc phản hồi đối với kế hoạch quản lý an ninh ",
}


def build_base_memory() -> dict[str, str]:
    config = load_json(BASE_CONFIG_JSON)
    memory: dict[str, str] = {}

    for block_name in ("full_overrides", "text_overrides"):
        block = config.get(block_name, {})
        for english, vietnamese in block.items():
            memory[normalize_text(english)] = normalize_text(vietnamese)

    return memory


def main() -> None:
    source = load_json(SOURCE_JSON)
    latest_proposals = load_optional_json(LATEST_PROPOSAL_JSON) or []
    current = {
        key_for(entry["slide"], entry["path"]): normalize_text(entry.get("text", ""))
        for entry in latest_proposals
    }

    base_memory = build_base_memory()
    part4_memory = load_bilingual_memory(PART4_EN_JSON, PART4_VN_JSON)
    part2_memory = load_bilingual_memory(PART2_EN_JSON, PART2_VN_JSON)

    curated_entries = []
    source_counts = {
        "manual_path_overrides": 0,
        "base_memory": 0,
        "part4_memory": 0,
        "part2_memory": 0,
        "current_proposal": 0,
        "terminology_cleanups": 0,
    }

    for slide in source["slides"]:
        for entry in slide["entries"]:
            slide_number = int(entry["slide"])
            path = str(entry["path"])
            entry_key = key_for(slide_number, path)
            english = normalize_text(entry.get("text", ""))

            if entry_key in MANUAL_PATH_OVERRIDES:
                proposal = dedent(MANUAL_PATH_OVERRIDES[entry_key]).strip("\n")
                source_counts["manual_path_overrides"] += 1
            elif english in base_memory:
                proposal = base_memory[english]
                source_counts["base_memory"] += 1
            elif english in part4_memory:
                proposal = part4_memory[english]
                source_counts["part4_memory"] += 1
            elif english in part2_memory:
                proposal = part2_memory[english]
                source_counts["part2_memory"] += 1
            else:
                proposal = current.get(entry_key, english)
                source_counts["current_proposal"] += 1

            if proposal != english:
                cleaned_proposal = cleanup_translation(proposal)
                if cleaned_proposal != normalize_text(proposal):
                    source_counts["terminology_cleanups"] += 1
                proposal = cleaned_proposal

            curated_entries.append(
                {
                    "slide": slide_number,
                    "path": path,
                    "text": finalize_text(proposal),
                }
            )

    OUTPUT_JSON.write_text(
        json.dumps(curated_entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Created curated proposal JSON: {OUTPUT_JSON}")
    print(json.dumps(source_counts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
