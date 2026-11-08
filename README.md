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
