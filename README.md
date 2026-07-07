<p align="center">
  <img src="assets/banner.gif" alt="Syriana Agent" width="100%">
</p>

# Syriana Agent ☤

<p align="center">
  <a href="https://github.com/alwalid-khllo/syriana-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://t.me/syriana_ai"><img src="https://img.shields.io/badge/Telegram-Syriana_AI-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"></a>
  <a href="#-arabic-عربي"><img src="https://img.shields.io/badge/Lang-العربية-red?style=for-the-badge" alt="Arabic"></a>
</p>

---

> **Syriana Agent** — The self-improving AI agent with a built-in learning loop. It creates skills from experience, improves them during use, persists memory across sessions, and builds a deepening model of who you are over time. Works with any AI provider, runs on any platform, extends through plugins and skills. Open source. MIT License.

---

## 🧠 Provider-Agnostic — Use Any AI Model

Syriana works with **every major AI provider** — and many obscure ones. You bring your own API key; Syriana handles the rest. No lock-in, no subscriptions, no hidden costs.

| Category | Providers |
|----------|-----------|
| **Cloud APIs** | OpenAI (GPT-4, GPT-4o, o1, o3), Anthropic (Claude 3.5, Claude 4), Google (Gemini 2.0+), OpenRouter (200+ models), DeepSeek, Moonshot/Kimi, MiniMax, Z.AI/GLM, NVIDIA NIM, NovitaAI, Amazon Bedrock, Azure OpenAI, Google Vertex AI |
| **Local & Self-Hosted** | Ollama (every model), LM Studio, vLLM, Text Generation WebUI, llama.cpp, any OpenAI-compatible endpoint |
| **Free Tiers** | Google AI Studio, OpenRouter free models, local models (zero cost) |
| **Custom** | Bring your own endpoint — air-gapped, private, or on-premise |

Switch providers with a single command — no config files, no restarts:

```bash
syriana model
```

---

## 🔄 The Learning Loop — What Makes Syriana Different

Most AI agents are **stateless shells** — the conversation ends, everything is forgotten. Syriana is the **only open-source agent with a closed learning loop**:

- **Autonomous skill creation** — Syriana creates new skills from its own experience, without you asking
- **Skill self-improvement** — It refines skills during use, learning what works and what doesn't
- **Persistent memory** — Agent-curated memory with periodic self-nudges to retain what matters
- **Cross-session recall** — FTS5 full-text search across past conversations, with LLM summarization
- **User modeling** — Builds a deepening model of your preferences, style, and patterns across sessions

The more you use it, the better it gets. It learns like a person — by doing, remembering, and improving.

---

## 🛠️ Built-in Skills — 450+ Capabilities

Syriana ships with a **450+ skill library** that gives it superpowers across every domain:

| Domain | Skills |
|--------|--------|
| **💻 Software Development** | Code review, debugging, TDD/BDD, architecture design, refactoring, Git workflows, dependency analysis |
| **🔒 Cybersecurity** | Pentesting, OSINT, vulnerability research, forensics, fuzzing, exploit analysis, red teaming |
| **📊 Data Science & ML** | Data analysis, visualization, Jupyter notebooks, ML pipelines, feature engineering, model evaluation |
| **📝 Productivity** | Email management, document editing, PDF manipulation, presentations, note-taking, scheduling |
| **🌐 Web & Research** | Web search & extract, YouTube analysis, arXiv papers, news monitoring, blog tracking, RSS |
| **🎨 Creative** | Image generation, ASCII art, music & songwriting, video creation, infographics, architecture diagrams |
| **🏢 Business & Finance** | Market analysis, DCF/LBO/M&A modeling, Excel automation, pitch decks, financial reports |
| **🔗 Communication** | Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, WeChat, Matrix, Teams |

Each skill is a **reusable, composable capability** that Syriana can call on demand — or create new ones automatically as it discovers patterns in your work.

---

## 🌍 Lives Where You Do

Syriana isn't tied to your laptop. **It runs everywhere** — and you talk to it from anywhere:

| Interface | Details |
|-----------|---------|
| **💻 Terminal (CLI)** | Full TUI — multiline editing, slash commands with autocomplete, streaming output, session history, interrupt & redirect |
| **📱 Telegram** | Chat from your phone while Syriana runs on a cloud VM. Voice memos transcribed automatically |
| **💬 Discord** | Full bot — slash commands, threads, voice channels |
| **🏢 Slack** | Team collaboration with threading |
| **📧 Email / SMS / Signal / WhatsApp** | Cross-platform messaging from a single gateway |
| **🖥️ Desktop App** | Native - macOS, Windows, Linux (Electron). Chat with streaming tool output, side-by-side previews, file browser, voice, settings |
| **🌐 Web Dashboard** | Browser-based admin & chat |

**20+ platforms from one gateway** — one process, one config, every channel.

---

## ⚡ Runs Anywhere (Not Just Your Laptop)

Deploy on infrastructure that fits your needs:

| Backend | Use Case |
|---------|----------|
| **Local** | Your machine — zero infra |
| **Docker** | Containerized, reproducible |
| **SSH** | Remote server, cloud VM |
| **Daytona** | Serverless — hibernates when idle, costs near zero |
| **Modal** | Serverless GPU/CPU |
| **Singularity** | HPC clusters |

Run it on a **$5 VPS**, a **GPU cluster**, or **serverless infrastructure** that costs nearly nothing when idle. It's not tied to your machine — talk to it from Telegram while it works on a cloud VM.

---

## 🔌 Extensible Architecture

- **30+ plugins** — Modular extensions for custom functionality (kanban, browser, image gen, cron, disk cleanup, and more)
- **450+ skills** — Built-in capability library. Also compatible with [agentskills.io](https://agentskills.io) open standard
- **MCP servers** — Connect any MCP-compatible tool with full tool filtering
- **Custom Python tools** — Write your own via `execute_code`
- **Subagent delegation** — Spawn isolated subagents for parallel workstreams

---

## 🖥️ Cross-Platform

Linux, macOS, Windows (native + WSL2), Android (Termux) — full support on every platform.

### Quick Install

**Linux / macOS / WSL:**
```bash
curl -fsSL https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "iex (irm https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.ps1)"
```

**Windows Arabic Users — ConEmu 🇸🇦:**
> The standard Windows terminal doesn't fully support Arabic (RTL) display. Install **ConEmu** ([conemu.github.io](https://conemu.github.io)) — a modern terminal that handles Arabic script perfectly — then run the install command inside it.

**Android (Termux):**
```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
pip install syriana-agent --no-deps
```

### After Installation

```bash
# Set your API key (any provider)
syriana config set OPENROUTER_API_KEY your_key_here

# Start chatting
syriana chat

# Run gateway for Telegram / Discord
syriana gateway run

# Update to the latest version
syriana update
```

---

## 📦 What's Inside

| Component | Description |
|-----------|-------------|
| `syriana` CLI | Chat, config, skills, tools, gateway, cron — full control |
| Gateway | 20+ messaging platforms — one process, every channel |
| Skills Library | 450+ built-in capabilities across every domain |
| Plugins | 30+ modular extensions |
| Desktop App | macOS, Windows, Linux — native, polished, powerful |
| Documentation | Full Docusaurus site — guides, API reference, tutorials |
| 1,900+ Tests | Production-grade — CI/CD, linting, type checking |

---

## 💬 Community

- **Telegram Group:** [https://t.me/syriana_ai](https://t.me/syriana_ai) — Join us! Ask questions, share ideas, contribute
- **GitHub Issues:** Bug reports & feature requests
- **Updates:** `syriana update` pulls directly from this repository

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details. Free to use, modify, and distribute.

---

<br>

# <a name="arabic"></a> 🇸🇦 سيريانا أيجنت — الدليل الكامل بالعربية

<p align="center">
  <img src="assets/banner.gif" alt="Syriana Agent" width="100%">
</p>

> **سيريانا أيجنت** — وكيل الذكاء الاصطناعي المحسّن ذاتياً مع حلقة تعلم مدمجة. ينشئ مهارات من التجارب، يحسّنها أثناء الاستخدام، يحفظ الذاكرة عبر الجلسات، ويبني نموذجاً متعمقاً لمن أنت مع الوقت. يعمل مع أي مزود ذكاء اصطناعي، على أي منصة، ويتوسع عبر البلجنز والمهارات. مفتوح المصدر. رخصة MIT.

---

## 🧠 محايد تجاه المزوّد — استخدم أي نموذج تريد

سيريانا تعمل مع **كل مزوّدي الذكاء الاصطناعي الرئيسيين** — وغيرهم. أحضر مفتاح API الخاص بك وسيريانا تتولى الباقي. لا إكراه، لا اشتراكات، لا تكاليف خفية.

| الفئة | المزوّدات |
|-------|-----------|
| **سحابية** | OpenAI (GPT-4, GPT-4o, o1, o3), Anthropic (Claude 3.5, Claude 4), Google (Gemini 2.0+), OpenRouter (200+), DeepSeek, Moonshot, MiniMax, Z.AI/GLM, NVIDIA NIM, Amazon Bedrock, Azure OpenAI, Google Vertex AI |
| **محلية** | Ollama, LM Studio, vLLM, Text Generation WebUI — أي نموذج تشغّله محلياً |
| **مجانية** | Google AI Studio، نماذج OpenRouter المجانية، نماذج محلية (بدون تكلفة) |
| **مخصصة** | أي endpoint متوافق مع OpenAI — شبكة خاصة، معزول، حكومي |

غيّر بين المزوّدات بأمر واحد دون تعديل أي ملف:

```bash
syriana model
```

---

## 🔄 حلقة التعلّم — ما يميز سيريانا

معظم الوكلاء **قوالب عديمة الحالة** — تنتهي المحادثة، يُنسى كل شيء. سيريانا هي **الوكيل مفتوح المصدر الوحيد بحلقة تعلم مغلقة**:

- **إنشاء مهارات ذاتي** — تنشئ مهارات جديدة من تجاربها تلقائياً دون أن تطلب
- **تحسين ذاتي للمهارات** — تحسّن مهاراتها أثناء الاستخدام، تتعلم ما ينفع وما لا ينفع
- **ذاكرة دائمة** — ذاكرة ينظمها الوكيل نفسه مع تذكيرات دورية للاحتفاظ بالمهم
- **استرجاع عبر الجلسات** — بحث كامل النص في المحادثات السابقة مع تلخيص بالذكاء الاصطناعي
- **نمذجة المستخدم** — تبني نموذجاً متعمقاً لتفضيلاتك وأسلوبك عبر الجلسات

كلما استخدمتها أكثر، أصبحت أفضل. تتعلم مثل الإنسان — بالممارسة، والتذكر، والتحسين.

---

## 🛠️ مهارات مدمجة — أكثر من 450 قدرة

سيريانا تأتي مع **مكتبة مهارات تضم أكثر من 450 قدرة** عبر كل المجالات:

| المجال | المهارات |
|--------|----------|
| **💻 تطوير برمجيات** | مراجعة كود، تصحيح أخطاء، TDD، تصميم معماري، إعادة هيكلة، Git |
| **🔒 أمن سيبراني** | اختبار اختراق، OSINT، بحث ثغرات، طب شرعي، تحليل استغلال |
| **📊 علوم بيانات** | تحليل بيانات، تصور، Jupyter، أنابيب تعلم آلة |
| **📝 إنتاجية** | بريد إلكتروني، مستندات، PDF، عروض تقديمية، جداول مواعيد |
| **🌐 بحث وويب** | بحث واستخراج ويب، يوتيوب، أبحاث أكاديمية، متابعة أخبار |
| **🎨 إبداع** | توليد صور، ASCII art، موسيقى، فيديو، إنفوغرافيك، مخططات |
| **🏢 أعمال ومالية** | تحليل أسواق، نمذجة مالية DCF/LBO، Excel، تقارير مالية |
| **🔗 تواصل** | تلغرام، دسكورد، سلاك، واتساب، سيغنال، إيميل، SMS |

كل مهارة هي **قدرة قابلة لإعادة الاستخدام** يمكن لسيريانا استدعاؤها عند الحاجة — أو إنشاء مهارات جديدة تلقائياً.

---

## 🌍 تعيش حيث تسكن

سيريانا ليست مرتبطة بجهازك المحمول. **تعمل في كل مكان** — وتتحدث معها من أي مكان:

| الواجهة | التفاصيل |
|---------|----------|
| **💻 تيرمنال (CLI)** | واجهة TUI كاملة — تحرير متعدد الأسطر، أوامر مائلة مع إكمال تلقائي، إخراج متدفق |
| **📱 تلغرام** | دردش من هاتفك وسيريانا تعمل على سحابة. رسائل صوتية تتحول لنص تلقائياً |
| **💬 دسكورد** | بوت متكامل — أوامر مائلة، ثريدز، قنوات صوتية |
| **🏢 سلاك** | تعاون جماعي مع ثريدينج |
| **📧 إيميل / SMS / سيغنال / واتساب** | جميع القنوات من بوابة واحدة |
| **🖥️ تطبيق سطح مكتب** | تطبيق أصلي — ماك، ويندوز، لينكس |
| **🌐 لوحة تحكم ويب** | إدارة ودردشة من المتصفح |

**أكثر من 20 منصة من بوابة واحدة** — عملية واحدة، إعدادات واحدة، كل القنوات.

---

## ⚡ يعمل في أي مكان (ليس فقط على جهازك)

انشر على البنية التحتية التي تناسب احتياجاتك: محلي، Docker، SSH، سيرفرلس.

شغّله على **VPS بـ 5$** أو **عنقود GPU** أو **بنية تحتية serverless** لا تكلف شيئاً عند الخمول.

---

## 💬 انضم إلينا

**مجموعة التلغرام:** [https://t.me/syriana_ai](https://t.me/syriana_ai)

انضم إلى مجتمع سيريانا — مطورين، مستخدمين، مهتمين. شاركنا أفكارك، اسأل، ساهم.

---

## 📄 الترخيص

MIT — راجع [LICENSE](LICENSE) للتفاصيل. مجاني للاستخدام والتعديل والنشر.

---

<p align="center">
  Made with ❤️ by <a href="https://fixology.dev">fixology Research</a> — Open source for everyone
</p>
