# DS-A2: Inference and uncertainty notebook

报告开头是 Abstract，内容来自实际执行结果。研究问题是 Adelie 企鹅雌雄平均体重差及其不确定性；主方法为 Welch 区间/检验，Bootstrap 作对照，模拟研究功效和独立性假设被破坏后的后果。

## 执行顺序

打开 `A2.ipynb`，选择 `/data2/xuhongbo/DS_HW/DS-A2/.venv/bin/python`。内核工作目录须为 `DS-A2`，然后按 Shift+Enter 依次执行：

| 代码格 | 内容 |
|---|---|
| 01 | 环境、预先制定的协议和结果目录 |
| 02 | 数据哈希、Adelie 筛选、排除记录及分组统计 |
| 03 | Welch 公式和模拟汇总函数 |
| 04 | 真实样本均值差、Welch 与 Bootstrap 区间 |
| 05 | 已知真实参数下的抽样分布和覆盖率 |
| 06 | 样本量 × 噪声 × 效应的 60 个功效情景 |
| 07 | 相关性反例、误报率与簇均值修正 |
| 08 | 实际结果摘要和本次 Abstract |
| 09 | AI 日志与完成标记 |

若要完整复现，先重启内核再按顺序运行。每次运行 01 会新建 `results/<UTC时间>/`，保留旧结果；失败时先保存错误输出副本再修改，不删除不利于结论的情景。

本次 200 g 是教学阈值，并非生物学标准。功效网格是预先设定的合成总体，不能称为从真实企鹅样本确认的总体功效。相关性结构也是专门构造的反例，不是对真实数据相关性的测量。

## Abstract 和 PDF

保存已执行的 Notebook，然后运行：

```bash
cd /data2/xuhongbo/DS_HW/DS-A2
.venv/bin/python export_report.py --pdf
```

脚本根据已保存 Notebook 最后一格指向的完成记录更新开头 Abstract，再导出包含代码和结果的 `A2.html` 和 `A2.pdf`。在 VS Code 中若文件已打开，请从磁盘重新加载以看到摘要更新，避免用编辑器中的旧版本覆盖。

若只需 HTML，省略 `--pdf`。HTML 可下载到本地浏览器打开，Ctrl+P 保存为 PDF。重新执行后必须再次导出，开头静态摘要才会更新。数值摘要同时保存为 `ABSTRACT.md` 和 `SUBMISSION_SUMMARY.md`。

## 提交前亲自完成

填写 Notebook 作者；阅读 `AI_USE_LOG.md`，补充实际做过的来源核验、独立计算和反思，随后重跑 09、保存并重新导出。自动执行通过不等于你已经完成个人核验。

提交材料包括 Notebook、PDF、原始 CSV/manifest、protocol、方法说明、results、环境依赖和 AI 日志。平台摘要为 150 至 300 词，并需稳定 GitHub URL 及 commit/tag。脚本不执行 Git push 或课程平台提交。

## 数据与文件

- `data/raw/penguins.csv`：企鹅项目上游 CSV，下载前固定了本项目分析协议。
- `data/raw/manifest.json`：上游 commit、URL、SHA-256、许可和下载时间。
- `protocol.json`：效应定义、阈值、种子、模拟网格、排除规则。
- `METHOD_NOTE.md`：方法和假设说明。
- `results/<时间>/`：分析记录、排除记录、全部情景汇总、逐次模拟结果、图和环境。
- `.venv/`、`.runtime/`：本地环境和缓存，不提交。

`power_replicates.npz` 的 scenario 编号对应 `power_grid.csv`；`cluster_replicates.npz` 对应 `cluster_summary.csv`，每个数组的列顺序为 `estimate, lower, upper, p`。NPZ 保存重复实验的统计输出；合成观测可由种子和代码重建。

Kaggle 页面用于发现数据。本项目实际下载上游仓库版本，没有把它冒充成 Kaggle 下载包。
来源：https://allisonhorst.github.io/palmerpenguins/ 。数据许可 CC0；引用 Horst, Hill & Gorman (2020), DOI 10.5281/zenodo.3960218，并致谢原始采集者。

## 新机器复现

创建自己的 Python 环境，执行 `python -m pip install -r requirements.txt`。直接依赖已固定；每次运行还保存完整 `requirements-lock.txt`。PDF 额外依赖见 `requirements-export.txt`，然后执行 `python -m playwright install chromium --only-shell` 安装本机浏览器。

服务器根分区满时，在启动内核/安装依赖前将临时路径放到 /data2：

```bash
cd /data2/xuhongbo/DS_HW/DS-A2
mkdir -p .runtime/tmp .runtime/jupyter .runtime/ipython
export TMPDIR="$PWD/.runtime/tmp"
export JUPYTER_RUNTIME_DIR="$PWD/.runtime/jupyter"
export JUPYTER_CONFIG_DIR="$PWD/.runtime/jupyter"
export IPYTHONDIR="$PWD/.runtime/ipython"
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.runtime/browsers"
```

PDF 尚含 TODO 时属于待个人审阅的草稿，不应当作已完成核验的提交件。
