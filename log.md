# Project Log

> Entries are dated (to the day); total <2.5k chars; consolidation requires user consent — in team mode the right belongs to the owner.
> Language switch 2026-10-06: new entries are written in English from this point on; historical Chinese entries below are preserved as-is (append-only, history untouched).

## Status (2026-10-06)

Positioning: **team project** (converted 2026-10-02; red lines & review-merge rules in AGENTS) — fix as used. Architecture end-state: the dual conceptual roots domain / wiki + domain instance families vault / lark / project / email / bili (query-and-answer + emergence archives) / cuhksz (bb·map·track·teach·quiz family + sis + registry) + calendar + cron + cross-cutting pieces & tmp — 35 plugins, no layering (topology + alphabetical; bridge law = principle 11); 13 commands (see README). Three projections, one source (mechanics master doc in the kernel reference skill). test-repo/ whitelist mirrors; connectors/ four (bb-cli / sis-cli / mail-cli / bili-cli). Docs language switched to English 2026-10-06 (full switch complete, PR #13 + #15).

## Stage

Framework build (done 09-08~12) → daily use & fix-as-used (**current**).

## Next steps

- teach/quiz first real-use round (scaling / scope / grading)
- AIE2040 re-basin + re-asking failed questions
- bb-cli user-info polish; email exploration; first cron task pages + harness replay field-test
- bili-cli logged-in field-test (personal data / write whitelist first round) and watch-list cold start
- i18n batches 2+: plugin disclosures (inject region rebuilds via kernel) → commands & connectors → docs & scripts
- Instance-library migration (user's live repo): wiki/bb/ → wiki/cuhksz/bb/, bb/ → cuhksz/bb/ + profile bridge rows update (awaiting owner's explicit repo location); sis-cli v0.3 agenda: tuition/cart component registration (raw probing), exam verification once published, registry PDF materialization first batch

## Past operations

- 2026-10-08 governance: PR #31 merged (post-#30/#25-interleave convergence — registry rebuilt + test-repo mirrors re-copied; manager delegated --admin, GitHub comment trail); merged branch deleted; #29 closed with landing summary; interim upstream-tracking directive broadcast on #24 / #20
- 2026-10-08 governance: PR #30 merged (cron v0.4 deferred-trigger generalization, issue #29; manager delegated --admin, GitHub comment trail); merged branch deleted
- 2026-10-08 plugin: cron v0.4 — schedule → trigger (time | condition, open kind vocabulary), executor names withdrawn from the inject line into replay recipes (owner ruling 2026-10-08: executor-agnostic recording & archiving), 2×2 matrix, per-form best-effort reconciliation (unreadable executor → info); language projections side-converged to manifest state (#26 content ruling pending)
- 2026-10-08 directive (interim): upstream-update tracking rides cron v0.4 task pages — instances declare template-repo watches (condition trigger where a conditional executor exists, else daily time trigger) until the #20 packaging lands; broadcast on issues #24 / #20 / #29
- 2026-10-07 topic: package-mechanism proposal filed as issue #20 (binding basis = family closure declared in PKG.yaml + kernel cross-check; directory-as-package core/ + domains/<pkg>/ with vault-trio exception; tap-style INDEX.yaml — no marketplace; flat package graph, compat ranges over framework VERSION+tag; three registration channels with the index PR as the human-review gate; two-round staging: binding round → split round via subtree under the owner's account); ruling recorded: cuhksz single package; execution pending team discussion
- 2026-10-06 governance: PR #19 merged (inject-line clip fix — quoted-span protection + stray-quote lint; manager delegated --admin, GitHub comment trail); merged branch deleted
- 2026-10-06 修复: inject-line clip bug (owner field report on the instance, issue #12) — kernel strip_comment fired inside quoted values, eating ` ## Section` tails (device/calendar/cron/user-profile, stray leading quote); quoted-span protection + stray-quote lint; four lines restored complete and tightened, tmp formatting back; region 15.2 K, blocks headroom 583 B
- 2026-10-06 governance: PR #18 merged (issue #12 tier migration — region 38K→14K, hard budget; manager delegated --admin, GitHub comment trail); merged branch deleted; #12 first-step family lands, packaging/repo-split stay deferred
- 2026-10-06 migration: issue #12 tier migration landed — 10 domain family members exit the injection region (bb five-piece, sis, registry, lark-docs/im/calendar; exposure via family rosters + skills + on-demand manifests), 13 core/root lines compressed to pointer density with rosters (region 38K→14K, 35→25 blocks), injection budget hard (over-budget = validate error); plugin versions bumped along changelogs
- 2026-10-06 governance: PR #17 merged (SASU-L layer discipline step 0 — contract + kernel mechanism, dormant-compatible; manager delegated --admin, GitHub comment trail); merged branch deleted; tier migration next
- 2026-10-06 protocol+kernel: SASU-L layer content & capacity discipline landed (issue #12 comments synthesis — A/S/L content contract, one home per fact, pointer-dense inject, exposure ladder for exited members; kernel inject_tier full|member + member-must-reach-family-root check + 15 KiB inject budget, warning until the tier migration lands); slimming round next
- 2026-10-06 governance: PR #15 merged (i18n batches 2-4, full English switch complete — 35 plugin disclosures + attached-audit scripts, 13 command skills, 4 connector docs & CLI messages, docs ×7, protocol artifacts, script comments; executed via 10 parallel subagents under a unified glossary + coordinator convergence; manager delegated --admin, GitHub comment trail); merged branch deleted
- 2026-10-06 governance: PR #13 merged (i18n batch 1/4 — charters to English; manager delegated --admin, GitHub comment trail); merged branch deleted
- 2026-10-06 topic：架构演进 issue #12 立档（单仓分层显性化→包格式+索引→subtree split 拆仓三步路线 + 第三方三通道与两安全面；方向共识未排期，痛点到达再走）
- 2026-10-06 治理：PR #11 审合入库（bili 0.3 + bili-cli 0.2.0，管理者代行 --admin，GitHub 评论留痕）；删已合分支
- 2026-10-06 域构：bili 0.3 视频入库批（用户四场景对照——看视频/评观点/管账号/追 UP）：改「视频不建页」为视频档案明示制涌现（video/ 两区制：摘要 ai 可覆写 + 评价 human 只增）；看视频降级链披露（实测：官方总结与 AI 字幕需登录 -101）；连接器 bili-cli 0.2.0（subtitle --ai / summary / fav move）
- 2026-10-06 治理：PR #10 审合入库（cron v0.1 + 三件挂桥，管理者代行 --admin，GitHub 评论留痕）；删已合分支
- 2026-10-06 插件：cron 时间自动化领地立设（用户三问收敛——统一登记处/对账+重放/每任务一页；声明为源执行侧为投影，session|script 两形态判据与失败纪律上提）——lark-calendar 0.2 / bili 0.2 / email 0.4 挂桥随迁，散落节奏披露归位；validate 35 全绿
- 2026-10-06 治理：PR #9 审合入库（bilibili 域 + bili-cli v0.1.0，管理者代行 --admin，GitHub 评论留痕）；删已合分支
- 2026-10-06 域构：bilibili 域立设（所有者问答收敛七项——功能三合一/web cookie/低危写白名单三项双层门/自研轻实现/先现拉后 cron/查询即答+涌现档案/连接器+域全套）——插件 bili v0.1（挂 todo/calendar/notes 三桥），连接器 bili-cli v0.1.0（WBI 签名+space 风控参数自研实测通，公开查询免登录、写命令 --yes 双门）；README/AGENTS 章程同步（三十四插件、connectors 四件，顺手修 bb/→cuhksz/ 陈旧引用）
- 2026-10-05 域构修：官方个人文件物化改域内（cuhksz/sis/ + 属地 docs/ 代理页，所有者裁定）——落地判据定为「域有自立容器则域内落地，vault 兜底无容器域」；cuhksz 0.2 / sis 0.2
- 2026-10-05 连接器：sis-cli v0.3（issue #6 实例首报三缺口）——ICAction POST 导航原语（submit_icaction + raw --post）、transcript 命令（SSS_TSRQST_UNOFF 真 身 + View Report → 官方 PDF 三语言）、identity 命令（prsnldata + PDF 双源 12 字段，覆盖 cuhksz 身份页全字段）、dpr 如实报告（Request Audit 待裁定）；issue 关闭留痕
- 2026-10-05 修复：域迁移批量替换的双重路径笔误（wiki/cuhksz/cuhksz/bb/——规则产物二次命中，残留检查排除项漏网）；实例侧首报；bb 0.9 / bb-map 0.15 / bb-track·teach·quiz 0.6 归一升版，全库复扫清零、validate 33 全绿
- 2026-10-05 域构：cuhksz 学校域立设（所有者裁定 bb 降为域内族）——基座（身份页+子系统导航）+ sis 学籍子域（速写页/查询即答/课表源补缺）+ registry 教务制度子域（物化+全校方案指针索引 schemes.md，42 专业页实测）；bb v0.8 挂靠迁路径（wiki/cuhksz/bb/、cuhksz/bb/），族内四件随迁升版；三十三插件 validate 全绿
- 2026-10-05 治理：PR #2/#3 审合入库（sis-cli v0.1/v0.2，管理者代行 --admin，GitHub 评论留痕）；同步远端 mail-cli 五提交（v0.1→包化）
- 2026-10-05 连接器：sis-cli v0.2——term 交互查询打通（radio 解析+POST Continue 纯查询）：grades 换真身 SSR_SSENRL_GRADE（学期成绩行+GPA）、appt 注册窗口、exam 登记（未发布为空）、history 全量直出、schedule --days 星期归属（center 页权威源）
- 2026-10-05 连接器：sis-cli v0.1 立设——SIS（PeopleSoft CS）只读 CLI：同源 ADFS OAuth2 复用、code 经 CUSZ_SSO_LOGIN 表单消费、PS_DEVICEFEATURES 破壳、psc+PTCNAV 组件直击；schedule 全解析（周事件+学期课程）、grades/center/history/appt 文本摘要、raw 透传；只读红线（选课类永不提供）；实证含组件 URL 双源（浏览器菜单+HTTP）
- 2026-10-04 部署收整：april-linux 实例库自 ~ 迁 ~/repo（库与上游原本分离——~/vault-wiki 为升级源，connectors 随迁）；家级 .agents 回归纯 lark skill，孤儿警告根治；dsh 升 0.2.0-rc.2 并修四插件适配
- 2026-10-04 部署：首座实例库落地 april-linux（家目录即库根）——机器清理三清单、clone 工程仓为升级源、三十插件收敛 verify 全绿、首批设备页两件（april-linux / windows-dev，互设 related）；device v0.2 增工具环境摘要节（在场级、多设备互查注册表、外壳以指针引页）先此入库
- 2026-10-04 插件：device v0.1 立设——设备档案复用 notes 领地（type: entity 建议、零 type 扩值），device 块映射最小键集（serial/purchased/warranty_until），附检临期扫描 30 天窗口、到期经确认受托入 todo；零命令零新领地
- 2026-10-04 插件：语言中性化清理批——tag v0.11（「中文为主」拆除，主语言跟 language 页 default 键）+ 八命令主本输出语言节统一改写（map/lark-map/profile/bb-map/bb-track/asset-read/query/save）；纪律级语言硬编码清零（余 AGENTS 准则 7 为开发期实例事实）；calendar 月页节名待裁
- 2026-10-04 插件：语言中性化批——language v0.2（缺席回落改跟会话语言，中文降为开发期实例事实；分层裁定：源对齐归域件、读者对齐归声明页键）+ bb-quiz v0.4（拆除「英文试题+中文解析」硬编码：题干源对齐、解析读者对齐 annotation 键）+ bb-teach v0.4（讲解语言取 teaching 键 + 术语锚点集优先全局表兜底）；国际生实例零改动可用
- 2026-10-04 插件：language v0.1 立设——行文声明页（language/terms 块映射 + 沉淀节两形分区），产出语言与行文基线、缺席容忍、默认基线非强制（域件特例优先）、术语涌现制；usage_routes 落 save（源侧路由首批应用）；test-repo 镜像重拷
- 2026-10-04 沙箱使用文档开卷 sandbox.md；沙箱重置并初始化外壳
- 2026-10-04 内核：cmd-inject 升源侧路由——manifest usage_routes 装即落投影、重复路由校验、披露序定序、ls 路由表；bb 族迁移（teach/quiz v0.3、track v0.4 命令瘦身）
- 2026-10-04 行文修订三批：docs 四件、README 与插件文档统一重写
- 2026-10-04 PLUGIN.md 二十八件分四批升格设计文档：设计概要节——为什么/族内位置/关键裁定与弃案/机制回指；六桥节按分工裁定降格；plugin 与内核参考 skill 形态规格对齐
- 2026-10-04 docs 补全：mechanics 机制详解（含域的生长节）与 usage 使用指南开卷，指针接线与陈旧修正，test-repo 镜像对齐
- 2026-10-04 docs 立卷：删 00/01/pointers，intro 导论与 quickstart v2 开卷，research×2 留，迁 .meta/docs，内核参考 skill v2 立机制总纲
- 2026-10-04 teach/quiz 改造（所有者裁定）：exams/ 废——素材归 bb notes/、提炼归 wiki（判分回流）；bb-exam 更名 bb-quiz；bb-track v0.3 + 命令；bb v0.7 共居
- 2026-10-04 治理：组员 CaoSuan-CODE 直推 master（署名冒用）——内容补审保留；test-repo 白名单追踪回正；master 开分支保护
- 2026-10-04 bb-teach/bb-exam 初版立设（组员）：teach 二维伸缩讲解 + 三层反馈；exam 范围出题 + 判分——后经所有者裁定改造（见上）
- 2026-10-02 全局域立宪三批（组会衍生）：准则 11 全局件/域件与桥；批一必依校验 + log 域标 + 基座补边；批二 todo/calendar/notes 派生归宿桥；批三认知桥 + bb-track 注册，mapping 边裁撤
- 2026-10-02 bb 认知线：bb v0.4 笔记区 + bb-track 立设（user.md 两区制、锚 sm-N）携 wiki v0.7、bb-map 0.12；挂缺：课表源与课后触发
- 2026-10-02 组会（第 3 周）：笔记裁定→bb-track 方向；产品线头脑风暴（teach/test 已立，addition_check/bridge 待议）
- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 + v0.11 分节登记裁定补录
- 2026-10-02 修订指引五批全清（C/D/F/todo/M）；bb v0.3（D1~D3）；实验收官：四课 94 页、八问全中
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队；Demo 历史清理（特批）；临时令×2（毕撤）；管理者委托代行；dev 审合（bb-map v0.9 + bb-cli 0.1.5）
- 2026-10-01 bb 域全套落地：bb v0.1→0.2（公告分拣、inbox、媒体分层）；bb-map v0.1→0.7（四桶、命令）；bb-cli v0.1.4、skill 移驻 connectors；AGENTS 准则 10 与 250 行；summary 并入
- 2026-09-14~30 扩域与连发（细则见 git 史）：structure/todo 立设、pointers 与市场调研；lark 族（基座+docs/im）、calendar/lark-calendar、project 容器外移、tmp、index 溢出减负、link 孤儿动态化；domain 0.1 契约与五域对齐、老八件补边；bb-cli v0.1→0.1.3（ADFS+REST 只读、dues 双源）与 email 域、profile 命令
- 2026-08-26~09-13 个人期奠基（细则见 git 史）：创始副本起建旋即重定位 vault-wiki → 原型落地（六插件四命令、registry/actions、装卸内核、trust）→ 定位重构（以用代验、SASU-L、零污染）→ 收束定形（user-profile、「开发框架非跑库」裁定、quickstart/三投影）

> 2026-10-04 多度整合（负责人同意）。
