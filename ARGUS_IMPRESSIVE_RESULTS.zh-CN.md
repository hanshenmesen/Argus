# Argus“亮眼成果”候选任务

> 目标：让 Argus 做出有实质分量、第三方看得懂、能复现、能核验的成果。
>
> 这是一份任务清单，不是 Argus 已完成成果清单。计划、跑通 demo 或内部 checker
> 变绿，都还不能算“亮眼成果”。

**公开来源核验日期：2026-08-07。** 下文会明确区分“技术背景”“外部已有结果”
“Argus 已有证据”和“Argus 后续计划”。这四类内容不能互相替代，数字也不能混用。

## 如何阅读这份文档

- **技术背景**：用非专业读者也能理解的方式解释这项技术是什么。
- **外部参考**：别人公开报告的结果，只能作为背景或 baseline 候选，不能写成 Argus 成果。
- **Argus 已有证据**：确由 Argus 运行产生，但结论范围不能超过明确写出的硬件、shape、
  重复次数和评审状态。
- **Argus 目标 / 待做**：尚未完成的工作。
- **可直接发给 Argus 的 Prompt**：每段都是独立 mission brief；复制完整代码块作为一条
  新消息发送，Argus 即可直接开始执行。

### 重要证据更正

1. 旧版文档中的 MiniMax-H3 **DGX Spark 3.92×** 和 **RTX 5090 4.52×**
   未能追溯到一手公开来源，现已删除。
2. 公开来源能确认**谢恩泽是 Sol-Engine 和 Sol-Attn 的共同作者**，但不能证明
   MiniMax-H3 的具体实现或某个桌面端 benchmark 由他个人独立完成。因此，官方 H3
   结果归于 **NVLabs Sol-Engine 团队**，不归于某一个人。
3. FLA PR
   [`#1054`](https://github.com/fla-org/flash-linear-attention/pull/1054) 已经
   **关闭且未合并**。D128 后续测量表明，D64 上的大幅收益没有延续到有代表性的训练
   workload。真正有上游价值的 SM100 正确性修复被拆成
   [`#1109`](https://github.com/fla-org/flash-linear-attention/pull/1109)；截至核验日，
   该 PR 仍为 open，但已获 maintainer approve。

## 小词典

| 术语 | 通俗解释 |
| --- | --- |
| **checkpoint** | 发布出来的模型权重和配置。换成更小或训练方式不同的模型，就已经换了任务。 |
| **baseline** | 要被超过的冻结版本；必须使用相同硬件、输入、质量要求和计时边界。 |
| **kernel** | 完成某一个操作的底层 GPU 程序。一个 kernel 变快，不代表整个应用一定变快。 |
| **GEMM** | 通用矩阵乘法，是神经网络绝大多数线性层背后的核心计算。 |
| **attention** | 让 token 之间交换信息的计算。完整 attention 要比较所有 query/key 对，视频序列越长越昂贵。 |
| **sparse attention** | 只算选中的 attention 关系。可能更快，但选择开销和近似误差都必须测量。 |
| **跨 step cache** | 复用相邻扩散去噪 step 的结果，通常能省很多计算，但一般属于近似。 |
| **端到端（end-to-end）** | 用户实际等待的完整路径，而不只是一个 kernel；仍要明确哪些阶段被计入或排除。 |
| **hot path** | 一次运行中反复执行、最昂贵的部分；可能不含模型加载、提示编码、编译或结果封装。 |
| **1.5× 加速** | 新耗时 = 旧耗时 ÷ 1.5；不等于“时间减少 150%”。 |
| **N>=10** | 至少十次同机 paired 测量，用来降低把噪声误判成收益的概率。 |
| **B/T/H/D** | batch / 序列长度 / attention head 数 / 每个 head 的维度。例如 `B8_T1024_H8_D64`。 |

H100 是 Hopper 架构的数据中心 GPU；B200 是更新的 Blackwell 数据中心 GPU。
DGX Spark 是使用 GB10 和统一内存的小型系统；RTX 5090 是桌面 GPU。不同平台的结果
不能不经重测直接互相外推。

## 什么结果可以进入正式清单

每个正式结果必须同时满足：

- **结果本身有分量：** 明显性能提升、真实榜单名次、上游采用、可用系统，或被独立核验的
  数学证明/反例。
- **比较公平：** 冻结 baseline、硬件、输入、精度、版本、质量要求和计分方法；不能只挑
  一个方便的 shape 做标题。
- **可以复现：** 有环境、命令、原始结果、补丁/代码、失败路线和已知限制。
- **有独立检查：** Reviewer 复核；性能结果重复测量；数学结果由独立专家或形式化工具验证。
- **确实由 Argus 推进：** 保留 session、任务轨迹、关键假设、代码改动和 Reviewer 结论；
  人工贡献单独写清楚。
- **不夸大：** 外部参考不能写成 Argus 结果，单机单 shape 结果不能写成通用结论。

### 状态词汇

- `exploration`：连具体问题或可行性门槛都还没有锁定。
- `candidate`：有方向，但还没有可靠 baseline 和执行协议。
- `active`：已有可运行任务和测量协议。
- `certified`：内部重复测量与独立 Reviewer 已通过。
- `externally-verified`：上游、榜单、外部复现或独立专家已经确认。
- `shipped`：已经进入可使用的代码、产品或公开成果。
- `retired`：证据表明某条路线不应继续；保留负面结果和停止原因。

## 候选总览

| ID | 方向 | 当前状态 | 主要平台 | 进入正式结果清单的关键条件 |
| --- | --- | --- | --- | --- |
| ARGUS-IR-01 | Sol-Engine / Sol-Attn 优化 | `candidate` | B200、H100 | 代表性 workload 上有重复可见的端到端收益，并形成可用 patch/PR |
| ARGUS-IR-02 | FLA `chunk_kda`：收口 SM100 修复并保留 D128 教训 | `active` | B200、Hopper CI | #1109 合并或被外部复现；不把 D64 写成通用性能结论 |
| ARGUS-IR-03 | MiniMax-H3 Speedrun | `candidate` | B200、H100 | 冻结公开协议，并取得质量达标、可复现的成绩 |
| ARGUS-IR-04 | MiniMax-H3：从数据中心到桌面 | `candidate` | DGX Spark、RTX 5090 | 明确保真/量化档位，在同设备 baseline 上取得可复现收益 |
| ARGUS-IR-05 | W2A4 GEMM | `exploration` | B200、H100、RTX 5090 | 先通过模型质量可行性，再实现真实 shape kernel 与端到端收益 |
| ARGUS-IR-06 | 证明或反证一个 Erdős 问题 | `exploration` | CPU/GPU + proof tools | 冻结精确命题，并得到独立核验的证明/反例 |

---

## ARGUS-IR-01 — 优化 Sol-Engine / Sol-Attn

### 技术背景：Sol-Engine 到底是什么？

[Sol-Engine](https://github.com/NVlabs/Sana/tree/sol-engine) 不是一个模型，也不是一种
GPU。它是 NVLabs 为高分辨率视频**扩散模型**准备的推理优化代码库，构建在 SGLang
`multimodal_gen` runtime 之上。视频扩散模型从噪声开始，反复调用大型 transformer
进行多步去噪；帧数和 step 数一多，计算成本很高。

Sol-Engine 组合五类优化：

1. **cache**：复用相邻去噪 step 中相似的计算；
2. **quantization（量化）**：在质量允许时使用更少 bit；
3. **kernel fusion**：把多个小 GPU 操作合并，减少 launch 与显存往返；
4. **sparse attention**：只计算选中的 token 关系；
5. **token pruning**：在部分阶段暂时删除不重要 token。

它把流程称为 **agent-native**：编码 agent 可以准备环境、尝试不同技术、组合候选栈，
再由人类验证输出质量。这不表示结果天然正确，也不表示全过程已经完全自主。
[Sol-Engine 论文](https://arxiv.org/abs/2606.23743) 在最初三个模型案例中报告了超过
2× 的端到端加速，并报告接近无损的 VBench 质量。

### 技术背景：Sol-Attn 是什么？

长视频会产生大量 token。完整 attention 要比较所有 query/key 对，计算量大致随序列
长度平方增长。Sol-Attn 是一种无需重新训练、运行时动态决定稀疏模式的 attention 方法。
它在 online-softmax 过程中挑出重要 key block，精确计算这些 block，并对未选 block
做轻量近似校正，而不是简单全部丢弃。它只是 Sol-Engine 加速链中的一项技术，不等于
整个 Sol-Engine。[Sol-Attn 论文](https://arxiv.org/abs/2607.24027) 在其视频生成/编辑
实验中报告 2.1× 和 2.3× 端到端加速，并报告视觉质量得到保持；这些是外部论文结果，
不是 Argus 测量。

### 外部参考：官方 MiniMax-H3 加速栈

当前 Sol-Engine H3 文档给出如下冻结的**团队结果**：

- 模型/workload：MiniMax-H3，1344×768，124 帧，50 steps；
- 硬件：同一 NVL72 rack 中的 8×GB200，Ulysses context parallel；
- 计时：hot path（去噪 + 视频解码），不包含约 2.1 秒固定的文本/音频编码、packing、
  scheduling 和结果组装；
- baseline：27.21 秒；
- 加入 lossless kernel line：19.51 秒；
- 再加入 Sol-Attn：17.74 秒；
- 再加入 FirstBlockCache：6.88 秒，累计 **3.97×**；
- 峰值显存：144,474 MiB 降到 120,763 MiB。

来源：官方
[`models/minimax_h3/README.md`](https://github.com/NVlabs/Sana/blob/sol-engine/models/minimax_h3/README.md)。
文档把 kernel line 描述为 lossless；Sol-Attn 与 FirstBlockCache 属于近似，因此必须同时
检查音频与视频质量。3.97× 是 8×GB200 hot-path 数字，不是 DGX Spark 或 RTX 5090 结果。

### 谢恩泽具体做了什么？

公开可核验的事实是：

- [谢恩泽的公开主页](https://xieenze.github.io/) 显示，他是 NVIDIA Research 的
  Staff Research Scientist，也是 MIT HAN Lab 的 visiting researcher。
- 他是 [SANA](https://arxiv.org/abs/2410.10629) 的共同一作、
  [Sol-Engine](https://arxiv.org/abs/2606.23743) 的共同作者，以及
  [Sol-Attn](https://arxiv.org/abs/2607.24027) 的共同作者。
- 按共同署名论文能够支持的粒度，SANA 工作提出了 32× deep-compression autoencoder、
  使用线性 attention 的 Diffusion Transformer、decoder-only text encoder，以及更高效的
  高分辨率图像生成训练/采样方法。论文没有把这些模块进一步拆成逐人 implementation credit。
- 其公开主页写明，他的 SANA 研究被用于 NVIDIA 的生成式 AI 项目。

公开记录**不能证明**的是：H3 的每一项优化都由他个人编写、DGX Spark/RTX 5090
benchmark 由他个人完成，或者官方 3.97× 只属于他一人。H3 官方页面记录了团队实现，
没有逐人贡献表。因此，本文只说明他可核验的研究与共同作者身份，把实现 benchmark
归于 Sol-Engine 团队。如要作更强的个人归因，必须有一手帖子、commit 或作者声明。

### Argus 目标

在冻结的 Sol-Engine baseline 之上找到新的、可复现并可上游的改进。优先检查 attention
耗时、GPU launch 开销、HBM 访问和可复用状态，但最终按端到端延迟与音视频质量判断，
不能只看 kernel latency。

### 先固定

- 仓库 commit、模型 checkpoint、prompt/seed、输出尺寸与 steps。
- B200/H100 软件栈、精度、GPU topology、batch/concurrency、功耗模式、warm-up 与计时边界。
- dense/reference 输出、音视频质量检查、峰值显存和端到端 baseline。
- 官方哪些优化已经打开；不能把 Sol-Engine 已有功能“重新发现”后当成新成果。

### 待做

- [ ] 在 B200 和/或 H100 上复现一个官方 Sol-Engine candidate。
- [ ] profile attention、launch、HBM 往返、collective 和稀疏路径浪费。
- [ ] 分别测试 fusion、稀疏 kernel、layout/tiling、跨 step 复用和调度。
- [ ] 每个改动记录 kernel 与端到端延迟、显存、音视频质量和保留/回退决定。
- [ ] 对保留改动做消融，说明收益机制。
- [ ] 在代表性 workload 集上重复测量，不用一个 cherry-picked case 做标题。
- [ ] 产出最小 patch、干净复现脚本和 upstream issue/PR。

### 完成标准

- B200/H100 至少一个配置有稳定、重复可见的端到端收益；
- correctness、音视频质量和显存没有未解释回退；
- 另一台机器能够复现；
- 代码得到上游实质评审，或形成边界明确、可维护的独立 fork。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请把“ARGUS-IR-01：优化 Sol-Engine / Sol-Attn”作为一个长期、证据驱动、允许修订计划的 mission 执行。不要只给我一份方案；请在现有权限和资源范围内持续行动，直到达到完成标准，或把无法继续的阻塞证据与最小下一步请求写清楚。

【使命】
在 NVLabs Sol-Engine 的冻结 baseline 之上，找到至少一项真正新增、可复现、可解释并适合上游的改进。重点关注 attention、kernel launch、HBM 往返、collective、layout/tiling、跨 step 复用与调度，但最终按端到端延迟、显存和音视频质量判断，不以单个 microbenchmark 代替真实收益。

【不可越过的边界】
1. Sol-Engine 团队已经公开的 3.97× 等数字只是外部参考，不得写成 Argus 成果。
2. 先确认实际可用的 B200/H100、模型权重、许可证与运行权限；没有对应硬件时，不得用其他 GPU 冒充，只完成可执行协议并明确标记 blocked。
3. 目标仓库、baseline workspace 与 candidate workspace 必须隔离；pin 仓库 commit、checkpoint、prompt/seed、尺寸、帧数、steps、精度、GPU topology、功耗模式、warm-up 和计时边界。不得污染或移动 baseline。
4. 近似优化必须同时检查视频和音频质量；不得用更低分辨率、更短视频、更少 steps 或隐藏缓存制造“加速”。
5. 不得把私有 technical_report 内容推到公共仓库。任何外部 push、PR、评论或大额 GPU 资源申请，先向 operator 请求明确批准。

【执行路径】
1. 阅读 Sol-Engine 官方仓库、论文、目标模型文档和已有 candidate，列出已经存在的优化，避免重复发明。
2. 根据可用硬件与权重选择一个代表性模型/workload；说明选择理由，并冻结 baseline contract 与复现命令。
3. 在同机 paired 条件下复现 baseline，分别记录 load、compile、cold、warm end-to-end、hot path、峰值内存和音视频有效性；稳定测量至少 N>=10。
4. 使用 profiler 建立 bottleneck 排名，把每个候选机制写成可证伪假设：预期改变什么指标、可能造成什么局部回退、什么结果触发 keep/revise/retire。
5. 每次只实现并测量一个最小改动；先过 correctness/quality/memory，再看性能。保留原始日志、失败尝试和环境指纹。
6. 对有效改动做消融、组合复测、cleared-cache 复测和代表性 shape 扩展；解释收益为何成立，而不是只展示最好数字。
7. 整理最小 patch、干净环境复现脚本与第二台机器复现计划；外部动作获批后再准备 upstream issue/PR。

【决策规则】
计划只是工作假设，可以根据 profiler 和实验结果修改。允许有解释且有边界的局部性能回退，只要它服务于更重要的端到端目标；但 correctness、用户目标、权限、安全与未披露质量损失不可让步。若连续证据显示某路线没有代表性端到端价值，就诚实 retire，并保留负面结果。

【必须交付】
- 冻结 baseline contract、环境清单与一键复现命令；
- 实验账本：假设、改动、原始数据、噪声、质量、keep/revert/retire 决定；
- N>=10 结果表、消融、内存与音视频质量报告；
- 最小代码 patch 和已知限制；
- technical_report/evidence/sol_engine_sol_attn/ 下的完整证据包；
- 一段严格限定硬件、workload 和计时边界的 one-line claim。

只有遇到会改变任务含义、需要新权限、需要昂贵资源或准备向外部发布时才询问我；其余可逆、低风险工作请自行推进。
```

---

## ARGUS-IR-02 — FLA `chunk_kda`：保留有用修复，停止弱性能路线

### 技术背景：用通俗语言理解 KDA 与 FLA

传统 transformer attention 要为所有历史 token 保存 key/value，所以 KV cache 随上下文
长度增长。**Kimi Delta Attention（KDA）** 是一种用固定大小 recurrent state 更新记忆的
线性 attention 模块。它在 Gated DeltaNet 基础上使用更细粒度 gate，决定如何擦除和写入
记忆。Kimi Linear 同时组合 KDA 与全局 MLA 层；KDA 是其中的机制，不等于整个模型。

[Kimi Linear 论文](https://arxiv.org/abs/2510.26692) 报告：在其一百万 token 设置下，
KV cache 最多减少 75%，解码吞吐最高 6×。这是论文特定架构/模型的整体结果，不是本次
Argus kernel patch 的收益。

[Flash Linear Attention（FLA）](https://github.com/fla-org/flash-linear-attention) 是一个
开源库，为 KDA 和其他新型序列机制提供高效 kernel 与可训练 layer。`chunk_kda` 把序列
切成 chunk，使 GPU 能并行计算，同时保持 KDA 的递推数学。训练既需要 forward，也需要
backward；如果只有 forward 变快，可能对真实用户没有价值。这条任务优化的是语言/序列
模型中的 KDA 算子，与 MiniMax-H3 的视频 attention 是两件事；它本身不会让 Sol-Attn 变快。

旧测试 shape `B8_T1024_H8_D64` 表示 batch=8、序列长度=1024、8 个 head、每 head
维度 64。上游用户更关心 D128/H32/H64；D 变大后，有效算术增加，减少一个固定 launch
所占总时间可能会大幅下降。

### Argus 已有证据：范围很窄的 D64 结果

相对冻结 FLA commit `ccb0ff94`，Argus 在一张 B200、
`B8_T1024_H8_D64`、BF16 上测得：

- component 累计栈 **+17.66%**，通过 N>=10 certification；
- 所有改动组合的一次 paired run **+29.93%**；
- correctness PASS，峰值显存未增加。

技术机制包括融合 q/k normalization、inter-solve epilogue 与 chunk-local cumulative-gate
producer，以减少 launch 和 HBM 往返。证据：
[`technical_report/evidence/fla_kernel_optimization/README.md`](technical_report/evidence/fla_kernel_optimization/README.md)。
这个结果现在仍然有效，但只代表一个旧 commit、一张 B200 和一个 D64 shape。

### 后续结果：为什么性能 PR 被关闭

PR [`#1054`](https://github.com/fla-org/flash-linear-attention/pull/1054) 的 maintainer
要求补有代表性的 D128 与 Hopper 数据。对当前代码的后续验证发现：

- 在当时可用的 H200 runner 上，四个 D128 shape 的 forward geomean 只有
  1.055–1.061×，forward+backward 只有 1.001–1.002×；
- `B4_T4096_H64_D128` 的 forward 略有退化，forward+backward 基本不变；
- 在 B200 上单独测 D128 q/k fusion 与 cumsum fusion，训练整体都约为 1.00×。

这与机制一致：D64 时固定 launch/HBM 成本占比高；D128 算术更多后，这些固定成本被摊薄。
为了近乎没有的真实训练收益维护 432 行性能 patch 不合理，因此 #1054 未合并并关闭。
这是有价值的负面结果：Argus 根据证据停止，而不是为了保留大标题继续夸大。

H200 属于 Hopper 家族，但不等于 H100 实测。本文不作宽泛 H100 性能声明。

### 当前有用产出：SM100 正确性 PR #1109

调查过程中独立复现了一个问题：B200/SM100 autotune backward kernel 时会尝试不安全配置，
触发 illegal memory access。Argus 把它拆成只改两行、仅针对 SM100 的过滤条件，提交为
[`#1109`](https://github.com/fla-org/flash-linear-attention/pull/1109)：

- 修复后完整 B200 KDA test file：**76 passed，7 skipped**；
- Hopper 与 SM120 的搜索空间不变；
- 2026-08-07 已获上游 maintainer approve，但仍等待 merge。

现在距离 externally verified upstream value 最近的是这个正确性修复，而不是已放弃的大型
性能栈。

### 待做

- [ ] 处理两个 non-blocking review nit，保持 #1109 rebase 后 CI 绿色。
- [ ] 获得完整上游 CI，并 merge 或由独立外部环境复现。
- [ ] 在证据包中补上 D128 负面结果与最终 PR 状态。
- [ ] 把 #1054 性能路线归档为 `retired`，不重新提交同一套 fusion。
- [ ] 只有当 profiling 找到能影响代表性 D128 forward+backward 的新机制时，才开启新性能路线。

### 完成标准

- **正确性成果：** #1109 被 merge，或被独立复现并采用。
- **任何未来性能成果：** 多个实际 D128 shape 在明确硬件上通过 correctness、memory 与
  N>=10 paired forward+backward 测量。

D64 数字可以保留为边界明确的 case study，但不能宣传成 KDA 通用加速。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请执行“ARGUS-IR-02：收口 FLA chunk_kda 的 SM100 正确性修复，并完整保存 D128 负面结论”。这是一个证据收口与上游闭环任务，不是重新追逐旧版约 30% 标题。

【第一原则】
开始前先实时核验 fla-org/flash-linear-attention 的 PR #1054、PR #1109、目标分支、CI 与 review 状态，不要假设本文记录仍是最新状态。根据事实选择分支：
- 如果 #1109 已合并：定位 merge commit，检查最终 diff/CI，复现或审计后完成 externally-verified 证据包，不重复提交同一修复。
- 如果 #1109 仍 open：在隔离 worktree 中 rebase，处理 review nit，运行相关测试并准备最小更新。
- 如果 #1109 被关闭或取代：查明原因和 superseding commit/PR，再决定验证、修订或 retire；不得悄悄换成另一项性能任务。

【事实边界】
1. #1054 的 D64 测量可以作为“旧 commit + 单张 B200 + 单个 D64 shape”的 case study，但该性能栈已经因 D128 forward+backward 基本无收益而 retired；禁止复活同一 432 行 fusion，除非出现新的 profiler 证据和不同机制。
2. H200 属于 Hopper 家族，但不等于 H100 实测；所有硬件结论必须按实际设备命名。
3. #1109 的价值是避免 SM100 backward autotune illegal memory access，不得包装成 KDA 通用性能加速。
4. 不修改或清理无关工作，不覆盖上游新提交；baseline 与 candidate 隔离。任何 external push、force-push、PR 评论或新 PR 都先取得 operator 明确批准。

【执行步骤】
1. 保存实时上游状态、commit SHA、review、CI URL 和时间戳。
2. 在 B200 可用时，从干净环境复现 pre-fix failure 与 post-fix success；确保 CUDA context、测试选择和依赖版本可审计。若无法安全复现 crash，说明原因，不制造结果。
3. 运行完整 KDA 相关测试以及上游要求的 dependent tests；记录 passed/skipped/failed 与基础设施 flake，不能把 cancelled CI 写成 PASS。
4. 审查 guard 的精确作用域：SM100/SM10x、BK、num_warps、剩余 autotune candidates，以及 Hopper/SM120 是否保持不变。
5. 更新 technical_report/evidence/fla_kernel_optimization/README.md：同时保留 D64 原始结果、D128 否定性数据、#1054 最终状态、#1109 最终状态和 claim 边界。
6. 如果新 profiling 暗示另一条 D128 性能路线，先提交一页 hypothesis 与代表性 forward+backward 预实验；没有明确机制和实际训练收益，不进入大规模实现。

【完成定义】
首选成功是 #1109 已 merge，或同一修复被另一个上游 commit 采用并可独立验证。若上游最终不采用，也要给出完整、可复现的正确性报告和拒绝原因。不要用“仍在 review”结束一个其实已经变化的 PR，也不要因为合并未发生而隐藏负面结果。

【交付物】
- upstream_status.md：实时状态、SHA、review/CI 与链接；
- reproduction.md 和原始测试日志；
- pre-fix/post-fix 最小复现或无法复现说明；
- 更新后的证据 README 与严格 one-line claim；
- 如获准，对现有 PR 的最小 patch/回复草稿；
- 明确结论：merged / externally reproduced / superseded / retired，以及下一步。

除外部写操作、新权限或硬件资源请求外，请自行完成所有可逆的本地核验与文档更新。
```

---

## ARGUS-IR-03 — 在 B200/H100 上建立 MiniMax-H3 Speedrun

### 技术背景

这里的“speedrun”是计划建立的一套工程 benchmark：所有人运行相同模型、输入、硬件类别、
质量门槛和计时器，再尝试缩短时间。之所以需要它，是因为 GPU 结果很容易通过修改分辨率、
帧数、去噪 steps、精度、warm-up 或计时排除项来“变快”。

目前没有找到已经独立核验的公开 MiniMax-H3 speedrun 榜单。因此，第一个交付物应是协议与
scorer，而不是名次。任务必须明确选择 MiniMax-H3 的某个专用 checkpoint（FL2VA 或
Ref2VA），并把本地 **H3-Base** 与完整 hosted 2K workflow 分开计分。

[MiniMax 官方模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3) 把 H3 描述为
omni-modal 系统：把文本、视觉和音频表示放入同一序列，由 33B dense H3-Omni-Transformer
共同预测视频和立体声音频 latent。官方系统支持 4–15 秒、24 FPS，完整三段式流程最高 2K；
H3-Context-IR 与 H3-Regenerate-2K 依赖 hosted/尚未完整开源模块，本地发布的 H3-Base
对应 768p 阶段。公平的公开 benchmark 必须说明自己测的是哪一段。

模型卡说明，公开 H3 checkpoint 是 BF16 且已经 **CFG-distilled**。因此，“官方 checkpoint”
表示使用这些已发布权重，不能把它描述成“未经蒸馏的模型”。

### 与其他任务的关系

- IR-01 产出可复用的 Sol-Engine/Sol-Attn 改进。
- IR-03 提供固定的数据中心 benchmark 与可审计排名。
- IR-04 把选定优化栈做成桌面部署。
- IR-05 只有先通过质量可行性，才可能贡献低精度 GEMM。

### 先固定

- checkpoint commit 与任务，例如 FL2VA text-to-audio-video。
- prompt、seed、分辨率、帧数/时长、FPS、去噪 steps 与输出 container。
- B200 与 H100 分榜；GPU 数量/topology 和功耗模式写清。
- 精度与允许的近似；使用 quantization/cache 的提交必须披露。
- cold start、首次编译、warm end-to-end 与 hot path 分列计时。
- 音视频有效性/质量门槛、显存与失败处理规则。
- 公开 scorer、原始日志 schema、允许/禁止优化和反作弊检查。

### 待做

- [ ] 优化开始前发布 protocol v1。
- [ ] pin 权威模型、baseline commit，并归档 scorer。
- [ ] 在 B200/H100 分别建立可复现 baseline，记录延迟、吞吐、显存、加载、编译和质量。
- [ ] 维护 Argus 实验账本：假设、patch、噪声、质量与保留/回退。
- [ ] 优化 graph、attention、GEMM、cache、quantization、kernel、collective 与调度。
- [ ] 对冠军栈做单项和组合复测，不把噪声存入最终结果。
- [ ] 提交公开榜单，或由独立机器运行同一 scorer。

### 完成标准

- 协议在声明成绩之前已经冻结；
- 质量达标的收益在重复测量中成立；
- 冠军栈能从干净环境重建；
- 有公开或独立可审计排名，而不只是“更快”的描述。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请创建并执行“ARGUS-IR-03：MiniMax-H3 Speedrun（B200/H100）”。这里的第一成果不是一个漂亮的加速数字，而是一套在优化开始前冻结、任何第三方都能审计的比赛协议；协议冻结后，再用 Argus 持续优化并产生质量达标的可复现成绩。

【使命】
建立 MiniMax-H3 的公开可审计 speedrun v1：同一 checkpoint、任务、输入、硬件类别、质量门槛与计时器下比较性能。B200 与 H100 必须分榜；本地 H3-Base 与依赖 hosted 模块的完整 2K workflow 必须分轨。

【协议先于优化】
在 baseline 或 candidate 优化前，先完成并 hash-lock protocol v1。协议至少固定：
- 官方模型仓库与 checkpoint commit，FL2VA 或 Ref2VA 任务；
- prompt/参考素材、seed、分辨率、帧数/时长、24 FPS、denoising steps、输出格式；
- GPU 型号、数量、topology、功耗模式、driver/CUDA/PyTorch 与精度；
- 允许和禁止的 quantization、cache、compile、offload、并行与预计算；
- cold load、first compile、warm end-to-end、hot path 的独立计时边界；
- 完整视频 decode、立体声音频、时长/帧数、质量阈值、显存和失败规则；
- 原始日志 schema、环境指纹、反作弊检查与同分规则。
协议一旦冻结，任何改变任务难度的修改都必须创建新版本，不能覆盖 v1。

【执行路径】
1. 核验官方 MiniMax-H3 模型卡、许可证和当前可用 checkpoint；明确公开 checkpoint 本身已经 CFG-distilled，不得称为“未经蒸馏”。
2. 盘点可用 B200/H100。没有某个平台时保留该赛道为 blocked，不用另一平台数字代替。
3. 实现独立 scorer 与 verifier；在候选代码之外保存，禁止 candidate 修改计时器或质量门槛。
4. 在冻结 baseline commit 上完成 N>=10 paired 测量，分别报告 load、compile、warm E2E、hot path、吞吐、峰值显存与音视频质量。
5. 建立 Argus 实验账本，按 graph、attention、GEMM、cache、quantization、kernel、collective、scheduler 分层提出假设；一次改变一个主要变量。
6. 只有通过 correctness/quality/resource gate 的改动才能进入 champion stack；单项与组合都要复测、消融并从干净环境重建。
7. 生成只读 leaderboard artifact；在获得 operator 批准后再公开或邀请独立机器运行同一 scorer。

【诚实比较】
不得通过降低分辨率、缩短视频、减少 steps、排除不利阶段、使用未披露缓存或只挑最好 seed 提升名次。近似方法可以参加，但必须单独标注并满足对应质量档。不存在外部榜单时，只能称为“auditable internal/public protocol result”，不能自称世界排名。

【必须交付】
- protocol_v1.md、protocol hash 与版本变更规则；
- scorer、verifier、固定输入和基线复现脚本；
- B200/H100 分轨 result schema 与 leaderboard 页面；
- N>=10 原始 baseline/champion 数据、方差、质量与显存报告；
- experiment_ledger.md、冠军栈 patch、消融和 clean-room rebuild；
- technical_report/evidence/minimax_h3_speedrun/ 下的证据包；
- 一段可公开但不夸大的结果说明。

计划可根据证据修订，但 protocol v1、质量门槛、安全、权限和公平性不可在看到成绩后倒推修改。只有需要新权限、昂贵 GPU 配额或对外发布时再询问我。
```

---

## ARGUS-IR-04 — MiniMax-H3：从数据中心走到桌面

### 技术背景：为什么这不是简单移植

Sol-Engine 官方 3.97× H3 结果使用八张 GB200 和 rack-scale NVLink。DGX Spark 只有一个
GB10 与 128GB 级统一内存；RTX 5090 内存更少，指令和访存特性也不同。因此，桌面移植
不是“重跑同一个脚本”，可能需要量化、CPU/offload、架构专用 kernel、更低并发，并且要
把编译和启动时间算清楚。

H3 的“33B”指 dense Omni-Transformer 参数量，不等于整个下载 pipeline 的大小。公开
checkpoint 还包含 processor/tokenizer、Qwen3-VL-32B text encoder、visual VAE 与 audio
VAE。桌面结果必须说明哪些模块常驻、哪些被预计算后释放、哪些被 offload。

### 外部参考，不是 Argus 结果

1. **NVLabs 官方：** 指定 8×GB200 hot path 从 27.21 秒降到 6.88 秒（**3.97×**）。
   它可以提供技术路线，但不是桌面 baseline。
2. **第三方 DGX Spark 可行性：**
   [`joeynyc/MiniMax-H3-DGX-Spark`](https://github.com/joeynyc/MiniMax-H3-DGX-Spark)
   报告了单 Spark、FL2VA、online dynamic FP8 的结果。在其固定 768×448、2 秒、20-step
   请求上，报告 warmed baseline 152.911 秒、最终 no-cache full-compute 111.373 秒、
   approximate Cache-DiT 档 80.579 秒；每项为两次 warm run。它能说明第三方部署可行，
   但改变了精度、workload 很小，既不是 NVIDIA benchmark，也不是谢恩泽个人结果。
3. **RTX 5090：** 本次核验没有找到能支持旧版 4.52× 声明的一手、可复现 MiniMax-H3
   端到端结果。

### 两个必须分开的诚实档位

- **保真档（fidelity tier）：** 保持官方发布 BF16 checkpoint 语义，不使用近似 cache 或
  weight quantization，只允许 exact/lossless 工程改动。
- **实用档（practical tier）：** 可以明确使用 FP8/FP4/W2A4、cache 或 offload，但必须与
  同一设备 baseline 比较，并通过清楚的音视频质量门槛；默认不能写成 lossless 或完全等价。

任一档位都可能形成成果，但禁止把两档数字混成一个 speedup。

### Argus 目标

至少在一个桌面平台做出干净、一键运行的 MiniMax-H3 部署，并在同设备 baseline 上取得
稳定收益，同时透明报告质量、内存、功耗、启动与编译成本。承诺 RTX 5090 端到端目标前，
必须先做可行性 gate。

### 待做

- [ ] pin 官方 checkpoint、任务、license 要求与可复现输入。
- [ ] 分别对单 DGX Spark 与单 RTX 5090 做内存/功能 preflight；不可行时记录结论，
      不能偷偷换模型。
- [ ] 在每个设备上建立自己的未优化 baseline。
- [ ] 分别移植并消融架构兼容 kernel、Sol-Attn、cache、quantization、compile 与 offload。
- [ ] 记录 load、first run、warm 端到端 latency、FPS、device/host 峰值内存、swap、功耗、
      compile cache 与完整音视频 decode。
- [ ] 用一组 prompt/seed 比较音视频质量，而不是只挑一个好看的 clip。
- [ ] 提供 container/environment lock、模型准备、一键运行和 verifier。
- [ ] 寻求第二台机器复现。

### 完成标准

- 至少一个平台在同规格、同设备冻结 baseline 上取得重复可见收益；
- 明确属于保真档还是实用档；
- 质量与资源代价可见，包括近似/量化损失；
- 干净机器能复现部署与输出验证；
- 通过消融说明每项主要优化的贡献。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请执行“ARGUS-IR-04：让 MiniMax-H3 从数据中心走到桌面”。目标是在至少一个真实桌面平台上完成可一键部署、可验证、可重复测量的 H3 路径，并相对该设备自己的冻结 baseline 取得稳定收益；不要拿 8×GB200 的 3.97× 当作桌面 baseline。

【平台顺序】
优先完成单台 DGX Spark 的端到端方法学与 packaging，再对单张 RTX 5090 做严格 feasibility gate。若 RTX 5090 因内存、算子或软件栈不可行，这个“不可行 + 证据 + 最小可行条件”本身是有效结论；不得偷偷换小模型、减少 checkpoint 组件或改成多卡后仍声称单卡成功。

【两个结果档位必须分开】
A. 保真档：官方发布 BF16 checkpoint 语义，不使用近似 cache 或 weight quantization，只允许 exact/lossless 工程改动。
B. 实用档：可使用明确披露的 FP8/FP4/W2A4、cache 或 offload，但必须与同设备、同任务 baseline 比较，并通过音视频质量门槛。
两档不能共用一个 speedup 标题。官方 NVLabs 数据与第三方 DGX Spark 仓库只能作为外部参考，不能写成 Argus 结果；未经证实的 3.92×/4.52× 不得重新出现。

【执行路径】
1. pin MiniMax 官方仓库、checkpoint commit、FL2VA/Ref2VA 任务、许可证、固定 prompt/seed、尺寸、时长、FPS 和 steps。
2. 对 DGX Spark 与 RTX 5090 分别完成 preflight：device/host memory、模型各组件大小、常驻/预计算释放/offload 计划、算子支持、driver/CUDA/容器与磁盘需求。
3. 为每个平台建立自己的 baseline；记录 cold load、first compile、warm E2E、hot path、FPS、峰值 device/host memory、swap、功耗、完整视频 decode 与立体声音频。
4. 先形成可重复的安装、模型准备和一键运行流程，再逐项测试 architecture-compatible kernel、Sol-Attn、compile、cache、quantization 和 offload。一次只改变一个主要变量。
5. 对近似/量化结果使用多 prompt、多 seed 的音视频质量套件；保留视觉差异、音频指标、失败样本和人工检查记录，不只展示最佳 clip。
6. 对保留改动做 N>=10 重复测量、消融、组合复测、无隐藏 cache 的 clean-room 重建，并寻求第二台同类机器复现。

【决策规则】
同设备 baseline 是唯一合法 speedup 分母。允许为了“能在桌面可靠运行”接受解释清楚的启动时间、功耗或局部 latency 回退，但必须把 trade-off 暴露出来；OOM、输出损坏、音频丢失、未披露近似或质量下降不能被性能数字覆盖。若某档不可行，明确 retire 该档并继续评估另一档，而不是改变任务定义。

【必须交付】
- hardware_preflight.md 与每个平台的可行性结论；
- 冻结 baseline contract、容器/环境 lock、模型准备和 one-command demo；
- fidelity/practical 两档分开的原始数据、N>=10 统计、质量与资源报告；
- verifier：模型身份、参数、输出音视频、计时边界和隐藏缓存检查；
- 每项优化的 patch、消融和已知限制；
- technical_report/evidence/minimax_h3_desktop/ 下的完整证据包；
- 一段严格限定平台、档位、workload 和质量代价的结果说明。

除下载许可、昂贵资源、外部发布或不可逆系统改动外，请自行推进所有安全、可逆步骤。
```

---

## ARGUS-IR-05 — 做一个真正可用的 W2A4 GEMM

### 技术背景：W2A4 是什么意思？

**W2A4** 表示 2-bit 权重与 4-bit 激活。矩阵乘法前，大型权重矩阵被压进 2-bit 表示，
当前 activation 被量化成 4-bit，累加通常使用更宽的数据类型。只按理想算术存储计算，
2-bit 权重是 BF16 的八分之一，4-bit activation 是 BF16 的四分之一；但 scale、zero point、
padding、packing 与临时 buffer 会减少真实节省。

它不等于 NVIDIA **NVFP4/W4A4**——后者的两个输入都是 4-bit。GPU 可能有很快的对称
4-bit 指令，却没有直接的 2-bit × 4-bit 非对称指令。软件就需要 unpack/upcast、拆成 bit
plane、查表，或重建 partial product。最优方法会随矩阵 shape 改变：在 autoregressive
LLM 中，大 `M` prefill 通常更偏 compute-bound，小 `M` decode 往往更受权重读取带宽限制。
MiniMax-H3 是 diffusion transformer，不是 autoregressive LLM；它反复执行的 GEMM shape
分布不同，因此 LLM kernel 结果不能不经重测直接搬过去。

量化包含两个不同问题：

1. **模型问题：** W2A4 数值是否还能保持可接受的输出质量？
2. **kernel 问题：** 在给定这些数值和 scale 后，GPU 能否更快完成乘法？

如果模型质量不过关，再快的 kernel 也没有用；好的量化方法也不保证 kernel 一定快。

### 外部技术版图与证据边界

OSDI 2026 论文
[ADAngel](https://www.usenix.org/conference/osdi26/presentation/liu-yao) 解释了三类
映射方法：padding、bit decomposition 与按 workload 动态选策略，并用 W2A4 图示解释
bit-disaggregation。但其端到端实验重点是 Jetson Orin/A100 上的 W2A8、W3A8、W4A8、
W5A8 等组合。它是重要设计背景，不是现成的 B200/H100/RTX 5090 W2A4 baseline。

截至核验日，在为本文检索的公开 CUTLASS 与 BitBLAS 来源中，没有找到官方成熟 W2A4
实现。这不能证明世界上不存在，而是说明“baseline discovery”必须成为第一个里程碑。
W4A4/NVFP4 数字绝不能改名成 W2A4 数字。

MiniMax-H3 当前发布 BF16 checkpoint；Sol-Engine 文档中的低精度路径主要是在其他模型上
使用 NVFP4。不能假设 H3 使用 W2A4 后质量仍然可接受。只有校准 checkpoint 和音视频质量
门槛存在后，才进入 H3 集成；否则它保持为独立 GEMM 任务，或直接 `retired`。

### 可行性 gate

- [ ] 选择目标模型/layer，并定义精确 W2A4 quantization recipe。
- [ ] 大规模 kernel 工程前，先相对 BF16 测模型质量。
- [ ] 在固定 commit 上盘点 framework、CUTLASS、Triton、BitBLAS 与相关论文 baseline，
      记录不支持的组合。
- [ ] 收集真实 `(M,N,K)`、batch 与 concurrency 分布。
- [ ] 如果质量失败，或算上转换成本后目标硬件明显不可能超过最强诚实 baseline，则停止或转向。

### Kernel 待做

- [ ] 固定 layout、signedness、group size、scale/zero-point 语义、accumulator、
      rounding/saturation 与误差范围。
- [ ] 实现慢速 reference 和 bit-exact 逐元素/矩阵测试，包括 tail shape。
- [ ] 比较 upcast/padding、split/partial-product、bit-plane 及其他有依据的映射。
- [ ] 优化 packing、dequant fusion、tile、pipeline、Tensor Core 使用和 epilogue。
- [ ] 如果单一静态策略不是全局最优，则按真实 shape autotune/dispatch。
- [ ] 在适用的 B200/H100/RTX 5090 上测 latency、吞吐、显存、pack/dequant/compile/transfer
      成本和功耗。
- [ ] 集成至少一个真实模型路径，测端到端收益与质量。
- [ ] 发布源码、shape suite、原始结果、复现命令和 integration PR。

### 完成标准

- W2A4 模型质量通过明确的应用门槛；
- kernel 在多个代表性 shape 上超过固定的强 baseline；
- 计入全部转换成本后，模型集成仍有重复可见的端到端收益；
- 第二台机器能复现 correctness 与 performance。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请执行“ARGUS-IR-05：设计、实现并验证一个真实可用的 W2A4 GEMM”。这是一个带强制 feasibility gate 的任务：先证明 W2A4 模型质量与硬件映射值得做，再进入 kernel 工程；不要先写一个漂亮但没有真实模型价值的 toy kernel。

【精度定义】
W2A4 只表示 2-bit 权重 × 4-bit activation，不能与 W4A4、NVFP4 或“平均 2.x bit”混用。开始实现前必须冻结：数值格式与 signedness、group size、scale/zero-point、layout/packing、rounding/saturation、accumulator、epilogue、误差容限，以及量化是 per-tensor/per-channel/per-group。任何语义变化都创建新版本。

【Phase 0：可行性与退出条件】
1. 根据当前可用模型、权重和硬件，选择一个真实 target model/layer；MiniMax-H3 只有在存在可审计量化 recipe 和音视频质量门槛时才可作为目标，否则选择独立、可公开复现的模型路径。
2. 从真实执行 trace 收集 `(M,N,K)`、batch、concurrency、频次和总耗时占比，形成加权 shape suite；不得先挑方便 kernel 的尺寸。
3. pin 并实测现有 framework、CUTLASS、Triton、BitBLAS 和相关论文实现；记录“原生不支持”而不是伪造 W2A4 baseline。
4. 先生成 W2A4 checkpoint/reference，并相对 BF16 测质量。若质量未过预先声明门槛，或 roofline/转换成本表明不可能带来端到端价值，停止或 revise，并保留负面结论。

【Phase 1：正确性优先】
实现一个慢速、清晰、可审计的 reference。覆盖随机值、极值、zero-point、不同 group、非对齐 M/N/K、tail、溢出、确定性和跨设备 case。逐元素验证 dequantized semantics 与 accumulator，禁止用宽松容差掩盖 bit packing 错误。

【Phase 2：候选映射】
分别评估 upcast/padding、split/partial-product、bit-plane/bitwise 以及有硬件依据的其他方法。用 profiler/roofline 解释瓶颈，再优化 pack、dequant+GEMM fusion、tile、pipeline、Tensor Core、shared memory、register pressure 和 epilogue。若不同 shape 最优策略不同，建立离线 autotune 与轻量 dispatcher，而不是强迫一个 kernel 覆盖全部。

【Phase 3：公平测量与集成】
在适用的 B200/H100/RTX 5090 上做同机 paired N>=10 测量，报告 latency、有效吞吐、显存、workspace、packing、dequant、compile、transfer 与功耗。随后接入真实模型，按 shape 频次加权，并测端到端 latency/throughput 和质量；kernel 赢但 E2E 不赢时，不得宣称任务完成。

【安全与决策边界】
baseline 和 candidate 必须隔离；不修改 scorer 来偏袒 candidate。不把 W4A4 数字改名为 W2A4，不把单 shape 峰值写成通用性能。允许有解释的局部 shape 回退，只要 dispatcher 和真实 workload 加权结果更优；correctness、质量、权限与数据完整性不可妥协。外部 push、PR、下载受限权重或昂贵 GPU 运行先请求批准。

【必须交付】
- precision_contract.md、quantization recipe 与质量 gate；
- real_shapes.json/说明、频次加权方法与 baseline inventory；
- reference implementation、完整 correctness tests 与差分结果；
- 各映射候选、profiler/roofline、N>=10 raw benchmark 和 dispatcher 规则；
- 模型 integration、端到端结果、质量报告、失败路线和已知限制；
- technical_report/evidence/w2a4_gemm/ 下的一键复现包；
- 最终结论必须是 certified、needs-revision 或 retired 之一，并说明证据。

请持续推进到通过 gate 的真实集成结果，或得到足以停止的可信负面结论；两者都比无边界的 microbenchmark 更有价值。
```

---

## ARGUS-IR-06 — 证明或反证一个 Erdős 问题

### 技术背景

并不存在唯一的“Erdős 猜想”。Paul Erdős 在数论、组合数学、图论和几何等领域提出或推广
了数千个问题。每个问题都有自己的量词、参数范围、已知部分结果和当前状态。

[UnsolvedMath](https://www.unsolvedmath.com/) 是有用的发现索引，但索引状态可能落后于文献。
选定命题必须对照原始论文与
[Erdős Problems 数据库](https://www.erdosproblems.com/) 等专业来源复核。这不是形式主义：
一个不等号、一个遗漏条件，或一个已经被解决的版本，都可能让数月工作失效。

对于“所有满足 A 的对象都满足 B”这类全称命题，**证明**必须覆盖所有允许对象；
**反例**只需给出一个满足 A、却不满足 B 的明确对象。检查十亿个例子仍只是证据，不能证明
全称命题；“没有找到反例”本身也不能证明命题成立。

### 选题 gate

优先选择：

- 表述短而明确，并且原始引用可获得；
- 有有意义的部分结果，但经核验仍未解决；
- 存在软件可精确验证的有限 case 或 lemma；
- 适合把部分边界交给 proof assistant；
- 有独立专家愿意评审。

不能只按奖金、知名度或网站 difficulty badge 选题。

### 先锁定问题

- [ ] 记录数据库 ID、精确 LaTeX 命题、全部量词、参数域、等价形式、奖金/状态与来源版本。
- [ ] 检索最新文献，并联系数据库编辑者或领域专家。
- [ ] 由数学专家确认冻结命题仍 open，且抄写无误。
- [ ] 大规模搜索前发布 statement hash/version；不能因为困难而悄悄换题。

### 证明与反例双路线

- [ ] 建立已知定理、失败方法、等价表述和可计算小 case 的来源资料包。
- [ ] 并行维护 proof 与 counterexample 路线；记录每次失败究竟排除了什么。
- [ ] 使用精确算术、可重放代码、确定性 seed 和完整的声明范围。
- [ ] 找到反例时给出具体对象；只有证明后才能声称“最小”；另提供独立 verifier 与第二套实现/证明。
- [ ] 找到证明时逐 lemma 检查依赖、边界 case 和量词；proof sketch 不算完成。
- [ ] 适合的部分进入 Lean/Isabelle/Coq；剩余 trusted axiom 或 informal step 必须显式标注。
- [ ] 把完整 artifact 交给至少两位独立领域 reviewer，并核对 novelty。

### 完成标准

满足以下任一项：

1. 完整证明通过独立专家评审并形成公开手稿；可形式化部分完成形式化验证；或
2. 精确反例由两套独立 verifier 复现，并且确实违反冻结的原始命题。

有限范围检查、数值迹象、“模型认为成立”，或只证明了邻近变体，都不能进入正式结果清单。

### 可直接发给 Argus 的 Prompt

复制下面整个代码块，作为一条新消息发送：

```text
请启动“ARGUS-IR-06：证明或反证一个明确的 Erdős 问题”。这是一个长程数学研究 mission，但在我或指定数学 reviewer 批准精确命题之前，只执行选题、文献核验和可行性工作，不得擅自进入大规模证明搜索，也不得把网站上的一句话当作权威命题。

【阶段一：选题与 statement lock】
1. 从 UnsolvedMath 发现候选，但必须逐一对照 Erdős Problems 数据库、原始论文、最新论文/预印本和可信专家来源核验当前状态。
2. 给出 3–5 个候选，每个包含：数据库 ID、完整 LaTeX statement、全部量词与参数域、已知 partial results、等价形式、奖金/状态、原始引用、最近状态更新时间、为何适合计算或形式化、主要风险。
3. 排除已经解决、状态有争议、来源缺失、命题版本不一致或只能靠大规模浮点猜测的问题。
4. 推荐一个候选，但在长期搜索前向我提交 statement packet。只有我或指定数学 reviewer 明确批准后，才生成 statement version/hash 并锁定；困难不能成为悄悄换题的理由。

【阶段二：研究地图】
对冻结命题建立可审计知识包：定义、已知定理、依赖图、经典失败路线、关键障碍、可计算小 case、可能的等价变换，以及 proof/counterexample 两条路线。每个事实标明 primary source；推测必须标为 conjectural，不得把模型记忆当引用。

【阶段三：双轨推进】
A. Proof track：把目标拆成可检查 lemma；逐项核验假设、量词、边界和依赖。适合的部分进入 Lean/Isabelle/Coq，并记录版本、imports、trusted axioms 与 `sorry`/未形式化缺口。
B. Counterexample track：使用精确算术和可重放搜索；先定义独立 verifier，再搜索。记录完整搜索范围、剪枝证明、seed、代码 commit 和失败排除的区域。浮点结果只能产生候选，必须经精确验证。
两条路线共享事实，但不得因一条困难就改变原命题。

【证据与反幻觉规则】
- 有限检查不是全称证明；没找到反例也不是证明。
- proof sketch、数值拟合、图形直觉或“模型认为正确”不能升级为 solved。
- 反例必须满足原命题全部前提并违反结论；“最小反例”只有在最小性被证明后才能声称。
- 每个关键 lemma 至少有独立复核路径；计算结果使用第二实现或独立 verifier。
- 在宣称 novelty 前重新检索最新文献并联系数据库编辑者/领域专家。
- 对外发布、联系专家、提交预印本或消耗大规模算力前，先取得 operator 批准。

【停止与转向规则】
计划可以修订，但 statement、权限、安全和数学有效性是硬边界。每条失败路线都要记录它真正排除了什么。若证据显示问题不适合当前工具，提交一份可复用的 negative research report 和更合适候选，而不是伪造进展或静默换题。

【必须交付】
- candidate_shortlist.md 与逐项来源核验；
- 获批后的 statement.tex、statement_hash.txt 与版本说明；
- literature_map.md、依赖图和 proof/counterexample 双轨账本；
- exact-search 代码、独立 verifier、完整日志与覆盖声明；
- formal/ 目录中的 proof assistant 工程及 trusted-boundary 报告；
- proof draft 或 counterexample certificate；
- 至少两位独立数学 reviewer 的问题清单与处理记录；
- technical_report/evidence/erdos_problem/ 下可从零复核的证据包。

最终只有两种正向完成：完整证明通过独立专家核验，或精确反例被两条独立路径复现。否则请准确报告 partial progress、被排除路线与下一步，不使用“解决”一词。
```

---

## 推荐执行顺序

1. **先合并 FLA #1109，并诚实归档 #1054：** 它离上游确认最近；不要继续投入已经被
   D128 数据否定的 D64→D128 fusion 假设。
2. **冻结并复现一个 Sol-Engine baseline：** 之后再 profile 新的 Sol-Attn/kernel 贡献。
3. **先发布 MiniMax-H3 Speedrun protocol v1：** 规则必须早于优化。
4. **先做 DGX Spark 桌面档：** 用它建立 packaging 与质量方法，再承诺 RTX 5090 可行性。
5. **W2A4 先过模型质量与 baseline discovery gate：** 证据通过后才做 kernel 工程。
6. **Erdős 路线独立运行：** 先锁命题与 reviewer，不阻塞 GPU 工程主线。

## 正式结果记录模板

```text
RESULT_ID=
TITLE=
ONE_LINE_RESULT=
STATUS=certified|externally-verified|shipped
CLAIM_SCOPE=
BASELINE_REPO_AND_COMMIT=
ARGUS_REPO_AND_COMMIT=
HARDWARE_AND_SOFTWARE=
WORKLOAD_TIMING_BOUNDARY_AND_QUALITY_BAR=
MEASURED_RESULT=
REPEAT_COUNT_AND_VARIANCE=
REPRODUCE_COMMAND=
CODE_OR_PR=
RAW_EVIDENCE=
ARGUS_SESSION_AND_TRACE=
HUMAN_CONTRIBUTIONS=
INDEPENDENT_VERIFICATION=
KNOWN_LIMITATIONS=
```

正式展示页只放通过标准的结果。失败路线、负面结果和被否决的 claim，也要留在各 campaign
的证据目录中供审计。

## 本次背景核验使用的一手来源

- [NVLabs Sol-Engine 分支](https://github.com/NVlabs/Sana/tree/sol-engine) 与
  [论文](https://arxiv.org/abs/2606.23743)
- [Sol-Engine 官方 MiniMax-H3 case study](https://github.com/NVlabs/Sana/blob/sol-engine/models/minimax_h3/README.md)
- [Sol-Attn 论文](https://arxiv.org/abs/2607.24027)
- [MiniMax-H3 官方模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [谢恩泽公开主页](https://xieenze.github.io/) 与
  [SANA 论文](https://arxiv.org/abs/2410.10629)
- [Kimi Linear 论文](https://arxiv.org/abs/2510.26692) 与
  [FLA 仓库](https://github.com/fla-org/flash-linear-attention)
- [FLA PR #1054](https://github.com/fla-org/flash-linear-attention/pull/1054) 与
  [focused PR #1109](https://github.com/fla-org/flash-linear-attention/pull/1109)
- [ADAngel，OSDI 2026](https://www.usenix.org/conference/osdi26/presentation/liu-yao)
- [UnsolvedMath](https://www.unsolvedmath.com/) 与
  [Erdős Problems](https://www.erdosproblems.com/)
