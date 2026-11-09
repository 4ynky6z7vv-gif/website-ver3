# McQueen Portfolio — HTML / CSS

从 Figma 文件 `McQueen Portfolio`（node `3:3`，画板 **Home**，1440 × 5900）1:1 导出的静态页面。

## 两种打开方式

| 文件 | 说明 |
| --- | --- |
| **`mcqueen-portfolio-standalone.html`** | **单文件版（推荐）**：CSS、字体、全部图片、SVG 都以 base64 内嵌，2.5 MB，拷到任何地方双击就能完整显示，不依赖同目录文件，也不会出现图片空白/字体回退 |
| `index.html` + `style.css` + `assets/` | 标准多文件版，结构清晰、便于二次编辑，但**必须把整个文件夹一起移动**，只拷 index.html 会丢图片和样式 |

> 如果之前预览时图片全白、字体变成系统默认，原因就是只加载了单个 HTML，相对路径的 `assets/` 没被一起加载。用单文件版即可避免。

## 文件结构

```
mcqueen-portfolio/
├── mcqueen-portfolio-standalone.html   # 单文件自包含版（CSS+图片+字体全内嵌）
├── index.html                          # 多文件版页面结构（109 个元素，按 Figma 图层顺序）
├── style.css                           # 多文件版样式：位置、尺寸、旋转、阴影、字体
├── mcqueen-portfolio.zip               # 整个文件夹的压缩包（下载/备份用）
└── assets/
    ├── n9-46.png …                     # 设计稿中每张图片的 2x 导出（含旋转/裁切/镜像效果）
    ├── noise.png                       # 纸张颗粒纹理（4% 不透明度 + multiply，整页平铺）
    ├── arrow-*.svg                     # 手绘箭头、圈选、感叹号的矢量图（Figma 原始 SVG）
    ├── circle-tennis.svg / excl-*.svg
    └── fonts/                          # 本地字体 Caveat 400/700、Inter 400/700（离线可用）
```

## 实现说明

- **精确定位**：每个元素都使用 Figma 的 `relativeTransform` 矩阵（`transform: matrix(a,b,c,d,e,f)` + `transform-origin: 0 0`），因此旋转、倾斜、镜像与设计稿一致（英雄区照片 2.2° 倾斜、胶带 45° 贴角、年份文字竖排 90°）。
- **图片**：按设计稿中的实际显示效果从 Figma 以 2 倍图导出，页面上看到的就是设计稿里的样子（原图裁切、旋转、镜像已烘进 PNG）。换图时替换 `assets/n*.png` 即可，宽高在 `style.css` 对应选择器的 `width/height`。
- **响应式**：设计稿固定 1440px 宽，页面末尾的脚本把整页按视口宽度等比缩放；若要做真正的响应式重排，需按断点改 `style.css`。
- **字体**：标题 Inter 700，手写体 Caveat 700/400，均为本地 woff2。

## 修改后如何更新单文件版

单文件版是从多文件版生成的。改完 `index.html` / `style.css` / `assets/` 后，重新内联即可：

```bash
python3 build_standalone.py
```

## 校验

与 Figma 官方渲染图逐像素比对（1440px 宽、0.5x 采样）：文字、卡片、图片位置误差 ≤ 1px，整页平均像素差约 4.9/255（主要来自抗锯齿与 headless 截图边缘裁剪）。
