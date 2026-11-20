#!/usr/bin/env bash
# render_check.sh GUIDE.html [OUT_DIR]: see an HTML guide the way readers will.
#
# Screenshots it in headless Chrome at desktop width (900px) in light and dark, and at phone
# width (390px) in dark, as slices short enough to read (NAME-01.png, NAME-02.png, ...). It
# also reports any element that sticks out past the right edge (outside scrollable boxes).
# The theme is forced through the `dark` class (Tailwind) and `data-theme`, so it works
# for the quick-learn template and for hand-written pages.
#
# Env: CHROME (path to Chrome/Chromium; default: the macOS app, then chromium on PATH).
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <guide.html> [out-dir]" >&2
  exit 2
fi
[[ -f "$1" ]] || { echo "No such file: $1" >&2; exit 2; }

guide="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
out="${2:-$(mktemp -d)/render-check}"
mkdir -p "$out"
out="$(cd "$out" && pwd)"

chrome="${CHROME:-}"
if [[ -z "$chrome" ]]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "$(command -v chromium || true)" "$(command -v google-chrome || true)"; do
    if [[ -n "$c" && -x "$c" ]]; then chrome="$c"; break; fi
  done
fi
[[ -n "$chrome" ]] || { echo "Chrome not found: set CHROME" >&2; exit 2; }

profile="$(mktemp -d)"
trap 'rm -rf "$profile"' EXIT
guide_url="file://$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$guide")"
slice=1600
status=0

# The guide runs in an iframe of the requested width (headless Chrome won't make a window
# narrower than ~500px). Once it has loaded, the wrapper forces the theme, sizes the frame
# to the page's full height, and records the height and any overflow in <body data-*>.
# OFFSET shifts the frame up, so a window SLICE pixels tall captures one slice.
wrapper() { # wrapper THEME WIDTH OFFSET > file
  cat <<EOF
<!doctype html><html><body style="margin:0;overflow:hidden">
<iframe id="f" src="$guide_url" style="display:block;position:absolute;left:0;top:-${3}px;width:${2}px;height:900px;border:0"></iframe>
<script>
var f = document.getElementById("f");
f.addEventListener("load", function () {
  var root = f.contentDocument.documentElement;
  // no colour transitions: headless Chrome can capture them half-finished
  var still = f.contentDocument.createElement("style");
  still.textContent = "*, *::before, *::after { transition: none !important; }";
  f.contentDocument.head.appendChild(still);
  root.classList.toggle("dark", "$1" === "dark");
  root.setAttribute("data-theme", "$1");
  setTimeout(function () {
    var doc = f.contentDocument, width = doc.documentElement.clientWidth, wide = [];
    doc.querySelectorAll("body *").forEach(function (el) {
      if (el.getBoundingClientRect().right <= width + 1) return;
      for (var a = el.parentElement; a && a !== doc.body; a = a.parentElement) {
        if (/auto|scroll|hidden/.test(getComputedStyle(a).overflowX)) return;  // inside a scroll box
      }
      wide.push(el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined ? "." + String(el.className).trim().split(/\s+/).join(".") : "") +
                " (" + Math.round(el.getBoundingClientRect().right - width) + "px over)");
    });
    var height = Math.min(doc.documentElement.scrollHeight, 30000);
    f.style.height = height + "px";
    document.body.setAttribute("data-height", height);
    document.body.setAttribute("data-wide", wide.slice(0, 12).join(" | "));
  }, 1500);
});
</script></body></html>
EOF
}

run_chrome() { "$chrome" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --user-data-dir="$profile" --virtual-time-budget=6000 "$@" 2>/dev/null; }

for view in desktop-light:light:900 desktop-dark:dark:900 phone-dark:dark:390; do
  IFS=: read -r name theme width <<<"$view"
  wrapper "$theme" "$width" 0 > "$out/$name.wrapper.html"
  dom=$(run_chrome --window-size=600,2000 --dump-dom "file://$out/$name.wrapper.html")
  height=$(sed -n 's/.*data-height="\([0-9]*\)".*/\1/p' <<<"$dom" | head -n 1)
  wide=$(sed -n 's/.*data-wide="\([^"]*\)".*/\1/p' <<<"$dom" | head -n 1)
  if [[ -z "$height" ]]; then
    echo "$name: the page didn't finish loading in time" >&2
    status=1
    continue
  fi
  # The window is at least 600px wide; anything right of WIDTH is blank wrapper page.
  window_width=$(( width < 600 ? 600 : width ))
  n=0
  for (( y = 0; y < height; y += slice )); do
    n=$((n + 1))
    h=$(( height - y < slice ? height - y : slice ))
    wrapper "$theme" "$width" "$y" > "$out/$name.wrapper.html"
    run_chrome --window-size="$window_width,$h" --screenshot="$(printf '%s/%s-%02d.png' "$out" "$name" "$n")" \
      "file://$out/$name.wrapper.html" >/dev/null
  done
  rm -f "$out/$name.wrapper.html"

  if [[ -n "$wide" ]]; then
    echo "$name: WIDER THAN THE SCREEN: $wide"
    status=1
  else
    echo "$name: ${height}px tall, $n slice(s), nothing wider than ${width}px"
  fi
done

echo "Slices: $out"
exit $status
