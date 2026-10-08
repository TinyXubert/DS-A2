# DS-A2: Inference and uncertainty notebook

**作者：xuhongbo · 学号：202618018629048**

本项目估计 Adelie 企鹅雄性与雌性的平均体重差，并通过模拟研究样本量、噪声和效应大小如何影响统计功效，以及违反独立性假设后区间覆盖率和误报率的变化。

分析包含 73 只雄性和 73 只雌性企鹅。平均体重差为 674.7 g，Welch 95% 置信区间为 [573.0, 776.3] g，Bootstrap 区间为 [577.4, 774.7] g。在组内相关系数为 0.6 的模拟反例中，忽略相关性使名义 5% 检验的误报率达到 29.5%；按独立簇均值分析后为 5.12%。完整方法、图表和结论见 [Notebook](A2.ipynb) 和 [PDF 报告](A2.pdf)。

## 环境配置

项目已在 Python 3.10 环境中运行。克隆仓库后，在仓库根目录创建环境并安装依赖：

```bash
git clone https://github.com/TinyXubert/DS-A2.git
cd DS-A2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` 固定直接依赖的版本，每次运行还会将完整依赖快照保存为 `results/<UTC时间>/requirements-lock.txt`。

## 执行顺序

打开 `A2.ipynb`，选择上述虚拟环境作为 Python 内核，工作目录设为仓库根目录。重启内核后，按顺序执行全部代码格并保存输出。

| 代码格 | 内容 |
|---|---|
| 01 | 环境、分析协议和结果目录 |
| 02 | 数据哈希、Adelie 筛选、排除记录及分组统计 |
| 03 | Welch 公式和模拟汇总函数 |
| 04 | 样本均值差、Welch 与 Bootstrap 区间 |
| 05 | 已知真实参数下的抽样分布和覆盖率 |
| 06 | 样本量、噪声和效应的 60 个功效情景 |
| 07 | 相关性反例、误报率与簇均值修正 |
| 08 | 数值汇总和 Abstract |
| 09 | AI 使用、个人核验记录与完成标记 |

每次运行 01 都会建立新的 `results/<UTC时间>/` 目录，保留已有结果。随机种子、模拟参数和排除规则记录在 `protocol.json` 中。

也可以通过命令行完整执行，并保存为单独的复现文件：

```bash
python -m jupyter nbconvert --to notebook --execute A2.ipynb \
  --output A2_rerun.ipynb --ExecutePreprocessor.timeout=300
```

## 报告导出

导出脚本读取已保存的 `A2.ipynb` 及其对应结果目录，更新开头 Abstract，并生成 HTML、完整 Markdown 和配套图片：

```bash
python export_report.py
```

导出 PDF 需要额外安装依赖及浏览器：

```bash
python -m pip install -r requirements-export.txt
PLAYWRIGHT_BROWSERS_PATH="$PWD/.runtime/browsers" \
  python -m playwright install chromium --only-shell
python export_report.py --pdf
```

输出包括 `A2.html`、`A2.pdf`、`A2_REPORT.md` 和 `figures/`，保留代码与执行结果。摘要另存为 `ABSTRACT.md` 和 `SUBMISSION_SUMMARY.md`。也可以在浏览器中打开 HTML，打印保存为 PDF。

脚本固定以 `A2.ipynb` 为报告源。如果使用命令行生成了 `A2_rerun.ipynb`，应先检查其输出，再将选定的复现版本另存为 `A2.ipynb` 后导出。

## 文件说明

| 文件或目录 | 内容 |
|---|---|
| `A2.ipynb` | 分析代码、方法说明及执行结果 |
| `A2.pdf`、`A2_REPORT.md`、`figures/` | PDF 和 Markdown 报告及图片 |
| `data/raw/penguins.csv` | 冻结的上游数据 |
| `data/raw/manifest.json` | 数据来源、上游 commit、SHA-256、许可和下载时间 |
| `protocol.json` | 预先确定的估计量、阈值、种子及实验设置 |
| `METHOD_NOTE.md` | 统计方法、推导与假设 |
| `AI_USE_LOG.md` | AI 使用说明、个人核验和反思 |
| `results/` | 各次运行的分析记录、排除记录、模拟输出、图表和环境信息 |

`power_replicates.npz` 的情景编号对应 `power_grid.csv`；`cluster_replicates.npz` 对应 `cluster_summary.csv`。数组列顺序均为 `estimate, lower, upper, p`。这些文件保存重复实验的统计输出，合成观测可通过种子和代码重建。

## 结论范围

200 g 是本次实验的教学阈值，并非生物学标准。功效分析使用预先设定的合成总体；反例中的相关性也是人为设定的，不代表真实企鹅数据的相关程度。真实数据的区间估计依赖抽样、缺失机制和独立性等假设，不能直接作因果解释或推广到所有 Adelie 企鹅。

## 数据来源与许可

数据来自 [palmerpenguins 上游项目](https://allisonhorst.github.io/palmerpenguins/)，原始采集者为 Kristen Gorman 和 Palmer Station LTER。Kaggle 页面用于发现数据，实际下载地址及固定版本见 `data/raw/manifest.json`。

数据许可为 **CC0**。引用：Horst, Hill & Gorman (2020), *palmerpenguins*, [DOI: 10.5281/zenodo.3960218](https://doi.org/10.5281/zenodo.3960218)。仓库代码的许可见 `LICENSE`。
