1、任务：把一张ARPER椅子的图片从eagle 同步到obsidian笔记中

2、逻辑拆解：

&#x09;1、第一步（GET)：从Eagle api获取图片地址和标签

&#x09;2、第二步（JSON): 把这些信息打包成JSON格式

&#x09;3、第三步（POST):通过obsidian API把内容写进指定的.MD文件



graph LR

&#x20;   A\[Eagle素材库] -- Webhook:发现新图 --> B(AI Agent)

&#x20;   B -- GET:获取大图 --> A

&#x20;   B -- AI分析:提取材质颜色 --> B

&#x20;   B -- POST:创建研究报告 --> C\[Obsidian知识库]



