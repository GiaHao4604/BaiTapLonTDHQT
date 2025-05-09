## Giới thiệu

Dự án này là một công cụ để thu thập dữ liệu tuyển dụng từ trang web **danang43edu.vn**, bao gồm các thông tin công việc như tiêu đề, công ty, mức lương, địa điểm làm việc và mô tả công việc. Dữ liệu thu thập được sẽ được lưu vào tệp CSV và có thể được sử dụng cho các mục đích phân tích dữ liệu hoặc xây dựng các ứng dụng tìm kiếm việc làm.

## Các tính năng chính:

- Thu thập dữ liệu tuyển dụng từ trang web **danang43edu.vn**.
- Trích xuất thông tin bao gồm: Tiêu đề công việc, công ty, mức lương, địa điểm và mô tả công việc.
- Lưu dữ liệu vào tệp CSV.
- Tự động chạy mỗi ngày lúc 6h sáng để thu thập dữ liệu mới.

## Yêu cầu cài đặt

Trước khi bắt đầu, hãy đảm bảo rằng bạn đã cài đặt các công cụ và thư viện sau:

- Python (Phiên bản 3.x)
- pip (Python Package Installer)

## Hướng dẫn cài đặt

### Bước 1: Cài đặt Python

Đầu tiên, hãy tải và cài đặt Python từ [python.org](https://www.python.org/downloads/) nếu bạn chưa cài đặt Python. Sau khi cài đặt, bạn có thể kiểm tra phiên bản Python đã cài bằng cách mở terminal (hoặc command prompt) và nhập lệnh:

bash
python --version

### Bước 2: Cài đặt các thư viện cần thiết

Chúng ta sẽ sử dụng các thư viện requests, BeautifulSoup, pandas và schedule để thực hiện việc thu thập dữ liệu và lưu vào tệp CSV.
Cài đặt các thư viện bằng lệnh:
pip install requests beautifulsoup4 pandas schedule

### Bước 3: Tải về mã nguồn

Tải mã nguồn của dự án từ GitHub về máy tính của bạn. Bạn có thể clone project từ GitHub bằng cách sử dụng lệnh sau trong terminal:
git clone https://github.com/GiaHao4604/baitaplon

### Bước 4: Chạy mã nguồn

Sau khi đã tải mã nguồn và cài đặt các thư viện, bạn có thể chạy chương trình bằng lệnh:
python BT.py
Điều này sẽ bắt đầu quá trình thu thập dữ liệu và lưu kết
