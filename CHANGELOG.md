# 变更记录

每次改动按日期追加记录，包含改动目的、涉及文件、测试与验证结果、影响或已知限制。

## 2026-10-14：重构效果页面整体布局为边狱终端科技风并明确标注原作者与优化人

### 改动

- 响应用户关于“主要是布局不是很喜欢、页面重构要彻底、界面标明原作者后面写明优化人”的明确要求，进行深度布局重构与致谢信息强化：
  1. **界面标明原作者与优化人 (`app_info.py`, `controls.py`)**：
     - 在 `app_info.py` 中新增 `OPTIMIZER = "优化：css521 (优胜)"`，并严格保留原作者 `CREATOR = "创作者：Bilibili-鈴仙優昙華院因幡"`；
     - 在控制面板侧边栏（`_build_sidebar`）中，于原作者与版本号之间醒目新增优化人标注：`优化：css521 (优胜)`，保证原作者致谢与优化人贡献清晰并存，且 100% 满足自动化测试对品牌标识与几何间距的断言。
  2. **歌词效果页面布局彻底重构 (`controls.py`)**：
     - 彻底改变此前将字体预览框（`FontPreview`）突兀夹在杂乱表单中下部的割裂设计，重构为层次分明的“边狱公司终端科技风（方案 A）”三大核心模块：
       - **模块 1：效果舞台与预设方案 (`stage_card`)**：
         - 整合为顶部“实时预览核心工作台”，上部紧凑排布预设方案下拉框与操作按键（另存为、更新、删除），配以轻量预设只读/修改状态说明；
         - 将明暗预览背景切换与动画重播按键整合至舞台工具条；居中展示开阔的全画幅歌词动画实时预览舞台（`FontPreview`），并针对特殊主题引入四角战术科技十字刻度（tactical reticle HUD）；
       - **模块 2：显示与文字外观 (`text_card`)**：
         - 结构化整合显示屏幕、显示区域、歌词字体与导入、字号、纯色/白芯发光、白芯风格（标准/卡门）、颜色选择器、发光强度滑块、透明度、翻译偏好与但丁 PDA 终端通知；
       - **模块 3：律动与动画动力学 (`motion_card`)**：
         - 归集歌词动画预设（脑叶危险等级/E.G.O侵蚀/金枝绽放等）、入场/退场速度滑块、抖动频率、跌落距离、逐字演唱强调开关与状态、运动方式、振幅、倾角与时钟偏移。
     - 优化滚动与窗口尺寸适应性，确保在 900×560 最小窗口下全部控件均 100% 可通过滚动无截断访问（`effects_scroll.ensureVisible`）。

### 测试与验证

- 自动化单元与文档测试：
  - 运行 `.venv/bin/python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_glyph_motion.py tests/test_text_effects.py tests/test_presets.py -v`：共 80 项自动测试全部通过（OK，skipped=1）；
- 集成验证与烟雾检查：
  - 运行 `.venv/bin/python main.py --smoke`：全部烟雾测试与视觉回归检查通过（`passed: true`，所有 11 种动画暖帧渲染 P95 均优于要求，`effect_controls_reachable_by_scrolling: true`，`unreachable_effect_controls: []`，`sidebar_branding_updated: true`，`both_theme_sidebars_fit_minimum_window: true`）；
- 构建打包与提取：
  - 运行 `.venv/bin/python tools/build_macos.py` 重新生成构建包；
  - 执行 `ditto -x -k artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip build/macos-dist` 将独立可执行 app 同步至 `build/macos-dist/`。

### 影响与限制

- 彻底解决了效果设置页面过长、预览与参数断层、表单杂乱的问题；
- 界面视觉焦点集中在顶部实时舞台，调参动线流畅，边狱公司终端风格与黑金科技感高度契合。

## 2026-10-14：重构控制面板 UI 界面视觉设计与版面层次

### 改动

- 响应用户关于“app 页面太丑”的反馈，对控制面板（`controls.py`）及主题样式（`themes.py`）进行系统级视觉重构与现代化打磨：
  1. **样式与控件现代美化 (`themes.py`)**：
     - 重构全局 QSS 样式表：优化表单输入框、下拉框（QComboBox）与微调框（QSpinBox）的内边距（padding: 8px 12px）与圆角（8px），消除复古机械感；
     - 升级复选框（QCheckBox）：尺寸提升至 16×16px，采用 4px 微圆角，悬停提供高亮边框反馈；
     - 优化滑块（QSlider）：轨道高度提升至 5px，滑块手柄增大至 14px，交互热区与视觉辨识度大幅提升；
     - 滚动条极简轻量化：宽度缩窄至 7px 细条微圆角样式，淡入深色背景，消除传统粗宽黄色滑块的违和感。
  2. **特殊主题（月亮门世界观皮肤）高级化与去土气**：
     - 色盘调优：底色调整为深邃玄黑（`#0e0c0a`），表面调整为质感黑曜石微暖调（`#1a1511`），边框使用典雅哑光古金（`#4a3c2a`），消除了此前浑浊偏黄的高饱和度土黄感；
     - 边框装饰重绘：重构 `ThemeFrame.paintEvent`，移除生硬刺眼的内部黄色嵌套方框与双重线，改为高精度抗锯齿单道切角科技感细线（`#7d6542`）与顶部极细金光微高亮（`#e8c076`）；
     - 按钮与导航状态：导航激活态增加深色温润渐变与柔和金色描边，悬停质感细腻。
  3. **布局呼吸感与侧边栏比例优化 (`controls.py`)**：
     - 侧边栏宽度从 200px 适度扩展至 220px，增加内边距与垂直间距，标题与副标题层级更加舒展；
     - 底部播放控制条边距扩展至 28px，间距增至 24px，黑胶唱片缩略图微调至 52×52px，让曲名、播放按键与音量滑块拥有充裕的呼吸空间；
     - 效果预览卡片（`FontPreview`）样式感知当前界面主题，根据亮色、暗色、特殊主题自适应边框与深浅底色，彻底消除浅色突兀断层。

### 测试与验证

- 自动化测试校验：
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_glyph_motion.py tests/test_text_effects.py tests/test_presets.py -v`：共 80 项自动测试 100% 全部通过；
  - 运行 `python main.py --smoke`：集成烟雾测试全部指标通过（`passed: true`），11 种风格渲染暖帧 P95（3.7ms ~ 19.1ms）均大幅优于 33ms 限制，暂停完全冻结。
- 打包交付：
  - 运行 `tools/build_macos.py` 重新编译打包生成 `city-echoes-0.6.0-beta.2-macos.1-arm64.zip`；
  - 使用 `ditto -x -k` 完整解压同步至 `build/macos-dist/` 目录，供直接运行验证。

### 影响与限制

- 控制面板在保持原有全部设置持久化、音频交互及快捷键功能 100% 兼容的同时，视觉质感与现代感显著提升；
- 特殊主题更加凸显深邃内敛的世界观高级感，不再有杂乱亮黄边框干扰。

## 2026-10-14：重构并大幅强化 E.G.O 侵蚀与金枝绽放动画动力学与视觉表现力

### 改动

- 响应视觉反馈，针对此前常态（steady-state）时间内色散趋近于零、位移缺乏专属物理特征的问题进行深度重构，使两种边狱公司／月亮门世界观特效在整句显示的常态、旋律高潮、入场与退场阶段呈现出极具视觉冲击力与辨识度的世界观质感：
  1. **E.G.O 侵蚀 (E.G.O Corrosion)**：
     - **常态黏滞下渗流淌**：重构波形为非对称重力拉扯（`drip_mult = 1.7 if wave > 0 else 0.7`），字形如粘液拖拽般持续向下流淌；叠加常态下垂（`droop`）与流体水平蠕动震颤（`tremor`，14Hz 阶梯时钟）；
     - **常态深渊·暴戾色散脉冲**：常驻深红色散脉冲（2.2px ~ 5.0px），随旋律能量与节奏呼吸抽搐；
     - **2D 异向色散图层渲染**：`text_effects.py` 扩展支持 `(dx, dy)` 二维位移，深渊漆黑层向左下流淌偏移（`dx=-split*0.8, dy=split*0.7`），暴戾深红向右上撕裂偏移（`dx=split, dy=-split*0.4`），图层不透明度提升至 0.85，立体下渗感极其鲜明；
     - **沉沦消解退场**：退场时受 `fall_distance` 驱动加速下坠跌落（`leaving ** 1.5`），伴随强烈的水平撕裂错位与倾角偏转。
  2. **金枝绽放 (Golden Bough Bloom)**：
     - **反重力轻盈浮升 (Levitation)**：全句文字优雅悬浮于基线之上（`float_dy = -3.5 - 2.5 * sin(...)`，整体向上抬升 1.0px ~ 6.0px），摆脱地面重力约束；
     - **金枝花蕾呼吸缩放 (Breathing Scale)**：字符伴随旋律起伏自然舒展与膨胀（`breathe_scale` 1.01 ~ 1.13），呈现如金枝共鸣开花般的光华律动；
     - **常态耀日金环交叉色散**：常驻暖日耀金与温润琥珀色散（2.2px ~ 4.7px），在 `text_effects.py` 中以十字交叉光晕（`dx=-split*0.8, dy=-split*0.5` 与 `dx=split*0.8, dy=split*0.5`）向外放射，金色光晕璀璨耀眼；
     - **升华消散退场**：退场时优雅向高空升华（`leave_dy = -leaving * 16.0`），字号膨胀化为光之粒子消散。
  3. **严格基线与包围盒契约**：
     - 当用户将跳动幅度设为 0（`jump = 0`）时，`jump_ratio = 0`，所有额外位移、缩放与色散完全归零，100% 维持像素级静态基线对齐与字号规范；
     - 精确微调 `motion_bounds`，在全倾角、高 DPR 与极端字符排版下均保证布局包围盒与屏幕边缘绝对无缝贴合、无截断。

### 测试与验证

- 自动化单元测试：
  - 运行 `python -m unittest tests/test_glyph_motion.py tests/test_text_effects.py tests/test_singing_sync.py tests/test_presets.py tests/test_core.py tests/test_workflow_docs.py -v`：全部 106 项测试 100% 通过（OK，skipped=1）；
  - 在 `tests/test_glyph_motion.py` 中新增常态色散下限（`split >= 1.5`）、金枝反重力浮升（`y < 0`）、呼吸膨胀（`scale > 1.02`）、侵蚀流体震颤与零跳幅绝对基线契约校验；
  - 在 `tests/test_text_effects.py` 中验证二维异向色散渲染与高透明度分色图层绘制。
- 完整烟雾测试与性能基准：
  - 运行 `python main.py --smoke`：全部指标通过（`passed: true`）：
    - 11 种动画风格在 3024×1898 物理画布、DPR 2.0、51 字符双句下的暖帧 P95 渲染耗时均在 3.2ms ~ 18.0ms 之间，远优于 33ms 限制（`corrosion_wave`: 10.45ms, `corrosion_shake`: 8.43ms, `bloom_wave`: 11.98ms, `bloom_shake`: 15.02ms）；
    - 暂停状态完全冻结（`singing_freezes_on_paused_song_clock: true`, `animation_parameters_preserve_paused_clock: true`）。
- 打包交付：
  - 运行 `tools/build_macos.py` 重新生成 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`；
  - 解压最新产物完整同步覆盖至 `build/macos-dist/`，包含 `都市回响.app`、`CityEchoes`、`安装播放读取工具.command` 及完整证书与说明文档。

### 影响与限制

- 侵蚀与绽放现在无论在整句播放常态还是高潮段，均呈现出极为鲜明、对比强烈的世界观物理动态与分色光晕；
- `jump = 0` 仍完全保留纯文字平静基线模式，满足静止展示需求。

## 2026-10-14：新增 E.G.O 侵蚀／金枝绽放歌词特效、脑叶公司危险等级预设及但丁 PDA 风格切歌浮窗

### 改动

- 新增边狱公司世界观专属歌词动画风格：**E.G.O 侵蚀 (E.G.O Corrosion)** 与 **金枝绽放 (Golden Bough Bloom)**：
  1. 风格注册：在 `settings.py` 中注册 `corrosion_wave`（侵蚀·波动）、`corrosion_shake`（侵蚀·抖动）、`bloom_wave`（绽放·波动）、`bloom_shake`（绽放·抖动），支持设置持久化保存与无效值安全回退。动画风格总数扩充至 11 种。
  2. 字符运动与色散：
     - **E.G.O 侵蚀**：入场伴随精神下沉流动，退场呈现下渗流淌（受 `fall_distance` 驱动）与流体错位；在材质预备阶段预乘深渊漆黑（`#140a0f`）与暴戾深红（`#dc1e2d`）鬼影图层，在动态脉冲下产生强烈的失真与侵蚀色散。
     - **金枝绽放**：入场温润自下微升展开（`enter_scale` 0.88 -> 1.0），退场升华微升（`leave_dy` < 0），光晕如金枝共振膨胀；材质预备暖日耀金（`#ffd700`）与温润琥珀（`#ff9b0a`）预乘图层。
  3. 极限包围盒更新：在 `glyph_motion.py` 中为侵蚀下沉与金枝膨胀预留充足 bounds，保证在任意倾角与 DPR 下均无像素截断。
- 新增脑叶公司危险等级（ZAYIN ~ ALEPH）全套内置预设 (`presets.py`)：
  1. `ZAYIN · 绿意安定`：安定翠绿描边（`#27e8a7`）、轻快波浪、适中光晕；
  2. `TETH · 冷青戒备`：警惕冷青描边（`#38bdf8`）、高频颤动、戒备光晕；
  3. `HE · 金枝自制`：金枝绽放动画（`bloom_wave`）、耀日金描边（`#facc15`）、逐字演唱同步；
  4. `WAW · 沉沦暗渊`：E.G.O 侵蚀抖动动画（`corrosion_shake`）、沉沦暗紫描边（`#c084fc`）、深渊下渗；
  5. `ALEPH · 拟态灾厄`：异想体扭曲撕裂动画（`glitch_shake`）、灾厄血红描边（`#ef4444`）、高频脉冲震颤；
  6. `卡门之声 · 阳光与血`：卡门阳光暖白字芯与琥珀金光晕（`#f2b772`）、猩红血色色散。
  7. `EFFECT_KEYS` 排除 `pda_banner`，使预设切换不覆盖用户的全局切歌通知开关。
- 新增**但丁 PDA 风格切歌浮窗** (Dante's PDA / LCB Banner Pill)：
  1. 悬浮通知：在 `overlay.py` 中实现但丁 PDA 终端通知横幅，检测到切歌或曲目切换时平滑滑入，展示曲目名称、艺术家、终端元数据（`LCB // DANTE PDA · NOW PLAYING`）及金色共鸣细线。
  2. 但丁时钟头矢量渲染：通过 `QSvgRenderer` 渲染高质量但丁燃烧时钟头图标（`assets/dante-clock.svg`），在异常环境优雅回退至罗马刻度盘。
  3. 零句柄与完全穿透：直接在 `LyricsOverlay.paintEvent` 顶层绘制，无需创建独立操作系统窗口，天然享有 `WA_TransparentForMouseEvents`（完全点击穿透，不阻断鼠标）与 `WA_ShowWithoutActivating`（绝不抢占前台焦点）。
  4. 播放联动与绝对冻结：切歌浮窗在音频活跃播放期间保持 33ms 动画刷新，展示 4.0 秒后平滑滑出退场；音频暂停时严格停止计时器并冻结画面，完全不产生额外 CPU 占用或状态偏差。
- 控制面板联动与设置持久化 (`controls.py`)：
  1. 在“显示与文字”设置分组中新增“切歌时显示但丁 PDA 终端通知”复选框（`pda_checkbox`），绑定 `prefs.pda_banner` 并支持持久化；
  2. 动画控制项联动：选择 `corrosion_*` 风格时自动启用“跌落距离（流淌下渗）”滑块，选择 `*_shake` 时启用抖动频率调节。

### 测试与验证

- 自动化单元测试：
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_macos.py tests/test_glyph_motion.py tests/test_text_effects.py tests/test_singing_sync.py tests/test_effect_parameters.py tests/test_presets.py -v`：共 137 项核心与集成测试全部通过（OK，skipped=1）。
  - 在 `tests/test_presets.py` 中测试全部 8 款内置预设（安静办公、轻快律动、ZAYIN ~ ALEPH 及卡门之声）的名称、色值与动画绑定，并验证 `pda_banner` 排除规则；
  - 在 `tests/test_controls.py` 中测试 11 项完整动画选择，并新增 `test_pda_banner_toggle_and_overlay_activation` 验证复选框切换与持久化；
  - 在 `tests/test_glyph_motion.py` 中新增 `test_corrosion_and_bloom_motion_and_split` 验证侵蚀与金枝动画的确定性、色散脉冲与平滑缩放；
  - 在 `tests/test_text_effects.py` 中新增 `test_corrosion_and_bloom_chromatic_split_rendering` 验证侵蚀漆黑/暴戾深红与金枝耀金/琥珀的分色图层渲染；
  - 在 `tests/test_macos.py` 中新增 `test_dante_pda_banner_triggers_on_track_change_and_renders` 验证切歌时浮窗激活、标题艺术家提取与 QPainter 绘制无异常。
- 完整烟雾测试与性能基准：
  - 运行 `python main.py --smoke`：全部指标通过（`passed: true`）：
    - 11 种动画风格在 3024×1898 物理画布、DPR 2.0、51 字符双句下的暖帧 P95 渲染耗时均在 3.3ms ~ 10.9ms 之间，远优于 33ms 限制（`corrosion_wave`: 4.88ms, `corrosion_shake`: 6.83ms, `bloom_wave`: 3.93ms, `bloom_shake`: 3.77ms）；
    - 暂停状态完全冻结（`all_animations_freeze_while_paused: true`, `pause_freezes_frame: true`）；
    - 缓存与显存占用均严格控制在限额内。

### 影响与限制

- 动画列表现已提供 11 种风格，全面覆盖经典整句、波纹、跌落、扭曲、侵蚀与金枝绽放；
- 脑叶危险等级预设可一键切换月亮门世界观氛围（从安定翠绿到拟态灾厄）；
- 但丁 PDA 切歌浮窗在播放切歌时自动升起 4 秒，提供沉浸式终端体验，且不影响任何点击操作。

## 2026-10-14：新增边狱公司／月亮门世界观专属风格“扭曲·故障频闪 (Distortion / Glitch)”歌词动画特效

### 改动

- 新增边狱公司／月亮门世界观“扭曲·故障频闪 (Distortion / Glitch)”动画风格：
  1. 风格注册：在 `settings.py` 的 `ANIMATION_STYLES` 中新增 `"glitch_wave": "扭曲·波动"` 与 `"glitch_shake": "扭曲·抖动"`，配置支持持久化存储与无效值安全回退。
  2. 纯函数阶梯时钟与断裂错位：在 `glyph_motion.py` 中扩展 `GlyphState` 增加 `split`（色散偏移量）。在入场（`stagger` entering）和退场（`stagger` leaving）时引入高频阶梯时间时钟，产生水平切片断裂错位（`glitch_dx`）与轻微旋转撕裂；在平稳播放时，以确定性伪随机检测由稳定种子和音乐能量共同激发的故障脉冲窗口，在窗口内产生单字微错位与频闪抖动。当用户设置 `jump = 0` 时，严格归零所有偏移，保证静止基线对齐。
  3. RGB 色散分色（Chromatic Aberration）：在 `text_effects.py` 中扩展 `_materials`，为每个字形在冷准备阶段预生成预乘 RGBA 的色散鬼影图像（标准发光下对应异想体共振青色 `#00e6ff` 与深赤色 `#f5324b`；卡门发光下对应琥珀金色 `#ffb93c` 与猩红血色 `#eb2d3c`）。在 `_render_states` 渲染时，当 `state.split > 0` 时分别向左偏移绘制青色/金色层、向右偏移绘制赤色层，中心保留清晰锐利的字身白芯与描边。
  4. 极限包围盒与零动态开销：更新 `glyph_motion.py` 中的 `motion_bounds`，为故障撕裂与色散预留充足的包围盒边距，确保在不同分屏比例（DPR 1.0、1.25、1.5、2.0）及倾斜排版下文字边框像素完全为 0 不发生裁剪截断；色散图层完全复用预计算材质，暖帧渲染 P95 维持在 12~16ms，远低于 33ms 限制。
  5. 控制面板联动：在 `controls.py` 中，动画下拉框自动呈现 7 项完整动画模式；选择“扭曲·抖动”时启用抖动频率调节，“扭曲·波动”时自动禁用频率与跌落距离，与现有参数逻辑完美协同。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_glyph_motion.py` 中新增 `test_glitch_deterministic_jitter_chromatic_split_and_jump_scaling`，验证故障位移与色散确定性、复现性、种子差异性及零 jump 下的基线保持；并验证 `test_all_modes_custom_font_extreme_layout_and_dpr_have_clear_edges`（6 种逐字模式全量通过）与 `test_overlay_pause_seek_and_setting_change_preserve_transport`（暂停完全冻结，跳转重现一致）；
  - 在 `tests/test_text_effects.py` 中新增 `test_glitch_chromatic_split_renders_offset_colored_fringes_and_leaves_core_intact`，验证左右青/红色散边缘及白芯完整性；
  - 在 `tests/test_controls.py` 中更新动画选项总数断言（由 5 项提升为 7 项），并新增 `glitch_shake` 与 `glitch_wave` 控件启用/禁用联动测试；
  - 在 `tests/test_effect_parameters.py` 中将两种扭曲风格纳入入场/退场速率缩放测试；
  - 在 `tests/test_presets.py` 中完善跨平台预设字体断言。
- 完整测试套件与性能基准：
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_macos.py tests/test_glyph_motion.py tests/test_text_effects.py tests/test_singing_sync.py tests/test_effect_parameters.py tests/test_presets.py tests/test_qqmusic.py -v`：全部通过。
  - 运行 `python main.py --smoke`：全量烟雾测试与性能基准通过（`passed: true`）：
    - `glitch_wave`：暖帧 P95 为 16.134ms（带逐字演唱为 15.894ms）；
    - `glitch_shake`：暖帧 P95 为 12.257ms（带逐字演唱为 12.905ms）；
    - 全部低于 33ms 阈值，缓存占用在 64MiB 范围内，暂停完全冻结。

### 影响与限制

- 动画列表现已提供 7 种风格：原有效果 · 整句渐隐、波纹·波动、波纹·抖动、跌落·波动、跌落·抖动、扭曲·波动、扭曲·抖动；
- 扭曲风格完美呈现 Project Moon / 边狱公司独有的现实失真、频闪撕裂与异想体 RGB 色散美学；
- 保持 100% 纯函数与无状态性，暂停时无任何动态游走，跳转进度条完美复现。

## 2026-10-14：修复按钮点击高亮圆框问题与 QQ 音乐暂停 6 秒延迟问题

### 改动

- 修复按钮点击后显示高亮圆框问题（按钮聚焦边框）：
  1. 根因剖析：在 `themes.py` 中，全局样式配置了 `QPushButton:focus { border: 1px solid #ff3656; }`（在特化主题下被映射为 `#ffb526` 金色/橘色）。用户点击“重播动画”等操作按钮后，按钮获得键盘焦点，导致控件外围被绘制上一圈醒目的聚焦矩形圆角边框（即“圆框”）。
  2. 修复方案：
     - 在 `themes.py` 中将 `QPushButton:focus` 改为 `outline: none;`，移除聚焦时边框颜色替换逻辑，并在特化主题追加配置中同样确保 `outline: none;`；
     - 在 `controls.py` 中为重播动画、导入字体、描边颜色、预设更新与删除、隐藏歌词等操作按钮统一设置 `setFocusPolicy(Qt.FocusPolicy.NoFocus)`，鼠标点击后不驻留焦点，消除聚焦圆框。
- 修复 QQ 音乐暂停时延迟 6 秒才停止问题：
  1. 根因剖析：QQ 音乐 Mac 客户端在暂停时未将系统的 `kMRMediaRemoteNowPlayingInfoPlaybackRate` 置为 0（保持 1.0），且其 CoreAudio 音频输出单元在进入暂停后会维持 5~6 秒的静音活跃状态才彻底关闭。都市回响由于完全依赖系统 Rate 与 CoreAudio 输出检测，导致在用户按下暂停后依然推移 6 秒（如用户在 00:33 暂停，都市回响推移至 00:39 才停止）。
  2. 修复方案：在 `macos_netease.py` 中新增 `get_mac_qqmusic_playback_state`，直接通过 macOS 系统菜单事件查询 QQ 音乐的“播放控制”菜单项（“暂停”代表当前正在播放，“播放”代表当前已暂停）。在后台轮询中即时识别暂停状态并同步修正 `state` 与 `rate`，暂停在毫秒级立即响应并冻结进度，彻底解决 6 秒延迟。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_core.py` 中新增 `test_theme_stylesheets_do_not_add_border_to_focused_pushbuttons`，覆盖浅色、深色与特化主题下按钮聚焦无边框规则；
  - 在 `tests/test_macos.py` 中新增 `test_qqmusic_playback_state_from_menu_overrides_rate_one_on_pause`，验证暂停时菜单状态即时将 state 置为 paused 并将 rate 修正为 0.0，消除 6 秒延迟；
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_macos.py tests/test_qqmusic.py tests/test_qqmusic_cache.py tests/test_mac_distribution.py -v`：154 项测试全部通过（OK，skipped=1）。
- 实际界面与系统调用实测：
  - 按钮聚焦：点击“重播动画”按钮抓取像素，原 1396 个高亮橙色像素完全降为 0，不再出现聚焦边框；
  - QQ 音乐菜单状态：实测 `get_mac_qqmusic_playback_state()` 在播放时准确返回 `True`，在暂停时即时返回 `False`，响应时间约 0.2 秒。

### 影响与限制

- 按钮点击后不再显示聚焦外框，视觉风格整洁统一；
- QQ 音乐暂停与播放切换实时响应，不再滞后 6 秒；
- 若环境未授予系统辅助权限，平滑回退至既有 CoreAudio 检测。

## 2026-10-14：彻底修复播放卡住冻结问题与歌手别名含符号匹配失败导致无歌词问题

### 改动

- 修复连续播放中歌词突然停滞卡死问题（如播放 Mili《TIAN TIAN》在 01:16 停滞）：
  1. 根因剖析：先前的停滞检测逻辑假设播放器采样位置（`info.position_ms`）会实时推移。但实机排查与系统采样证实，QQ 音乐 macOS 客户端在连续播放时上报的 `ElapsedTime` 保持完全静态，整个播放过程完全依赖播放器的本地虚拟时钟平滑累加。先前的判定逻辑导致任何单曲在正常播放 1.8 秒后都会触发 `(now - self._last_pos_advanced_at) >= 1.8`，从而将正常播放误判为暂停，造成歌词在特定时间点（如 01:16）被永久冻结。
  2. 修复方案：在 `macos_netease.py` 中彻底移除错误的采样位置停滞检测代码，恢复依据 CoreAudio 音频设备输出状态与 PlaybackRate/状态标签的精确播放判定。播放中本地虚拟时钟平滑推移无任何阻断，在暂停时 CoreAudio 与 Rate 置 0 立即冻结，杜绝正常播放中停滞卡住。
- 修复带特殊符号或括号别名歌手（如 Mario & Nesty (마리오&네스티)）歌词匹配失败提示网络问题：
  1. 根因剖析：QQ 音乐 SMTC 上报的艺人常带有跨语种括号别名，且别名本身可能包含 `&`（例如 `Mario & Nesty (마리오&네스티)`）。原有逻辑直接按 `[/、,，;&]` 切分，导致括号结构被破坏，切出如 `nesty(마리오` 和 `네스티)` 等碎片，导致歌曲严格匹配（`select_song`）全部失败，提示“未找到可靠匹配的 QQ 音乐歌词，可点击‘重新获取歌词’重试”，常被误认为是网络故障。
  2. 修复方案：在 `qqmusic_lyrics.py` 中新增 `clean_artist_tokens`，优先剥离整句尾部括号别名再按分隔符切分各歌手，并对子 token 再次安全清洗。对于《Never Say Good Bye》等歌曲 100% 成功识别并秒级匹配 121 句带逐字时间戳的 QRC 歌词。

### 测试与验证

- 自动化单元测试：
  - 更新 `tests/test_macos.py` 中的 `test_qqmusic_continuous_playback_does_not_freeze_when_position_static`，覆盖静态 ElapsedTime 下播放连续推移与暂停冻结判定；
  - 更新 `tests/test_qqmusic.py`，新增包含 `&` 符号括号韩文别名艺人的歌曲匹配单测；
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_macos.py tests/test_qqmusic.py tests/test_qqmusic_cache.py tests/test_mac_distribution.py -v`：152 项测试全部通过（OK，skipped=1）。
- 实际播放验证：
  - Mario & Nesty (마리오&네스티)《Never Say Good Bye》：成功匹配并加载 121 句全量逐字 QRC 歌词，不再出现歌词未匹配错误；
  - Mili《TIAN TIAN》：在 01:16 及更长播放过程中虚拟时钟连续推进，完全不再发生卡死。

### 影响与限制

- 保持 macOS 平台只读监听架构，无须修改外部播放器状态；
- 所有包含多语言及带符号别名的歌手均能精确匹配。

## 2026-10-14：支持 QQ 音乐在线 QRC 逐字歌词展示与暂停检测停滞判定增强

### 改动

- 支持 QQ 音乐逐字歌词（Word-by-word timing / QRC）在线获取与动画渲染：
  1. 根因与背景：先前 QQ 音乐逐字时间仅依赖 Windows 本地磁盘缓存（`QQMusicLyricNew/*.qrc`），而 macOS QQ 音乐沙盒限制且不落盘散列 QRC 缓存文件，网络请求仅获取整句 LRC，导致 QQ 音乐在 macOS 及无本地缓存的 Windows 环境下无法开启逐字动画。
  2. 实现方案：
     - 在 `qqmusic_lyrics.py` 中引入 Triple-DES 解密与 zlib 流式安全解压 `_decompress_qrc`，实现 `parse_qrc_lyrics`；
     - 在 `musicu.fcg` 请求中以单次往返批量请求 `req_qrc`（`qrc: 1, crypt: 1, trans: 1`）与 `req_0`（`qrc: 0, crypt: 0, trans: 1`），网络零额外耗时；
     - 优先解密并解析官方 QRC 歌词，生成包含字词级时间戳（`TimedWord`）的 `LyricDocument`，并支持加密译文与 base64 译文自动对齐；
     - 当歌曲无 QRC 时无缝回退至标准 LRC，并兼容 `fcg_query_lyric_new.fcg` 接口；
     - 控制面板“歌曲逐字时间”状态即时反映“逐字时间可用”，桌面歌词自动呈现逐字高光与演唱律动效果；
     - 更新 `macos_netease.py` 中的 `_fetch_qq_lyrics_by_mid` 统一复用 `fetch_qq_lyrics`，确保合唱及精选集歌曲亦享受逐字歌词。
- 修复 QQ 音乐在蓝牙耳机挂载等系统音频常开场景下暂停无法识别问题：
  1. 根因：QQ 音乐 Mac 客户端暂停时未将系统的 `kMRMediaRemoteNowPlayingInfoPlaybackRate` 设为 0（保持 1.0），且在挂载蓝牙耳机或有其他系统音频发声时，CoreAudio 全局音频输出状态持续为 True；
  2. 解决方案：在 `macos_netease.py` 中增加停滞漂移检测：当音频状态活跃但采样位置连续停滞超过 1.8 秒且本地虚拟时钟推移超过 1.2 秒时，判定为暂停（`playing = False`），冻结歌词动画与进度；当采样位置再次前进时立即恢复播放。
- 更新 `QQMUSIC.md` 说明网络与本地缓存 QRC 双通道支持。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_qqmusic.py` 中新增 `test_parse_qrc_lyrics_with_word_timings_and_translations` 与 `test_fetch_qq_lyrics_prefers_qrc_and_falls_back_to_lrc`，验证 QRC 解密解析、字级区间提取、译文合并与无逐字回退；
  - 在 `tests/test_macos.py` 中新增 `test_qqmusic_pause_with_active_audio_and_rate_one_detects_pause_by_position_stall` 与 `test_macos_qqmusic_loads_qrc_word_timings_via_network`，覆盖蓝牙耳机场景暂停识别与 macOS QQ 音乐逐字歌词加载；
  - 运行 `python -m unittest tests/test_core.py tests/test_workflow_docs.py tests/test_macos.py tests/test_qqmusic.py tests/test_qqmusic_cache.py tests/test_mac_distribution.py`：149 项测试全部通过（OK）。
- 真实网络检索与解密实测：
  - 周杰伦《等你下课》：57 句全部携带逐字字词时间；
  - 周杰伦《晴天》：63 句全部携带逐字字词时间；
  - Mili《Iron Lotus》：63 句逐字歌词，61 句中文译文精确对齐；
  - YOASOBI《夜に駆ける》：69 句全部携带逐字字词时间。
- 发布包构建与审计：
  - 执行 `./.venv/bin/python tools/build_macos.py --output-dir artifacts/mac-release`，成功生成应用与归档文件。

### 影响与限制

- QQ 音乐在 macOS 与 Windows 上均支持在线获取官方逐字歌词，无需手动指定缓存目录；
- 若个别歌曲官方未提供逐字数据，自动回退到整句 LRC 动画；
- 维持既有只读安全原则，不向 QQ 音乐发送控制命令。

## 2026-10-13：修复 QQ 音乐频繁获取失败（错误码 2001）与自动切歌歌词不重新加载问题

### 改动

- 解决 QQ 音乐热门歌曲搜索高频报错 2001（限制/不可用）导致歌词获取失败问题：
  1. 根因剖析：在 `qqmusic_lyrics.py` 与 `macos_netease.py` 中，网络搜索请求体使用了旧版桌面客户端标识 `"comm": {"ct": 11, "cv": 0}`。对于热门歌曲（如司南《冬眠》、LBI利比《可我只是海》），QQ 音乐后端对 `ct: 11` 触发了严格频控与鉴权限制，直接返回 `code: 2001`，抛出 `ValueError("QQ 音乐歌曲搜索暂不可用")`。该异常导致播放器进入 10 秒重试等待（`_retry_at = now + 10`），桌面歌词出现“QQ 音乐歌词获取失败，可点击‘重新获取歌词’重试。”。
  2. 将客户端标识全面升级为现代 QQ 音乐 PC 客户端标准标识 `"comm": {"ct": 26, "cv": 0}`：司南《冬眠》（43 句）、LBI利比《可我只是海》（44 句）、梁博《男孩 (Live)》（67 句）等热门歌曲均秒级返回 `code: 0` 并 100% 成功同步歌词。
- 解决自动切换歌曲时歌词不会重新加载问题：
  1. 根因 A（起播时长补全导致误判切歌）：macOS 系统的 `nowplaying-cli` 在刚切歌的第 1 个 tick 时往往先给出曲名和歌手，而 `duration` 为 0 或延迟上报；在第 2 个 tick 时才补齐准确时长。原代码单凭 `[title, artist, duration]` 序列化 JSON 判断 `switched`，导致同一首歌在 200ms 内触发两次切歌，`self._generation` 递增使得第一次发起的歌词请求结果在返回时因 generation 失配被当作陈旧任务直接丢弃。
  2. 根因 B（旧任务阻塞新任务发起）：切歌发生时，如果上一首歌曲的后台歌词请求尚未完成，原代码没有重置 `self._lyrics_job`，导致切歌后当前 tick 看到 `self._lyrics_job is not None` 而无法提交新歌的加载任务，直到旧任务超时结束。
  3. 优化解决方案：
     - 重构切歌判定 `same_track`：同名同歌手在起播阶段从 0 补全为实际时长（或毫秒差异在容差内）时不认定为切歌，不递增 generation，不中断正在执行的加载任务；
     - 切歌时立即解绑 `self._lyrics_job = None`，使切歌后的当前 tick 能够毫无延迟地立即提交新歌曲的歌词加载任务；
     - 歌词接收改为 generation 周期校验（`if generation == self._generation:`），即使起播时长发生补全，也能平滑接收歌词并双向写入当前 key 缓存；
     - 在 `_find_mac_song_candidate` 中兼容起播初期 `duration_ms == 0` 的情况，只要歌名与歌手精确匹配即可命中，消除起播初期的空白等待。
- 重新使用 `tools/build_macos.py` 打包最新 `build/macos-dist/都市回响.app` 与 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_macos.py` 中新增 `test_song_duration_zero_to_positive_does_not_cancel_or_drop_lyrics`，覆盖切歌起播 duration 为 0 到补全为正数时平滑接收歌词且不触发二次切歌。
  - 在 `tests/test_macos.py` 中新增 `test_fast_song_switching_cancels_previous_holding_and_loads_new_lyrics`，覆盖快速切歌时旧任务即时解绑并立即发起新歌词加载。
  - 运行 `./.venv/bin/python -m unittest tests/test_macos.py`：38 项测试全部通过（OK）。
  - 运行全套相关测试：`test_core.py`、`test_workflow_docs.py`、`test_macos.py`、`test_mac_distribution.py`、`test_qqmusic.py`、`test_qqmusic_cache.py` 共 148 项测试全部通过（1 项 Windows 语法跳过）。
- 真实网络检索与切歌实测：
  - 测试司南《冬眠》（269s 及 0s 模拟）：成功获取 43 句歌词。
  - 测试 LBI利比《可我只是海》（175s）：成功获取 44 句歌词。
  - 测试梁博《男孩 (Live)》（310s）：成功获取 67 句歌词。
- 发布包构建与审计：
  - 执行 `./.venv/bin/python tools/build_macos.py --output-dir artifacts/mac-release`，成功生成应用与归档文件。
  - 运行 `./.venv/bin/python -m unittest tests/test_mac_distribution.py`：12 项发行版结构与安全审计测试全部通过（OK）。

### 影响与限制

- 客户端标识切换为现代桌面客户端 `ct: 26`，大幅降低被频控限制概率；
- 兼容起播 0ms 检索仅在歌名与歌手精确相符时生效，不会引入非同名曲目误匹配；
- 维持既有网易云音乐与 Windows 版本行为一致。

## 2026-10-13：macOS QQ 音乐 CoreAudio 硬件级暂停识别与精选集/合唱歌词匹配优化

### 改动

- 修复 macOS QQ 音乐播放中卡死在 00:00 及暂停后应用无法停止的问题：
  1. 根因剖析：QQ 音乐 Mac 客户端在正常播放中不会实时递增 `kMRMediaRemoteNowPlayingInfoElapsedTime`（仅在歌曲起播、手动 Seek 或切歌时上报一次），而暂停时也不会将 `kMRMediaRemoteNowPlayingInfoPlaybackRate` 置为 0。先前采用的“位置连续 1.2 秒未前进判定暂停”逻辑导致正常播放到 1.2 秒后被误判暂停并把进度冻结在 00:00；而单凭播放速率 `rate > 0` 又无法在用户暂停时停止歌词。
  2. 接入 macOS 底层 CoreAudio HAL 架构：
     - 实现 `is_mac_bundle_audio_running(target_bundle)`：利用系统属性 `kAudioHardwarePropertyProcessObjectList` 遍历音频客户端，直读 `com.tencent.QQMusicMac` 对应的 `kAudioProcessPropertyIsRunningOutput`（音频输出活跃度），单次耗时小于 1ms，不受其他后台应用发声干扰；
     - 实现 `is_mac_audio_output_running(bundle)`：当进程级状态不可用时，自动回退查询系统默认输出硬件（`kAudioHardwarePropertyDefaultOutputDevice`）的活跃状态（`kAudioDevicePropertyDeviceIsRunningSomewhere` / `goin`）；
     - 优化状态转移与时钟推进：QQ 音乐播放中持续发声时，`playing = True` 且本地高精时钟平滑推移；用户在 QQ 音乐中按下暂停时，音频输出停止，`playing = False`，歌词动画停止并将位置精确冻结在暂停点；用户恢复播放或拖动进度时无缝接续。
- 解决 QQ 音乐经典歌曲（如《别怕我伤心》）及合唱单曲（如《STORM Pt. 2》）大概率匹配不到歌词的问题：
  1. 根因剖析：经典老歌客户端精选集/重制版与云端原唱片时长存在 3~6 秒差异（如张信哲《别怕我伤心》精选集 286 秒 vs 原版 291 秒），原先 2000ms 硬性容差直接误判为不匹配；合唱歌曲 macOS 系统仅上报主唱，导致歌手全等校验失败。
  2. 重构 `_find_mac_song_candidate`（并兼容 `_find_mac_collab_song`）：
     - 梯度 1：歌名归一化一致且歌手完全匹配，时长容差扩至 8.5 秒，按时长差绝对值排序选取最接近项；
     - 梯度 2：主唱属于合唱阵容子集（如 `GENER8ION` 属于 `GENER8ION/Yung Lean`），按时长差排序选取最接近项；
     - 命中候选歌曲后，优先调用 `_fetch_qq_lyrics_by_mid` 直接根据 `mid` 解析并拉取歌词。实测张信哲《别怕我伤心》（50 句）与 GENER8ION《STORM Pt. 2》（57 句）均 100% 同步命中。
- 重新使用 `tools/build_macos.py` 打包最新 `build/macos-dist/都市回响.app` 与 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_macos.py` 中新增 `test_mac_coreaudio_detection`，覆盖 CoreAudio 硬件级/进程级音频检测、非 darwin 与不存在 bundle 回退及播放器 bundle 参数传递。
  - 更新 `test_qqmusic_playback_stalled_detects_pause_and_freezes_position`，覆盖发声时进度平滑推进、用户暂停时音频停止并冻结在当前插值位置、恢复播放时平滑接续。
  - 更新 `test_qqmusic_compilation_and_collab_fuzzy_matching`，覆盖精选集时长差与合唱歌词匹配。
  - 运行 `./.venv/bin/python -m unittest tests/test_macos.py`：36 项测试全部通过（OK）。
  - 运行全套相关测试：`test_core.py`、`test_workflow_docs.py`、`test_mac_distribution.py`、`test_qqmusic.py`、`test_qqmusic_cache.py` 共 145 项全部通过（1 项 Windows 语法跳过）。
- 真实云端网络检索实测：
  - 测试张信哲《别怕我伤心》（286s 精选集）：成功命中原版（291s），同步 50 句歌词。
  - 测试 GENER8ION《STORM Pt. 2》（主唱匹配合唱阵容）：成功命中，同步 57 句歌词。
- 打包产物校验：
  - 生成 `build/macos-dist/都市回响.app`，`codesign --verify` 校验签名有效。
  - 发布归档 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`（SHA-256: `7dd8eeead6bb2457f47bfc3b01a3d2a2112779852a7c9c853300d279fc655434`，大小: 55,117,324 字节）。

### 影响与限制

- CoreAudio 进程级检测依赖 macOS HAL 架构（macOS 10.15 及更高版本支持），旧版本或权限受限环境自动安全回退至系统默认输出设备活跃检测；
- 时长容差放宽至 8.5 秒并严格要求歌名与歌手匹配，仅吸收专辑/剪裁版前后静音差，不会引入同名不同曲的串歌风险；
- 原有网易云音乐 macOS 适配与 Windows 版本功能行为均保持完全一致。

## 2026-10-13：支持多屏幕选择显示与 macOS 暂停状态检测修复

### 改动

- 支持选择屏幕显示（多显示器支持）：
  1. 在 `settings.py` 中为 `Preferences` 增加 `target_screen` 偏好字段（默认空字符串代表跟随主屏幕），并在 `presets.py` 的效果预设排除项中排除该字段，确保预设切换不改变用户的屏幕选择。
  2. 在 `overlay.py` 中改造屏幕绑定逻辑：根据 `target_screen` 匹配当前连接的显示器名称（`QScreen.name()`），屏幕未找到或拔出时自动回退至系统主屏幕；监听 `primaryScreenChanged`、`screenAdded` 与 `screenRemoved` 事件，支持屏幕热插拔自适应更新；窗口切换屏幕时自动更新几何位置（`setGeometry`）、原生屏幕归属（`windowHandle().setScreen`）并清理排版与文字效果纹理缓存。
  3. 在 `controls.py` 的“显示与文字”设置分组中增加“显示屏幕”下拉框，列出当前所有物理显示器名称与分辨率（自动标明主屏幕），支持动态热插拔刷新，选项修改后即时生效并保存到配置文件。
- 修复 macOS QQ 音乐暂停后 app 播放未停止的问题：
  1. 根因：QQ 音乐 Mac 客户端暂停时未将系统的 `kMRMediaRemoteNowPlayingInfoPlaybackRate` 设置为 0（仍保持为 1），而播放位置 `ElapsedTime` 保持静止；原先播放器单凭 `rate > 0` 判定为播放中，且时钟插值保护未限制单次轮询累加，导致客户端暂停后 app 依然单方面推进进度并持续播放歌词动画。
  2. 在 `macos_netease.py` 中增加静止检测（Stall Detection）：当采样位置连续 1.2 秒未前进时，即使 `rate > 0` 也准确识别为暂停（`playing = False`），停止本地时钟插值并将位置稳定冻结在实际毫秒数；当位置恢复递增时立即恢复 `playing = True`。
  3. 修复 `position()` 的插值上限，最多基于锚点外推 1.2 秒，防止无数据时进度无休止递增；播放器暂停时自动触发 `changed` 信号，使 `LyricsOverlay` 的高精度刷新定时器停止运作，完全冻结画面。
- 重新使用 `tools/build_macos.py` 打包最新 `build/macos-dist/都市回响.app` 与 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_macos.py` 中新增 `test_qqmusic_playback_stalled_detects_pause_and_freezes_position` 测试，验证 QQ 音乐在 rate=1 但位置静止时能够正确识别暂停，`position()` 冻结且恢复播放后平滑接续。
  - 在 `tests/test_macos.py` 中新增 `test_screen_selection_and_overlay_binding` 测试，验证屏幕选择、指定副屏、不存在屏幕回退主屏以及控制面板 UI 下拉框交互。
  - 运行 `./.venv/bin/python -m unittest tests/test_macos.py`：34 项测试全部通过（OK）。
  - 运行全套相关测试：`test_core.py`、`test_workflow_docs.py`、`test_mac_distribution.py`、`test_qqmusic.py`、`test_qqmusic_cache.py` 共 110 项全部通过（1 项跳过）。
- 打包产物校验：
  - 生成 `build/macos-dist/都市回响.app`，`codesign --verify` 校验签名有效。
  - 发布归档 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`（SHA-256: `ce5405d29e013d96c134d572ac9141bf3c905ecaf3dc231abca9f7ed6ee2c7df`，大小: 55,114,632 字节）。

### 影响与限制

- 屏幕选择通过 Qt 跨平台接口（`QScreen`）实现，支持 macOS 与 Windows 多显示器环境；
- 静止暂停检测容差为 1.2 秒，既能平滑吸收网络或客户端 1 秒一次的采样抖动，又能确保在用户按下暂停后快速响应并冻结歌词；
- 其它原有视觉效果、逐字歌词渲染和网易云客户端联动行为均保持完全兼容。

## 2026-10-13：macOS QQ 音乐接口 2001 修复与歌词自适应回退

### 改动

- 解决用户实机测试 `都市回响.app` 时出现的“QQ 音乐歌词获取暂时失败，10 秒后自动重试”问题：
  1. 在 `qqmusic_lyrics.py` 中为 `DoSearchForQQMusicDesktop` 请求加入客户端身份块 `"comm": {"ct": 11, "cv": 0}`，并统一配置标准桌面端浏览器 User-Agent，修复因缺少身份参数和默认 Python UA 导致的 `code: 2001`（参数错误/限制）报错。
  2. 在 `macos_netease.py` 的 `load_qqmusic_lyrics` 中增加专辑名自适应回退：当 macOS 系统 `nowplaying-cli` 传回的单曲专辑名与 QQ 音乐云端正式唱片专辑不一致时，自动清空专辑限制重试匹配。
  3. 增加合唱歌曲主歌手包含匹配与回退机制（`_find_mac_collab_song` 与 `_fetch_qq_lyrics_by_mid`）：针对 macOS 系统媒体控制仅汇报主歌手而云端为多歌手合唱的情形，在歌名与时长严格吻合的前提下判定子集匹配，并直接按歌曲 `mid` 获取完整歌词。
- 重新使用 `tools/build_macos.py` 编译打包生成最新 `build/macos-dist/都市回响.app` 及 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip`。

### 测试与验证

- 自动化单元测试：
  - 在 `tests/test_macos.py` 中新增 `test_load_qqmusic_lyrics_collab_and_album_fallback`，覆盖单曲专辑名不一致回退及合唱多歌手主唱子集匹配逻辑。
  - 运行 `./.venv/bin/python -m unittest tests/test_macos.py`：32 项测试全部通过。
  - 运行核心与文档校验：`test_core.py` (21 项)、`test_workflow_docs.py` (18 项通过，1 项 Windows 跳过)、`test_qqmusic.py` (27 项)、`test_qqmusic_cache.py` (32 项)、`test_mac_distribution.py` (12 项) 全部通过。
- 真实歌曲云端网络检索与匹配验证：
  - 测试 Alexandra Stan《All My People》（单曲/专辑差异）：成功解析同步 70 句歌词。
  - 测试 h3R3刘清云《先说谎的人》（多歌手合唱）：成功解析同步 81 句歌词。
  - 测试 Odesza《A Moment Apart》：成功解析同步 21 句歌词。
- 打包产物校验：
  - 生成 `build/macos-dist/都市回响.app`，`codesign --verify` 校验签名有效。
  - 发布归档 `artifacts/mac-release/city-echoes-0.6.0-beta.2-macos.1-arm64.zip` 生成成功，大小 55,112,643 字节。

### 影响与限制

- 仅优化网络搜索参数与 macOS 平台上的歌手/专辑回退容错机制，未修改原有歌词逐字渲染、动画逻辑和 Windows 平台功能。
- 打包为本地自签名应用，首次打开可能需右键选择“打开”或在系统“安全性与隐私”中允许运行。

## 2026-10-13：macOS 适配 QQ 音乐播放及 QRC 歌词格式

### 改动

- 针对 macOS 环境下播放 QQ 音乐时面板与格式仍显示为“网易云”且无法获取歌词的问题，扩展 `macos_netease.py`：新增对 QQ 音乐 Mac 客户端（`com.tencent.QQMusicMac`）的客户端 Bundle 标识识别（兼容 `kMRMediaRemoteNowPlayingInfoClientBundleIdentifier` 与 `bundleIdentifier`），并提取 `album` 专辑信息以支撑歌词精准匹配。
- 引入 `MacMusicPlayer`（兼容保留 `MacNeteasePlayer` 别名），实现播放来源自动检测与动态切换。来源名称、短标签（`QQ 音乐` / `网易云`）、播放器状态提示、面板格式列、播放栏文案（`QQ 音乐播放`）及进度条提示均根据当前实际播放源动态响应。
- 为 macOS 联动接入 QQ 音乐歌词接口（`qqmusic_lyrics.load_song_lyrics`）与本地缓存优先机制（`QQCacheReader`），支持“重新获取歌词”与选择歌词缓存目录。在 `qqmusic_cache_paths.py` 中为 macOS 平台添加 QQ 音乐 Mac 客户端常见歌词缓存路径。
- 在 `lrc.py` 中扩展 `load_lrc`：新增对 `.qrc` 文件扩展名、XML 节点格式以及 DES 加密 QRC 二进制数据的解码与解析支持，完整保留字词级时间戳（`TimedWord`）并复用逐字演唱强调。
- 在 `controls.py` 中为本地歌词选择对话框加入 `*.qrc` 支持，并在打开本地音乐时自动检测同名 `.qrc` 文件。
- 在 `main_mac.py` 中增加 `--qqmusic` 与 `--netease` 互斥参数，支持指定单一客户端模式；保存的 QQ 音乐缓存目录设置自动载入播放器；新增 `启动QQ音乐联动.command` 便捷脚本并更新 `MACOS.md` 说明文档。

### 测试与验证

- `tests/test_macos.py`：新增 6 项测试覆盖 QQ 音乐 Bundle 识别与专辑提取、来源自动判定与动态切换、手动重试与缓存目录配置、QRC 文件解码（包含明文与合成密文）、`main_mac.py` 命令行参数、QQ 音乐控制面板 UI 动态呈现；全量 31 项测试全部通过。
- `tests/test_workflow_docs.py`：18 项文档与链接校验全部通过（1 项 Windows 语法跳过），确保文档链接与变更规范完整。
- `tests/test_core.py`、`tests/test_mac_distribution.py`、`tests/test_qqmusic.py`、`tests/test_qqmusic_cache.py`：全量共 141 项相关测试全部通过。
- 语法与脚本校验：对 `start.sh`、`安装.sh`、`卸载.sh`、`启动.command` 及新增的 `启动QQ音乐联动.command` 执行 `bash -n` 校验，语法全部合规。

### 影响与限制

- macOS 下 QQ 音乐与网易云支持自动识别与无缝切换，原有网易云联动逻辑、Windows 平台实现与本地音频播放功能保持完全兼容。
- macOS 下媒体信息读取仍依赖 `nowplaying-cli` 外部工具输出的原始 JSON，要求系统授权或已正确安装该工具。
- QQ 音乐 Mac 客户端可能随更新调整缓存文件存放路径；当本地缓存未命中时会自动回退至官方接口网络搜索取词，也可通过控制面板手动配置歌词缓存目录或点击重新获取。

## 2026-10-11：安装等待反馈与安全取消（0.7.0-beta.7）

### 改动

- 针对 beta.5 安装界面持续显示“正在检查并处理”、关闭无反馈及本地 DLL 选择疑问，改进 `installer_ui.py`、`netease_install.py`。显示进程、版本、框架下载／本地校验、备份和写入阶段及已用时间，增加取消按钮；右上角关闭及 Esc 请求协作取消，后台线程结束后自动关闭。完成结果通过 `finished` 信号交付，GUI 不再调用阻塞的线程等待。
- 框架下载使用 45 秒总时间预算及 5 秒单次网络等待，进程检查超时提供独立提示。显式本地路径无效时停止，不静默回退为下载；大于 32MiB 的 DLL 不读入内存。准备期间响应取消，写入期间完成或回滚事务再退出；仍保留原有哈希、架构、版本和运行中保护。
- 版本更新为 beta.7，README、网易云使用说明及包内指南说明实际 DLL 文件选择与等待排查；更新产品、技术文档、发行说明和原生截图。新增 `tests/test_installer_wait.py` 与 [实际验证摘要](docs/research/installer-wait-20261011.json)，重建两份 Windows ZIP。

### 测试与验证

- `.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v`：343 项通过，15.992 秒；新增 13 项覆盖慢下载总预算、下载前后取消、本地文件及超大文件、进程检查超时、窗口关闭／Esc／取消后重试、GUI 非阻塞完成和写入期间安全关闭。最终结果 `artifacts/installer-wait-all-tests.txt`。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\installer-wait-source"`：Windows 原生静音 75 项通过。真实 Windows 窗口的 14 项响应、取消及 WM_CLOSE 检查通过，慢进程检查为测试桩，不是对方电脑复现；`artifacts/installer-wait-native/report.json`。实际 DPR 1／1.25／1.5、默认与 480×480 窗口共 69 项检查通过，按钮可见且内容可滚动。
- 网易云 ZIP 9 项检查通过：真实 EXE／官方 DLL 的隔离源码安装、更新、恢复、卸载与本地校验，成品运行中保护、三个实际 BAT 窗口及公开启动静音；成品静音 75 项通过。源码隔离验收明确使用“目标未启动”检测桩，成品运行中保护不绕过。QQ ZIP 的中文路径、无开发 PATH、原生窗口及重复启动等 6 项通过。两份最终 ZIP 的 CRC、SHA-256、同一 EXE 和私人数据排除检查通过。
- 本机成品更新时仅短暂重启歌词及其音频助手，18 份状态文件复制哈希一致；网易云进程保持，未发送播放命令。后台歌词进程、本地监听及正常网易云均运行，无调试端口。隐藏面板的原生版本读取未成功，不将其计为通过；成品版本由公开入口检查及 EXE 哈希确认。

### 影响与限制

- 未取得反馈用户的完整客户端版本和实际 DLL 文件路径，未复现对方电脑的具体卡点；截图的 DLL 栏仍为占位提示，不能据此断言已经选择本地文件，也不能将所有等待归因于网络。
- 取消与总预算需要当前系统／网络调用返回后检查，不能保证任意文件系统阻塞都立即结束；文件事务不使用强杀线程。为保持正在播放的网易云，本轮未重跑成品正向安装事务、实曲暂停／拖动／切歌、第二台干净电脑或所有网络阻塞情形。音乐客户端未重启，原有接入及用户数据保留；Mac 发行包不变。

## 2026-10-11：客户端兼容检测与实验性安装（0.7.0-beta.6）

### 改动

- 新增 `compatibility.py` 与 `compatibility/clients.json`：完整构建号区分已验证、未验证及已知不兼容；固定 HTTPS 来源后台刷新、限长校验、7 天缓存和离线回退。列表只提供数据，不下载或执行代码。
- `netease_install.py`、`installer_ui.py`、`main.py` 新增单次实验性安装确认、目标版本家族授权、持久安装备份和恢复入口。保留 x64、官方框架哈希、退出及文件冲突检查；已知不兼容禁止安装。恢复时校验安装文件及备份，保留个人设置，仅移除该次新建且未变化的框架。
- 网易云插件更新至 `0.1.5`，按实际歌词标识选择客户端状态或按歌曲读取本机缓存；只订阅宿主原播放流。`netease.py` 增加认证诊断和本机授权的新版本接收，接口异常停止歌词并持续提示，连接异常不传播至宿主回调。QQ `qqmusic.py` 与 `controls.py` 增加媒体会话、有效进度及歌词来源提示。
- `build.ps1`、打包及验证工具同步内置策略与“恢复网易云联动.bat”；开发安装脚本复用成品窗口。更新 README、两版使用说明、技术文档、维护指南、安装截图和实际验证证据 `docs/research/compatibility-20261011.json`，生成 QQ／网易云两个独立 ZIP。

### 测试与验证

- `.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v`：330 项通过，15.675 秒。新增策略更新／损坏／离线／过期／撤销、授权隔离、实验确认、安全检查不可绕过、恢复事务及损坏备份、运行时接口选择和诊断心跳测试；结果 `artifacts/compatibility-final-tests.txt`。最终说明修订后，按测试发现方式复验兼容专项 20 项及文档 18 项通过，插件版本与历史功能起始版本说明一致。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\compatibility-source"`：原生 Windows 静音集成 75 项通过。最终网易云 ZIP 在中文路径、移除开发 PATH 下安装／更新／首次恢复／更新恢复／重复卸载、三个 BAT 窗口和成品静音验证共 13 项通过，成品静音 75 项通过；结果 `artifacts/compatibility-netease-public-final`。
- QQ ZIP 实际 BAT 原生窗口、版本、兼容提示、自动启动／缓存入口、重复启动复用共 6 项通过；结果 `artifacts/compatibility-qq-public-verified-final`。实际设备像素比 1／1.25／1.5、默认及 480×480 窗口共 63 项可达性检查通过，截图 `docs/images/compatibility-installer.png`。
- 正常网易云 `3.1.41.205529` 加载插件 `0.1.5`，只读观察 4 次，收到真实歌曲与 69 句歌词，确认采用客户端歌词状态；客户端处于暂停、位置保持不变，未发播放命令。4 个原有文件哈希和连接令牌保留；两个 ZIP 的完整性、SHA-256、同一 EXE 和私人数据排除检查通过。

### 影响与限制

- 未验证未来网易云实际版本，测试新版本号为夹具；在线列表只调整安装许可，接口或框架变化仍需代码更新。网易云运行时仅提供三段版本，完整构建检查在安装时进行；升级其他版本家族后需重新安装联动。原有字体、主题、预设、动画与纯音乐行为保留。
- 自动审批拒绝了带远程调试端口重启网易云的验收方式，原因是可能暴露已登录客户端调试接口和会话数据；改用正常启动和只读 UI 检查。本轮未重跑实曲进度推进、拖动、切歌和 QQ 实曲播放，未做第二台干净电脑或长期稳定性验收，不将静音与夹具测试当作这些项目通过。网易云已恢复正常参数启动。
- 旧安装没有本版备份时无法自动恢复；原有框架本身不兼容时需要另行更新框架或使用已验证客户端。后续文件变化或新增共用插件时恢复会停止并提示；备份含本机令牌，须保留且不可公开。

## 2026-10-11：QQ 音乐自动启动与发行更新（0.7.0-beta.5）

### 改动

- `qqmusic_startup.py` 增加默认关闭的当前用户登录启动、无窗口监听、中文／空格路径转义、失败回滚、有限重试和 260 字符登录命令限制。每 2 秒检查 QQ 根进程；已有实例复用，手动退出后等待下一 QQ 会话，关闭开关后结束监听。只检查进程名称，不打开或控制 QQ，不修改客户端文件。
- `controls.py` 在 QQ 版“当前音乐”新增自动联动卡片、开关与持续状态提示，其他播放源不显示，独立于效果预设。明确 Windows 登录时运行监听、面板默认收在托盘；修复显式退出被普通关闭到托盘逻辑拦住的问题。
- `main.py` 在 Qt 导入前分流监听入口，QQ 正常运行增加当前用户／会话互斥与显示事件防重，验证入口继续隔离；`start.ps1` 识别重复启动后恢复的既有 QQ 窗口。更新 README、QQ 说明、包内说明与验证记录。
- 将用户更新后的 QQ **22.75（2275.14.47.28）** 纳入实机验证。系统媒体会话与 QRC 格式可沿用现有适配器；增加真实 Opened／播放数据样本、等待清除旧句及重连回归。README 和发行说明标明 **22.52／22.75 共用同一 QQ ZIP**、更新后开启系统媒体控制和暂停延迟校正的处理，新增自动启动实机图及 [公开验证摘要](docs/research/qq-autostart-release-20261011.json)。

### 测试与验证

- 新增 19 项自动启动测试和 1 项说明校验，更新原 QQ 文档断言；全量自动测试 **303 项通过**，`artifacts/qq-autostart-all-tests.txt`。覆盖目录迁移、登录命令、回滚、防重、有限重试、手动退出、界面及预设独立性。
- Windows 原生静音及最终重建后实际 `启动.bat -Smoke` 各 **75 项通过**。三主题 × 默认／最小窗口 × 100%／125%／150% 共 **18 个布局通过**，`artifacts/qq-autostart-layout`。最终构建完整通过，`artifacts/qq-autostart-build-final.txt`；原有 **8 份个人数据文件** SHA-256 保持一致。
- 真实 QQ 22.52 与 Windows 注册表／原生界面 **14 项检查通过**，`artifacts/qq-autostart-native/report.json`。开关启停、监听防重、自动启动到托盘、重复入口恢复、实例复用、显式退出不重拉、关闭监听但当前歌词继续及真实歌词均验证，QQ 曲目／播放状态不受影响。单次监听开启至窗口创建约 **1,390ms**，不是取词延迟；监听工作集 **31,555,584 字节**。PyInstaller 的启动钩子预载 Qt6Core，监听代码自身只用标准库，未加载 GUI／音频／NumPy。
- 首次替换遇旧成品残留的 SMTC 辅助进程占用目录，核对路径清理后替换成功；首轮原生检查跨越歌曲自然结束，重选时间充足窗口后通过。没有向 QQ 发播放、暂停、拖动或切歌命令。
- 发行最终全量自动测试 **308 项通过，11.016 秒**：`artifacts/qq-autostart-release-final-tests.txt`。`build.ps1 -SkipDependencies` 重建 `0.7.0-beta.5` 成功，`artifacts/qq-autostart-release-build.txt`；最终实际 `启动.bat -Smoke` **75 项通过**，`artifacts/qq-autostart-release-launcher/smoke-report.json`。
- QQ **22.75** 的原生自动启动 **14 项通过**，`artifacts/qq-autostart-release-native/report.json`；单次拉起 1,391ms，监听工作集 31,473,664 字节。实际 QQ ZIP 在中文路径、移除开发 PATH 后 **9 项通过**，`artifacts/qq-autostart-release-public-verified/qq-public-report.json`；网易云 ZIP 隔离安装／更新／重复卸载、保留数据与实际 BAT **8 项通过**，`artifacts/qq-autostart-release-netease-public/release-report.json`，包内静音 **75 项通过**。
- QQ 22.75 最终真实静音播放回归 **7 项通过**，`artifacts/qq-22.75-playback/actions.json`，配套成品采集 **6 项通过**。76 句、309 个真实字词区间，进度推进、稳定暂停冻结、效果不改播放及原曲／播放状态恢复。单次首个观察快照到歌词为 **172ms**，非 P95、不含首次写盘或启动。首轮暂停后发现客户端一次延迟校正，等 6 秒稳定后复验通过；未屏蔽真实时间轴变化。初次新包取词检查在 Opened／零时长阶段未通过，用户开启媒体控制并播放后完整复验通过；等待阶段原生检查跨越用户开始播放，也未算作成功记录。
- 两个 ZIP 的 CRC／SHA-256、相同 EXE 与私人数据排除通过，`artifacts/releases/autostart-package-integrity.json`。QQ 70,674,961 字节／309 项，网易云 70,680,922 字节／313 项；8 份原有个人文件哈希一致，已恢复本机原先开启的自动启动。README 使用最终实际窗口截图。

### 影响与限制

- 用户确认设计并授权提交与发行更新；版本升级至 `0.7.0-beta.5`，提供 QQ／网易云两个独立 ZIP，README 和包内说明增加启用、取消及更新步骤。未实际注销／重启 Windows 检查登录触发，未重启真实 QQ，下一会话逻辑有自动测试；未验第二台电脑和长期稳定性。系统可以延后或禁用登录启动；移动目录后重新开启，更新／删除前先关闭开关并等待监听结束。
- 本轮没有重新验收 QQ 22.75 手工拖动／切歌或网易云实曲播放，相关原有自动回归通过。22.75 暂停后可能有客户端延迟位置校正，稳定后冻结；保持真实客户端位置以支持暂停时拖动。用户自行更新 QQ 后的客户端仍正常运行，Mac 下载版本保持原样。

## 2026-10-11：QQ 本地缓存优先取词与真实字词强调（0.7.0-beta.4）

### 改动

- `qqmusic_cache_paths.py`、`qqmusic_cache.py` 只读发现并匹配 QQ 已加载的歌词缓存，提供有限目录索引、严格完整身份核验、读前后文件校验和 32 首解码缓存；`qqmusic_des.py`、`qqmusic_qrc.py` 移植 MIT 解码参考，无新增运行依赖，兼容真实 QQ XML 中未转义引号和原文换行，拒绝未知格式及未验证外层偏移。
- `qqmusic.py`、`qqmusic_lyrics.py` 改为本地优先、官方网络兜底；独立线程在切歌或重试后的 20 秒内每 500ms 检查迟到缓存，按歌曲和代次隔离旧结果，不因网络等待阻塞缓存更新。QRC 真实词区间复用现有演唱强调，零时长跳过、不可靠行回退整句；译文按有效时间唯一对齐。
- `controls.py`、`settings.py`、`main.py` 新增“选择歌词缓存目录”“自动查找缓存”和独立保存的目录设置；`presets.py` 明确排除缓存目录，已有设置缺省自动发现。`qqmusic_validation.py` 记录真实缓存来源、词区间和效果切换的播放状态。
- 应用更新至 `0.7.0-beta.4`；更新 README、QQ 使用说明、技术文档、设计方案、两份包说明与发行说明，并换成实际缓存界面截图。研究报告保留历史阶段说明，新增无歌词正文的 [产品验证数据](docs/research/qq-cache-product-20261011.json)。`release/licenses/qq-qrc-MIT.txt` 与第三方说明保留参考算法的两份 MIT 归属。
- 新增独立参考合成密文、QMC 32KiB／64KiB 边界以及缓存读取／迟到／切歌隔离／设置／文档／许可随包测试；测试数据没有真实歌词或账号数据。

### 测试与验证

- 全量自动测试 **283 项通过**：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，完整结果 `artifacts/qq-cache-all-tests.txt`。覆盖密文损坏、未写完、限长解压、偏移、组合字符、重复身份、缓存与网络竞争、迟到译文、中文目录和预设独立性。
- Windows 原生静音集成 **75 项通过**：`main.py --smoke --report-dir artifacts/qq-cache-windows-smoke`。默认 1100×760、最小 900×560 和 100%／125%／150% 缩放下，目录按钮均可滚动访问；实际截图在 `artifacts/qq-cache-layout`。
- 本机 QQ 22.52 的 14 份原文解码与独立 MIT 参考哈希完全一致，保留 **3,910** 个有效字词区间、跳过 1 个零时长单位。每文件 20 次 Python 暖读取／解码／解析，P95 **6.305–21.895ms**；不是 QQ 首次加载或切歌端到端延迟。
- 45 秒真实 QQ 回归：Within 的 26 句、132 个词区间来自本地缓存，歌词网络请求 **0**；首个歌曲快照至歌词应用单次 **250ms**。原生播放进度、暂停冻结、动画／译文／演唱强调切换不改变播放均通过，原播放状态已恢复；`artifacts/qq-cache-pause/actions.json` 与 `qqmusic-report.json`。
- PowerShell 7 执行 `build.ps1 -SkipDependencies` 重建成品，9 份原有用户数据逐文件哈希保持一致。`tools/package_release.py --player all` 生成两份独立 ZIP，共用同一 EXE、附 MIT 解码许可，排除设置、令牌和日志。
- QQ ZIP 在中文解压路径、移除开发环境 PATH 后实际打开 BAT，窗口、版本、缓存来源和目录入口 **6 项通过**；网易云 ZIP 的隔离安装、更新、两次卸载、数据保留与实际 BAT 启动 **8 项通过**。根目录 `启动.bat -Smoke` 原生入口验证通过，结果分别位于 `artifacts/qq-cache-public-20261011`、`qq-cache-netease-public`、`qq-cache-launcher-bat`。
- QQ ZIP：70,612,076 字节、309 项，SHA-256 `f451bc4835ec3251adcf2f90d95845801c0f2c939014e9694f743cf92c82bbfe`；网易云 ZIP：70,618,530 字节、313 项，SHA-256 `0cb989acf3b729613f30f6b7effdc069a0197c20a048acacf4801b560688f5d3`。提交前检查最终差异与空白。

### 影响与限制

- 已有缓存能直接取词；首次播放写盘等待、非零外层偏移、第二台电脑、其他 QQ 版本、长期稳定性与人工听音对齐未验收，不能保证所有歌曲与网易云一样快。元数据缺失、歧义、未知格式或未验证偏移继续网络回退，超过 20 秒的迟到缓存可手动重试。
- QQ 切歌时观察到“新歌名＋旧时长”的过渡数据，严格缓存匹配会暂时拒绝并可能发起联网兜底，正确时长到达后接入对应缓存。完整手工拖动／切歌回归本轮未重新验收，相关状态隔离与跳转自动回归已通过；网易云协议未修改，本轮重验成品安装和启动，没有重复真实网易云播放验收。移除 PATH 不等于第二台干净电脑。

## 2026-10-11：在 README 突出 QQ 音乐取词速度与缓存限制

### 改动

- `README.md` 的 QQ 音乐使用介绍新增 GitHub IMPORTANT 提示，明确当前下载版仍联网取词、缓存尚未接入，区分已缓存歌曲的提速潜力与首次未缓存歌曲的写盘等待；说明研究中的毫秒测量不等于切歌到显示的总延迟，并链接研究报告。
- `tests/test_workflow_docs.py` 新增文档回归，检查提示位于 QQ 介绍内、使用突出格式且保留当前发布状态和性能边界。

### 测试与验证

- 全量自动测试 **250 项通过，14.225 秒**：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，记录在 `artifacts/qq-readme-latency-all-tests.txt`；新增的 QQ 介绍提示回归通过，既有文档编码与本地链接校验通过。最终差异与空白检查通过。

### 影响与限制

- 仅修改说明与文档测试，不修改程序、版本或下载 ZIP；本地缓存及 QQ 字词同步仍未接入成品，其他电脑、客户端版本和首次写盘延迟仍待验证。

## 2026-10-11：研究 QQ 已加载歌词与本地缓存可行性

### 改动

- 新增 `docs/QQ歌词缓存研究.md` 与不含歌词正文的 `docs/research/qq-cache-20261011.json`，记录真实 QQ 22.52 缓存发现、离线解码、字词时间、译文对齐、匹配歧义、性能及后续接入建议；在 `QQMUSIC.md` 添加入口。
- `tests/test_workflow_docs.py` 新增 2 项校验，检查研究证据计数／性能一致性、隐私边界与尚未接入成品的说明，并将研究文档加入既有链接和编码检查。
- 本轮仅交付研究和文档，不修改播放器、歌词网络流程、应用版本或发行 ZIP；研究用第三方源码与原始观测只留在忽略的 `artifacts`。

### 测试与验证

- Windows 11 x64 build 26200、QQ 音乐 22.52：从已打开的磁盘文件句柄找到真实歌词缓存目录，14 首歌的 28 个原文／译文文件全部离线解码成功，均无读取时尺寸／时间变化。原文共 3,911 个字词时间单位，全部起点落在所属句子的时间范围；发现 1 个零时长单位。
- 译文与全部原文句首在 10ms 内对齐；14 份原文在复核时 SHA-256 未变。空文件、截断文件及破坏密文均被拒绝，未用模拟歌词冒充真实缓存。
- 约 125 秒只读观察 23 个 SMTC 样本，加上观察后的实际复核，Through Patches of Violet 与 In Hell We Live, Lament (Let's Lament) 均唯一匹配已存在的缓存。没有发送任何播放命令，没有请求歌词网络服务；下载研究解码器源码属于单独的准备步骤。
- Node.js 研究进程中，4 份原文分别重复读取及解码 100 次，暖缓存 P95 为 1.262–3.845ms；28 文件首次扫描读取解码总计 76.796ms。未包含进程启动或 QQ 首次写盘等待，未声称为成品端到端耗时。
- 全量自动测试 **249 项通过，15.370 秒**：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，原始记录 `artifacts/qq-cache-research-all-tests.txt`。

### 影响与限制

- 结论是“本地缓存优先、现有官方接口兜底”可行，并非所有歌曲即时可取或已完成成品集成。QQ 内存对象读取未验证；SMTC 本身没有完整歌词字段。
- 未验收第二台电脑、其他 QQ 版本、首次未缓存歌曲落盘时间、非零偏移、纯音乐实曲、中文原文实曲、实际并发写入及字词与音频听感同步。文件名替换字符、版本省略和没有会话歌曲 ID 的歧义仍需严格拒绝。
- 本轮没有涉及桌面启动、绘制或打包改动，因此未重新打包、未重做静音集成或发布验证；现有公开下载保持原样。

## 2026-10-11：减少 QQ 音乐取词与切歌等待

### 改动

- `qqmusic_http.py` 为每次取词流程建立独立的 HTTPS 复用作用域，搜索成功后沿用连接下载歌词；沿用 urllib 系统代理、TLS 证书验证、HTTP 错误处理和 5 秒超时。接口拒绝时关闭连接再回退，已失效的复用连接最多重连一次，结束后释放连接，无新增运行依赖。
- `qqmusic.py` 取词工作线程从 1 个调整为最多 2 个；切歌、重试和断开时取消旧任务，`qqmusic_lyrics.py` 在后续搜索／取词／备用接口前检查取消。新歌不再等待旧歌的完整回退链；保留歌曲身份与代次校验、32 首内存缓存及失败后手动重试。
- `tests/test_qqmusic_latency.py` 新增 13 项连接复用、代理隧道、证书／超时失败、接口拒绝换连接、线程隔离及旧歌阻塞时新歌优先完成测试；更新既有切歌、重试与使用说明测试。
- 版本升级为 `0.7.0-beta.3`，更新 README、QQ 指南、两包使用说明、技术与产品文档、网易云版本说明和发布说明，继续提供 QQ／网易云两个独立 ZIP。

### 测试与验证

- 最终原生全量自动测试 **247 项通过，9.780 秒**，`artifacts/qq-latency-final-tests.txt`。源码实际 BAT Windows 静音检查 **75 项通过**，`artifacts/qq-latency-source-windows/smoke-report.json`。
- 同曲真实成功采样：Between Two Worlds (Let's Lament)／Mili／KIHOW，旧连接方式 **7.169 秒**（搜索 2.487 秒、取词 4.679 秒）；最终复用方式 **2.711 秒**（搜索 2.113 秒、取词 0.595 秒），均匹配 MID `004D7rAM2SPnrR`、取得 **76 句**。记录为 `artifacts/qq-latency-current.json`、`artifacts/qq-latency-final.json`。
- 对比过程中也遇到官方 2001 拒绝与 SSL 握手超时，保存在 `artifacts/qq-latency-comparison.json`；没有将失败请求的较短耗时当作成功提速。最终版遇到拒绝时换新连接回退。
- 最终成品重新构建；旧实例强制退出后残留媒体／音频助手导致原子更新被拦截，清理核验路径的本项目助手后重建成功。QQ 专用 ZIP 从中文路径、移除开发 PATH 后实际 BAT 启动 **4 项通过**（原生窗口、版本、QQ 连接与真实歌词），`artifacts/qq-latency-public-20261011/qq-public-report.json`。
- 网易云 ZIP 隔离安装／更新／重复卸载、设置／字体／预设／令牌／框架保留与实际 BAT 检查通过，成品静音 **75 项通过**，`artifacts/qq-latency-netease-public/release-report.json`。原用户 4 个配置文件 SHA-256 保持一致，`artifacts/qq-latency-state-preservation.json`；两个 ZIP 完整且 EXE 一致，`artifacts/releases/latency-package-integrity.json`。

### 影响与限制

- 上述为本机单次成功采样，不是 P95 或全曲保证；首次联网、官方拒绝及超时仍可能等待数秒。连续切换多首时最多两个任务执行，已经发送的旧请求不能强行中断，仍可能等待本次网络超时，但取消后不再执行后续查询。
- 不增加歌词持久缓存、账号 Cookie、第三方服务或播放控制。网易云协议及纯音乐处理不变，Mac 公开包不变。没有第二台干净电脑、更多 QQ 版本或本轮新的网易云实曲播放验收；暂停冻结由自动测试覆盖，没有把旧实测当作本轮新结果。

## 2026-10-11：QQ 音乐与网易云音乐独立分包

### 改动

- `tools/package_release.py` 按 `qqmusic`／`netease` 白名单生成两个 ZIP，文件名与根目录明确区分播放器。QQ 包只保留 QQ BAT 和 SMTC 助手；网易云包保留安装、卸载、本地音乐入口和插件模板。均排除另一播放器资源、Mac 脚本、个人设置及日志。
- 增加 `package-info.json` 和各自 SHA-256；缺少 QtCore／QtGui／QtWidgets 或对应播放器运行资源时停止打包，避免分发缺失模块的成品。两包使用同一份 EXE，沿用 `0.7.0-beta.2` 和已验证的 QQ 搜索修复。
- 新增 `release/qqmusic/使用说明.txt`、`release/netease/使用说明.txt`；README 提供两份下载，说明不同解压目录及旧 `.state` 迁移。更新 QQ／网易云指南、技术文档、发布说明与 `tools/verify_release.py`，许可归属文档的 Mac 链接改为仓库 URL。
- 更新 `tests/test_distribution.py`，新增缺失运行文件和错误包类型回归；原打包测试扩展为两包入口隔离、目录隔离、许可及私人数据边界、版本元数据与迁移说明检查。

### 测试与验证

- 全量自动测试 **234 项通过，9.611 秒**，`artifacts/split-packages-tests.txt`。最终 EXE 重新构建；遇到本次源码测试进程占用音频助手，清理已核验路径的测试实例后重建通过，未终止 QQ 音乐。
- QQ 专用 ZIP 从中文路径完整解压、移除开发环境 PATH 后，实际 BAT 启动 4 项检查通过：原生窗口、版本、真实 QQ 连接与歌词同步，`artifacts/split-qq-public-20261011/qq-public-report.json`。检查只读，不强制暂停或切歌；暂停冻结由本轮先前真实 QQ 6 项采集核验。
- 网易云专用 ZIP 的隔离安装／更新／重复卸载、设置／字体／预设／令牌／框架保留、安装／卸载原生 BAT 窗口及普通 BAT 验证全部通过，成品静音 75 项通过，`artifacts/split-netease-public-20261011/release-report.json`。真实网易云客户端当时未运行，不需要重启。
- 原本机 4 个实际设置／预设／联动配置文件的 SHA-256 保持一致，`artifacts/split-packages-state-preservation.json`。两包 ZIP 与校验文件一致、EXE 一致、无私人配置，`artifacts/releases/split-package-integrity.json`：QQ 307 项、70,476,646 字节；网易云 311 项、70,483,478 字节。

### 影响与限制

- 从旧通用包迁移到新的播放器目录时需复制 `.state`；网易云程序路径变化后需重新安装联动。不会自动在两套独立目录之间同步设置，同一时间只运行一个歌词实例。
- 本轮没有第二台干净电脑、新的网易云实曲播放或更多 QQ 版本验收。QQ 官方搜索仍可能拒绝某些歌曲，无法可靠匹配时提示重试／保持空白；没有宣称所有歌曲全面支持。Mac 公开包保持原样。

## 2026-10-11：修复 QQ 组合搜索失败后无法显示歌词

### 改动

- 排查用户本机没有效果：QQ 音乐在运行但歌词程序未启动；实际打开 QQ 联动后，官方组合搜索返回 2001，而仅歌名查询返回正确歌曲。
- `qqmusic_lyrics.py` 在组合搜索失败或没有可靠结果后，依次回退仅歌名及歌手在前的搜索（最多三种不同查询）；全部歌手、专辑、版本与时长校验不变，合并已知候选以保留歧义，不循环请求。
- `tests/test_qqmusic.py` 新增 6 项回归，覆盖错误码回退、空结果、错误版本、歧义与有界失败。应用更新为 `0.7.0-beta.2`；README、QQ 指南、成品使用说明和版本文档明确需要单独启动，不随 QQ 自动出现。

### 测试与验证

- 原生 Windows 最终全量自动测试 **232 项通过，9.506 秒**，`artifacts/qq-search-fix-final-tests.txt`；受限沙箱首次运行出现临时文件替换与本地连接权限错误，改在原生环境重跑通过，没有跳过失败测试。
- 真实 QQ 22.52 当前歌曲 45 秒采集 6 项通过，`artifacts/qq-search-fix-live-20261011/qqmusic-report.json`；收到 Between Two Worlds (Let's Lament) 的 76 句歌词，效果切换不改变播放，暂停进度冻结。没有发送 QQ 播放、暂停、切歌或进度命令。
- Windows 源码实际 BAT 静音验证 75 项通过，初次统一成品的普通 BAT 静音验证也为 75 项通过。首次成品 QQ 检查发现 Compass 的前两种查询也被拒绝，且播放期间没有暂停样本；没有发布该中间包。
- 增加第三种查询后，实际官方歌词读取 Between Two Worlds (Let's Lament) 76 句／Compass 35 句通过，`artifacts/qq-search-fix-two-songs.json`；实际源码 BAT 打开修复版，当前 Between Two Worlds (Realm of Darkness) 已同步 88 句，`artifacts/qq-search-fix-current-window.json`。按用户新要求，两份独立成品的验证记录放入后续分包改动。

### 影响与限制

- 此回退只改善匿名搜索查询，不保证所有接口限制或所有歌曲均可用。无法唯一匹配仍保持空白并提示；QQ 逐字演唱时间及其他版本实测范围不变。
- QQ 联动仍为需手动启动的桌面伴侣；没有安装到 QQ 内部，没有添加自启动。本轮不重做网易云实曲试听或第二台干净电脑验证。

## 2026-10-11：新增 Windows QQ 音乐只读联动

### 改动

- `qqmusic.py`、`native/qqmusic_smtc.ps1` 只读跟随 QQMusic.exe 的系统媒体会话，以实际时间轴同步进度、暂停和切歌；客户端重启或会话不可用时清空旧歌词并等待重连。
- `qqmusic_lyrics.py` 在线程中访问 QQ 官方匿名接口，严格匹配歌名、全部歌手、专辑和时长，读取整句 LRC 与中文译文；保留歌手大小写及显示顺序，避免实机搜索拒绝。防止旧请求覆盖新歌，最多缓存 32 首，失败可手动重新获取。
- `main.py`、`controls.py`、`process_audio.py` 加入 QQ 独立入口与对应来源文案、重试按钮和进程音频捕获，复用现有主题、字体、参数、动画及预设。版本为 `0.7.0-beta.1`；网易云协议及插件版本不变。
- 源码及成品新增 `启动QQ音乐联动.bat`；更新 `build.ps1` 收集读取助手。实机遇到旧进程占用后，构建增加运行检查和整目录原子重命名，避免 PowerShell 部分移动旧目录。更新 README、QQ 说明、使用说明、技术文档及对应测试。

### 测试与验证

- 最终完整自动测试 **226 项通过，10.475 秒**，`artifacts/qq-all-tests-delivery.txt`；`tests/test_qqmusic.py` 覆盖来源过滤、时间轴、歌词严格匹配、译文、旧请求、断开、缓存、重试、暂停、跳转、界面及打包入口。
- QQ 22.52 真实静音回归通过：播放推进、原生进度条跳转、暂停冻结、切换到 Fly, My Wings 后返回原歌、效果设置不修改播放。恢复原歌暂停约 3 秒，原位置 3.622 秒，恢复 3.113 秒；临时静音撤销。记录 `artifacts/qq-live-final-regression-20261011/`。
- `启动.bat -Smoke -ForceSource` 原生 Windows 75 项通过；重新打包后的独立中文解压路径，网易云成品安装／更新／重复卸载、设置／字体／预设保留和两个安装 BAT 及普通启动 BAT 验证通过，成品原生 75 项通过。记录 `artifacts/qq-public-final-20261011/`，移除开发环境 PATH，不等于干净电脑验证。
- 新版 ZIP 中的 QQ 联动 BAT 实际启动通过，6 项真实 QQ 检查通过（独立中文目录、无开发环境 PATH）：`artifacts/qq-public-qq-entry-verified-20261011/`。公开包 314 项、70,482,176 字节，SHA-256 `84609fb2e528cb4f186db4bc43d605f3aa80257281a2cdff468e2e99a7b1c4f5`。

### 影响与限制

- QQ 采用独立桌面伴侣入口，不修改客户端，不需要 BetterNCM，不自动随 QQ 启动。暂无 QQ 逐字演唱时间；严格匹配失败、网络失败或无歌词会明确提示／保持空白。会员试听、其他 QQ 版本、第二台电脑与 QQ macOS 均未全面验收。
- 网易云本体恢复正常启动，原插件入口保留；本轮网易云真实歌曲播放未重做，采用现有自动回归和成品安装验证。Mac 公开包仍为原版本，不发布虚构的 Mac QQ 支持。

## 2026-10-11：记录最终 Mac 双架构公开包验证

### 改动

- 更新 `MACOS.md`、Mac 发布说明与验证记录，保存实际公开包源码、下载版本、大小、SHA-256 与两种芯片的原生启动结果；附件采用通过全部检查的最终构建。

### 测试与验证

- 工作流 `38070395911` 成功，源提交 `e611829`；Mac arm64 / x86_64 各 93 项通过（2.607 / 11.464 秒），两份解压后的冻结应用启动报告均通过。压缩包各 529 项，内置运行依赖、框架链接、执行权限及中文路径检查通过。
- 下载后在本机复核 ZIP / SHA-256 及许可来源清单，两个包均通过；保存至 `artifacts/releases/`。最终全量 207 项通过，8.959 秒，`artifacts/mac-package-release-record-tests.txt`。

### 影响与限制

- 预发行版本 `v0.6.0-beta.2-macos.1`，真实网易云播放与用户电脑上的 Gatekeeper / Finder / Spaces 仍待验收。既有 Windows 公开 ZIP 保持不变。

## 2026-10-11：增加 Mac 成品下载入口与发布说明

### 改动

- README 首屏增加 Apple Silicon / Intel 两个 Mac ZIP 入口；`MACOS.md` 区分普通用户应用包与源码安装，说明外部工具、数据迁移、更新卸载及未公证应用的首次打开方式。增加 Mac 发布说明、文档链接回归和实际成品验证记录。
- 发布前核对 Mac 许可来源清单，使用实际 Python 版本和对应架构 NumPy 许可摘要替换 Windows 的运行时元数据，新增清单一致性测试；工作流只在包内文件或代码变化时重建，发布记录更新不重复构建。

### 测试与验证

- Mac 实际工作流 `38069875108` 成功，两端各 92 项测试通过；冻结应用、ad-hoc 签名、529 项 ZIP 审计、中文路径及解压后 LaunchServices 原生 Cocoa 启动通过。已查看原生窗口截图；成品大小、SHA-256 与测试边界详见验证记录。
- 下载说明及许可清单回归更新后，Windows 全量 207 项通过，9.104 秒，`artifacts/mac-package-public-tests.txt`；公开包在修正清单后重新构建与验证。

### 影响与限制

- Mac 附件为 `v0.6.0-beta.2-macos.1` 预发行；已有 Windows 下载继续使用原版本。需单独安装 nowplaying-cli，未做 Apple 公证，真实网易云歌曲与用户电脑的权限 / Finder / Spaces 行为待试用。

## 2026-10-11：修复 Mac 压缩包中文文件名校验

### 改动

- `tools/package_macos.py` 显式使用 UTF-8 读取 ditto 的 ZIP 文件名；ditto 未设置 ZIP 的 UTF-8 标志，默认解码会把中文应用名及说明误读为乱码。增加去除编码标志的真实结构回归测试。

### 测试与验证

- 首轮 Mac 双架构均成功构建 `.app` 并通过 ad-hoc 签名校验，压缩包审计因上述编码误判失败，未执行启动验证、未公开包。下载失败产物核验了原始与 UTF-8 文件名的差异。
- 修复后 Windows 全量 205 项通过，9.964 秒，`artifacts/mac-package-encoding-tests.txt`；两份真实 ditto 产物重新审计通过（各 529 项）。

### 影响与限制

- 只修正审计器，不改动 Mac 压缩包的链接结构或 Windows 行为。远端成品验证通过前不发布附件。

## 2026-10-11：制作 Mac 双架构实验应用压缩包

### 改动

- 新增 `CityEchoes.spec`、原生 Mac 构建／压缩包审计／LaunchServices 验证工具及双架构工作流；生成内置 Python、Qt 和 NumPy 的 `.app`，用 ditto 保留框架链接和执行权限，剔除个人数据与外部播放读取工具。
- 冻结 Mac 应用将设置、字体和预设保存在 `~/Library/Application Support/CityEchoes/`，源码版保持原 `.state`；新增显式隔离的静音验证入口及包内安装播放读取工具、使用说明。
- 公开包标为 `macos.1` 实验构建，分别提供 arm64 和 x86_64；新增发布边界、缺失 QtCore、执行权限、路径和持久数据回归测试。

### 测试与验证

- 本机全量 204 项通过，26.066 秒，日志 `artifacts/mac-package-all-tests.txt`；实际 BAT 静音集成通过，报告 `artifacts/mac-package-windows-20261011/smoke-report.json`、`passed=true`、Qt `windows`。远端 Mac 原生构建与成品验证在发布前补齐，当前不宣称已有可下载成品。
- 为手写 Mac spec 添加 Git 忽略例外及源码边界检查后，最终全量 204 项通过，17.603 秒，`artifacts/mac-package-final-tests.txt`。

### 影响与限制

- 不改动现有 Windows ZIP。Mac 仍需通过 Homebrew 单独安装 `nowplaying-cli`；应用采用 ad-hoc 签名，未做 Apple Developer ID 公证。模拟数据的成品启动验证不等于真实网易云播放验收。

## 2026-10-11：记录 macOS 双架构 CI 与源码安装方式

### 改动

- `README.md`、`MACOS.md` 与 `验证记录.md` 记录 Intel / Apple Silicon 实际 CI 结果，增加主分支源码 ZIP 入口，明确区分自动测试与尚未完成的真机播放验收；更新文档回归检查，防止安装指南遗漏这一限制。

### 测试与验证

- 修复提交 `c9bb004` 的 GitHub Actions 两次工作流均成功；macOS 15.7.9、Python 3.12.10 下，Apple Silicon 81 项通过（3.024 秒）、Intel 81 项通过（11.415 秒），安装依赖与脚本语法检查通过。
- 更新安装和验证说明后，最终 Windows 全量 194 项通过，9.671 秒，日志 `artifacts/mac-integration-final-all-tests.txt`。

### 影响与限制

- 合入主线的是带来源署名的实验源码支持；Mac 安装包、真实网易云播放、Finder、权限与 Spaces / 全屏尚待验收。现有 Windows 下载包保持不变。

## 2026-10-11：固定 macOS 回归测试时钟

### 改动

- `tests/test_macos.py` 的歌词偏移回归改用注入的固定时钟，继续精确验证偏移只影响歌词时间、不改变播放器进度。真实 macOS 的高精度时钟使原测试在两次断言之间前进不足 1ms；生产代码无需调整。

### 测试与验证

- 第一轮 GitHub Actions 在 Apple Silicon 和 Intel 上均完成 81 项测试，仅上述精确时间断言失败；依赖安装、脚本语法及其余 80 项通过。后续重跑结果记录于 `验证记录.md`。
- 固定时钟后 Windows 全量 194 项通过，10.237 秒，日志 `artifacts/mac-integration-clock-all-tests.txt`。

### 影响与限制

- 仅修正测试的确定性，保留真实播放时钟的正常插值。macOS 真机音乐播放验收仍待完成。

## 2026-10-11：整合社区 macOS 适配并增加贡献署名

### 改动

- 在当前 Windows 主线基础上迁移 `qingyin-alice-zhong/mac-version` 的平台方案，固定来源提交 `5109df2c99ee87ee6ad5370fed70fa5d880336a5`；新增 `main_mac.py`、`macos_netease.py`、Bash 安装／卸载与 Finder `启动.command` 入口。README 增加贡献者，整合提交保留共同作者署名。
- 平台字体分别采用 Windows 微软雅黑／宋体／楷体和 macOS 苹方／宋体／楷体，主题字体与安静办公预设按平台选择；保留 Windows 的 Tool 窗口标志与原生焦点保护，macOS 使用 Qt 的失焦可见属性，增加无托盘时的面板恢复路径。
- 修正参考分支中的可靠性问题：耗时操作移到后台、有界任务和歌词缓存、丢弃切歌后的旧请求、网络失败重试、严格匹配歌曲身份、复用原文逐字范围和翻译回退；歌词偏移独立于歌曲进度，零偏移可恢复，偏移文件原子保存且损坏不覆盖。
- 不复制未标明构建来源的外部二进制，不新增 `requests` 或 PyObjC 依赖；联网使用标准库，外部 `nowplaying-cli` 通过 Homebrew 单独安装。macOS 不伪造音频强弱，首次使用轻波浪；播放控制留在音乐客户端。
- 新增 `MACOS.md`、第三方来源记录、25 项适配器／界面／脚本测试及 Intel / Apple Silicon macOS CI；安装器明确只接受当前 NumPy 支持的 Python 3.10–3.12，更新和卸载保留 `.state`。

### 测试与验证

- 最终全量 **194 项自动测试通过，12.279 秒**，日志 `artifacts/mac-integration-all-tests.txt`；其中 macOS CI 所用的 81 项测试组在本机全部通过，2.112 秒。
- 实际 `启动.bat -Smoke -ReportDirectory "$PWD\artifacts\mac-integration-windows-20261011"` 通过，报告 `passed=true`、Qt 平台 `windows`、DPR 1.5；原生窗口可见、任务栏身份、点击穿透、不抢焦点、置顶、暂停冻结、进度跳转、字体／主题／预设与译文保持歌曲进度均通过。
- 标准发光暖缓存 P95 9.194ms、卡门 4.875ms，四种动画加同步开关的八组 P95 3.195–6.194ms，均满足 33ms 目标。已查看最小窗口底部截图，底栏和设置可访问。
- Bash 逐文件语法检查与 Windows 拒绝运行 Mac 安装脚本检查通过。macOS CI 运行状态与进一步实际结果在验证记录中单独记录，不把配置了 CI 写成已通过真机播放。

### 影响与限制

- 本轮为源码整合，应用版本和既有 Windows 公开 ZIP 保持 `0.6.0-beta.2`；没有制作或发布未经验证的 Mac 成品包。
- 尚未完成 Mac 真机网易云播放、Finder 双击、权限、跨 Spaces / 全屏和长时间运行验收。macOS 仍为实验支持，系统来源缺失时不能保证 Now Playing 信息来自网易云，在线歌词接口也不保证长期稳定。
- 本轮 Windows 验证为实际源代码入口静音集成，网易云协议与播放器回调没有改动；未新增真实联网歌曲播放结论。GitHub 自动贡献统计需相关提交进入默认分支，README 与共同作者署名已提供。

## 2026-10-09：公开安装包更新至 0.6.0-beta.2

### 改动

- 将已完成的图书馆预览文案打入公开 Windows x64 成品，版本升级为 `0.6.0-beta.2`。新文件为 `dancing-lyrics-0.6.0-beta.2-windows-x64.zip`；保留旧版附件，README 下载和演示入口指向新版本。
- 同步 `app_info.py`、README、网易云说明、产品／技术文档、成品使用指南和发布说明。新增版本一致性测试，校验下载标签、ZIP 名称、演示链接、包内说明与应用版本，避免只更新源码而遗漏下载入口。
- 同一个 ZIP 延续 `3.1.40.205461／3.1.41.205529` x64 的自动识别与安装；插件版本保持 0.1.4。

### 测试与验证

- 全部 169 项自动测试通过，8.647 秒，日志 `artifacts/beta2-all-tests.txt`。初次沙箱运行受临时文件原子替换与本地网络限制而失败；在 Windows 原生环境重跑全部通过，原始日志保留为 `artifacts/beta2-sandbox-tests.txt`。
- `build.ps1 -SkipDependencies` 成功构建；发布 ZIP 为 70,454,992 字节，SHA-256 `cf48be48307febe945047ee16474e8b13206cfbab731c0a0bed79d0062fd93e2`，CRC 与个人数据排除检查通过。
- 使用两版真实客户端 EXE 的版本资源，分别从新的中文／空格路径解压公开 ZIP，以独立英文框架目录验证，`beta2-public-3140`／`beta2-public-3141` 各通过 8 项：安装、覆盖更新、卸载、重复卸载、个人数据与共用框架保留、安装／卸载 BAT 原生窗口、启动 BAT 完整静音集成检查。移除开发 PATH，不依赖外部 Python。
- 两次原生静音检查均通过，DPR 1.5，默认及最小窗口、滚动访问、字体材质、动画、暂停与跳转检查通过。标准发光 P95 分别为 8.793／8.079ms，卡门为 5.713／3.666ms，八种动画同步组合为 3.392–6.430／2.984–5.844ms，均低于 33ms。
- 已查看成品中的新文案、卡门预览和最小窗口版本号；正常设置与连接配置哈希在构建前后相同，`artifacts/beta2-user-preservation.json` 通过。恢复正常网易云和后台歌词引擎。

### 影响与限制

- 本次更新面向公开包版本及下载指引。真实播放协议没有改动，两版网易云歌曲回归沿用上一版的实际验证结果；本轮原生检查为安装入口和静音成品验证，不冒充新的联网播放测试。
- 尚未完成第二台干净电脑／虚拟机试装；本机移除开发 PATH 不能替代该项。网易云支持范围仍为上列两个完整构建号。


## 2026-10-09：效果预览采用图书馆文案

### 改动

- 按用户图片，将面板效果预览文案统一改为“啊，对了！但丁。有一天，去一趟图书馆吧。”，白芯发光、卡门的声音、经典纯色和各动画共用 `EFFECT_PREVIEW_TEXT`。
- 逐字强调预览按新文案重新生成演示时间，标点不参与演唱强调；更新无障碍描述及演示提示。卡门静态验证截图与 README 深浅底预览图同步采用新文案。
- 更新 `app_info.py`、`controls.py`、`effect_validation.py`、界面测试及当前产品／技术说明；保留现有绘制、动画和音乐同步方式。

### 测试与验证

- 全部 168 项自动测试通过，8.542 秒，日志 `artifacts/preview-quote-tests.txt`。新增检查覆盖三种文字材质、五种动画、700px／240px 预览宽度下的完整文案，以及新文案的逐字时间、标点排除和有效范围。
- `build.ps1 -SkipDependencies` 成品构建成功；实际 `启动.bat -Smoke` 全部通过，报告 `artifacts/preview-quote-smoke/smoke-report.json`，Windows 原生面板可见，DPR 1.5，默认／最小窗口、滚动访问、字体、材质、暂停和跳转验证通过。已查看实际卡门效果及面板预览截图。
- 本机 EXE 更新并恢复正常网易云启动；设置与连接令牌哈希不变，预设和导入字体保留。记录 `artifacts/preview-quote-user-preservation.json`。

### 影响与限制

- 改动面向效果预览文案及其演示时间，网易云真实歌词、翻译和播放协议保持现有处理。公开 `v0.6.0-beta.1` 发布附件保持原文件，本次成品更新位于本机 `dist/FloatingLyrics`。


## 2026-10-09：双版本网易云兼容与都市回响新版发布包

### 改动

- 应用升级至 `0.6.0-beta.1`，同一个 Windows x64 ZIP 自动识别 `3.1.40.205461` 和 `3.1.41.205529`。安装器、原生开发脚本、插件清单与 WebSocket 白名单统一支持两个构建号，安装记录保存实际版本。
- 真实检查发现 3.1.40 的共享歌词状态没有歌曲 ID；插件按 ID 只读网易云自己的本机缓存并复用其格式化函数，校验缓存 ID、隔离切歌世代并丢弃迟到响应。3.1.41 保留已有状态 ID 校验。继续订阅客户端原有进度事件，不覆盖播放回调、写缓存或新增歌词服务。
- BetterNCM 1.3.4 无法可靠解包中文数据路径，安装器和开发脚本提前拒绝并提示使用默认 `C:\betterncm` 或英文路径；应用与客户端的中文路径继续支持。
- 扩展安装／协议、旧版缓存隔离和客户端验证器测试。开发验证器通过实际模块导出定位歌曲详情，兼容两版进度控件；缺少控件或加载失败时明确失败，不以零进度或模拟数据代替。新增真实译文开关及保存、播放锚点不变的集成断言。
- 更新 README、网易云说明、产品／技术文档、发布说明、使用指南与验证记录，附深浅底色的卡门实际渲染预览。公开 ZIP 排除个人设置、令牌、字体、预设、日志和开发环境。

### 测试与验证

- 全部 166 项自动测试通过，最终 8.054 秒，`artifacts/city-final-all-tests.txt`。新增／扩展覆盖两个完整构建号、实际安装记录、重复更新令牌保持、非英文框架路径拒绝、跨歌曲迟到缓存、客户端偏移迁移和两种原生进度控件。
- `build.ps1 -SkipDependencies` 完成成品构建；实际 `启动.bat -Smoke` 的 100%／125%／150% 检查全部通过，报告 `artifacts/city-final-scale-*`。默认／最小窗口、三种主题、滚动表单、固定底栏、字体、暂停与跳转通过；已查看实际截图。卡门双句暖缓存 P95 为 4.492／4.352／4.626ms，八种动画同步组合范围 1.706–4.539ms，全部低于 33ms。
- 真实 3.1.40 `artifacts/city-live-3140-cache` 和 3.1.41 `artifacts/city-live-3141-final` 各通过引擎 29 项、宿主 10 项及原生鼠标入口 3 项；各 364 采样、21 次重定位。真实英文 8 行／40 时间单位、中文 19 行／131 单位，演唱强调峰值 1.0；进度、暂停画面、跳转、连续三次切歌、整句／纯音乐回退和参数／预设／主题切换不改变播放均通过。真实译文 33 行的句首时间保持，开关保存、原文恢复和播放锚点不变通过。
- 同一个公开 ZIP 在 `artifacts/city-public-3140`、`city-public-3141` 各完成 8 项安装／覆盖更新／卸载／重复卸载／实际双击入口检查。移除开发工具 PATH，在中文与空格应用／客户端路径运行；保留设置、字体、预设、令牌和共用框架。安装记录分别识别正确完整版本，公开 BAT 的静音检查也通过。
- ZIP 大小 70,454,791 字节，SHA-256 `476ec47aca03d520f4e55bd87481992817edd247e554b4e988ed2cc2c012f663`；CRC 通过。正常 `settings.ini` 与 `netease-bridge.json` 哈希不变，原本为空的字体目录和不存在的预设文件未新增；非空保留由隔离更新／卸载检查验证。正常 3.1.41 和后台歌词引擎已恢复，无调试端口。

### 影响与限制

- 兼容范围为本机 Windows 11 x64、以上两个完整客户端构建号、BetterNCM 1.3.4；3.1.40 使用官方签名安装包的隔离客户端副本，不覆盖正常 3.1.41。未完成第二台干净电脑／虚拟机、3.1.40 新系统完整安装和长期稳定性检查，保持预发行版。无可确认歌词缓存的旧版歌曲保持等待，不把其他歌曲的共享歌词当成当前歌词。
- 初轮隔离副本误将 `redist_packages` 中旧 VC 运行库复制到主目录，加载框架崩溃；测试副本恢复正常运行布局，使用本机系统 VC 运行库 14.51.36247.0 后通过。中文框架路径、初始更新弹窗及验证器字段差异的失败证据保留，最终没有弱化真实播放断言。ZIP 不分发网易云、BetterNCM DLL 或修改过的客户端文件。


## 2026-10-09：中文译文优先显示

### 改动

- “显示与文字”新增默认关闭的“有中文翻译时优先显示译文”，立即应用和保存。每句无可靠中文译文时保留原文；歌词语言独立于效果预设。
- 插件 0.1.4 仅增加可选 `translation` 字段，读取客户端 `tlyricLines`，根据已经应用偏移的原文时间对齐；迟到译文触发更新，切歌清除旧内容。旧插件无需译文字段仍可使用。
- 原文和 YRC 保存在模型中，显示译文的句子不套用原文字词时间，按整句动画显示；保留空白边界、用户同步偏移与纯音乐处理。新增协议、逐句回退、偏移、迟到更新、暂停、设置和预设独立性测试。

### 测试与验证

- 全部 162 项自动测试通过，8.677 秒，`artifacts/translation-tests.txt`；实际 BAT 静音入口 `artifacts/translation-smoke` 通过，开关保存、演示译文重建、暂停时钟和小窗口滚动访问均通过。
- 真实 3.1.40 和 3.1.41 客户端均读取《Fly, My Wings》的 `tlyricLines`，与原文 `lyricLines` 时间一致，例如首个演唱句 13.535 秒；两个版本分别定位到原生详情模块 14/Oh 与 15/ji。证据在 `artifacts/compat-3140/translations.json`、`translations-41.json`，检查后恢复原播放队列和正常客户端。

### 影响与限制

- 不调用外部翻译服务、不修改网易云播放回调；译文演唱强调保持关闭，因为原文时间不能可靠映射译文。客户端 3.1.40 的完整插件播放回归与最终成品验证继续在兼容性改动中完成。

## 2026-10-09：卡门的声音发光风格

### 改动

- 在“白芯发光”内加入“发光风格 → 卡门的声音”，采用固定暖白 `#ffe6bd` 字芯、柔和琥珀描边与金色 `#ffb655` 光晕；强度仍可调，原有颜色保留。经典纯色和标准白芯保持现有效果。
- 新增 `glow_variant` 设置与预设保存，旧设置默认 `standard`；桌面与预览共用材质、渐隐、逐字动画和缓存，扩大卡门光晕布局边界。
- 新增设置、界面、预设和像素测试；静音验证加入真实样式切换、保存、暂停不变、深浅背景截图与独立暖缓存性能检查。

### 测试与验证

- 全部 157 项自动测试通过，7.948 秒，`artifacts/carmen-final-tests.txt`。首次沙箱运行受到原子替换和本机 WebSocket 限制，原生 Windows 重跑全部通过。
- 实际 `启动.bat -ForceSource -Smoke` 通过，`artifacts/carmen-final-smoke-fixed`；原生窗口、默认／最小尺寸滚动访问、暂停和跳转检查通过，DPR 1.5 下卡门双句暖帧 P95 为 4.907ms，复用缓存且低于 64MiB。
- 已查看真实渲染的 `carmen-dark.png`，同时生成浅色与透明底效果。验证截图曾使用临时 QImage 的缓冲引用而崩溃，现已改为保留图像对象后读取，最终入口退出码 0。

### 影响与限制

- 卡门风格仅改变歌词材质，不改变网易云播放接口；字体、动画、用户颜色和预设继续保留。更多缩放与两版本播放回归随最终发布包一起复核。

## 2026-10-09：应用更名为都市回响

### 改动

- 窗口、侧栏、托盘、网易云入口、安装界面及当前使用文档统一采用“都市回响”；应用名由 `APP_NAME` 管理。插件显示名称一起更新。
- 保留 `FloatingLyrics.exe`、插件 slug、连接协议、任务栏身份和用户设置目录，更新继续使用原设置、字体与预设。修正 BAT 启动器中的 Unicode 转义窗口标题匹配，并新增界面及安装身份回归检查。

### 测试与验证

- 全部 152 项自动测试通过，最终耗时 7.744 秒，日志 `artifacts/city-name-final-tests.txt`。
- 实际 `启动.bat -ForceSource -Smoke` 通过，报告 `artifacts/city-name-smoke-final`；Windows 原生新名称面板可见，主题、布局、静音播放及暂停／跳转检查通过。
- 首次启动器仍匹配旧名称的 Unicode 转义文本，导致应用自行检查通过但启动器报错；已修正并补测试，最终入口退出码 0。

### 影响与限制

- 本轮完成显示名称更新，仓库地址、EXE 文件名及已有安装身份不变；新版发布包将在后续功能与兼容性验证全部结束后统一生成。

## 2026-10-08：README 使用创作者提供的实机演示 GIF

### 改动

- 将用户提供的《演示.mp4》完整转换为 `docs/images/lyrics-demo.gif`，替换首页原有预览动图；README 图片说明改为网易云联动与桌面歌词实机演示，并说明无声循环播放。
- 保留原视频的 16:9 画面和全部时长，输出 960×540、15fps、128 色 GIF。新增两项文档／媒体测试，检查首页内嵌位置、完整帧解码、有效帧时长、循环、画面变化、比例和文件大小。
- 更新 `验证记录.md`，记录转码参数及实际媒体检查结果；没有新增程序运行依赖。

### 测试与验证

- `.venv/Scripts/python.exe -m unittest discover -s tests -v`：150 项全部通过，耗时 7.398 秒，日志为 `artifacts/readme-gif-tests.txt`。
- Qt 逐帧解码与 FFmpeg 全文件解码通过；输出 276 帧、总时长 18.400 秒、无限循环，文件 5,982,543 字节。已查看 GIF 的首帧、中间帧和末帧，确认完整画面与歌词效果保留。
- 文档更新后复核相关文档测试和本地链接，提交前检查 Git 差异及空白错误。

### 影响与限制

- 本次仅更新公开演示素材、README、测试和记录；应用版本、已发布 ZIP、用户设置及网易云播放行为保持当前状态。
- GIF 不支持音轨，播放采用 15fps 和缩小后的 960×540 画面；原视频未修改。未重新运行启动／播放集成检查，本次没有改动程序或启动入口。

## 2026-10-07：增加便携安装入口并准备首次公开试用版

### 改动

- 应用升级到 `0.5.1-beta.1`。`netease_install.py` 与 `installer_ui.py` 将安装／卸载封装进成品 EXE，提供原生窗口、客户端自动寻找、完整版本及 x64 检查、官方 BetterNCM 1.3.4 下载和 SHA-256 校验、管理员重试、原子写入及失败回滚；通过 `--install-netease`／`--uninstall-netease` 调用。记录安装目录，重装复用本机令牌；卸载仅删除指向本程序的插件，保留共用框架、设置、字体和预设。
- `build.ps1` 将无连接令牌的三个插件模板放入成品；`tools/package_netease.py` 复用安装器打包逻辑。`release` 提供安装、卸载、独立启动 BAT 和使用说明；入口失败保留提示。`tools/package_release.py` 只打包 EXE、运行目录、入口和许可，剔除 `.state`、预配置插件、日志、开发环境及未使用的 Qt PDF／Virtual Keyboard 组件，并生成 SHA-256。首次公开包约 67MiB。
- 新增 MIT、第三方归属与完整运行组件许可；只从官方固定版本单独下载 BetterNCM，不装入 ZIP。README 首屏添加动图、成品下载和三步安装说明；新增 Issues 模板、传播文案、原生公开包验证器及 30 秒无音乐演示制作工具。音乐协议、歌词、动画及纯音乐处理沿用原逻辑。

### 测试与验证

- Windows 全部自动测试最终 148 项通过。新增 16 项覆盖中文／空格路径、重复安装、网络失败、散列错误、不兼容／x86 客户端、失败回滚、损坏配置、目录记忆、所有权检查、用户数据保留、公开包内容和许可原字节；扩展文档校验。上游许可通过 Git 属性保留原始空白及来源散列，不进行项目格式化。实际完整版本字符串是 `3.1.41.205529`，数字资源的构建段会截成 `8921`，安装器已正确读取 Windows 的字符串资源并用独立原生版本读取验证。
- `build.ps1 -SkipDependencies`、源码实际启动器静音检查及成品 100%／125%／150% 的实际 `启动.bat -Smoke` 均通过，原生窗口、三种主题、默认／最小窗口、滚动及固定底栏正常；报告在 `artifacts/release-source-smoke` 和 `artifacts/release-launcher-*`。发光暖帧 P95 分别为 15.452／17.237／22.767ms，八种动画同步组合也均 ≤33ms。精简后的最终公开 ZIP 还通过三个 DPR 的同样完整检查，记录见验证记录；首次构建替换目录因旧引擎占用失败，退出旧进程后构建成功。
- `tools/verify_release.py` 对最终公开 ZIP 清除 Python／开发工具 PATH 后独立解压，安装、覆盖更新、卸载、重复卸载及三个 BAT 原生入口均通过；用户数据、令牌和共用框架保留。最终报告为 `artifacts/release-public-verified/release-report.json`。官方框架实际在线下载散列通过。程序本身在 EXE 内携带 Python，不依赖系统 Python。
- 真实网易云 `artifacts/release-netease-confirmed` 引擎 24 项、宿主 10 项及鼠标入口 3 项均通过，347 个采样、21 次重定位，真实演唱强调峰值 1.0；中英文 YRC、整句和纯音乐回退、进度、暂停、跳转、连续切歌及设置／预设切换不改变播放均通过。首次把初始化绘制基准合并到播放采样时，采样错过了逐字时间区间，仅“实际强调已观察”未通过；保留 `artifacts/release-netease-verified`，将已单独通过的绘制检查与真实播放采样分开后全部通过，未降低功能断言或改歌词协议。
- 30 秒 H.264 演示为 1280×720、900 帧／30fps，无歌曲音频；全文件解码及抽帧通过。安装截图使用原生窗口绘制，避免其他桌面窗口遮挡或进入公开素材。正常网易云及后台歌词引擎已恢复；`artifacts/release-user-preservation.json` 证明正常设置及连接配置 SHA-256 不变。

### 影响与限制

- 首次发布仅声明本机已验证的 Windows 11 x64、网易云 3.1.41.205529 x64、BetterNCM 1.3.4；不兼容客户端拒绝安装，不覆盖不同版本的框架。安装到长期保留且可写的目录；移动程序或更新后重新安装联动，退出网易云后再安装／卸载。
- 本机独立解压并移除开发环境路径不等同于干净电脑验证。尚无第二台无开发环境电脑或干净虚拟机的实测；朋友试装、Bilibili 投稿和群消息由创作者后续完成。发布为预发行版，保留上述边界；源码、标签与公开下载通过指定 GitHub 仓库发布。

## 2026-10-07：新增黑金特殊主题与但丁钟头运行图标

### 改动

- 应用升级到 `0.5.0`，保留默认主题和深色主题，新增“特殊主题”。`themes.py` 增加黑金配色、琥珀控件、切角双层边框及机械图纸底纹；`controls.py` 使用仅在该主题绘制装饰的框架，沿用原页面、滚动和底栏布局。新增透明矢量资源 `assets/dante-clock.svg`、`assets/special-blueprint.svg`。
- 特殊主题同时替换侧栏、窗口、运行中 Windows 任务栏和系统托盘图标，后台仍为但丁钟头；切回默认或深色主题恢复原红色波形。`settings.py` 接受 `theme=special`，即时保存并在重启时恢复，旧配置及无效值继续使用默认主题。歌词材质、预览背景、字体、动画、效果预设和音乐播放独立。
- `app_info.py`、`main.py` 在窗口创建前设置稳定的 Windows 任务栏应用标识，避免源码窗口使用 Python 分组图标。扩展 `validation.py` 和 `netease_validation.py`，检查实际 HICON 位图切换／恢复、应用／窗口／托盘图标一致及三种主题的原生布局。新增图标尺寸、透明背景、保存重建、原主题像素恢复、原生调用边界及文档测试，更新使用和设计文档，重新打包。

### 测试与验证

- Windows `.venv/Scripts/python.exe -m unittest discover -s tests -q`：最终 132 项全部通过，包含设置、界面、图标、字体、绘制、歌词同步、插件、启动及协作文档检查；实际结果见 [验证记录](验证记录.md)。
- `build.ps1 -SkipDependencies` 成功，旧包备份为 `artifacts/previous-package-20261007-220255-273`。最终包通过实际 `启动.bat -Smoke` 验证，报告为 `artifacts/special-launcher-100`、`special-launcher-125`、`special-launcher-150`；实际 DPR 为 1.0、约 1.25、1.5，三套主题在默认／最小窗口全部可访问，底栏、原生可见性及图标切换恢复均通过。已查看实际页面、最小窗口、125% 截图和任务栏钟头截图。
- 最终 150% 八种动画组合暖帧 P95 为 11.280–18.181ms，原有发光基准为 26.227ms。真实网易云最终 `artifacts/special-netease-verified` 的引擎 34 项、宿主 10 项、真实鼠标入口 3 项全部通过；75 秒记录 255 样本、21 次重定位。中英文 YRC、整句和纯音乐四类歌曲进度正常，连续三次切歌稳定；主题保存、原生图标恢复、暂停冻结、跳转和最小化继续正常，主题切换不改变播放锚点、歌词文档或预览。播放负载下发光 P95 为 26.852ms，八种动画组合为 13.926–21.837ms。
- 首轮源码窗口 HICON 正确，但实际任务栏仍显示 Python 图标；补上独立应用标识后最终包原生检查与截图通过。首次网易云回归只有发光基准略超目标（33.485ms），其余全部通过；保持相同测量方法和 33ms 阈值复核，最终全部通过，没有修改绘制规则或放宽检查。首轮报告保留在 `artifacts/special-netease-live`。
- `artifacts/special-preservation.json` 证明用户设置和桥接配置散列前后一致；个人字体原为空，自定义预设原不存在，均保持原样。正常网易云及新版后台引擎已恢复，不带调试端口；运行时插件仍为 `0.1.3`，适配器与原源码一致。实际演示设置截图为 `artifacts/special-preview/special-settings-preview.png`，采用独立静音示例，未改正常用户设置。

### 影响与限制

- 特殊主题由用户在侧栏选择，不会自动覆盖旧主题；没有新增运行依赖或改动网易云协议、播放订阅及纯音乐处理。默认和深色主题的原配色与红色图标保持原样。
- 本轮替换运行窗口／任务栏和后台托盘图标；EXE 文件和未运行的固定快捷方式仍由 Windows 管理。Windows 原生标题栏和文件对话框沿用系统外观。
- 缩放检查使用进程 Qt 比例，未改系统设置；软件绘制耗时会受当时机器负载影响，不是 GPU 帧率或长期稳定性保证。其他客户端版本、多屏与长时间运行的验证边界沿用既有说明。

## 2026-10-07：更新创作者文案与版本并增加界面主题

### 改动

- 新增 `app_info.py` 集中管理应用版本 `0.4.0`、创作者与标语；`main.py` 设置 Qt 应用版本，`controls.py` 将侧栏说明替换为“创作者：Bilibili-鈴仙優昙華院因幡”，其下显示版本号，底部标语改为“FACE THE SIN. SAVE THE E.G.O”。长文案按语义换行，最小窗口保持完整。
- 新增 `themes.py`，原浅色外观命名为“默认主题”，另提供“深色主题”；侧栏可切换，页面、底栏、图标、控件及托盘菜单一起更新。滑块仍使用红色进度，勾选框采用可见边框与 `assets/check-white.svg` 白色勾选标记。
- `settings.py` 新增 `theme=light/dark`，旧配置与无效值回退默认主题；立即保存，重启恢复。`presets.py` 明确排除界面主题，切换效果预设不覆盖主题，主题切换不修改歌词样式、预览背景或播放状态。
- 扩展设置、界面、像素、预设及文档测试，`validation.py` 生成两种主题的默认／最小窗口截图，`netease_validation.py` 检查播放中切换主题。`start.ps1` 仅将静音诊断的完成等待上限扩展至 120 秒，普通启动的原生窗口可见性期限仍为 30 秒。更新使用、网易云、产品、技术及验证说明，重新打包。

### 测试与验证

- Windows `.venv/Scripts/python.exe -m unittest discover -s tests -q`：127 项全部通过。覆盖文案与版本顺序、旧配置回退、主题持久化和重建窗口、预设独立、播放／歌词／预览不变、两种主题的滑块及勾选框像素、启动脚本语法与等待边界、文档链接和源码可追踪性。
- 最终打包版 `artifacts/themes-final-100`、`themes-final-125-verified`、`themes-launcher-complete` 全部静音检查通过，实际 DPR 为 1.0、约 1.25、1.5；默认及最小窗口两种主题的控件可滚动访问，侧栏完整，歌词画面、暂停时钟及预览背景保持不变，SVG 勾选资源加载成功。已查看实际深色／默认主题、最小窗口及 125% 截图。
- 最终 `启动.bat -Smoke -ReportDirectory artifacts/themes-launcher-complete` 退出码 0、Windows 原生面板可见；125% 同样通过实际 BAT 入口。最终 150% 静音报告中八种动画组合暖帧 P95 为 10.277–17.030ms，发光基准为 24.185ms，均小于 33ms。
- 首次 BAT 诊断窗口已经可见，但增加两套主题截图后完成阶段超过原 30 秒期限；补充有界诊断等待及测试后复验通过。125% 首次直接以 Hidden 启动验证进程导致原生可见性检查失败；改用实际 BAT 的原生窗口恢复流程后全部通过，没有绕过该检查。
- `artifacts/netease-probe/run-words-regression.ps1 -ReportName themes-netease-complete`：引擎 32 项、宿主 10 项、真实鼠标入口 3 项全部通过，75 秒记录 254 样本及 21 次重定位。中英文 YRC、整句歌词及纯音乐四类歌曲进度正常；主题切换保存且不改变播放锚点、歌词文档或预览背景，暂停冻结、跳转、连续三次切歌和最小化继续正常。
- 改动前包备份为 `artifacts/previous-package-20261007-205918-449`，最终构建前中间包为 `artifacts/previous-package-20261007-211047-539`。`artifacts/themes-preservation.json` 证明正常设置与连接配置散列前后一致；个人字体原为空，自定义预设原不存在，保持原样。正常网易云及新版引擎已恢复启动，无调试端口，运行时插件适配器与源码一致。

### 影响与限制

- 界面主题独立于歌词的白芯发光／经典纯色、动画、字体、效果预设和网易云协议；纯音乐行为保持原状，插件仍为 `0.1.3`。没有新增应用运行依赖。
- Windows 原生标题栏与文件对话框沿用系统外观；主题只控制应用界面与托盘菜单。缩放检查通过进程 Qt 比例完成，未改变系统设置；本轮没有扩展长期稳定性或其他网易云版本的验证范围。

## 2026-10-07：接入真实 YRC 演唱强调并完成参数与预设交付

### 改动

- 插件升级为 `0.1.3`，`adapter.js` 读取当前歌 `yrcInfo.yrc`，精确原文与句首 250ms 内匹配，应用一次客户端偏移，追加可选字词绝对时间和码点范围；没有新增歌词服务或播放回调，协议仍为 1，原整句与纯音乐流程兼容。
- `lrc.py`、`netease.py` 扩展可靠时间模型、逐项坏数据回退、同步偏移及收数状态；`animation.py` 为字形簇保留原文范围，`glyph_motion.py` 按歌曲位置计算平滑 8% 放大，`text_effects.py` 在缓存合成阶段增强光晕，零发光与经典模式保持原材质。`overlay.py` 保留迟到时间数据的布局，纳入强调边界，暂停与跳转不累积状态。
- `controls.py` 提供默认关闭的演唱同步、四种数据状态、中英文演示预览；开关包含在预设中，原偏好保持不变。补齐 `presets.py` 损坏文件移走后可重试保存的行为。
- 新增 `tests/test_singing_sync.py`、真实数据验证器 `tools/verify_netease_words.mjs` 及其证据校验测试，扩展界面、插件、打包保留及静音／网易云验证。`main.py`、`netease_validation.py` 增加 `--singing-smoke`；重复诊断已有开启状态时也明确保存。`animation_validation.py` 测量八种组合，`tools/record_animations.py` 支持标明演示时间的同步录制。
- 更新使用、网易云、产品、技术及验证文档；重新打包，原用户 `.state` 整体保留，完成真实 BAT 入口和原客户端插件更新。

### 测试与验证

- Windows `.venv/Scripts/python.exe -m unittest discover -s tests -q`：最终 121 项全部通过。覆盖配置与参数、预设保存／确认／重启／损坏、中文单字与多字词、英文单词、组合字符／emoji／换行、偏移、无数据／损坏／迟到／切歌、暂停／跳转、透明度及最大跌落／强调／光晕边界；包含文档和真实验证器拒绝假阳性检查。
- 原生 Windows 源码静音 `artifacts/singing-source-100`、`singing-source-125`、`singing-source-150` 全部通过，实际 DPR 为 1.0、约 1.25、1.5。默认与最小窗口滚动控件、固定底栏、暂停冻结及结束清理通过；100% 导入 TTF、125% 导入 TTC，最终网易云回归导入 OTF。已查看面板、最小窗口、深浅预览及演示中间帧，未发现裁切、残影或矩形底色。
- `build.ps1 -SkipDependencies` 通过；原任务开始前包备份到 `artifacts/previous-package-20261007-152754-763`，收尾诊断修复前的中间包为 `artifacts/previous-package-20261007-153456-326`。插件安装记录为 `artifacts/netease-install-20261007-152826-133`，确认运行时版本 0.1.3 和适配器散列一致。
- 最终 `启动.bat -Smoke -ReportDirectory artifacts/singing-launcher-final` 退出码 0，窗口 Windows 原生可见，全部静音检查通过。51 字符双句、八组合、每组合 90 个暖帧，P95 为 3.755–6.778ms；均小于 33ms，复用模糊缓存。
- `artifacts/netease-probe/run-words-regression.ps1 -ReportName singing-netease-verified2`：引擎 29 项、宿主 10 项、真实鼠标入口 3 项全部通过；75 秒采集 334 样本、21 次重定位。真实《Fly, My Wings》8 行／40 单位、《星辰大海》19 行／131 单位到达引擎，二者均观察到完整强调；《起风了》70 行整句正常回退，《Holy Termination》纯音乐保持无歌词。四类歌曲进度移动，暂停冻结画面，跳转结束，连续三次切歌保持选定歌曲，最小化继续及断连清理通过；参数、两个预设及同步开关不改变播放锚点／状态。播放负载下八组合 P95 为 3.929–6.487ms。
- 首轮宿主验证把跳转误差设为 150ms，并在纯音乐尚未开始音频时采样，导致不通过；修正为等待真实进度及记录原生解码落点，实测英文误差 227ms、中文 462ms，加载状态归零。又发现隔离诊断已有开关开启时未触发保存、原曲暂停时无法检验最小化推进；补回归测试并明确保存，验证阶段临时播放后恢复原状态。最终所有检查通过，未修改插件播放订阅。
- 四种强调演示 GIF 由 Windows Qt 窗口录制，`artifacts/singing-demo` 每份 5.5 秒，源 165 帧／30fps，编码重开确认 151 合并帧；明确为中英文演示时间，不冒充实际歌曲。真实客户端强调截图另存于 `singing-netease-verified2/netease-singing-overlay.png`。
- 正常设置与连接配置散列前后一致；个人字体目录原为空，自定义预设原不存在且未生成，打包保留非空文件由自动测试覆盖。证明为 `artifacts/singing-preservation.json`；原队列、歌曲和暂停状态恢复，正常网易云及新版引擎运行，无调试端口。

### 影响与限制

- 同步默认关闭，旧偏好保持当前体验；只有原文与时间都可靠的行增强，不能声称所有歌曲都有逐字支持。真实两首 YRC 的客户端偏移为 0；非零偏移由客户端格式化源码及自动测试验证，未改用户偏移进行人工校准。英文按词而非按字母强调，普通 LRC 不猜测演唱时间。
- 没有新增运行依赖；性能是本机暖缓存软件绘制，冷准备另见报告，不包含 GPU 合成，也不代表长时间稳定性。字体材质与句子缓冲另有开销；其他网易云版本、多屏和 30 分钟稳定性仍沿用原验证边界。

## 2026-10-07：增加内置和自定义效果预设

### 改动

- 新增 `presets.py`：安静办公／轻快律动内置只读方案，版本化 JSON 原子保存、完整视觉组合、同名保护、更新／删除、损坏文件保留；旧方案新增字段使用默认值，设置数值归一化复用 `settings.py`。
- `controls.py` 新增预设选择、另存、更新和删除入口，覆盖与删除确认，手动调整标记已修改；一次性应用与保存，缺失字体回退并提示，保留显示区域／偏移／音量／预览背景。预设包含默认关闭的 `singing_sync` 数据字段，其开关及绘制在下一项交付。
- 新增 `tests/test_presets.py`，扩展界面测试、`validation.py`，更新说明和验证记录。静音检查使用独立 `smoke-effect-presets.json`，不操作个人方案。

### 测试与验证

- Windows `.venv/Scripts/python.exe -m unittest discover -s tests -v`：108 项全部通过；覆盖原子替换失败、损坏／未知版本原文件不变、完整组合重启恢复、同名与内置保护、确认取消、更新删除、一次刷新及缺失字体回退。
- Windows `main.py --smoke --report-dir artifacts/presets-source-150`：全部通过；两个预设实际窗口截图、完整方案再加载、独立设置保留、暂停时切换及默认／最小窗口可访问。已查看原生预设面板截图。

### 影响与限制

- 内置方案不会覆盖当前设置，需手动选择；自定义方案保存在设置目录 `effect-presets.json`，包含字体家族名称，不重复打包字体文件。正式打包沿用整个设置目录保留流程。
- 损坏方案文件会保留且禁止覆盖写入，内置方案仍可用。演唱同步字段默认关闭，本次未改变歌曲或逐字时间处理。

## 2026-10-07：开放动画速度、抖动频率和跌落距离

### 改动

- `settings.py`、`lrc.py`、`glyph_motion.py`、`overlay.py` 新增并使用入场／退场速度 25–300%、抖动频率 1–15 次／秒、32px 基准跌落距离 0–128px；默认 100%／100%／6／48 保留原时序与运动。短句和结束边界继续压缩时长。
- `controls.py` 提供滑块与数值配对，禁用当前动画不适用的参数，动画、参数、深浅预览和重播归于同一分组；`animation.py`、`text_effects.py` 计入最大自定义跌落距离。扩展 `validation.py` 和界面测试，新增 `tests/test_effect_parameters.py`；更新使用说明和验证记录。

### 测试与验证

- Windows `.venv/Scripts/python.exe -m unittest discover -s tests -v`：100 项全部通过，覆盖旧配置、范围、速度反比、密集／空白／结束、确定性采样、零距离淡出及最大跌落高分屏边界。
- Windows `main.py --smoke --report-dir artifacts/parameters-source-150`：全部检查通过，实际 DPR 1.5；参数保存、暂停时修改不移动进度、默认／最小窗口滚动访问通过。四模式 P95 为 3.318／3.299／3.722／3.692ms，均低于 33ms。
- 独立网易云数据探测 `artifacts/word-data-probe/run-probe.ps1`：7 项宿主进度／暂停／跳转／切歌检查通过；探测到英文歌曲原生 YRC，数据保存在忽略的诊断目录。未修改插件或正式设置。

### 影响与限制

- 本次提交只交付参数；效果预设和演唱同步随后独立提交。跌落距离按实际字号缩放，速度较慢时仍受歌词边界限制；逐字时间不参与本次动画计算。
- 无新增运行依赖；首次受限环境测试无法完成字体文件替换和本机连接，已在正常 Windows 权限下重新运行全部测试通过。新增控件通过滚动访问。

## 2026-10-07：增加四种逐字歌词动画与重播预览

### 改动

- [设置](settings.py)新增 `animation_style`，提供波纹·波动、波纹·抖动、跌落·波动、跌落·抖动；旧配置和无效值仍使用原有效果。[面板](controls.py)增加歌词动画选择、独立重播预览，将跳动幅度改名为律动幅度；立即保存，隐藏或滚动不可见时停止预览刷新。
- 新增 [字符运动模块](glyph_motion.py)，按歌曲位置计算逐字透明度与运动，保持暂停、跳转和确定性随机颤动。通常 700ms 入场、下一句开始时 600ms 退场，密集歌词压缩；波动频率 1.5Hz，抖动每秒 6 次平滑采样。跌落按字号加速下移并旋转，整句倾斜时仍沿屏幕竖直方向。
- [时间轴](lrc.py)增加入场结束和退场起点；新模式长句保持到下一条标签，空白及结束边界前退出，未知时长最后一句沿用 6 秒兜底。[桌面层](overlay.py)共享字符状态，不叠加原整句渐隐，不改变播放控制或网易云协议。
- [文字效果](text_effects.py)缓存完整字符材质后统一施加逐字透明度，分层排除白芯下的邻字光晕，复用句子缓冲与光晕缓存。白芯发光、经典纯色和导入字体均可组合。[布局](animation.py)计入颤动、跌落、字符旋转及光晕；空格只保留宽度，极窄区域长句必要时取消句子倾斜。
- 新增 [动画测试](tests/test_glyph_motion.py)与 [性能验证器](animation_validation.py)，扩展 [界面测试](tests/test_controls.py)、[静音检查](validation.py)、[入口](main.py)、[网易云检查](netease_validation.py)、[外观验证器](effect_validation.py)，提供 `--animations-smoke`。
- 新增 [原生录制](tools/record_animations.py)及 [动图编码](tools/encode_animation_recording.py)，更新使用说明、网易云说明、产品设计、技术文档和验证记录；重新打包，插件 0.1.2 无需重装。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：94 项全部通过，新增覆盖四模式顺序、短句／单字／密集歌词、空格与组合字符、长停留、多行、空白及最后一句、确定性噪声、零幅度、竖直跌落、像素透明度、白芯、经典填充、自定义字体外伸、缓冲复用、暂停／往返跳转、保存及可见预览计时器。测试发现的空格替代字形和极窄区域长句运动余量问题已修正后复验。
- Windows 源码 `main.py --smoke --font-smoke-file <夹具> --report-dir artifacts/animations-source-<比例>`：100%／125%／150% 全部通过，分别使用 TTF／TTC／OTF，实际 DPR 为 1.0、约 1.25、1.5。进程缩放因子 0.6666666667／0.8333333333／1，未改系统比例；默认及最小窗口新控件可滚动访问、底栏完整，静音解码、暂停、跳转、恢复及结束清理通过。
- 51 字符双句、整屏透明画布、各 90 帧暖缓存绘制，按波纹·波动／波纹·抖动／跌落·波动／跌落·抖动顺序，P95：100% 为 `2.770 / 3.573 / 5.179 / 4.899ms`；125% 为 `5.065 / 5.154 / 6.823 / 6.858ms`；150% 为 `4.034 / 4.333 / 4.536 / 4.846ms`。全部低于 33ms，暖帧不生成新光晕。
- `.\build.ps1 -SkipDependencies` 通过，旧包为 `artifacts/previous-package-20261007-134824-197`。`.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\animations-launcher"` 退出码 0，原生面板可见，全部检查通过；最终包四模式 P95 为 `4.383 / 4.376 / 4.996 / 5.263ms`。
- `artifacts/netease-probe/run-fonts-regression.ps1 -ReportName animations-netease-live -Effects -Animations`：23 项桌面／字体／外观／动画检查、7 项宿主播放检查及 3 项实际鼠标入口检查全部通过；45 秒采集 189 个样本、10 次重定位，最高平滑能量 0.0714。四模式切换保存不改变播放锚点及状态；跌落·抖动参与随后真实暂停、跳转、连续三次切歌、最小化继续和断连清理。切换到《Value》《我们终会在大地深处重逢 (feat. 诗岸)》《Sinos De Natal》，宿主进度与歌词匹配正常，没有额外跳歌；同次四模式 P95 为 `7.661 / 6.616 / 7.131 / 7.545ms`。
- 录制实际 Windows Qt 预览窗口 165 帧，DPR 1.5，原生可见性为真；本机已有 Pillow 编码并重新打开四份 GIF，各为 151 个合并后帧、5.5 秒，保留平均 30fps 时钟。输出为 `artifacts/animations-demo`。已查看退场中间帧、125% 最小窗口及默认面板截图，光晕和控件无裁切、矩形底色或遮挡。
- 正常设置 SHA-256 前后保持 `8B191C98DB9E5456AB7489FFB7AB3872B95255A120F1D02DD883DC7D8462B645`，连接配置散列、字体目录一致，证明为 `artifacts/animations-preservation.json`。已恢复原网易云及新版后台引擎正常启动，无调试端口；文档收尾后单独运行文档校验。

### 影响与限制

- 默认动画保持原样，四种新效果需手动选择；字体、颜色与纯音乐流程保留。逐字入场属于句级视觉编排，尚未接入逐字演唱时间或精准节拍。
- 无新增应用运行依赖；Pillow 只用于开发录制输出。64MiB 限额仍针对共享光晕图像，当前字符材质与句子缓冲另有开销。
- 性能为本机暖缓存软件绘制，包含整屏清空和合成，不包含 GPU／桌面合成。首次字形冷准备另见报告；长期稳定性、多屏和其他网易云版本的验证范围未扩大。

## 2026-10-07：增加白芯彩色描边与柔和发光效果

### 改动

- [设置](settings.py)新增 `text_style` 和 `glow_strength`，默认白芯发光与 60% 强度；保留经典纯色。原颜色在新模式用作描边及同色光晕，字芯固定白色；旧配置保留原值并补齐新默认。
- [控制面板](controls.py)加入样式、描边颜色、0–100% 发光强度及白芯提示；经典模式恢复文字颜色并禁用强度。中英文预览共用实际绘制，默认深色背景，可切换浅色；背景只影响预览，不保存或改变桌面。
- 新增 [共享效果模块](text_effects.py)，用现有 NumPy 做字形 alpha 的分离式高斯模糊，缓存上限 64MiB，按实际路径、字体、字号、颜色及设备像素比分组。32px 下外露描边约 1.2px，光晕支撑约 8px，按字号缩放；强度为 0 保留字芯和描边。
- [桌面层](overlay.py)复用逐句透明缓冲，依次绘制所有光晕、描边和白芯，再统一施加淡出与总体透明度；每帧清空缓冲，避免染色、透明度叠加和残影。[布局](animation.py)计入光晕、实际图像舍入边界及动画余量，缩放改变时清理缓存。跳动、倾斜、歌曲时钟和纯音乐处理沿用原逻辑。
- 新增 [效果与性能验证器](effect_validation.py)、[像素测试](tests/test_text_effects.py)，扩展 [面板测试](tests/test_controls.py)、[配置测试](tests/test_core.py)与 [本地静音检查](validation.py)。[入口](main.py)和 [网易云检查](netease_validation.py)增加可选 `--effects-smoke`，检查播放中的设置与同步状态。
- 更新 [使用说明](README.md)、[网易云说明](NETEASE.md)、[产品设计](产品设计方案.md)、[技术文档](技术文档.md)和 [验证记录](验证记录.md)，重新打包引擎；现有插件 `0.1.2` 无需修改。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：最终 75 项全部通过，覆盖白芯与边色、光晕梯度及强度、相邻字重叠、整句透明度、经典样式、残影清理、缓存命中与限额、细笔画、自定义字体外伸、缩放失效、布局边界、保存及旧配置。文档收尾后另行运行文档校验。
- 普通沙箱下原有字体原子移动与本机 WebSocket 测试受 Windows 权限限制；在真实 Windows 环境复验后全部通过。静音验证器补齐已保存经典样式／零强度时的控件默认同步，并增加对应回归测试。
- 源码 `main.py --smoke --font-smoke-file <夹具> --report-dir artifacts/glow-source-<比例>`：100% 使用 TTF、125% 使用 TTC、150% 使用 OTF，三个报告全部通过。100%／125% 分别设置进程 `QT_SCALE_FACTOR=0.6666666667`／`0.8333333333`，实际设备比例为 1.0、约 1.25、1.5，未改系统比例。默认及小窗口控件可滚动访问，底栏可见，暂停、恢复、跳转及结束清理通过。
- 51 字符双句、整屏透明画布的 90 帧暖缓存软件绘制 P95：源码 100% 为 `4.398ms`、125% 为 `4.626ms`、150% 为 `6.785ms`，均小于 33ms。150% 缓存图像约 `1,267,040` 字节，暖帧无需重新生成光晕。
- `.\build.ps1 -SkipDependencies`：原生助手及 PyInstaller 构建通过。改动前包保留在 `artifacts/previous-package-20261007-124509-361`，最终构建前中间包为 `artifacts/previous-package-20261007-124954-595`。最终构建只额外更新本地验证器默认同步逻辑，发光、播放和网易云代码与已联动验证版本一致。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\glow-launcher-final"`：最终包实际入口退出码 0，面板 Windows 原生可见，全部静音检查通过。最终包暖缓存中位数 `6.288ms`、P95 `6.667ms`，冷准备 `23.078ms`。
- `artifacts/netease-probe/run-fonts-regression.ps1 -ReportName glow-netease-live -Effects`：18 项桌面／字体／发光检查、7 项宿主播放检查、3 项真实鼠标入口检查全部通过。45 秒采集 214 个样本、10 次重定位，最高平滑声音强度 `0.11`；播放中的样式切换和强度保存不改变同步锚点、歌曲与播放状态，暂停画面冻结、跳转、连续三次切歌、最小化继续及退出清理正常。该次暖缓存 P95 `11.877ms`，仍低于目标。
- 已查看深浅背景发光示例、150% 默认面板和 125% 小窗口截图，字芯、细描边与柔光清楚，新控件和底栏无遮挡。最终包 `glow-dark.png`、`glow-light.png` 使用独立粉色示例设置；正常颜色未被替换。
- 构建、联动及最终正常恢复后，用户 `settings.ini` SHA-256 仍为 `F1458570A9FD07A80953C98B3CA5345CDF01997D17334CD185134707BFE86754`，桥接配置散列一致，个人字体目录前后相同。证明见 `artifacts/glow-preservation.json` 及 `artifacts/glow-netease-live/settings-preservation.json`。已恢复原网易云及后台引擎正常启动，不带调试端口。

### 影响与限制

- 首次读取旧配置默认启用白芯发光；原颜色、字体、字号及其他设置保留，后续保存时写入两项新字段，可随时切回经典样式。光晕亮度不随音乐闪烁，运动仍由原歌曲时间及声音强度驱动。
- 无新增运行依赖。64MiB 限额针对共享缓存中的光晕图像，不代表整个程序内存上限；另有当前句子缓冲、路径和 Qt 界面开销。
- 性能数据为本机软件绘制测量，包含整屏透明画布和逐句合成，不包含 GPU／桌面合成，也不声明整机帧率。实测环境仍为网易云 `3.1.41.205529`、BetterNCM `1.3.4` 和 Windows 本机；长期稳定性及跨显示器动态体验范围未扩大。

## 2026-10-07：增加歌词字体选择与个人字体导入

### 改动

- [歌词效果面板](controls.py)增加“歌词字体”、中英文预览及“导入字体”，提供原有微软雅黑、宋体和楷体。选择立即应用并自动保存，预览与桌面文字使用相同字形布局。
- 新增 [字体库](fonts.py)，支持 TTF、OTF、TTC；通过 Qt 验证字体后按内容散列原子保存到 `.state/fonts`，重启时加载副本，移动原文件不影响使用。处理重复文件、损坏字体、导入失败及失效选择回退；TTC 中各家族分别加入列表。
- [设置](settings.py)新增 `font_family`，旧配置默认微软雅黑并保留其他值。[布局](animation.py)同时计算实际字形外伸范围，避免个人字体笔画越界；字体改变清理缓存，界面主题与歌词颜色保持独立。纯音乐及无歌词处理沿用原逻辑。
- 更新 [入口](main.py)、[本地验证器](validation.py)、[网易云验证器](netease_validation.py)，隔离正常与验证字体目录，增加可选 `--font-smoke-file`。新增 [字体测试](tests/test_fonts.py)、[原创夹具](tests/fixtures/README.md)及 [夹具生成器](tools/make_test_font.py)，扩展 [界面](tests/test_controls.py)、[配置](tests/test_core.py)和 [联动](tests/test_netease.py)回归测试。
- 更新 [使用说明](README.md)、[网易云说明](NETEASE.md)、[技术文档](技术文档.md)和 [验证记录](验证记录.md)，重新打包桌面引擎。网易云插件仍为 `0.1.2`，此次无需更新客户端或插件。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：59 项全部通过，覆盖三款预置字体、保存及重建面板、取消与无效导入、字体副本重载、重复导入、复制失败清理、TTC 多家族、OTF CFF 轮廓、字形外伸、旧配置和无歌词保持空白。文档收尾后另行运行文档校验。
- `.\.venv\Scripts\python.exe main.py --smoke --font-smoke-file tests/fixtures/lyrics-test.ttf --report-dir artifacts/fonts-source-150`：源码 Windows 静音检查通过。另以 `QT_SCALE_FACTOR=0.6666666667` 和 `0.8333333333` 验证 100% 与 125%；125% 使用 TTC 夹具。三个实际比例为 1.0、约 1.25、1.5，字体实际家族、三种歌词画面、默认及最小窗口可达性均通过。报告在 `artifacts/fonts-source-100`、`fonts-source-125`、`fonts-source-150`。
- `.\build.ps1 -SkipDependencies`：原生音频助手与 PyInstaller 构建通过。改动前包备份为 `artifacts/previous-package-20261007-000046-775`，最终构建前的中间包为 `artifacts/previous-package-20261007-000916-125`；正常 `.state` 保留。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\fonts-launcher-final"`：实际启动入口退出码 0，Windows 面板原生可见，最终打包版全部静音检查通过。最终 EXE 以 `--smoke --font-smoke-file tests/fixtures/lyrics-test.otf --report-dir artifacts/fonts-packaged-otf` 启动也全部通过，确认真实 OTF 导入、保存与副本重载。
- `artifacts/netease-probe/run-fonts-regression.ps1`：最终 `netease-report.json` 13 项桌面、字体与设置窗口检查、`host-report.json` 7 项宿主播放检查、`settings-clicks.json` 3 项真实鼠标检查全部通过。45 秒采集 218 个样本、12 次重定位，最高平滑声音强度 `0.1266`。播放时完成预置字体切换及导入，耗时与进度增加均为 735 毫秒，同步锚点、歌曲编号和播放状态未改变；覆盖暂停、跳转、连续三次切歌、最小化和退出清理。
- 首轮字体联动的固定时间差检查误将正常播放前进判为跳转，已改为验证同步锚点和状态不被修改，并增加接受正常前进、拒绝主动跳转的两项回归测试。一次真实鼠标复验未打开窗口；验证辅助脚本改为在窗口恢复后重新测量 CEF 按钮坐标，再次复验通过。首轮报告保留在 `artifacts/fonts-netease-first-run`。
- 已查看 150% 默认、小窗口及最终网易云字体设置截图，字体选择、导入按钮、预览和固定底栏完整，其他设置可滚动访问。原九项用户设置值保持一致，仅新增默认 `font_family`；证明见 `artifacts/fonts-update-settings-preservation.json`。最终联动前后正常设置 SHA-256 一致，见 `artifacts/fonts-netease-live/settings-preservation.json`；连接配置散列不变，正常字体库未混入测试夹具。原网易云已恢复正常启动，不带验证调试端口。

### 影响与限制

- 宋体、楷体引用本机系统字体，不分发 Windows 字体文件；字体未安装时标为不可用。个人字体仅加载到本程序并保存副本，不安装到系统；同一家族仅显示一次，使用常规字重，缺字继续由 Qt 回退。
- 验证字体采用项目原创矩形字形，仅用于测试，正常模式不加载它们。fontTools 仅供开发者重建夹具，应用无需新增依赖。
- 本次实测仍为 Windows 本机、网易云 `3.1.41.205529` 与 BetterNCM `1.3.4`；没有扩大对其他客户端、长时间稳定性或跨显示器动态缩放的验证范围。纯音乐维持原样。

## 2026-10-06：修复后台设置窗口右键无反馈

### 改动

- 用户反馈右键“跳动的词”没有反应。真实鼠标跟踪确认右键处理和打开请求均已执行，但后台启动的 Qt 面板在 Windows 原生状态中仍隐藏；直接调用原生窗口恢复后能够显示。
- [控制面板](controls.py)打开时增加 Windows 原生恢复、置前和可见状态日志，处理后台隐藏和最小化；新增 `show_effects()`，由 [联动入口](main.py)将插件的设置请求直接送到“歌词效果”页。
- [网易云插件](plugins/netease/index.js)保留右键入口，并在开关旁新增可左键点击的“设置”按钮。阻止设置点击传播，连接断开时允许显式重启引擎，连接恢复后补发打开请求；打开设置不会改变歌词开关。[插件清单](plugins/netease/manifest.json)升级至 `0.1.2`。
- 扩展 [面板测试](tests/test_controls.py)和 [插件测试](tests/test_netease_plugin.cjs)，覆盖隐藏及最小化恢复、页面选择、播放状态不变、两个设置入口、断线启动和补发请求。[真实联动验证器](netease_validation.py)新增可选 `--settings-smoke` 检查，要求效果页原生可见；此模式不自动显示面板，避免掩盖后台启动问题。
- 更新 [使用说明](README.md)、[网易云说明](NETEASE.md)和 [验证记录](验证记录.md)，重新打包引擎并更新本机插件。保留原 `.state`、网易云和 BetterNCM 框架。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：44 项全部通过，包含新增窗口恢复测试及扩展插件设置入口回归检查；文档更新后另行运行文档校验。
- `.\.venv\Scripts\python.exe main.py --smoke --report-dir artifacts/netease-settings-local-smoke`：源码 Windows 静音播放、动画、窗口和布局检查通过。
- `.\build.ps1 -SkipDependencies`：原生音频助手与 PyInstaller 打包通过；最终构建前的包保存在 `artifacts/previous-package-20261006-184534-637`，修复前的包保存在 `artifacts/previous-package-20261006-184015-885`。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\netease-settings-launcher"`：实际启动入口面板原生可见，打包版全部静音检查通过。
- `.\.venv\Scripts\python.exe tools\package_netease.py` 生成 `0.1.2` 插件包，已更新 `C:\betterncm\plugins\FloatingLyrics.plugin`。修复前插件备份为 `artifacts/netease-settings-fix-20261006-184706/FloatingLyrics.plugin`。
- `artifacts/netease-probe/run-settings-regression.ps1`：后台冷启动后，真实鼠标右键首次打开效果窗口通过；再次将窗口原生隐藏后，真实鼠标左键“设置”恢复窗口通过。`artifacts/netease-settings-live/settings-clicks.json` 三项检查全部为真。验证脚本等待客户端按钮就绪，并将尚未创建原生窗口的后台状态视为隐藏，不依赖预先打开面板。
- 同次验证的 `host-report.json` 7 项宿主播放检查、`netease-report.json` 10 项桌面与设置窗口检查全部通过。45 秒采集 217 个样本，9 次重定位，最高平滑声音强度 `0.1738`；包含暂停冻结、跳转、连续三次切歌、最小化继续同步及退出网易云清除歌词。
- 已查看 `netease-settings.png`，确认真实打开“歌词效果”页，150% 比例下字号、颜色和透明度控件显示完整，剩余效果可滚动访问。原用户设置 SHA-256 前后一致，记录在 `artifacts/netease-settings-live/settings-preservation.json`；最终恢复原网易云正常启动，关闭验证调试端口。

### 影响与限制

- 设置入口仍使用独立桌面效果面板；歌词透明层继续鼠标穿透。窗口恢复遵循 Windows 前台激活规则，不更改全局焦点策略。
- 本次实测网易云 `3.1.41.205529`、BetterNCM `1.3.4` 和本机 Windows；其他客户端版本及长期运行仍需另行验证。截图使用独立验证设置，正常用户偏好未被替换。

## 2026-10-06：修复网易云进度冻结并补齐切歌验证

### 改动

- 用户反馈网易云进度条停止、音乐和歌词仍播放，以及切歌跳过。确认旧 [适配器](plugins/netease/adapter.js)通过独立 `window.legacyNativeCmder` 注册 `PlayProgress`、`Seek`，其回调表与客户端播放器分离，可能覆盖客户端的原生事件槽，使网易云自身收不到进度和跳转完成事件。
- 改为订阅客户端已加载模块导出的 `audioPlayerPlayProgress$`、`audioPlayerSeek$`，复用播放器自己的事件实例；保留暂停迟到事件和歌曲编号过滤，隔离插件处理异常，卸载页面时只取消本插件的订阅。[插件入口](plugins/netease/index.js)接入新订阅方式，[清单](plugins/netease/manifest.json)升级为 `0.1.1`。
- 扩展适配器、插件生命周期测试，新增 [宿主回调隔离测试](tests/test_netease_host.cjs)与 [宿主验证器测试](tests/test_netease_host_validation.cjs)，纳入 [自动测试](tests/test_netease.py)。新增 [真实宿主验证工具](tools/verify_netease_host.mjs)，直接检查网易云进度条、暂停、跳转及连续切歌；外部驱动计时，兼容客户端旧 Chromium。
- 更新 [网易云说明](NETEASE.md)与 [验证记录](验证记录.md)。原桌面引擎不变，重新生成并安装插件包，保留原框架、客户端版本和用户配置。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：43 项通过。新增回归检查覆盖宿主回调不被覆盖、连续换歌后的事件过滤、插件异常不阻断宿主、退订不删除宿主回调，以及验证器能识别进度冻结和未经操作的跳歌。
- `.\.venv\Scripts\python.exe main.py --smoke --report-dir artifacts/netease-progress-local-smoke`：原本地播放和桌面动画的 Windows 静音集成验证通过。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\netease-progress-launcher"`：退出码 0，实际入口面板可见，打包版静音集成检查全部通过。
- `node tools/verify_netease_host.mjs artifacts/netease-host-regression`：真实网易云宿主 7 项检查通过，连续播放包含《感官过载》在内的多首歌曲，进度持续移动，切歌后没有再次跳过所选歌曲，歌词所属歌曲正确。
- `artifacts/netease-probe/run-progress-regression.ps1`：已安装 `0.1.1` 与原客户端联合检查通过，`artifacts/netease-progress-live/host-report.json` 的 7 项宿主检查、`netease-report.json` 的 9 项桌面检查全部通过。45 秒采集 220 个样本、10 次进度重定位，最高平滑声音强度约 `0.096`；覆盖暂停画面冻结、最小化后继续同步、退出网易云后清除歌词及不创建第二个播放器。
- 已查看修复后网易云及歌词面板截图。正常用户设置 SHA-256 前后一致，记录为 `artifacts/netease-progress-live/settings-preservation.json`。原有插件备份在 `artifacts/netease-progress-fix-20261006-174417/FloatingLyrics.plugin`；最终已恢复原网易云正常启动，不带调试端口，实际加载的适配器与项目源码 SHA-256 一致。

### 影响与限制

- 之前的 9 项桌面检查仅覆盖歌词引擎，没有检查网易云自身进度条及连续切歌，未能发现此次宿主干扰；本次增加独立宿主验证。
- 仍仅适配网易云 `3.1.41.205529`、BetterNCM `1.3.4`。验证覆盖本机多首歌曲与短时操作，不代表全部歌曲版权、网络状态或长期稳定性均已验证。

## 2026-10-06：接入网易云音乐插件与桌面歌词引擎

### 改动

- 新增 [BetterNCM 插件](plugins/netease/index.js)和 [3.1.41 播放器适配](plugins/netease/adapter.js)，在网易云播放栏提供“跳动的词”开关和右键设置入口。读取当前歌曲、网易云自身歌词及原生播放进度，音乐由网易云播放。
- 新增 [本地连接与播放状态](netease.py)，用本机 WebSocket 和随机令牌传输歌词、播放位置与状态。连接丢失时停止动画并清空歌词；切歌清理旧歌词；暂停后忽略迟到的进度回调，未变化的歌词不重复随机布局。
- 新增 [进程音频助手](native/process_energy.cpp)及 [能量接入](process_audio.py)，仅计算网易云进程树的声音强度，不保存音频。复用透明歌词层和现有外观设置。
- [启动入口](main.py)增加网易云模式、后台启动和真实联动检查；[面板](controls.py)在联动模式显示歌曲及只读进度，播放和音量操作保留在网易云。退出歌词引擎后插件停止自动重启它。
- 新增 [打包](tools/package_netease.py)、[安装](tools/install_netease.ps1)及 [音频助手构建](tools/build_energy.ps1)工具。[构建脚本](build.ps1)先完成新包，再备份旧版并保留 `.state`；`.gitignore` 排除客户端产生的 `debug.log`。
- 新增协议、真实回环连接、插件生命周期、暂停迟到事件和 DOM 重复更新测试，扩展界面与文档测试；更新使用、产品和技术文档，增加 [网易云说明](NETEASE.md)及 [真实验证器](netease_validation.py)。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：41 项通过，包括原有 29 项及 12 项新增/扩展检查；JavaScript 适配与插件生命周期检查由 Node.js 执行，本地 WebSocket 使用真实握手验证。
- `.\.venv\Scripts\python.exe main.py --smoke --report-dir artifacts/netease-local-smoke`：原本地音乐流程 Windows 静音验证通过，真实解码、暂停、跳转、布局、透明穿透、置顶和禁止激活检查全部通过。
- `.\build.ps1 -SkipDependencies`：Visual Studio C++ 工具与 Windows SDK 成功构建音频助手；PyInstaller 6.11.1 完成新版打包。旧包备份为 `artifacts/previous-package-20261006-165349-025`。
- `.\启动.bat -Smoke -ReportDirectory "$PWD\artifacts\launcher-bat-netease"`：实际批处理入口退出码 0，原生控制面板可见，打包版全部静音检查通过。
- 使用项目内隔离副本验证 BetterNCM 1.3.4 在网易云 3.1.41.205529（64 位）实际可加载，再通过 `tools/install_netease.ps1` 安装到原客户端。普通权限写入安装目录被 Windows ACL 拒绝后，通过 Windows 管理员授权完成安装，未降级网易云；记录为 `artifacts/netease-install-20261006-165956-440/receipt.json`。
- `artifacts/netease-probe/run-installed.ps1`：原客户端与打包引擎真实联动验证通过，45 秒采集 220 个样本；9 项检查全部通过，包括真实歌曲、35 行歌词、实际歌词画面、暂停时间与画面冻结、跳转、最小化后进度继续、进程声音强度、退出客户端清除歌词及不创建第二个播放器。最终最高平滑强度约 0.0491；报告为 `artifacts/netease-live-installed/netease-report.json`。
- 已查看原网易云播放栏入口、联动面板及透明歌词截图。新旧打包版、安装及验证后的正常 `settings.ini` SHA-256 一致，记录为 `artifacts/netease-settings-preservation.json`。

### 影响与限制

- 本次适配网易云 Windows 3.1.41.205529（64 位），依赖第三方 BetterNCM 1.3.4。客户端更新后需重新验证；本地音乐模式保留。
- 进程音频回环需要 Windows build 20348 或更新版本；不可用时可以选择“轻波浪”。仍为按句同步，尚未实现逐字演唱时间或精准节拍检测。
- 真实客户端验证覆盖短时功能行为，未完成长时间稳定性、多显示器动态切换或所有歌曲类型检查。安装目录、产物、连接令牌、用户配置、截图和测试报告不纳入 Git。

## 2026-10-06：改为浅色音乐播放器布局

### 改动

- 参照用户提供的浅色音乐软件截图，重组 [控制面板](controls.py)：浅灰背景、白色圆角卡片、红色强调色、约 200px 侧栏，以及固定的底部播放栏。
- 增加“当前音乐”和“歌词效果”导航，分别呈现单首歌曲信息与分组设置；保留本地音乐导入、同名 LRC 匹配、演示、播放控制、透明桌面歌词和托盘操作。
- 歌曲信息同步到内容区与底栏，长名称省略并保留完整路径提示；错误提示跨页面保持可见，导入不存在的音乐时保留原歌曲和歌词。颜色选择按钮使用独立色块，浅色歌词颜色不会使按钮文字难以阅读。
- 更新 [启动入口](main.py) 的屏幕适配与 Qt 控件风格；使用绘制的本地图标和细进度条，保留 Windows 原生窗口操作及原有歌词颜色配置，更新 `assets/app.ico`。
- 新增 [界面测试](tests/test_controls.py)，扩展 [集成验证](validation.py) 和 [文档校验](tests/test_workflow_docs.py)，更新 [使用说明](README.md) 与 [验证记录](验证记录.md)。
- 在隔离目录构建新版，再替换 `dist/FloatingLyrics`。旧版保留在 `artifacts/ui-previous-package-20261006`，复制原有 `.state` 并核对用户设置文件 SHA-256。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：29 项通过，包含 11 项新增界面测试、15 项核心测试及 3 项扩展文档与 Git 范围校验。
- `.\.venv\Scripts\python.exe main.py --smoke --report-dir artifacts/ui-150`：Windows 集成验证通过，控制面板原生可见，真实音频解码、暂停、跳转、恢复、歌词动画与窗口输入标志均正常。
- 分别使用 `QT_SCALE_FACTOR=0.6666666667`、`0.8333333333` 及系统默认比例启动源码检查；报告的实际像素比例为 1.0、约 1.25、1.5，三个报告均通过。默认及最小窗口下播放栏可见、设置可通过滚动完整访问；已查看两个页面、空状态及缩放截图。
- PyInstaller 6.11.1 在隔离的 `artifacts/ui-package` 目录构建成功；打包版静音验证通过。
- 从 `D:\Work` 运行实际入口 `启动.bat -Smoke -ReportDirectory D:\Work\跳动的歌词\artifacts\launcher-bat-ui`：退出码 0，控制面板原生可见，全部集成检查通过。
- 替换打包版前后及入口验证后，正常用户配置 `settings.ini` 的 SHA-256 一致；保存记录为 `artifacts/ui-settings-preservation.json`。

### 影响与限制

- 本次改动为界面重排和视觉更新，功能仍以单首本地音频与 LRC 为基础；网易云截图仅用于视觉参考。
- 缩放检查通过 Qt 应用级比例完成，未修改 Windows 系统显示设置；跨显示器动态切换、独占全屏和 30 分钟稳定性测试仍需实际体验。
- 音频检查使用静音解码，未人工听音；打包产物、用户设置、验证报告和截图继续由 `.gitignore` 排除。

## 2026-10-06：建立 Git 基线与协作规则

### 改动

- 初始化 `main` 分支，将现有桌面歌词源码、文档、测试和演示资源纳入首次提交，建立后续追踪与回滚的基线。
- 新增 [AGENTS.md](AGENTS.md)，要求每次改动提交 commit、编写或更新相关测试、交付前全部验证通过，并记录每次改动。
- 新增本变更记录及 [协作文档校验](tests/test_workflow_docs.py)，校验文档编码、链接、记录结构和 Git 忽略范围。

### 测试与验证

- `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`：18 项测试全部通过，其中包括 15 项核心测试及 3 项新增文档与 Git 范围校验。
- 新增校验确认 UTF-8 文档可读、代码围栏配对、文件链接有效、变更条目完整，以及运行产物被忽略、源码可跟踪。
- `git diff --cached --check`：通过；人工检查暂存文件范围及三项协作要求，均符合本次任务。

### 影响与限制

- 本次新增协作规则和版本管理记录，应用功能未改动。
- 现有功能和此前启动修复作为初始基线纳入版本管理；它们的已有验证见 [验证记录.md](验证记录.md)。
- 虚拟环境、个人运行配置、打包产物和验证截图沿用 `.gitignore` 的忽略规则。
