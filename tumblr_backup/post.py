import json
from pathlib import Path

try:
    import quickjs
    have_quickjs = True
except ImportError:
    from py_mini_racer import MiniRacer
    have_quickjs = False

bundle_src = Path("npf2html.iife.js").read_text(encoding="utf-8")

if have_quickjs:
    # 1) Create a JS context
    ctx = quickjs.Context()

    # 2) Load the bundled library (adds globalThis.npf2html)
    ctx.eval(bundle_src)

    # 3) Define a tiny JS bridge function in the SAME context
    ctx.eval("globalThis.__npf2html_call = function(npf) { return globalThis.npf2html.default(npf); };")

    def get_html(content):
        return ctx.eval("globalThis.__npf2html_call(%s)" % json.dumps(content, ensure_ascii=False))
else:
    ctx = MiniRacer()
    ctx.eval(bundle_src)

    def get_html(content):
        return ctx.call("npf2html.default", content)  # or .default if default export

content = [
  {
    "type": "text",
    "text": "Test Post!",
    "subtype": "heading1"
  },
  {
    "type": "text",
    "text": "1234!"
  }
]
print(get_html(content))
