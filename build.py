#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
personal-page 构建脚本
用法: python build.py
功能: 读取 content/*.md，渲染为静态 HTML 页面（零第三方依赖）
输出: index.html / intro.html / paper.html / path.html
"""
import html as html_lib
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
TEMPLATE_PATH = os.path.join(ROOT, "template.html")

# 页面定义: 文件名 -> (md 源文件, 页面标题)
PAGES = {
    "intro.html": ("intro.md", "Personal Introduction · Shiming Li's Website"),
    "paper.html": ("paper.md", "Important Papers · Shiming Li's Website"),
    "path.html": ("path.md", "Learning Path · Shiming Li's Website"),
    "index.html": ("intro.md", "Shiming Li's Website"),
}


def strip_frontmatter(text):
    """剥离 +++ ... +++ 或 --- ... --- 头部"""
    for delim in ("+++", "---"):
        if text.startswith(delim):
            parts = text.split(delim, 2)
            if len(parts) == 3:
                return parts[2]
    return text


def render_inline(text):
    """行内元素: 链接/图片/粗体/斜体/行内代码"""
    # 行内代码 (先处理，避免内部符号被转义)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # 链接
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)",
                  lambda m: f'<a href="{m.group(2)}">' + (f' title="{m.group(3)}"' if m.group(3) else "") + f'>{m.group(1)}</a>',
                  text)
    # 粗体
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # 斜体
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_markdown(text):
    """极简 markdown -> HTML (支持标题/段落/列表/引用/分隔线)"""
    lines = text.strip().split("\n")
    out = []
    i = 0
    in_ul = False
    in_ol = False
    in_quote = False
    para = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + render_inline(" ".join(para)) + "</p>")
            para = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i].rstrip()

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush_para(); close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{render_inline(m.group(2))}</h{level}>")
            i += 1; continue

        # 分隔线
        if re.match(r"^\s*[-*_]{3,}\s*$", line):
            flush_para(); close_lists()
            out.append("<hr />")
            i += 1; continue

        # 无序列表
        m = re.match(r"^\s*[-*]\s+(.*)", line)
        if m:
            flush_para()
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append("<li>" + render_inline(m.group(1)) + "</li>")
            i += 1; continue

        # 有序列表
        m = re.match(r"^\s*\d+\.\s+(.*)", line)
        if m:
            flush_para()
            if not in_ol:
                out.append("<ol>"); in_ol = True
            out.append("<li>" + render_inline(m.group(1)) + "</li>")
            i += 1; continue

        # 引用
        m = re.match(r"^\s*>\s?(.*)", line)
        if m:
            flush_para(); close_lists()
            if not in_quote:
                out.append("<blockquote>"); in_quote = True
            out.append("<p>" + render_inline(m.group(1)) + "</p>")
            i += 1; continue

        # 空行
        if not line.strip():
            flush_para(); close_lists()
            if in_quote:
                out.append("</blockquote>"); in_quote = False
            i += 1; continue

        # 普通段落
        if in_quote:
            out.append("</blockquote>"); in_quote = False
        close_lists()
        para.append(line.strip())
        i += 1

    flush_para(); close_lists()
    if in_quote:
        out.append("</blockquote>")
    return "\n".join(out)


def main():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    for out_name, (md_name, title) in PAGES.items():
        md_path = os.path.join(CONTENT_DIR, md_name)
        with open(md_path, "r", encoding="utf-8") as f:
            raw = f.read()
        text = strip_frontmatter(raw)
        content = render_markdown(text)
        page = template.replace("{TITLE}", title).replace("{CONTENT}", content)
        out_path = os.path.join(ROOT, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  ✓ {out_name}  <-  {md_name}")


if __name__ == "__main__":
    main()
