# CapCut Cache Video Recovery (Windows)

**Khôi phục video cache CapCut Desktop — giao diện tiếng Việt, xử lý hàng loạt, không cần cài thư viện Python ngoài.**

*An unofficial Windows utility for recovering compatible CapCut Desktop compound-clip cache videos stored in BDVE Type 1 format.*

Công cụ Python có giao diện tiếng Việt để **khôi phục video MP4 từ cache dự án CapCut Desktop**, đặc biệt với tệp `*_video.mp4` nằm trong thư mục `Resources/combination`.

> **Lưu ý:** Đây là công cụ khôi phục dữ liệu cache không chính thức, **không phải tính năng CapCut Pro**, không mở khóa tài khoản hay gói trả phí. Cache có thể chứa bản dựng tạm của các clip đã được xử lý (compound clip), nhưng không bảo đảm khôi phục được mọi video, hiệu ứng, âm thanh hoặc chất lượng. Hãy sử dụng với nội dung mà bạn có quyền sử dụng và tự kiểm tra điều khoản của CapCut.

## Vì sao có công cụ này?

Khi dùng tính năng **Compound Clip → Pre-process** trong CapCut Desktop, một số dự án tạo ra video tạm trong `Resources/combination`. Tệp đó đôi khi có đuôi `.mp4` nhưng không thể phát trực tiếp do cách lưu dữ liệu cache. Công cụ thử nhận diện và phục hồi các tệp tương thích thành MP4 có thể mở bằng trình phát thông thường.

Đây là công cụ **khôi phục cache của dự án bạn có quyền sử dụng**, không phải cách kích hoạt CapCut Pro hay đảm bảo xuất được mọi hiệu ứng trả phí.

## Tính năng

- Giao diện Tkinter tiếng Việt trên Windows.
- Chọn từng tệp hoặc cả thư mục chứa `*_video.mp4`.
- Khôi phục cache **BDVE Type 1** với ba bộ tham số đã nhận biết; không cần mã hóa lại video.
- Kiểm tra cấu trúc MP4 sau khôi phục; lưu file mới, không sửa file gốc.
- Báo lỗi theo từng file nếu cache không được hỗ trợ hoặc thiếu dữ liệu.

## Yêu cầu

- Windows 10/11 (hoặc môi trường có Python 3 và Tkinter).
- Python 3.x (không cần thư viện ngoài).
- File cache từ dự án CapCut của bạn; không cần upload lên dịch vụ bên ngoài.

## Chạy chương trình

1. [Download repository as ZIP](../../archive/refs/heads/main.zip) rồi giải nén, hoặc clone repo.
2. Nhấp đúp **`Chay Cong Cu.bat`**, hoặc mở terminal trong thư mục và chạy:

   ```powershell
   python khoi_phuc.py
   ```

3. Chọn **Chọn video** hoặc **Chọn thư mục video** để chọn `*_video.mp4` trong `Resources/combination`.
4. Chọn nơi lưu, bấm **Khôi phục video**, xem thông báo kết quả.

### Tệp `Resources/combination` từ đâu?

Trong CapCut Desktop, sau khi một **Compound Clip** được *Pre-process*, CapCut có thể tạo các tệp render tạm trong thư mục dự án, thường theo dạng:

```text
<CapCut project folder>/Resources/combination/<identifier>_video.mp4
```

Vị trí chính xác tùy phiên bản và cấu hình CapCut. Tệp có đuôi `.mp4` nhưng không nhất thiết là MP4 thông thường: một số bản cache sử dụng BDVE Type 1, không mở được trực tiếp trong trình phát video. Ứng dụng này cố gắng khôi phục loại cache đã nhận diện.

## Giới hạn đã biết

- Chỉ xử lý **BDVE Type 1** và các bộ tham số có trong `PROFILES` của `khoi_phuc.py`.
- **Không khôi phục timeline**, lớp chỉnh sửa, project `.json`, hoặc cấu trúc compound clip gốc.
- Kết quả kiểm tra cấu trúc container MP4 **không đảm bảo** mọi frame đều phát chuẩn.
- File cache có thể không chứa âm thanh, thiếu đoạn hoặc không phản ánh chất lượng xuất chính thức.
- Một số phiên bản CapCut có thể thay đổi định dạng cache, khiến công cụ không hoạt động.
- Chưa có bộ kiểm thử tự động và chưa xác nhận tương thích trên mọi phiên bản Windows/CapCut.

## Cấu trúc repo

```text
.
├── Chay Cong Cu.bat
├── HUONG DAN.txt
├── khoi_phuc.py
├── capcut_cache_recover/
│   ├── __init__.py
│   ├── cryptor.py
│   └── validator.py
├── LICENSE-third-party.txt
├── .gitignore
└── README.md
```

## Nguồn & ghi nhận tác giả

Các thành phần xử lý BDVE và kiểm tra MP4 sử dụng/phát triển dựa trên mã từ **[pikadexofc/capcut-cache-recover](https://github.com/pikadexofc/capcut-cache-recover)**, tác giả gốc Shanto (pikadexofc), theo giấy phép **MIT**. Nội dung giấy phép gốc được giữ trong [`LICENSE-third-party.txt`](LICENSE-third-party.txt).

Giao diện tiếng Việt và quy trình xử lý tích hợp trong `khoi_phuc.py` được đóng gói lại cho trải nghiệm sử dụng đơn giản hơn. **Quyền cấp phép đối với những phần đóng góp mới cần được chủ repo xác nhận** trước khi phát hành với một LICENSE chung.

Dự án không liên kết hay được CapCut/ByteDance bảo trợ.

## An toàn dữ liệu

Chương trình thao tác **cục bộ**, không gửi video lên mạng. File nguồn được mở chế độ đọc; kết quả được tạo ở vị trí riêng. Trước khi thao tác với cache quý giá, nên sao lưu thư mục dự án.
