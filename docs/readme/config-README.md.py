# 🎛️ Config: The Persona & System Control Panel

欢迎来到“方舟之心”的**总控制台**！本目录下的配置文件，定义了你的宠物几乎所有的行为、性格、算法乃至功能开关。通过编辑这些文件，你可以将你的宠物从一个标准模板，“调教”成一个完全独一无二的、属于你的灵魂伴侣。

**⚠️ 重要警告：** 修改此处的配置可能会导致宠物出现非预期、奇怪甚至令人不悦的行为。在进行任何修改前，**强烈建议您备份您的 `user_config.yaml` 文件！**

---

## 🚀 快速上手：如何个性化你的宠物

你**永远不应该**修改程序自带的`default_config.yaml`文件。所有的自定义都应在你的**用户配置**文件中进行。

### 1. 找到你的用户配置文件

- **文件位置：** `user_config.yaml`
- **路径：**
    - Windows: `C:\Users\<你的用户名>\AppData\Roaming\ArkHeart\user_config.yaml`
    - macOS: `~/Library/Application Support/ArkHeart/user_config.yaml`
    - Linux: `~/.config/ArkHeart/user_config.yaml`
- *(注：如果文件不存在，请先启动一次应用，它会自动创建。)*

### 2. 进行你的第一个修改

假设你想让你的宠物更“任性”一点。

1.  打开`default_config.yaml`，找到相关参数：
    ```yaml
    # in default_config.yaml
    persona:
      defaults:
        L2_personality_traits:
          obedience: 0.8
    ```
2.  打开你的`user_config.yaml`（它一开始可能是空的），并只写入你**想要覆盖**的部分：
    ```yaml
    # in your user_config.yaml
    persona:
      defaults:
        L2_personality_traits:
          obedience: 0.5 # 将服从度从0.8降到0.5
    ```
3.  **保存文件并重启“大脑”服务。** 下次启动时，你的宠物就会以新的`obedience`值来运行，变得更有主见了。

### 3. 如何恢复默认设置？

- 如果你把配置改乱了，最简单的恢复方法就是**删除或清空你的 `user_config.yaml` 文件**，然后重启“大脑”。系统将自动恢复到安全的默认设置。

---

## 📜 配置加载机制 (How Configuration Works)

系统采用**分层覆盖**的机制来加载配置，这给予了极高的灵活性和安全性。

1.  **`default_config.yaml` (程序内置):**
    - 这是系统的“**出厂设置**”和“**唯一真理之源**”。它定义了**所有**可配置项的结构和最安全的默认值。**请把它当作一本只读的“字典”。**

2.  **`user_config.yaml` (用户自定义):**
    - 这是你的“**个性化MOD**”。你在这里写入的任何值，都会**覆盖**掉`default_config.yaml`中的同名值。系统会进行深度合并，你无需复制整个文件，只需写出你想改动的部分。

---

## 🔑 关键可配置项详解 (Key Configurable Parameters)

以下是`default_config.yaml`中一些最有趣、最强大的配置项说明。

### 功能开关 (Feature Flags)

- **位置：** `features:`
- **作用：** 这是整个系统各大功能模块的总开关，`true`为开启，`false`为关闭。
    - **`enable_autonomous_learning:`** 宠物是否会在空闲时自主“上网学习”？
    - **`enable_romance_system:`** (实验性) 是否开启高级情感（爱情）模块？
    - **`rpg_attributes.enable_rpg_system:`** 是否启用“高级RPG属性”系统？关闭后，所有RPG属性将使用标准默认值。

### 核心人格 (Core Persona)

- **位置：** `persona: defaults:`
- **作用：** 这里定义了宠物的“灵魂”。
    - **`L2_personality_traits:`** 调整所有PPM性格模型和（在开启后）高级RPG属性的基础值。
    - **`L4_narrative_layer:`**
        - **`core_drives:`** 调整宠物的“原型”，决定了它最底层的动机（成为“守护者”还是“探索者”？）。
        - **`persona_description:`** **[最强大的配置]** 在这里用自然语言写入你为宠物设计的完整“人设剧本”，AI会尝试去理解并扮演它。

### 算法参数 (Algorithm Parameters)

- **位置：** `algorithms:`
- **作用：** **[硬核]** 这里是AI行为“物理定律”的调节旋钮。
    - **`prospect_theory.lambda_coefficient:`** 调整宠物对“损失”的敏感度。值越高，它对负面事件的反应就越强烈。
    - **`decision_priority.L1_weight` 等:** 调整AI在决策时，对“用户指令”、“生理本能”、“情感驱动”等的权重。想让它更“听话”？提高`L1_weight`。想让它更“情绪化”？提高`L3_weight`。

### 服务配置 (Service Configurations)

- **位置：** `services:`
- **作用：** 配置与外部世界的连接。
    - **`llm.provider:`** 在已支持的服务商之间切换（如`"OpenAI"` -> `"Anthropic"`）。
    - **`llm.api_key:`** **[重要]** 如果你想使用自己的API Key，请在这里填入（推荐使用`.env`文件）。
    - **`llm.model_smart:`** 定义在进行复杂思考时，使用的具体模型名称（如`"gpt-4o"`）。

---