import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time


def extract_detail(info_detail, index, default="Không rõ"):
    """Hàm trích xuất thông tin chi tiết từ danh sách các thẻ HTML."""
    try:
        return info_detail[index].text.strip()
    except (IndexError, AttributeError):
        return default


def get_job_data_from_detail_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tiêu đề và tên công ty
        job_info = soup.find("div", class_="job-info")
        title = job_info.find("h1").text.strip() if job_info and job_info.find("h1") else "Không có tiêu đề"

        # Tên công ty
        company_tag = soup.find("h1", class_="job-name")
        company = company_tag.text.strip() if company_tag else "Không rõ"

        # Mức lương và địa điểm
        job_info_detail = soup.find("div", class_="job-info-detail")
        salary = job_info_detail.find_all("div", class_="job-detail-col")[0].text.strip() if job_info_detail else "Không rõ"
        location = job_info_detail.find_all("div", class_="job-detail-col")[3].text.strip() if job_info_detail and len(job_info_detail.find_all("div", class_="job-detail-col")) > 3 else "Không rõ"

        # Mô tả
        description_tag = soup.find("div", class_="entry-content")
        description = description_tag.text.strip() if description_tag else "Không có mô tả"

        return [{
            "Tiêu đề": title,
            "Tên công ty": company,
            "Mức lương": salary,
            "Địa điểm": location,
            "Mô tả": description
        }]

    except requests.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu từ trang chi tiết công việc: {e}")
        return []


def get_job_data_from_list_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        job_list = []

        # Xử lý công việc đầu tiên
        first_job_content = soup.find("div", class_="job-content")
        if first_job_content:
            job_name = first_job_content.find("h1", class_="job-name")
            job_name = job_name.text.strip() if job_name else "Không có tên công việc"

            company = first_job_content.find("div", class_="job-company")
            company = company.text.strip() if company else "Không có tên công ty"

            job_info_detail = first_job_content.find("div", class_="job-info-detail")
            details = job_info_detail.find_all("div", class_="job-detail-col") if job_info_detail else []
            job_list.append({
                "Tên công việc": job_name,
                "Tên công ty": company,
                "Mức lương": extract_detail(details, 0, "Không rõ mức lương"),
                "Ngày ứng tuyển": extract_detail(details, 1, "Không rõ ngày ứng tuyển"),
            })

        # Xử lý các công việc còn lại
        job_boxes = soup.find_all("div", class_="box-job-small")
        for job_box in job_boxes:
            job_name_tag = job_box.find("h3", class_="job-name")
            job_name = job_name_tag.text.strip() if job_name_tag else "Không có tên công việc"

            company_tag = job_box.find("div", class_="job-company")
            company = company_tag.text.strip() if company_tag else "Không có tên công ty"

            job_info_detail = job_box.find("div", class_="job-info-detail")
            details = job_info_detail.find_all("div", class_="job-detail-col") if job_info_detail else []

            job_list.append({
                "Tên công việc": job_name,
                "Tên công ty": company,
                "Mức lương": extract_detail(details, 0, "Không rõ mức lương"),
                "Ngày ứng tuyển": extract_detail(details, 1, "Không rõ ngày ứng tuyển"),
            })

        return job_list

    except requests.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu từ trang danh sách công việc: {e}")
        return []


def crawl_all_pages():
    print("Bắt đầu thu thập dữ liệu từ các trang...")

    # URL trang chi tiết công việc (ví dụ)
    detail_url = "https://danang43.edu.vn/viec-lam/chuyen-vien-kinh-doanh-luong-cb-8-15-trieu-khong-dat-kpi-van-nhan-du-luong-13092.html"
    jobs_from_detail_page = get_job_data_from_detail_page(detail_url)

    # URL trang danh sách việc làm (ví dụ)
    list_url = "https://danang43.edu.vn/nganh-nghe/viec-lam-bat-dong-san"
    jobs_from_list_page = get_job_data_from_list_page(list_url)

    # Kết hợp dữ liệu từ các trang lại với nhau
    all_jobs = jobs_from_detail_page + jobs_from_list_page

    if all_jobs:
        # Lưu dữ liệu vào file CSV
        try:
            df = pd.DataFrame(all_jobs)

            # Kiểm tra xem file đã tồn tại hay chưa
            try:
                existing_df = pd.read_csv("danang43edu.csv")
                df = pd.concat([existing_df, df], ignore_index=True)
            except FileNotFoundError:
                pass

            df.to_csv("danang43edu.csv", index=False, encoding='utf-8-sig')
            print(f"Thu thập dữ liệu hoàn tất: đã lưu {len(all_jobs)} công việc vào 'danang43edu.csv'")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
    else:
        print("Không có dữ liệu để lưu")


#  Tự động chạy vào 6h sáng mỗi ngày
schedule.every().day.at("06:00").do(crawl_all_pages)

if __name__ == "__main__":
    # Gọi hàm để chạy ngay lập tức
    crawl_all_pages()

    # Sau đó, chờ đến 6h sáng mỗi ngày để tiếp tục
    print("Đang chờ đến 6h sáng hàng ngày để thu thập dữ liệu")
    while True:
        schedule.run_pending()
        time.sleep(60)
