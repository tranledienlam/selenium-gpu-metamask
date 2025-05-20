# AUTOMATION GPU + METAMASK WALLET với Selenium Python

## ⚠ Lưu ý quan trọng

🔴 **Dự án này có chứa code hint.** Vui lòng tìm đến **bài ghim** trong kênh [Telegram Channel](https://t.me/+8o9ebAT9ZSFlZGNl) để kiểm tra trước khi sử dụng.

---

## 📖 Mục lục
1. [Giới thiệu](#-giới-thiệu)
2. [Video demo](#-video-demo)
3. [Chức năng chính](#-chức-năng-chính)
4. [Yêu cầu ban đầu](#-yêu-cầu-ban-đầu)
5. [Cấu trúc file](#-cấu-trúc-file)
6. [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
7. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
8. [Tùy chỉnh cấu hình](#-tùy-chỉnh-cấu-hình)
9. [Tips](#-tips)
10. [Thông tin liên hệ](#-thông-tin-liên-hệ)

## 🔔 Bật thông báo để theo dõi mã nguồn khi có update

1. Đăng nhập vào GitHub.
2. Nhấn vào biểu tượng 🔔 **Watch** (góc trên bên phải của repository này).
3. Chọn **"All Activity"** để nhận tất cả thông báo hoặc **"Custom" > "Pull Requests"** để nhận thông báo khi có thay đổi trong mã nguồn.

---

## 🌐 Giới thiệu

📌 **Trang dự án**: [token.gpu.net](https://token.gpu.net/?ref=YW0IAN)

<p align="center">
    <img src="intro.jpg" alt="Giới thiệu">
</p>

---

## 🚀 Chức năng chính

- **Metamask**: Import và Unlock ví.
- **Check-in GPU**: Connect và check-in "Say GM" hằng ngày.

---

## 🔧 Yêu cầu ban đầu

- **Metamask**: Import sẵn 12 seeds vào Metamask (nếu không cung cấp 12 seed trong file data.txt).

- **GPU**: Cần kết nối tài khoản X trước khi check-in

---

## 📂 Cấu trúc file

| File                           | Mô tả                                    |
| ------------------------------ | ---------------------------------------- |
| `extensions/meta-wallet-*.crx` | Tiện ích mở rộng Metamask Wallet.        |
| `browser_automation.py`        | Code tự động hóa trình duyệt.            |
| `utils.py`                     | Các hàm hỗ trợ chung.                    |
| `w_metamask.py`                    | Xử lý các thao tác liên quan đến Metamask. |
| `index.py`                     | File khởi chạy chương trình chính.       |
| `requirements.txt`             | Danh sách các thư viện cần thiết.        |
| `intro.jpg`                    | Hình ảnh giới thiệu.                     |
| `run_menu.bat`                 | Chạy code với 1 click.                   |
| `run_hidden.vbs`               | Chạy code với Task scheduler (window).   |

---

## 📌 Hướng dẫn cài đặt

### 1️ Tạo file `data.txt`

- Mỗi dòng chứa thông tin một profile theo cấu trúc:
  ```plaintext
  [tên_profile]|[mật_khẩu_ví_meta]|[12_seeds (tuỳ chọn)]|[proxy (tuỳ chọn)]
  ```

  Trong đó:

    - `tên_profile`: Tên của profile.
    - `mật_khẩu_ví_meta`: Mật khẩu đăng nhập ví MetaMask.
    - `12_seeds (tuỳ chọn)`: cụm từ bí mật. Nếu không có, thì cần import thủ công.
    - `proxy (tuỳ chọn)`: Có thể là một trong hai dạng sau:
      - `ip:port` → Proxy không có xác thực.
      - `user:pass@ip:port` → Proxy có xác thực bằng tài khoản & mật khẩu.

- Ví dụ:
  ```plaintext
  profile1|12345678|word1 word2 ...|38.154.227.167:2534             // Proxy (không yêu cầu mật khẩu)
  profile2|12345678|word1 word2 ...|user:pass@138.154.227.167:2534  // Proxy (yêu cầu mật khẩu)
  profile3|12345678|word1 word2 ...                                 // Không dùng proxy
  profile4|12345678                                 // Không có mật khẩu, đăng nhập thủ công
  ```

- **Lưu ý:** Khi sử dụng proxy, trình duyệt có thể **hiển thị cảnh báo "Not Secure"** do vấn đề chứng chỉ bảo mật. Điều này không ảnh hưởng đến hoạt động.

### 2️⃣ Tạo file `token.txt` (Tùy chọn)

- File này dùng để lưu trữ token của **Telegram Bot** và **AI Bot**. Bạn có thể cấu hình một trong hai hoặc cả hai bot.

- Chức năng của từng bot:
  - **Telegram Bot**: Gửi ảnh chụp màn hình đến tài khoản Telegram cá nhân trong quá trình thực thi. Nếu không được cấu hình, ảnh sẽ được lưu vào thư mục snapshot.
  - **AI Bot**: Hỗ trợ phân tích và xác định luồng thực thi. Nếu không được cấu hình, các chức năng AI sẽ bị bỏ qua.

- Cấu trúc file: Mỗi dòng bắt đầu bằng từ khóa `tele_bot` hoặc `ai_bot`
  ```plaintext
  tele_bot|[User_ID]|[Bot_ID:Telegram_Bot_Token]
  ai_bot|[AI_Bot_Token]
  ```
- Ví dụ:
  ```plaintext
  tele_bot|123456789|7934583453:AAFcOebukTPfkL6dfg4_PH_ahBA0lU36xyc
  ai_bot|AIzaSyAasvkX_3nexsTcRALfsvbUeLmzpSz0JvA
  ```

### 3️ Cài đặt Python & thư viện

Trước tiên, cần cài đặt Python (phiên bản 3.8 trở lên). Nếu chưa có, hãy tải và cài đặt từ [Python Official Site](https://www.python.org/downloads/).

- Kiểm tra phiên bản Python bằng lệnh:
  ```sh
  python --version
  ```
- Cài đặt thư viện yêu cầu:
  ```sh
  pip install -r requirements.txt
  ```

Tuỳ thuộc vào phiên bản và cách cài đặt, có thể gọi python với các lệnh sau: `py`, `python`, `python3`.

---

## ▶ Hướng dẫn sử dụng

### 1️ Chạy chương trình

```sh
python index.py
```

Tuỳ chọn khác

```sh
# Bỏ qua menu và chạy tự động tất cả các profile.
python index.py --auto 

# Chạy tự động ở chế độ ẩn trình duyệt
python index.py --auto --headless

# Chạy ở chế độ tắt GPU vật lý (dùng khi máy tính không có GPU vật lý, ví dụ: VPS, server)
python index.py --disable-gpu
```

### 2️ Các chế độ hoạt động

- **1. Set up**: Chạy chế độ cài đặt ban đầu và chọn profile.
- **2. Chạy Auto**: Chạy chế độ tự động theo cấu hình đã thiết lập.
- **3. Xoá profile**: Chọn xoá profile trong thư mục `user_data` (Nếu có).
- **0. Thoát**: Dừng chương trình.

**💡 Lưu ý:**

- **Lần đầu:** Chạy **Set up (1)** để thiết lập cấu hình cần thiết.
- **Những lần sau:** Chạy **Auto (2)** để tự động thực thi theo luồng đã lập trình.

---

## ⚙ Tùy chỉnh cấu hình

### 🔹 **Thay đổi số lượng profile chạy đồng thời**

```python
browser_manager.run_terminal(
    profiles=PROFILES,
    max_concurrent_profiles=4,
    ...
)
```

Đổi số `4` thành số bất kì

**Lưu ý:** Hầu hết trường hợp bị lỗi là do quá trình load chậm khi chạy nhiều profile cùng lúc. Tuỳ thuộc vào tài nguyên máy tính và tốc độ internet, hãy điều chỉnh con số thích hợp.

### 🔹 **Chặn hình ảnh và video để tăng tốc độ tải trang**

```python
    block_media=True,
```

`True`: không tải hình ảnh và video.

`False`: tải hình ảnh và video (nếu trang web có cloudflare thì bắt buộc phải là `False`).

---

## 🎯 Tips

### 1️⃣ Cấu hình `tele_bot` trong file `token.txt` để theo dõi lỗi

- Mỗi dự án có một bot Telegram riêng, giúp theo dõi lỗi dễ dàng hơn.
- **Hướng dẫn lấy token Telegram:** Truy cập [channel](https://t.me/+8o9ebAT9ZSFlZGNl), tìm bài viết `Cách lấy thông tin cho file token.txt`.

### 2️⃣ Cấu hình **ai_bot** trong file `token.txt` để xác định luồng tốt hơn.

- **Hướng dẫn lấy token AI bot:**
  - Truy cập [aistudio google](https://aistudio.google.com/apikey)
  - Chọn/Nhấn "Create API Key"
  - Copy "API key"

- **Lưu ý:**
  - Source dùng model `gemini-2.0-flash`.
  - Với gói miễn phí, chạy được khoảng 20-30 dự án/ngày, cho 5-10 profiles/dự án, tương đương khởi chạy **300 lần profile/ngày**

### 3️⃣ Tự động hóa với một cú click (Chỉ áp dụng cho Windows)

Để chạy chương trình đơn giản hơn, bạn có thể sử dụng file `run_menu.bat` bằng cách click đúp chuột trực tiếp vào file, thay vì phải mở code và gõ lệnh trong CMD.

Nếu bạn đang sử dụng Python trong môi trường ảo (virtual environment), hãy chỉnh sửa đường dẫn Python `H:\venv_selenium\Scripts\python.exe` trong file `run_menu.bat`:

```
set VENV_PATH=H:\venv_selenium\Scripts\python.exe
```

### 4️⃣ Chạy tự động ẩn với Windows Task Scheduler

1. Mở **Task Scheduler** bằng cách tìm kiếm trên Windows.
2. Menu > Action > **Create Task..**.
3. Tab **General**: đặt tên cho task
4. Tab **Triggers**: thiết lập lịch chạy
  - Click **New...**
  - Tại **Begin the task**: chọn **At startup** để chạy khi khởi động Windows, hoặc **On a schedule** để đặt lịch cụ thể.
  - Chọn **Enabled** để kích hoạt trigger.
5. Tab **Actions**: thiết lập chương trình chạy
  - Click **New...**
  - **Action**: chọn **Start a Program**
  - **Program/script**: nhập `wscript.exe`
  - **Add arguments**: dán đường dẫn đầy đủ tới file `run_hidden.vbs`
6. Tab **Conditions** (optional): 
  - Bỏ chọn **Start the task only if the computer is on AC power**
  - Bỏ chọn **Stop if the computer switches to battery power**
7. Tab **Settings** (optional):
  - Chọn **Run task as soon as possible after a scheduled start is missed**
  - Chọn **If the task fails, restart every: 1 minute** và **Attempt to restart up to: 3 times**
8. Click **OK** để lưu task.

Bây giờ, chương trình sẽ tự động chạy ẩn dưới nền window theo lịch trình đặt trước. 🚀

---

## 🔗 Thông tin liên hệ

📢 **Telegram Channel:** [Airdrop Automation](https://t.me/+8o9ebAT9ZSFlZGNl)

💰 **Ủng hộ tác giả:**

- **EVM:** `0x3b3784f7b0fed3a8ecdd46c80097a781a6afdb09`
- **SOL:** `4z3JQNeTnMSHYeg9FjRmXYrQrPHBnPg3zNKisAJjobSP`
- **TON:** `UQDKgC6TesJJU9TilGYoZfj5YYtIzePhdzSDJTctJ-Z27lkR`
- **SUI:** `0x5fb56584bf561a4a0889e35a96ef3e6595c7ebd13294be436ad61eaf04be4b09`
- **APT (APTOS):** `0x557ea46189398da1ddf817a634fa91cfb54a32cfc22cadd98bb0327c880bac19`

🙏 Khi ủng hộ, nếu không thấy phiền, Bạn có thể gửi token chính của mạng. Cám ơn Bạn đã hỗ trợ!