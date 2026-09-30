"""Check local links and anchors on the static portfolio page."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.targets.append(attrs[key])


root = Path(__file__).parent
page = Links()
page.feed((root / "index.html").read_text(encoding="utf-8"))
for target in page.targets:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith("mailto:"):
        continue
    if parsed.path:
        assert (root / unquote(parsed.path)).is_file(), f"Missing local file: {target}"
    if parsed.fragment:
        assert parsed.fragment in page.ids, f"Missing anchor: {target}"
print(f"Checked {len(page.targets)} local/external references and anchors")
