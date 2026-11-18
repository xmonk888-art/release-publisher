# 发布助手 v1.2.0 · 按功能变化更新图文 / Change-aware release materials

2026-11-18

## 新增与调整

- 比较已发布基线与候选，根据用户可见影响判断更新范围，不只看版本号。
- 把重要变化映射到功能正文、使用入口、配图和证据；准确旧图复用，流程关系变化时重构相应图文。
- 中英文首页、详情说明、版本摘要、图文、ZIP 与 Release 同步；候选与公开下载明确区分。
- 保留 Skill、Windows 软件、真实截图/GIF、附件哈希和公开回验能力。
- 同步双语介绍和桌面/手机配图，加入项目管家 v1.3.0 的实际发布案例。

## 获取与使用

[下载 release-publisher-v1.2.0.zip](https://github.com/xmonk888-art/release-publisher/releases/download/v1.2.0/release-publisher-v1.2.0.zip) · [固定版本源码](https://github.com/xmonk888-art/release-publisher/tree/v1.2.0) · [v1.1.0 → v1.2.0 文件差异](https://github.com/xmonk888-art/release-publisher/compare/v1.1.0...v1.2.0)

解压顶层为 `release-publisher/`，中文 `README.md`、英文 `README.en.md`。Codex 安装器根目录参数：`--repo xmonk888-art/release-publisher --ref v1.2.0 --path . --name release-publisher`。已有版本先备份并保留自定义内容。调用 `$release-publisher` 后给出项目和本次范围；仅准备候选不会自动授权上传。

## 验证范围

本版已用于项目管家 v1.3.0 的图文准备和实际发布，提供有限的维护者记录摘要：[公开案例](https://github.com/xmonk888-art/release-publisher/blob/v1.2.0/cases/project-manager-1.3.0.md)。本次发行检查双语页面、桌面/手机配图、ZIP 解压与引用、运行文件一致性和公开下载哈希。手机采用浏览器视口模拟；其他电脑、其他客户端和桌面列表刷新/重启未经实际验证。不把历史软件案例当作新增规则的实测，也不宣称效率提升。

## English

Version 1.2.0 compares a published baseline with the candidate and maps user-visible changes to feature explanations, usage entries, visuals, and evidence. It reuses accurate graphics and rebuilds affected relationships when core flows change. Bilingual pages, latest summaries, installation links, ZIPs, and releases stay synchronized. Existing skill/software and public verification workflows are retained.

Download the standalone ZIP above. The skill lives at the repository root; the Codex installer arguments are shown above. Back up existing customizations and invoke `$release-publisher` with the project and scope. Candidate preparation alone does not authorize publishing.

The updated skill was used to prepare and publish Project Manager v1.3.0. The public case is a limited maintainer-reported summary, not an efficiency benchmark. This release checks bilingual pages, desktop/emulated-phone graphics, extracted ZIP resources/links, runtime consistency, and public-download hashes. Other computers/clients and desktop refresh/restart are untested. Historical software evidence retains its original attribution.
