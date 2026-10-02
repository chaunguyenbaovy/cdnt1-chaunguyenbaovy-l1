# <Tên phạm vi bằng một câu>
Sinh viên:
Châu Nguyễn Bảo Vy - 2374802010578 - Track DA
Học phần:
Chuyên đề Tốt nghiệp 1, HK1 2026-2027
Luồng nghiệp vụ:
L1 – Hồ sơ khách hàng & Phân khúc
## 1. Mục tiêu
Hệ thống hỗ trợ phân tích dữ liệu khách hàng và tính toán, gán phân khúc khách hàng theo các quy tắc đã xác định. 
Bài toán tập trung vào việc sử dụng dữ liệu mua hàng để tính các chỉ số như tổng giá trị mua hàng, tần suất mua hàng và thời gian từ lần mua gần nhất.
Kết quả giúp nhân viên bán hàng và marketing biết khách hàng thuộc nhóm nào để phục vụ và chăm sóc phù hợp.
Quản lý cửa hàng có thể theo dõi số lượng và danh sách khách hàng theo từng phân khúc.
## 2. Yêu cầu môi trường
- Python 3.11+
- PostgreSQL 16
- Pandas
- NumPy
- Matplotlib
- Jupyter
- SQLAlchemy
- psycopg2-binary
- Biến môi trường: xem `.env.example`
## 3. Hướng dẫn chạy
1. Tạo và kích hoạt môi trường Python, sau đó cài các thư viện cần thiết:
   `pip install -r requirements.txt`

2. Cấu hình các biến môi trường trong file `.env` dựa trên `.env.example`.

3. Chạy Jupyter Notebook để thực hiện khám phá và xử lý dữ liệu:
   `jupyter notebook`

4. Thực hiện quy trình tính toán và gán phân khúc khách hàng theo các notebook/script trong dự án.
## 4. Cấu trúc thư mục
- `docs/`: Tài liệu mô tả bài toán và dự án.
- `data/raw/`: Dữ liệu nguồn ban đầu, không commit dữ liệu lớn.
- `data/processed/`: Dữ liệu sau khi xử lý.
- `data/sample/`: Dữ liệu mẫu nhỏ dùng để kiểm thử.
- `notebooks/`: Notebook dùng để khám phá và phân tích dữ liệu.
- `src/etl/`: Các chương trình Extract, Transform và Load dữ liệu.
- `dashboard/`: Thành phần hiển thị kết quả phân tích.
- `requirements.txt`: Danh sách thư viện Python cần cài đặt.
- `.env.example`: Mẫu các biến môi trường.
- `.gitignore`: Các file/thư mục không đưa lên Git.
## 5. Kiểm thử
Kiểm tra môi trường và trạng thái dự án bằng các lệnh Python/Git.

- Kiểm tra Python:
  `python --version`

- Kiểm tra Pandas:
  `python -c "import pandas; print(pandas.__version__)"`

- Kiểm tra Git:
  `git status`

- Đảm bảo `venv/`, `.env` và dữ liệu nguồn lớn không xuất hiện trong Git.
## 6. Trạng thái hiện tại
 Khởi tạo project, smoke test chạy được (buổi 2)
□ Module tiếp nhận yêu cầu (buổi 8–10)
□ Module phân công kỹ thuật viên (buổi 10–12)