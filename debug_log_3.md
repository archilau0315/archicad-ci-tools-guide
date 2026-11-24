# Debug Log 3

## 时间
2026-11-24

## 模块
source/fix_cross_refs.py（重写）、site/quantities.html、site/metadata.html

## 变更简述
修复 quantities.html 里大量裸文本章节引用（"见 2.3.8"、"see sections 3"、"4 至 4.4 节"）没有可点击跳转链接的问题。

### fix_cross_refs.py 完整重写，核心改动：
1. **非正文区域先 protect**：`<head>`、`<style>`、`<script>`、`<link>`、`<code>`、`<pre>` 替换为 `\x00H0\x00` / `\x00S0\x00` 等占位符，防止 CSS 数字、CDN 版本号被误伤
2. **分阶段累积保护链**：
   - 阶段 1A（复数/范围）→ protect → 阶段 1B（单数中文/section+小数）→ protect → 阶段 2（see/裸数）→ protect → 阶段 3（安全兜底+h3_ids 校验）
   - 每阶段用不同 prefix（`P10/P11/...`）避免 key 冲突
3. **h3_ids 安全校验兜底**：只有存在对应 h3 锚点的编号才替换，防止误伤 CSS/JS 中的浮点数字
4. **复数/范围正则升级**：允许中间夹 `<em>...</em>`、`(...)`、逗号等

### quantities.html / metadata.html：
- 所有裸文本章节引用 → `<a href="#s-X-Y" class="xref">编号</a>`
- 0 嵌套 `<a>`、0 裸引用、0 死锚点
- 297 个 xref 链接生效

## 部署方式（新发现）
- 服务器：阿里云 ECS `47.93.210.248`，宝塔面板
- SSH 登录：`root` / `100422lyf`（不是 Archilau-kbitai！）
- Web root：`/www/wwwroot/kbitai.com.cn/`
- 部署：paramiko SFTP 直接上传（服务器无 git clone）
- owner 修正：上传后需 `chown www:www`

## Bug 踩过的坑
1. **用户名错误**：用 `Archilau-kbitai` 登录被拒，正确用户是 `root`
2. **key 前缀冲突**：不同 protect 阶段必须用不同 prefix，否则后续 protect 覆盖前面的 key，还原时部分丢失
3. **CSS/CDN 误伤**：裸数字兜底 regex 会把 CSS 里的 `line-height:1.75`、CDN URL 里的版本号都变成 xref → 解决：先 protect 非正文区域
4. **嵌套 `<a>`**：4d (section+decimal) 匹配后，4g (section+plain) 的 `\b` word boundary 把 `.` 当边界，又在内部匹配了裸数字 → 解决：阶段 1A/1B 之间加 protect
5. **范围裸数字锚点错误**：`4 至 4.4` 里的裸 `4` 应该跳 `#s-4-1`，脚本生成了 `#s-4` → 修复：range 函数里加 `if "." in a` 判断
