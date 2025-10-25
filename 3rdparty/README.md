# Third-Party Dependencies

To build the minified npf2html.iife.js from source:
```
esbuild src/index.ts --bundle --format=iife --global-name=npf2html --platform=neutral --target=es2020 --outfile=dist/npf2html.iife.js --minify --sourcemap
```
