#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble humanities-paper-xray structure demo from the kit blocks (block-faithful)."""
import re, pathlib

KIT = pathlib.Path("/Users/willowwang/Library/Application Support/DoubaoWork/Profile 3/.doubaowork/agent_mode/workspace/.user_skills/humanities-paper-xray/references/reader-kit.html")
OUT = pathlib.Path("/Users/willowwang/Library/Application Support/DoubaoWork/Profile 3/.doubaowork/agent_mode/workspace/.user_skills/humanities-paper-xray/demos/structure-demo/structure-demo.html")

kit = KIT.read_text(encoding="utf-8")
start_marker = "<!-- ===== XRAY BODY TOP END ===== -->"
end_marker = "<!-- ===== XRAY BODY BOTTOM START: copy whole block ===== -->"
head = kit.split(start_marker)[0] + start_marker
tail = end_marker + kit.split(end_marker)[1]

BODY = """<h1>结构演示：论证地图与按章节精读（示意内容）</h1>
<div class="info"><span class="k">论文</span><b>An Example Argument（示意论文，非真实文献）</b><br><span class="k">作者</span>A. Demo（示意）<br><span class="k">出处</span>示意 · 仅用于演示页面结构<br><span class="k">类型</span>论证型<br><span class="k">核心洞见</span>认知活动的社会性维度不可回避（示意）。</div>
<div class="note"><b>读法</b>这是 humanities-paper-xray 的结构演示：先读论证地图把握骨架，再按论文自己的章节顺序精读。地图节点可点击跳到正文，节点上的「不懂 / 已懂」可单独标记论证环节。</div>

<h2 id="sec-map">论证地图</h2>
<div class="am" id="am"></div>
<p class="tcap">主干是 thesis → views → conclusion。观点一和观点二各有一个支撑论证，展开即可看到前提-结论链；反对意见与回应成对列在下方。</p>

<h2 id="sec-1">引论：把主张摆出来（Why Bother）</h2>
<div class="el">承载要素：Thesis · 铺垫</div>
<p>示意正文：这一节把读者带到那个值得较真的主张面前。作者在这里做两件事：把要辩护的主张摆出来，并预告论证路线。</p>

<h2 id="sec-2">第一观点与论证（The First View and Its Argument）</h2>
<div class="el">承载要素：View 1 · Argument A1</div>
<p>示意正文：作者辩护第一个观点。前提一直接来自上一节的铺垫，前提二是本节引入的区分。</p>
<div class="arg"><div class="arg-label">论证 A1 · 【文中有据】p.4</div>
<ol><li>P1 前提一（示意）。</li><li>P2 前提二：概念区分（示意）。</li></ol>
<div class="arg-conc">∴ C 结论：观点一成立（示意）。</div></div>
<h3 id="sec-2a">一个反例的排除</h3>
<p>示意正文：作者处理一个看起来反驳观点一的例子。</p>

<h2 id="sec-3">第二观点与论证（The Second View）</h2>
<div class="el">承载要素：View 2 · Argument A2</div>
<p>示意正文：第二个观点从第一个延伸出来，共享同一个前提，但结论更强。</p>
<div class="arg"><div class="arg-label">论证 A2 · 【文中有据】p.7 · 隐含前提【推断】</div>
<ol><li>P1 沿用论证 A1 的结论（示意）。</li><li>P2 新引入的经验假设（示意）。</li></ol>
<div class="arg-conc">∴ C 结论：观点二成立（示意）。</div></div>

<h2 id="sec-4">反对意见与回应（Objections and Replies）</h2>
<div class="el">承载要素：Objection O1 · Response R1 · Objection O2 · Response R2</div>
<p>示意正文：作者主动处理一个反对意见，然后补充回应一个读者可能会提的异议。</p>

<h2 id="sec-5">结论（Conclusion）</h2>
<div class="el">承载要素：Conclusion C1</div>
<p>示意正文：回到 thesis，说明论证走到了哪里、还留下什么。</p>

<h2 id="sec-gloss">概念对照表</h2>
<table class="t left">
<tr><th>英文</th><th>中文译法</th><th>首次出现</th><th>译法说明</th></tr>
<tr><td>standpoint</td><td>立场 / 视角</td><td>§2</td><td>译法不一</td></tr>
<tr><td>structural harm</td><td>结构性伤害（试译）</td><td>§1</td><td>试译</td></tr>
</table>

<h2 id="sec-write">写作启示</h2>
<ol>
<li><b>用铺垫把读者带进主张</b>：作者在引论里先让读者需要这个主张（p.2）——写自己的论文时，先想读者为什么要在意你要辩护的东西。</li>
<li><b>论证共享前提以控制篇幅</b>：观点二的论证直接沿用观点一的结论（p.7）——多个观点共用一条论证链，比重复展开更紧凑。</li>
<li><b>主动处理最严重的反对意见</b>：作者把最强的那条反对意见放在正文而不是脚注（p.9）——选择回应什么，本身就是立场。</li>
</ol>
"""

NOTES = '{"v":1,"doc":{"title":"结构演示：论证地图与按章节精读（示意内容）","source":"An Example Argument（示意论文）","made":"2026-10-22","lang":"zh","file":"/Users/willowwang/Library/Application Support/DoubaoWork/Profile 3/.doubaowork/agent_mode/workspace/.user_skills/humanities-paper-xray/demos/structure-demo/structure-demo.html"},"marks":[],"folds":[],"updated":null,"saved":null}'

AMCFG = '{"v":1,"title":"论证地图","trunk":["T1","V1","V2","C1"],"nodes":[' \
'{"id":"T1","kind":"thesis","label":"认知活动的社会性维度不可回避","src":"text","page":"2","sec":"sec-1","secLabel":"1"},' \
'{"id":"V1","kind":"view","label":"观点一：社会性维度至少是必要的","src":"text","sec":"sec-2","secLabel":"2"},' \
'{"id":"A1","kind":"argument","label":"论证 A1：从铺垫到区分","premises":["P1 前提一（示意）","P2 概念区分（示意）"],"conclusion":"观点一成立（示意）","src":"text","grade":"文中有据","page":"4","sec":"sec-2"},' \
'{"id":"V2","kind":"view","label":"观点二：社会性维度还是构成性的","src":"text","sec":"sec-3","secLabel":"3"},' \
'{"id":"A2","kind":"argument","label":"论证 A2：从观点一到更强结论","premises":["P1 沿用论证 A1 的结论（示意）","P2 经验假设（示意）"],"conclusion":"观点二成立（示意）","src":"text","grade":"推断","page":"7","sec":"sec-3"},' \
'{"id":"C1","kind":"conclusion","label":"结论：回到 thesis，论证成立","src":"text","sec":"sec-5","secLabel":"5"},' \
'{"id":"O1","kind":"objection","label":"反对意见：区分不成立","src":"text","response":"R1","page":"9","sec":"sec-4"},' \
'{"id":"R1","kind":"response","label":"区分经反例检验后仍成立","src":"text","sec":"sec-4"},' \
'{"id":"O2","kind":"objection","label":"读者补充：经验假设未证","src":"reader","response":"R2","sec":"sec-4"},' \
'{"id":"R2","kind":"response","label":"可进一步检验（读者视角）","src":"reader","sec":"sec-4"}],' \
'"edges":[{"from":"T1","to":"V1","rel":"support"},{"from":"T1","to":"V2","rel":"support"},{"from":"V1","to":"A1","rel":"support"},{"from":"V2","to":"A2","rel":"support"},{"from":"V1","to":"C1","rel":"leadto"},{"from":"V2","to":"C1","rel":"leadto"}]}'

def fill(html, sid, content):
    return re.sub(r'(<script type="application/json" id="' + sid + r'">)[\s\S]*?(</script>)',
                  lambda m: m.group(1) + content + m.group(2), html, count=1)

html = head + "\n" + BODY + "\n" + tail
html = fill(html, "xray-notes", NOTES)
html = fill(html, "xray-am", AMCFG)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print("written", OUT, len(html), "chars")
