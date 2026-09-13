from datetime import datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


class PlaywrightCollector:
    """
    Reusable browser collector for permitted airline/OTA pages.

    AERIS policy:
    - Respect robots.txt and the site's Terms of Service.
    - Use conservative request rates.
    - Do not bypass CAPTCHA, authentication, access controls,
      bot protection, or other technical restrictions.
    """

    def __init__(self, headless=True, timeout_ms=30000):
        self.headless = headless
        self.timeout_ms = timeout_ms

    def open_page(self, url: str):
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only HTTP/HTTPS URLs are allowed.")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page(
                viewport={"width": 1440, "height": 900},
                user_agent=(
                    "AERIS-Research/1.0 "
                    "(airfare price index research prototype)"
                ),
            )

            started_at = datetime.now()

            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=self.timeout_ms,
            )

            page.wait_for_timeout(2000)

            result = {
                "url": page.url,
                "status": response.status if response else None,
                "title": page.title(),
                "collected_at": started_at.isoformat(),
            }

            browser.close()

            return result


if __name__ == "__main__":
    collector = PlaywrightCollector(headless=True)

    result = collector.open_page("https://www.google.com")

    print("Collector test:")
    for key, value in result.items():
        print(f"{key}: {value}")
