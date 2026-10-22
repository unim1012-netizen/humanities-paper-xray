# humanities-xray · 文科论文 X 光

把一篇文科论文还原成它的**论证结构**，再按论文自己的章节顺序逐节精读。fork 自 [paper-xray](https://github.com/Wang-auspicious/paper-xray)，为文科阅读习惯重写。

## 它做什么

- **论证地图先行**：thesis → views → arguments → conclusion → objections → responses 六要素骨架，可交互、可折叠、每个节点能单独标记「不懂 / 已懂」。
- **按论文原章节精读**：正文严格跟随论文自己的章节顺序，每节标注它承载哪个论证要素，前提-结论链用自然语言重建，隐含前提补出并标注。
- **四种类型分流**：论证型 / 综述型 / 考据-历史-文本解释型 / 其他，入口自动检测，歧义时问一次。
- **双语术语**：关键概念「英文（中文译法）」对照，译法有争议时如实标注，文末附概念对照表。
- **写作启示**：从这篇论文提炼可迁移的写作技法，每条带页码。
- **标注闭环**：划线、笔记、反馈（不懂/啰嗦/已懂）、节点级标记，写回 HTML 文件，下次运行读取并调整讲解（读者档案记忆）。

## 安装

```
git clone git@github.com:unim1012-netizen/humanities-paper-xray.git ~/.claude/skills/humanities-xray
# 或 HTTPS：git clone https://github.com/unim1012-netizen/humanities-paper-xray.git
```

支持Codex、Claude、Doubao等平台：把整个目录放进你的 skills 目录（如 `.user_skills/humanities-xray`），确认注册后即可调用。

## 使用

```
/humanities-xray D:/papers/epistemic-injustice.pdf
/humanities-xray https://philpapers.org/rec/XXXX html
/humanities-xray 康德定言命令的论证结构 md
```

1. 提供材料：本地 PDF、链接（PhilPapers/JSTOR/DOI）或粘贴正文。
2. 选格式：`md` 文字长文，`html` 交互可标注页面（推荐，含论证地图）。
3. 首次使用会问三个问题（领域熟悉度 / 阅读目的 / 论证分析水平），据此调整讲解深度。

## 目录结构

```
humanities-xray/
├── SKILL.md            # 中文规格：工作流、四种模式、论证地图、双语术语、读者档案
├── VERSION
├── references/
│   ├── html.md         # HTML 交付规格：五段式结构、AM schema、自检
│   └── reader-kit.html # 页面骨架：版式、标注层、AM 论证地图组件
├── demos/
│   └── structure-demo/ # 结构演示（示意内容）
└── user/               # 运行时生成：读者档案与阅读记录（不进 git）
```

## 许可证

MIT，继承自 paper-xray。
