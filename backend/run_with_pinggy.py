import os

import pinggy
import uvicorn


def main():
    port = int(os.getenv("PORT", "8000"))
    forward = f"localhost:{port}"

    tunnel = pinggy.start_tunnel(forwardto=forward)
    print("Pinggy tunnel started. Public URLs:")
    for url in getattr(tunnel, "urls", []):
        print(" -", url)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
