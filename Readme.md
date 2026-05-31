# Agents-skills

简洁说明：本仓库收集、组织并维护与 Agent / Skill 相关的示例、模板与工作流，方便复用与快速初始化项目。

快速开始
- 安装（推荐）：确保已安装 `python3`。
- 初始化示例工程（考试助手）：

```bash
python3 Exam_Helper/scripts/init_exam_workspace.py
```

- 初始化报告工作流：

```bash
python3 report-workflow/scripts/init_report_project.py
```

项目结构（主要目录）
- [Exam_Helper](Exam_Helper/README.md#L1)：考试/学习相关的技能、模板与示例。
- [report-workflow](report-workflow/SKILL.md#L1)：报告生成与质量检查的工作流模板。
- [HydraProject](HydraProject/SKILL.md#L1)：其他项目示例与技能说明。

实用文件与模板
- 模板与启动文件位于 `Exam_Helper/templates` 与 `Exam_Helper/assets/starter_files`。
- 常用脚本位于各子项目的 `scripts/` 目录（参见上方示例）。

如何贡献
- 新增技能：在相应子目录下添加文件或新目录，遵循已有模板。
- 编写示例：在 `examples/` 放置示例 Markdown，便于他人参考。

联系与维护
- 提交改动请使用 PR 或在仓库中直接编辑相关文件，并保持目录与命名清晰。

该 README 旨在提供快速入门指引；如需更详细说明，请查看子目录内的 README/SKILL 文档。