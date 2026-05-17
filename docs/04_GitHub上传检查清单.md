# 04 GitHub 上传检查清单

## 上传前必须检查

1. 确认是否公开仓库。公开仓库不要提交未授权教材、课件、试卷和同学笔记。
2. 检查大文件：

```powershell
Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 95MB } | Select-Object Length, FullName
```

3. 确认 `.gitignore` 已排除：

- 根目录 AIMA 原书 PDF
- `专业核心-人工智能（93）.zip`
- 超过 100MB 的 `ppt/第10讲 不确定性的量化.pptx`
- 实验生成的 `.exe`

4. 如果要把 PDF/PPTX/DOCX 放进私有仓库，建议启用 Git LFS：

```powershell
git lfs install
git lfs track "*.pdf" "*.pptx" "*.doc" "*.docx" "*.zip"
```

## 建议上传步骤

```powershell
git init
git status --short
git add README.md AGENTS.md .gitignore .gitattributes docs 学习规划.md tools output/pdf/aima_learning_splits/README.md
git add 作业 实验 ppt 专业核心-人工智能（93）
git status --short
git commit -m "Prepare AI final review materials"
```

如果 `git add` 后看到大文件或未授权资料进入暂存区，先取消暂存：

```powershell
git restore --staged <path>
```

## 更安全的公开版上传范围

如果要建公开 GitHub，建议只上传：

- `README.md`
- `AGENTS.md`
- `docs/`
- `学习规划.md`
- 自己写的作业/实验 Markdown
- 自己写的工具脚本

教材、课件、试卷、同学笔记保留在本地或私有仓库。

