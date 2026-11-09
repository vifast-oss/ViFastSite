# ViFastSite

Trang đích tĩnh cho **ViFast** — ba dự án mã nguồn mở của một người Việt:
[ViFastKey](https://key.vifast.org) (bộ gõ), [ViFastTts](https://tts.vifast.org) (giọng đọc)
và [ViFastOs](https://os.vifast.org) (hệ điều hành microkernel).

Site thuần HTML/CSS/JS: không build step, không framework, không CDN, không font ngoài.
Yêu cầu duy nhất ra mạng là GitHub API để lấy tag bản phát hành mới nhất; nếu lỗi thì huy hiệu
tự ẩn và trang vẫn hoạt động bình thường.

## Chạy local

```sh
cd /Users/mps/dvchd/ViFastSite
python3 -m http.server 8000
# mở http://localhost:8000
```

Mở trực tiếp `index.html` bằng `file://` cũng được; khi đó huy hiệu phiên bản có thể không
hiển thị do CORS/API, phần còn lại vẫn chạy.

## Build và chạy Docker

```sh
docker build -t vifastsite .
docker run --rm -p 8080:80 vifastsite
# mở http://localhost:8080
curl -i http://localhost:8080/healthz   # 200 OK
```

## Quản trị + thống kê truy cập

Trang chủ vẫn là HTML tĩnh, nhưng có thêm service `portal/` (FastAPI + SQLite) lo
ba việc: form đăng nhập quản trị, đo lượt truy cập, và bảng thống kê.

- `/login` — nhập mật khẩu trong biến `ADMIN_PASSWORD` (cookie phiên `vf_admin`,
  HttpOnly + SameSite=Lax + Secure, hạn 12 giờ).
- `/admin` — hôm nay / 7 ngày / 30 ngày, khách duy nhất, biểu đồ 24 giờ và 14
  ngày, trang xem nhiều, nguồn giới thiệu, thiết bị, trình duyệt, ngôn ngữ,
  `/admin/stats.csv` để tải CSV.
- `/track.js` + `/api/track` — beacon 1 dòng nhúng ở cuối trang; chỉ đếm lượt xem
  của người dùng thật (bỏ qua bot, tài nguyên tĩnh, chính trang quản trị) và
  không lưu IP thô, chỉ hash có muối đổi mỗi ngày.

nginx chuyển riêng các đường dẫn này sang container `portal` (Docker DNS
`127.0.0.11`); phần còn lại vẫn do nginx phục vụ tĩnh với cache 7 ngày.

```sh
cp .env.example .env      # đặt ADMIN_PASSWORD, STATS_SALT
mkdir -p portal-data && sudo chown 10001:10001 portal-data
docker compose up -d --build
```

Dữ liệu nằm ở `portal-data/stats.sqlite3`. Đổi `ADMIN_PASSWORD` rồi
`docker compose up -d portal` là mọi phiên cũ hết hiệu lực.

## Tên miền

- `vifast.org` (và `www.vifast.org` nếu trỏ cùng) — trang này.
- `key.vifast.org`, `tts.vifast.org`, `os.vifast.org` — các dịch vụ riêng, chỉ được liên kết
  từ trang này, không được phục vụ bởi image này.

## Cấu trúc

| File | Vai trò |
| --- | --- |
| `index.html` | Nội dung trang, tiếng Việt là chính |
| `styles.css` | Toàn bộ giao diện, font hệ thống |
| `app.js` | Menu di động, cuộn mượt, huy hiệu phiên bản |
| `nginx.conf` | Cấu hình server tĩnh (gzip, cache, `/healthz`) |
| `Dockerfile` | Image `nginx:alpine` chứa site |
