"""Dịch vụ quản trị cho vifast.org (trang tĩnh).

Trang chủ vifast.org vẫn do nginx phục vụ; service này chỉ nhận ba nhóm đường
dẫn do nginx chuyển sang:

* ``/login``, ``/logout``, ``/admin`` — form mật khẩu + bảng thống kê truy cập.
* ``/track.js`` — đoạn JavaScript nhỏ nhúng vào trang chủ.
* ``/api/track`` — nhận beacon từ ``/track.js`` và ghi vào SQLite.

Dữ liệu nằm ở ``DATA_DIR/stats.sqlite3`` (volume ``./portal-data``).
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from admin_portal import Portal

DATA_DIR = Path(os.getenv("DATA_DIR", "/app/data"))

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

portal = Portal(
    site="vifast.org",
    title="ViFast",
    db_path=DATA_DIR / "stats.sqlite3",
    accent="#C0392B",
    favicon="/brand/vifast-icon-32.png",
    admin_key="site",
)
portal.install(
    app,
    dashboard="Trang chủ là HTML tĩnh, số liệu lấy từ beacon <code>/track.js</code> "
    "(chỉ đếm khi trình duyệt bật JavaScript).",
)

# Đoạn beacon: 1 dòng, không thư viện, không cookie, không theo dõi liên trang.
TRACK_JS = """(function(){try{var b={p:location.pathname,r:document.referrer||"",l:navigator.language||""};
fetch("/api/track",{method:"POST",credentials:"omit",cache:"no-store",keepalive:true,
headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}).catch(function(){});}catch(e){}})();
"""


@app.get("/healthz", include_in_schema=False)
def healthz() -> JSONResponse:
    return JSONResponse({"ok": True})


@app.get("/track.js", include_in_schema=False)
def track_js() -> Response:
    return Response(
        TRACK_JS,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "public, max-age=300"},
    )


@app.post("/api/track", include_in_schema=False)
async def track(request: Request) -> Response:
    try:
        payload = await request.json()
    except Exception:  # body rỗng hoặc không phải JSON
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    portal.track(
        request,
        200,
        {
            "p": str(payload.get("p") or request.headers.get("referer") or "/")[:200],
            "r": str(payload.get("r") or ""),
            "l": str(payload.get("l") or ""),
            "src": "beacon",
        },
    )
    return Response(status_code=204, headers={"Cache-Control": "no-store"})
