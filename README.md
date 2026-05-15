# [![QR Pigeon Banner](./static/readme/banner.gif)](https://www.qrpigeon.pics/)

# QR Pigeon

Tool for quickly sharing photos between devices via QR codes.

## How to Use

<img src="./static/readme/tutorial.png" width="500">

## Features

- Generates a unique QR code for each browser session
- Provides a mobile-friendly upload page accessible by scanning the QR code
- Supports image upload from mobile devices
- Automatically converts HEIC images to PNG format
- Displays uploaded images on the host page for easy download

## Links

[Try it out!](https://qrpigeon.pics)
[Buy us a Coffee!](https://www.buymeacoffee.com/qrpigeon)

## Deploying with Dokploy

This app is Docker-ready for Dokploy as a single-container Application.

### Dokploy settings

- Build type: Dockerfile
- Container port: `8080`
- Health check path: `/vet`
- Domain: `qrpigeon.edwardgaibor.me`
- HTTPS: enabled with Let's Encrypt

### Environment variables

Use `.env.example` as the starting point. Set a real `SECRET_KEY` in Dokploy before deploying.

Recommended production values:

```env
PUBLIC_BASE_URL=https://qrpigeon.edwardgaibor.me
COOKIE_SECURE=true
PORT=8080
WEB_CONCURRENCY=1
WEB_THREADS=8
UPLOAD_FOLDER=/app/static/images
COUNTER_FILE=/app/data/counter.txt
```

`WEB_CONCURRENCY` should stay at `1` unless session storage is moved out of process. QR upload sessions are currently stored in memory.

### Persistent storage

For uploads and the counter to survive redeploys, add Dokploy mounts for:

- `/app/static/images`
- `/app/data`

Without these mounts, uploaded files and the counter are ephemeral and will reset when the container is replaced.

### DNS

Point `qrpigeon.edwardgaibor.me` at the server running Dokploy, then add the domain in the Dokploy Application's Domains tab with container port `8080`.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
