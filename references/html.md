# HTML 交付规格
HTML 分支读这一份。正文的写作要求一条不减，这里只管页面、论证地图、交互和标注层。

## 1. 页面骨架：照抄 reader-kit
页面从 `references/reader-kit.html` 起步，不自己设计骨架。文件里有五段带 START / END 注释的块，**整段复制，一个字不改**：

| 块 | 放在哪 | 管什么 |
|---|---|---|
| `XRAY HEAD` | `<head>` | 首屏定主题（不闪白）、KaTeX |
| `XRAY PAGE CSS` | `<style>` 开头 | 版式、配色变量、标注层样式、AM（论证地图）样式 |
| `XRAY BODY TOP` | `<body>` 开头 | 顶栏四个键、目录栏、`<main>` 开头 |
| `XRAY BODY BOTTOM` | 正文之后 | `</main>`、标注数据块 `xray-notes`、地图配置块 `xray-am`、`XRAY JS`、`AM JS` |

正文写在 `<main>` 里，h2、h3 必须是 `<main>` 的直接子元素，目录、折叠、标注都靠这一点找到章节。`<html lang>` 写 `zh-CN`，标注层的按钮文字跟着它切换。

`xray-notes` 块里的 `doc` 在生成时填好：`{"title":"文档标题","source":"论文名或主题","made":"YYYY-MM-DD","lang":"zh","file":"文件绝对路径"}`。`marks`、`folds` 保持空数组。

`xray-am` 块在生成时填好论证地图配置（schema 见第 4 节）。页面没有论证地图的（极少数），删掉这个块。

**三条硬约束**，违反任何一条，标注保存后再打开会出错：

1. AM 宿主（`.am` 元素）在源文件里是空的，内容只由 `XRAY.ready` 里的脚本画出。
2. 不自己调用 `renderMathInElement`，公式由 `XRAY JS` 统一渲染。
3. 不在 `XRAY.ready` 外面改 DOM。

原因：保存标注时，页面把载入那一刻的源码原样写回文件，只替换 `xray-notes` 这一块。在 `ready` 之前改过的东西会被一起写进去，下次打开就会重复。

## 2. 版式数值
reader-kit 已经实现了下面这些数值。列在这里是为了自检，不需要重写。

| 项 | 值 |
|---|---|
| 容器 | `max-width: 1560px`，左右内边距 48px |
| 栅格 | `224px minmax(0,1fr)`，`gap: 48px`。目录贴页面最左缘，正文从目录右边 48px 开始铺到右缘 |
| 目录 | 由 h2、h3 自动生成；13px / 1.55，条目最多两行；当前节加 2px 强调色左竖条 |
| 行文宽度 | 段落、列表、卡片上限 88ch；有边注时自动收窄；图、表、论证地图占满整列 |
| 顶栏 | 左上角四个纯文字键：☰ 目录、◐ 明暗、✎ 标注开关、⤓ 保存（有未写回的标注时右上角亮一个小点） |
| 进度条 | 2px，强调色，`opacity .38`，停止滚动 1.2s 后淡出 |
| 窄屏 | ≤1100px 目录收进浮层、边注改为插在段落下方；≤640px 内边距 20px，h1 25px，正文 16px |
| 字体 | 正文和标题 `Anthropic Serif`，界面 `Anthropic Sans`，代码和数字 `Anthropic Mono`；本机有字体文件就 base64 内联，没有就用回退栈 |
| 字号 | 正文 17px / 1.78；h1 31px / 700，下加 3px 双线；h2 22px，上间距 64px；h3 18px；数字 `tabular-nums` |

调色板（Claude Warm Paper）和论证地图角色色写在 CSS 变量里，暗色主题覆写同一批变量。正文里不写死十六进制色值。

## 3. 五段式页面结构

页面自上而下固定五段。标题和小标题的写法见 SKILL.md 的 `<organizing_the_document>`。

**① 信息块 + 一句话 thesis**

```html
<h1>自拟标题：说出核心洞见</h1>
<div class="info"><span class="k">论文</span><b>原文标题（中文译题）</b><br>
<span class="k">作者</span>A. Author<br>
<span class="k">出处</span>Journal 2024 · <a href="#">链接</a><br>
<span class="k">类型</span>论证型<br>
<span class="k">核心洞见</span>一句话 thesis。</div>
<div class="note"><b>读法</b>先读论证地图把握骨架，再按论文自己的章节顺序精读。</div>
```

**② 论证地图**

```html
<h2>论证地图</h2>
<div class="am" id="am"></div>
<p class="tcap">一句话说明怎么读：主干是 thesis → views → conclusion，每个 view 展开它的支撑论证；objection 与 response 成对列出。</p>
```

AM 宿主只放一个 `<div class="am" id="am"></div>`，内容由 `#xray-am` 配置 + AM JS 生成，源文件里保持为空。

**③ 正文：严格按论文原章节顺序**

```html
<h2>论文章节一（Original Section One）</h2>
<div class="el">承载要素：View 1 · Argument A1</div>
<p>正文。</p>
<div class="arg"><div class="arg-label">论证 A1 · 【文中有据】p.4</div>
<ol><li>P1 前提一。</li><li>P2 前提二。</li></ol>
<div class="arg-conc">∴ C 结论。</div></div>
```

- 节标题用论文自己的标题：`论文章节一（Original Section One）`，不重命名。
- 每节开头放要素标记 `.el`：`承载要素：View 1 · Argument A1`、`承载要素：回应 Objection O1`、`承载要素：铺垫（无独立论证）`。
- 论证块 `.arg`：前提-结论链，自然语言，隐含前提补出并标注【推断，依据：……】；证据分级和页码写在 `.arg-label` 里。
- 要素缺失处正文写一句【隐含】说明，与地图一致。

**④ 概念对照表**

```html
<h2>概念对照表</h2>
<table class="t left">
<tr><th>英文</th><th>中文译法</th><th>首次出现</th><th>译法说明</th></tr>
<tr><td>epistemic injustice</td><td>认知非正义</td><td>§1</td><td>无争议</td></tr>
<tr><td>standpoint</td><td>立场 / 视角</td><td>§2</td><td>译法不一</td></tr>
</table>
```

**⑤ 写作启示**

```html
<h2>写作启示</h2>
<ol>
<li><b>技法名</b>：这篇论文怎么做（p.4）——你能怎么用。</li>
</ol>
```

## 4. 正文里的块

按需使用，不堆砌。正文是 HTML，加粗写 `<b>`，不要留下 Markdown 的 `**`，`XRAY.lint` 会报出来。

- **要素标记** `<div class="el">承载要素：…</div>`：每节开头，说明这一节在论证里承担什么。
- **论证块** `<div class="arg">`：前提-结论链。`.arg-label` 写论证名、证据分级、页码；`<ol>` 列前提；`.arg-conc` 写结论。
- **边注** `<span class="side">`：译法的另一种读法、一个反例、一个数字的来源。窄屏时自动变成段内小块。
- **Note / Warning**：`<div class="note">` 放容易忽略的提醒，`<div class="warn">` 放论文没说清的地方或陷阱。第一个 `<b>` 是两到四个字的标签。
- **表格** `<table class="t">`，数字列默认右对齐；以文字为主的表（观点谱系、概念对照）用 `<table class="t left">` 整表左对齐。表注 `<p class="tcap">`；需要强调的行加 `class="hl"`。
- **术语悬停**：关键概念首次出现用 `<span class="term" title="英文原文（译法说明）">中文译法</span>` 或直接写「英文（中文译法）」。没有现成组件时用边注。
- **公式**：人文论文通常不需要。偶尔出现用 KaTeX `$…$`，写法同 SKILL.md 的要求（不用形式逻辑符号呈现论证）。
- **论文原图**：需要时 `<figure class="pf"><img src="data:..."></figure>`，图下一两句话说该看哪里。哲学论证很少用图，论证树和概念关系图才是主要视觉。

不用**如果你真读懂了，应该能回答**这类自查块。

## 5. AM：论证地图

AM 组件由 `#xray-am` 配置驱动，页面作者只写配置，不碰渲染代码。

**配置 schema**：

```json
{
  "v": 1,
  "title": "论证地图",
  "trunk": ["T1", "V1", "V2", "C1"],
  "nodes": [
    {"id":"T1","kind":"thesis","label":"…","src":"text","page":"4","implicit":false,"sec":"sec-1","secLabel":"1"},
    {"id":"V1","kind":"view","label":"…","src":"text","sec":"sec-2","secLabel":"2"},
    {"id":"A1","kind":"argument","label":"…","premises":["P1 …","P2 …"],"conclusion":"C …","src":"text","grade":"文中有据","page":"6","sec":"sec-2"},
    {"id":"C1","kind":"conclusion","label":"…","src":"text","implicit":true},
    {"id":"O1","kind":"objection","label":"…","src":"text","response":"R1","page":"9"},
    {"id":"R1","kind":"response","label":"…","src":"reader","page":"-"}
  ],
  "edges": [
    {"from":"T1","to":"V1","rel":"support"},
    {"from":"V1","to":"A1","rel":"support"},
    {"from":"V1","to":"C1","rel":"leadto"}
  ]
}
```

**字段**：

- `kind`：`thesis | view | argument | conclusion | objection | response`。综述/考据模式可自定义（如 `framework`、`stance`、`viewpoint`），颜色回退到默认，`kindLabel` 可自定义显示名。
- `src`：`text`（文中明说）或 `reader`（读者补充）。objection 必填；其余节点有就填。
- `implicit`：要素缺失时 `true`，卡片虚线边框 + 【隐含】标签。
- `premises` / `conclusion`：argument 节点的前提-结论链，自然语言数组。view 即 argument 时直接写在 view 上。
- `sec`：正文对应节的元素 id（h2/h3 的 id，不填则不可跳转）；`secLabel` 显示用的节号；`page` 显示用的页码。
- `grade`：证据分级（【文中有据】【推断】【猜测】，考据型用【文中明说】【文本依据】【解释推断】），显示在卡片上。
- `response`：objection 节点指向它回应的 response 节点 id，侧栏里成对显示。
- `edges`：`support`（支撑：view→argument、thesis→view）与 `leadto`（导向：view→conclusion）。argument 归属用 `support` 边。
- `trunk`：主干节点 id 的有序数组，通常 thesis → views → conclusion。

**渲染行为**（AM JS 已实现，不用自己写）：

- 主干横向排布，节点间 `→` 连接；窄屏自动换行。
- 每个 view 节点下方是 `<details>` 展开器，列出它的支撑 argument 卡片（前提-结论完整显示）。
- objection 与 response 成对列在侧栏；objection 的 `response` 指向谁，就在谁下面显示「回应：…」。
- 点击节点跳到正文对应节（自动展开被折叠的节）。
- 每个节点右下角「不懂 / 已懂」按钮：点击写入节点级标注（存进 `xray-notes` 的 marks，带 `node` 字段），节点高亮；再点一次取消。
- 打开页面时已有的节点级标注自动恢复高亮。

**建模规则见 SKILL.md 的 `<argument_map>`**。核心几条：主干只放 thesis/views/conclusion；一个 view 可挂多个 argument；view 即 argument 时合并；要素缺失标【隐含】；读者补充的 objection 最多 2-3 条且来自审读弱点；STS 论文给 argument 标证据来源。

## 6. 交互

人文版只有一个核心交互：**论证地图**（展开/折叠、点击跳转、节点标记）。其余从简。

- 不要给论证加花哨动画。节点高亮、展开/折叠用 CSS transition。
- 每个交互组件对应正文里一个具体疑问：上方一句话说操作之后该看到的变化，下方一句话说明这个变化的含义（写在 `.tcap` 里）。
- 数字用 `tabular-nums`；构造的数字标注**示意**，论文里的页码注明出自第几页。

## 7. 标注层

reader-kit 自带标注层，读者不需要装任何东西。

- **开关**：✎ 打开后，选中文字会弹出小工具条，有**划线**、**笔记**、**反馈**三项；反馈再分**不懂**、**啰嗦**、**已懂**。关闭 ✎ 时，选中就是普通的选中。
- **笔记卡片**：显示在右侧边栏，用细线连回原文，窄屏时插在段落下面。
- **节点级标注**：论证地图节点右下角的「不懂 / 已懂」按钮，标注存进同一个 `xray-notes`，带 `node` 字段。
- **撤销**：右键划线或卡片，菜单里有撤销。
- **折叠**：每个 h2、h3 左侧有小三角，可以把整节收起，只留标题。
- **保存**：
  - 标注先自动存进浏览器本地。
  - ⤓ 把标注写回这个 HTML 文件本身，写在 `<script type="application/json" id="xray-notes">` 里。
  - Chrome 和 Edge 第一次选一次文件，之后自动写回；其他浏览器下载一份新文件替换原文件。
- **下一次运行时**：skill 会读这个块，评估读者的掌握情况（见 SKILL.md 的读者档案一节，节点级标注优先处理）。

作者不需要为标注层写任何代码，只要遵守第 1 节的三条约束。

## 8. 技术约束与自检

**约束**：

- 单文件，原生 JS 加少量 SVG，不引框架、不需要构建。唯一外部依赖是 CDN 的 KaTeX，离线时公式退化成源码，其余功能照常。
- 论文原图 base64 内嵌；合计超过约 20MB 时改用 `file:///` 绝对路径。

**交付前逐条过**：

1. 把所有内联 `<script>` 抽到临时文件跑 `node --check`（有 node 时），查完删掉。
2. 有 Chrome 或 Edge 时，跑 `chrome --headless=new --virtual-time-budget=8000 --dump-dom "file:///…/x.html?lint"`：
   - 读 `<pre id="xr-lint">`（XRAY.lint 检查标题问句、破折号、引号数量、空的 AM 宿主、残留的 Markdown 记号、`xray-notes` 元数据、`xray-am` 是否合法 JSON）和 `<pre id="am-lint">`（AM.lint 检查节点 id 重复、边指向未知节点、sec 目标缺失、argument 缺前提或缺结论、objection 缺 src）。
   - 两者都清零才交付。
3. 用 `--screenshot` 加 `?theme=dark` 和 `?theme=light`，各截一张 1440 宽和一张 560 宽，自己看一遍：论证地图主干是否排布正常、节点标签是否溢出、亮暗两套下可读。
4. 检查五段式齐全：信息块 + thesis、论证地图、按章节正文（每节有 `.el` 标记）、概念对照表、写作启示。
5. 目录贴最左缘，没有滚动条；亮暗两套下卡片、表格层次分明；刷新后主题保持，不闪白。
