# Bài tập lớn CSDL Phân Tán – Personalized PageRank (Bài 10.10)

>  **Đề tài**: Cài đặt Hadoop và thực hiện bài 10.10 – Personalized PageRank bằng MapReduce  
>  **Công nghệ**: Python, Hadoop 3.3.6, Hadoop Streaming, Windows  
>  **Kết quả**: Hội tụ sau 14 vòng — kiểm tra bằng script `check_converged.py`

## Thông tin sinh viên

- **Họ tên**: Thạch Thị Nhanh  
- **MSSV**: N21DCCN159  
- **Lớp**: D21CQCNHT01-N  
- **Email**: n21dccn159@student.ptithcm.edu.vn  
- **GitHub**: [LyThach](https://github.com/LyThach)

## Giới thiệu

Dự án này triển khai thuật toán **Personalized PageRank (PPR)** – một biến thể của PageRank cổ điển, trong đó xác suất lan truyền ưu tiên quay về một node nguồn cụ thể (_personalized source_). 

Thuật toán được thực hiện theo mô hình **MapReduce** và triển khai bằng **Hadoop Streaming**, sử dụng ngôn ngữ **Python**.  

Đây là nội dung của **Bài 10.10** trong sách _Principles of Distributed Database Systems_, 4th ed., Özsu & Valduriez (Springer, 2020).  
Mục tiêu là tính toán PageRank cá nhân hóa trên đồ thị ví dụ gồm 6 node (hình 10.21), lặp đến khi hội tụ với sai số epsilon nhỏ hơn 0.0001.

---

### A. Lý do chọn Hadoop Streaming

Hadoop Streaming cho phép sử dụng bất kỳ ngôn ngữ lập trình nào (như Python) để viết các hàm Map và Reduce, giúp đơn giản hoá việc phát triển thuật toán. Việc kết hợp với hệ sinh thái Hadoop còn tạo điều kiện cho khả năng mở rộng theo chiều ngang và dễ tích hợp với các công cụ quản lý dữ liệu lớn như Hive hoặc Pig [5].

---

### B. Cài đặt môi trường và chuẩn bị dữ liệu

**Yêu cầu hệ thống:**
- Hệ điều hành: Windows 10 hoặc mới hơn
- Java 8 trở lên (JAVA_HOME trỏ về: `C:\Program Files\Java\jdk1.8.0_191`)
- Hadoop 3.3.6 (đã thử nghiệm thành công trên Windows)
- Python 3.11.9

**Cài đặt Hadoop trên Windows:**
- Tải và giải nén Hadoop 3.3.6 từ: https://hadoop.apache.org/releases.html [2]
- Cấu hình biến môi trường:
  - `HADOOP_HOME`: trỏ tới thư mục cài Hadoop (ví dụ: `C:\hadoop`)
  - Thêm `%HADOOP_HOME%\bin` vào biến `PATH`
- Cấu hình `core-site.xml` và `hdfs-site.xml` để sử dụng local filesystem
- Đặt file `hadoop-streaming-3.3.6.jar` vào thư mục:  
  `%HADOOP_HOME%/share/hadoop/tools/lib/`

**Chuẩn bị dữ liệu đầu vào:**
- Tạo thư mục đầu vào (chỉ cần 1 lần nếu chưa có):
```bash
hadoop fs -mkdir /input
```

- Tải file đồ thị vào HDFS:
```bash
hadoop fs -put graph.txt /input/graph.txt
```

**Nội dung của tập tin `graph.txt` (đồ thị đầu vào):**  
Tập tin đồ thị được định dạng với ba trường: tên node, giá trị PR ban đầu, và danh sách liên kết ra.
```
P1 1.0 P2,P3
P2 0.0
P3 0.0 P1,P2,P5
P4 0.0 P5,P6
P5 0.0 P4,P6
P6 0.0 P4
```

---

### C. Thực thi thuật toán bằng Hadoop Streaming

Thuật toán được thực hiện theo các vòng lặp:

1. Khởi chạy MapReduce vòng 1 với đầu vào là tập tin đồ thị.
2. Sau mỗi vòng, kết quả được ghi vào HDFS và làm đầu vào cho vòng kế tiếp.
3. Dừng lặp khi sự chênh lệch PR giữa hai vòng nhỏ hơn ε.

**Lệnh chạy Hadoop Streaming:**

_Vòng 1: Chạy thuật toán Personalized PageRank lần đầu:_
```bash
hadoop jar %HADOOP_HOME%/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar ^
-input /input/graph.txt ^
-output /output_pr_1 ^
-mapper "python mapper_ppr.py" ^
-reducer "python reducer_ppr.py" ^
-file mapper_ppr.py ^
-file reducer_ppr.py
```

**Tạo thư mục lưu kết quả mỗi vòng:**
Trước khi chạy các vòng lặp, hãy tạo thư mục để lưu trữ kết quả từng vòng lặp:
```bash
mkdir result_rounds
```

**Sau mỗi vòng:**
- Thay `/input` bằng đầu ra của vòng trước: `/output_pr_<n>`
- Lưu kết quả vào thư mục `result_rounds/` bằng lệnh:
```bash
hadoop fs -cat /output_pr_<n>/part-00000 > result_rounds/result<n>.txt
```

**Kiểm tra hội tụ:**  
Dùng script `check_converged.py` để so sánh PR giữa hai vòng:
```bash
python check_converged.py result_rounds/result<n>.txt result_rounds/result<n + 1>.txt
```

Nếu sự chênh lệch nhỏ hơn epsilon (ví dụ `0.0001`) thì xem như đã hội tụ.

**Các file quan trọng:**
- `mapper_ppr.py`: Bộ phân phối PR theo đồ thị
- `reducer_ppr.py`: Tổng hợp giá trị PR mới
- `check_converged.py`: So sánh PR giữa 2 vòng để kiểm tra hội tụ
- `graph.txt`: Đồ thị đầu vào
- `result_rounds/`: Thư mục chứa kết quả từng vòng
---

## D. Kết quả 14 vòng lặp (PageRank)

| Vòng | P1 | P2 | P3 | P4 | P5 | P6 |
|------|------|------|------|------|------|------|
| R01 | 0.150000 | 0.425000 | 0.425000 | 0.000000 | 0.000000 | 0.000000 |
| R02 | 0.270417 | 0.184167 | 0.063750 | 0.000000 | 0.120417 | 0.000000 |
| R03 | 0.168063 | 0.132990 | 0.114927 | 0.051177 | 0.018063 | 0.051177 |
| R04 | 0.182563 | 0.103989 | 0.071427 | 0.051177 | 0.054313 | 0.029427 |
| R05 | 0.170238 | 0.097827 | 0.077589 | 0.048096 | 0.041988 | 0.044833 |
| R06 | 0.171984 | 0.094335 | 0.072351 | 0.055953 | 0.042424 | 0.038286 |
| R07 | 0.170499 | 0.093593 | 0.073093 | 0.050573 | 0.044279 | 0.041810 |
| R08 | 0.170710 | 0.093172 | 0.072462 | 0.054357 | 0.042203 | 0.040312 |
| R09 | 0.170531 | 0.093083 | 0.072552 | 0.052201 | 0.043633 | 0.041038 |
| R10 | 0.170556 | 0.093032 | 0.072476 | 0.053426 | 0.042742 | 0.040729 |
| R11 | 0.170535 | 0.093021 | 0.072486 | 0.052785 | 0.043241 | 0.040871 |
| R12 | 0.170538 | 0.093015 | 0.072477 | 0.053118 | 0.042971 | 0.040811 |
| R13 | 0.170535 | 0.093014 | 0.072479 | 0.052952 | 0.043110 | 0.040838 |
| R14 | 0.170536 | 0.093013 | 0.072477 | 0.053034 | 0.043040 | 0.040826 |

---

## E. Clone và chạy nhanh

```bash
git clone https://github.com/LyThach/CSDLPT_BTL_PersonalizedPageRank.git
cd CSDLPT_BTL_PersonalizedPageRank
python check_converged.py result_rounds/result13.txt result_rounds/result14.txt
```

 Nếu bạn cần kiểm tra lại thuật toán thì chỉ cần chạy lại file `mapper`, `reducer`, `check_converged` theo hướng dẫn trên.
---

## F. Mục tiêu bài toán

Thuật toán Personalized PageRank (PPR) mở rộng từ PageRank truyền thống, cho phép tính **độ quan trọng của các node trong đồ thị** từ góc nhìn cá nhân hoá, tức là bắt đầu từ **một node nguồn cụ thể** (trong đồ thị này là P1).  
Mục tiêu của dự án là tính toán và theo dõi sự lan truyền trọng số trong mạng, để từ đó tìm ra các node có ảnh hưởng cao nhất đến node nguồn.

---

## G. Ứng dụng thực tiễn

Thuật toán Personalized PageRank được ứng dụng rộng rãi trong nhiều hệ thống thực tế:

-  **Hệ thống gợi ý** (Recommendation Systems): Netflix, YouTube, Spotify dùng để gợi ý dựa trên sở thích cá nhân.
-  **Hệ thống tìm kiếm học thuật**: Google Scholar sử dụng để đề xuất tác giả và tài liệu liên quan.
-  **Mạng xã hội**: Facebook, Twitter phân tích mức độ ảnh hưởng giữa người dùng.
-  **Phát hiện spam/phishing**: đánh giá độ tin cậy của các node/máy chủ/email dựa vào mạng liên kết.

---

## H. Tài liệu tham khảo

[1] L. Page, S. Brin, R. Motwani, and T. Winograd, “The PageRank Citation Ranking: Bringing Order to the Web,” Stanford InfoLab, Technical Report, 1999.  
[2] Apache Hadoop Documentation. [Online]. Available: https://hadoop.apache.org/  
[3] M. T. Özsu and P. Valduriez, *Principles of Distributed Database Systems*, 4th ed., Springer, 2020.  
[4] J. Dean and S. Ghemawat, “MapReduce: Simplified Data Processing on Large Clusters,” *Communications of the ACM*, vol. 51, no. 1, pp. 107–113, Jan. 2008.  
[5] T. White, *Hadoop: The Definitive Guide*, 4th ed., O’Reilly Media, 2015.  
[6] J. Leskovec, A. Rajaraman, and J. D. Ullman, *Mining of Massive Datasets*, 2nd ed., Cambridge University Press, 2014.

## I. Kho chứa mã nguồn trên GitHub

Toàn bộ mã nguồn được tổ chức tại kho:  
🔗 https://github.com/LyThach/CSDLPT_BTL_PersonalizedPageRank.git

Cấu trúc thư mục chính:
- `mapper_ppr.py`: Script phân phối PageRank qua các node liên kết.
- `reducer_ppr.py`: Tổng hợp PR mới tại mỗi node, tính hội tụ.
- `check_converged.py`: Kiểm tra sai số giữa hai vòng liên tiếp.
- `graph.txt`: Đồ thị đầu vào có định dạng chuẩn.
- `result_rounds/`: Lưu kết quả từng vòng từ 1 đến 14.

> Hướng dẫn đầy đủ đã có sẵn trong README này.


