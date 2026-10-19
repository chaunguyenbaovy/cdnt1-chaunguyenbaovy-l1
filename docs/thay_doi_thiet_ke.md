\# NHẬT KÝ THAY ĐỔI THIẾT KẾ (BUỔI 8 - SPRINT 1)
\### TD-01: Bổ sung Sơ đồ Kiến trúc &amp; Star Schema có Kiểu dữ liệu - 
\*\*Phản hồi của GV\*\*: Thiếu sơ đồ kiến trúc phân lớp, Star Schema chưa có kiểu dữ liệu SQL.
\- \*\*Quyết định\*\*: SỬA
\- \*\*Lý do\*\*: Cần làm rõ cấu trúc phân lớp ETL/DWH và kiểu dữ liệu chuẩn làm khung cho BT2.
\- \*\*Ảnh hưởng\*\*: Đã tạo file \`docs/architecture.drawio\`, \`docs/star\_schema.drawio\` và cập nhật \`docs/data-requirements.md\`.
\### TD-02: Bổ sung Wireframe 3 khung Dashboard &amp; Nguồn dữ liệu -
 \*\*Phản hồi của GV\*\*: Thiếu hình vẽ 3 khung Wireframe và ghi chú nguồn dữ liệu từng khung.
 \- \*\*Quyết định\*\*: SỬA
  - \*\*Lý do\*\*: Đảm bảo tính nhất quán giữa giao diện báo cáo và mô hình dữ liệu DWH. 
  - \*\*Ảnh hưởng\*\*: Đã bổ sung mô tả nguồn dữ liệu (\`dim\_customer\`, \`fact\_customer\_segment\`) cho 3 view Dashboard.
  \### TD-03: Sửa lỗi truy vết UC2 &amp; Lập luận NFR3 
  - \*\*Phản hồi của GV\*\*: UC2 chưa có FR truy vết; NFR3 ghi sai tên loại yêu cầu.
  \- \*\*Quyết định\*\*: SỬA 
  - \*\*Lý do\*\*: Đảm bảo bảng truy vết không có ô trống và câu lập luận khớp đúng SRS. 
  - \*\*Ảnh hưởng\*\*: Gán FR1 cho UC2; chỉnh câu lập luận 3 về NFR3 (Chất lượng dữ liệu SĐT 100% Uniqueness).