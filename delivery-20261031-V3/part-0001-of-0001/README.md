# 五型号独立目录交付包

## 状态与使用边界

**打包校验通过不等于工程验收通过，不应直接上线或用于电路设计。**
本模式只装配指定验收根里已经生成的物料，不查数据库、不在打包时重渲染。
参数是否已按指定页缓存修订，以随包《交付说明.md》和 manifest 的 release_status 为准。
TXT内容原字节复制为HTML，symbols文件统一为.symbols.html。
《修复方案.md》是审计要求；它本身不是修复已经完成的证明。
原47/47或83/83报告不沿用，打包校验通过不代表工程参数、对象归属或本地化验收通过。

## 组织格式

```text
manifest.csv                    五型号总清单（UTF-8 BOM，Excel可打开）
manifest.json                   每件状态/缺项、物料来源与SHA-256
README.md                       本说明
修复方案.md                     已有复核方案
包校验报告.json                 ZIP路径/源哈希/CRC校验（仅打包层）
part-0001-of-0001.zip            五件一卷，内含五个型号独立目录
part-0001-of-0001/               与ZIP相同的解压检查目录
  <型号>/<型号>.json
  <型号>/<型号>.html
  <型号>/<型号>.symbols.html
```

分卷根同时带总清单、说明及已有修复方案。每型号的物料集中于其独立文件夹，
不再使用parsed/txt/symbols三个平行交付目录。原型号中斜杠仅在文件名中替换为下划线，
例如ADS1201U-1/1K对应ADS1201U-1_1K；JSON和总清单保留请求型号。

## 物料缺项与语言

本批实际存在的物料以manifest为准。未发现的.alts.json、.alts.html、.seo.json
不从全局旧目录补齐，不伪造替代料或图片SEO侧车。JSON内seo/alternatives不等于这些独立物料。
本次不含PDF原件，清单的PDF哈希仅保留源JSON已有记录，并非本包对PDF内容的重新核验。
源JSON可含multi_language内容，但是否已有独立ja/ko/de/es页面另列；目录名i18n是命名约定，
不是五语完整性声明。语言未检查状态为not_checked，缺少变体明确列为missing_html_languages。
三块板的.symbols.html是板卡说明页，不伪造芯片三视图；两颗芯片符号仍须核对原厂。
应用图是站点共享素材，本包不复制公共图片，也不把图片路径视为芯片参数证据。

## 页面片段与 SEO 侧车（交付契约）

本包的 HTML **是内容片段，不是整页**：每个 `.html` 以 `<div class="pd-wrap">` 开头，
**不含** `<html>` / `<head>` / `<title>` / `<meta>` / `<link rel="canonical">` / `hreflang`。
这是契约，不是缺漏——片段由独立站前端框架套壳时注入头部。

因此：

- 标题、meta description、keywords、多语标题在 `<型号>.seo.json` 的 `page` 节点；
- 多语叙述段在 `<型号>.ja.html` / `.ko.html` / `.de.html` / `.es.html` 片段内；
- 片段里的 `<h1>` 已使用 `seo.json` 对应语种的标题（注入管线只接到 h1，未接 head）；
- 复核时**请勿**把「片段没有 `<title>`」判为缺陷，应判「框架是否注入」；
- 若需求方要求整页交付，须先改本契约并同步渲染层，不能靠片段自带头部。

## 校验边界

包校验检查恰好五件、ZIP成员正斜杠无路径穿越、无重复成员、CRC正确、
源文件/独立目录/ZIP成员SHA-256相同，并保存最终ZIP的哈希。
校验报告存于ZIP外，以免报告引用最终ZIP哈希形成循环。
**哈希口径：sha256 按 CRLF→LF 归一化后计算**，与平台无关；报告 `hash_rule` 字段
显式记录该口径。若直接对原始字节算哈希，Windows 写出的 CRLF 与 git clone 得到的 LF
会得出不同值（实测同一文件 752afff8… 与 df10bcd6…），那不是数据被改，是换行符差异。
