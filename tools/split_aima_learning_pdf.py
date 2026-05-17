from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter


@dataclass(frozen=True)
class SplitSpec:
    order: int
    filename: str
    title: str
    reason: str
    start_page: int
    end_page: int

    @property
    def page_count(self) -> int:
        return self.end_page - self.start_page + 1


SPLITS = [
    SplitSpec(1, "01_intro_ch01_p022-050.pdf", "第1章 绪论", "阶段1：AI 基本概念与课程起点", 22, 50),
    SplitSpec(2, "02_agents_ch02_p051-077.pdf", "第2章 智能Agent", "阶段1：PEAS、环境类型、Agent 结构", 51, 77),
    SplitSpec(3, "03_search_ch03_p078-123.pdf", "第3章 通过搜索进行问题求解", "阶段2：BFS、DFS、UCS、贪心、A*", 78, 123),
    SplitSpec(4, "04_beyond_search_ch04_p124-155.pdf", "第4章 超越经典搜索", "阶段2：局部搜索、模拟退火、遗传算法", 124, 155),
    SplitSpec(5, "05_adversarial_search_ch05_p156-187.pdf", "第5章 对抗搜索", "阶段2：minimax、alpha-beta、chance", 156, 187),
    SplitSpec(6, "06_csp_ch06_p188-215.pdf", "第6章 约束满足问题", "阶段2：CSP、约束传播、回溯", 188, 215),
    SplitSpec(7, "07_logic_agents_ch07_p216-256.pdf", "第7章 逻辑Agent", "阶段3：命题逻辑、真值表、CNF、归结入门", 216, 256),
    SplitSpec(8, "08_first_order_logic_ch08_p257-286.pdf", "第8章 一阶逻辑", "阶段3：一阶逻辑语法、语义与知识工程", 257, 286),
    SplitSpec(9, "09_fol_inference_ch09_p287-322.pdf", "第9章 一阶逻辑的推理", "阶段3：合一、前向/反向链接、归结", 287, 322),
    SplitSpec(10, "10_probability_ch13_p420-444.pdf", "第13章 不确定性的量化", "阶段4：基本概率、独立性、Bayes", 420, 444),
    SplitSpec(11, "11_prob_reasoning_ch14_p445-491.pdf", "第14章 概率推理", "阶段4：贝叶斯网络、条件独立、精确推理", 445, 491),
    SplitSpec(12, "12_temporal_prob_ch15_p492-527.pdf", "第15章 时间上的概率推理", "阶段4：过滤、预测、HMM", 492, 527),
    SplitSpec(13, "13_ml_core_ch18_p600-632.pdf", "第18章核心：监督学习、决策树、评估、神经网络", "阶段5：覆盖 18.2-18.7，重点包含 18.3、18.4、18.7", 600, 632),
    SplitSpec(14, "14_naive_bayes_ch20_p688-690.pdf", "第20章补充：20.2 带完整数据的学习与朴素贝叶斯", "补充：覆盖 20.2.2 朴素贝叶斯及其直接上下文", 688, 690),
]


def build_manifest(output_dir: Path) -> None:
    lines = [
        "# AIMA 学习内容切分清单",
        "",
        "按 `学习规划.md` 的主线章节切分，所有导出文件都不超过 50 页。",
        "",
        "| 序号 | 文件名 | 内容 | PDF页码 | 页数 | 对应学习阶段 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for spec in SPLITS:
        stage = spec.reason.split("：", 1)[0]
        lines.append(
            f"| {spec.order} | `{spec.filename}` | {spec.title} | {spec.start_page}-{spec.end_page} | {spec.page_count} | {stage} |"
        )

    lines.extend(
        [
            "",
            "补充说明：",
            "- `第18章核心` 采用课程重点小节的连续页范围 600-632，兼顾上下文，页数仍在 50 页以内。",
            "- `第20章补充` 提取 688-690 页，包含 `20.2.2 朴素贝叶斯模型` 及其直接上下文。",
            "- `CNN / ResNet` 不在这本教材的对应正文中，因此无法从本 PDF 内切出，只能作为教材外补充内容单独整理。",
        ]
    )

    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    pdf_candidates = sorted(root.glob("*.pdf"))
    if not pdf_candidates:
        raise FileNotFoundError("No PDF found in project root.")

    source_pdf = pdf_candidates[0]
    output_dir = root / "output" / "pdf" / "aima_learning_splits"
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(source_pdf))

    for spec in SPLITS:
        if spec.page_count > 50:
            raise ValueError(f"{spec.filename} exceeds 50 pages.")

        writer = PdfWriter()
        for page_index in range(spec.start_page - 1, spec.end_page):
            writer.add_page(reader.pages[page_index])

        target = output_dir / spec.filename
        with target.open("wb") as handle:
            writer.write(handle)

    build_manifest(output_dir)

    print(f"Source PDF: {source_pdf.name}")
    print(f"Output dir: {output_dir}")
    for spec in SPLITS:
        print(
            f"{spec.order:02d} {spec.filename} | {spec.start_page}-{spec.end_page} | {spec.page_count} pages"
        )


if __name__ == "__main__":
    main()
