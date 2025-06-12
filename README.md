# Personalized PageRank - Bài tập lớn CSDL Phân Tán

## Thông tin sinh viên

- **Họ tên**: Thạch Thị Nhanh  
- **MSSV**: N21DCCN159  
- **Lớp**: D21CQCNHT01-N  
- **Email**: n21dccn159@student.ptithcm.edu.vn

## Mô tả

Dự án triển khai bài toán **Personalized PageRank** sử dụng Hadoop Streaming và ngôn ngữ Python.  
Đây là **bài 10.10 trong Chương 10** thuộc tài liệu:

> _Principles of Distributed Database Systems_ — M. Tamer Özsu, Patrick Valduriez (4th Edition)

## Cài đặt và chạy

### Yêu cầu:

- Hệ điều hành: **Windows 10 hoặc mới hơn**
- Java 8 trở lên (để chạy Hadoop)
- Hadoop 3.3.6 (đã thử nghiệm thành công trên Windows)
- Python 3.11.9

### Cài đặt Hadoop trên Windows:

1. Tải và giải nén Hadoop 3.3.6 từ: [https://hadoop.apache.org/releases.html](https://hadoop.apache.org/releases.html)
2. Cấu hình biến môi trường:
   - `HADOOP_HOME`: trỏ tới thư mục cài Hadoop (ví dụ: `C:\hadoop`)
   - Thêm `%HADOOP_HOME%\bin` vào biến `PATH`
3. Cấu hình `core-site.xml` và `hdfs-site.xml` để sử dụng local filesystem.
4. Kiểm tra lệnh Hadoop:

```bash
hadoop version
```

5. Đặt file `hadoop-streaming-3.3.6.jar` vào đường dẫn:  
`%HADOOP_HOME%/share/hadoop/tools/lib/`

### Chuẩn bị dữ liệu đầu vào:

Trước khi chạy vòng 1, bạn cần tạo thư mục `/input` trên HDFS và tải file `graph.txt` lên:

```bash
# Tạo thư mục đầu vào (chỉ cần 1 lần nếu chưa có)
hadoop fs -mkdir /input

# Tải file đồ thị vào HDFS
hadoop fs -put graph.txt /input/graph.txt
```

### Chạy từng vòng Personalized PageRank:

```bash
# Vòng 1
hadoop jar %HADOOP_HOME%/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar ^
-input /input/graph.txt ^
-output /output_pr_1 ^
-mapper "python mapper_ppr.py" ^
-reducer "python reducer_ppr.py" ^
-file mapper_ppr.py ^
-file reducer_ppr.py
```

- Sau mỗi vòng, thay `/input` bằng đầu ra của vòng trước: `/output_pr_<n>`
- Kết quả sau mỗi vòng được lưu vào thư mục `result_rounds/` bằng lệnh:

```bash
hadoop fs -cat /output_pr_<n>/part-00000 > result_rounds/result<n>.txt
```

### Kiểm tra hội tụ:

Sử dụng file `check_converged.py` để so sánh kết quả hai vòng liên tiếp:

```bash
python check_converged.py result_rounds/result13.txt result_rounds/result14.txt
```

Nếu sự chênh lệch nhỏ hơn epsilon (ví dụ `0.0001`) thì xem như đã hội tụ.

## File quan trọng

- `mapper_ppr.py`: Bộ phân phối PR theo đồ thị
- `reducer_ppr.py`: Tổng hợp giá trị PR mới
- `check_converged.py`: So sánh PR giữa 2 vòng để kiểm tra hội tụ
- `graph.txt`: Đồ thị đầu vào
- `result_rounds/`: Thư mục chứa kết quả từng vòng

