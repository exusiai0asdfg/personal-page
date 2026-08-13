# personal-page

个人学术主页（原 my-blog 的 Work 部分），纯静态站点，无框架依赖。

## 目录结构

```
personal-page/
├── index.html      ← 首页（= intro 内容）
├── intro.html      ← Personal Introduction
├── paper.html      ← Important Papers
├── path.html       ← Learning Path
├── content/        ← 文章源文件（Markdown）
│   ├── intro.md
│   ├── paper.md
│   └── path.md
├── css/work.css    ← 样式
├── img/            ← 图片资源
│   ├── XJTU.jpg    ← 页面背景图（换背景直接替换此文件）
│   └── mouse.jpg   ← 头像
├── template.html   ← 页面骨架模板
└── build.py        ← 构建脚本（零依赖，仅需 Python 3）
```

## 写文章

直接编辑 `content/*.md`，支持：标题、段落、列表、引用、分隔线、`**粗体**`、`*斜体*`、`[链接](url)`、`行内代码`。

## 构建

```bash
python build.py
```

## 本地预览

```bash
python -m http.server 8080
# 打开 http://localhost:8080
```

## 部署

`index.html` + `intro.html` + `paper.html` + `path.html` + `css/` + `img/` + `favicon.ico` 全部是纯静态文件：

- **Vercel / Netlify**：仓库根目录指向本项目即可，无需构建命令（或构建命令填 `python build.py`）
- **GitHub Pages**：直接 push 到仓库，或把生成的 HTML 推到 `gh-pages` 分支
- **任意静态托管**：整个文件夹直接上传

## 换背景图

1. 替换 `img/XJTU.jpg`（文件名保持不变即可）
2. 若换文件名，同时修改 `template.html` 中的 `--work-bg-image: url('img/...')`

## 底部 Life 链接

页面底部的 "Life" 指向 `https://exusiaiblog.vercel.app/`（blog 项目）。如需修改，编辑 `template.html` 中的链接。
