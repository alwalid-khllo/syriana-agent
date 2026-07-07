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

## 🌟 What is Syriana Agent?

**Syriana Agent** is a next-generation, open-source AI agent platform — a powerful autonomous assistant that lives in your terminal, Telegram, Discord, or desktop. Unlike ordinary chatbots, Syriana features a **built-in learning loop**: it creates skills from experience, improves them during use, remembers across conversations, and grows smarter over time.

Think of it as your **personal AI engineer** — always ready, always learning, always working for you.

---

## 🧠 Multi-Provider — Use Any AI Model You Want

Syriana is **provider-agnostic**. You bring your own API key from any provider, and Syriana works immediately — no lock-in, no subscriptions, no hidden fees.

### 🔑 Supported Providers (All Major + Local)

| Category | Providers |
|----------|-----------|
| ☁️ **Cloud APIs** | OpenAI (GPT-4, GPT-4o), Anthropic (Claude 3.5/4), Google (Gemini 2.0+), OpenRouter (200+ models), DeepSeek, Moonshot/Kimi, MiniMax, Z.AI/GLM, NVIDIA NIM, NovitaAI, Amazon Bedrock, Azure OpenAI, Google Vertex AI |
| 🏠 **Local Models** | Ollama (Llama, Mistral, Qwen, DeepSeek local), LM Studio, vLLM, Text Generation WebUI (Oobabooga) |
| 🆓 **Free APIs** | Google AI Studio (free tier), OpenRouter free models, local models (no cost) |
| 🔧 **Custom** | Any OpenAI-compatible endpoint — self-hosted, private, air-gapped |

**No vendor lock-in.** Switch between providers with a single command: `syriana model`

---

## ✨ What Makes Syriana Different?

### 🔄 Built-in Learning Loop (Unique)
Most AI agents are **stateless** — once the conversation ends, everything is forgotten. Syriana is different:
- **Creates skills** from its own experience automatically
- **Improves skills** during use based on what works
- **Persists memory** across sessions — it remembers who you are
- **Searches past conversations** for context when needed
- **Builds a user model** of your preferences and style over time

### 🛠️ Skills System
Syriana comes with a **rich library of 450+ built-in skills** that give it superpowers:

| Skill Category | Examples |
|----------------|----------|
| 💻 **Software Development** | Code review, debugging, TDD, architecture design, refactoring, Git workflows |
| 🔒 **Cybersecurity** | Penetration testing, OSINT, vulnerability analysis, forensics |
| 📊 **Data Science** | Data analysis, visualization, Jupyter notebooks, ML pipelines |
| 📝 **Productivity** | Email management, document editing, PDF manipulation, presentations |
| 🌐 **Web & Research** | Web search, YouTube transcripts, academic papers (arXiv), news monitoring |
| 🎨 **Creative** | Image generation, ASCII art, music/songwriting, video creation, architecture diagrams |
| 🏢 **Business & Finance** | Market analysis, DCF modeling, LBO modeling, presentations, Excel automation |
| 🔗 **Channels** | Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, WeChat, and more |

Each skill is a reusable capability the agent can call on demand — or create new ones automatically.

### 🌍 Works Anywhere
| Platform | Mode |
|----------|------|
| 💻 **Terminal (CLI)** | Full TUI with multiline editing, slash commands, streaming output |
| 📱 **Telegram** | Chat from your phone while Syriana runs on a cloud VM |
| 💬 **Discord** | Full bot integration with slash commands |
| 🏢 **Slack** | Team collaboration |
| 📧 **Email / SMS / Signal / WhatsApp** | Cross-platform messaging |
| 🖥️ **Desktop App** | Native macOS, Windows, Linux (Electron) |
| 🌐 **Web Dashboard** | Browser-based UI |

### 🔌 Extensible Architecture
- **30+ plugins** — extend functionality without touching core
- **450+ skills** — built-in capabilities library
- **MCP server support** — connect any MCP-compatible tool
- **Custom tools** — write your own in Python

### 🖥️ Cross-Platform
Linux, macOS, Windows (native), Android (Termux) — run it anywhere, even on a $5 VPS.

---

## 🚀 Quick Install

### Linux / macOS / WSL

```bash
curl -fsSL https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.sh | bash
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "iex (irm https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.ps1)"
```

### Windows — Arabic Users (ConEmu) 🇸🇦

> **⚠️ Important for Arabic Windows users:**
> The standard Windows Terminal does not fully support Arabic text (RTL) display. To use Syriana Agent with full Arabic support, install **ConEmu** — a modern Windows terminal that handles Arabic script perfectly.

1. Download ConEmu: [https://conemu.github.io](https://conemu.github.io)
2. Install and launch ConEmu
3. Run the PowerShell install command above inside ConEmu

### Android (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
pip install syriana-agent --no-deps
# See full guide: https://syriana-agent.fixology.dev/docs/getting-started/termux
```

---

## 🔧 Quick Start After Installation

```bash
# Set your API key (any provider)
syriana config set OPENROUTER_API_KEY your_key_here

# Or use OpenAI
syriana config set OPENAI_API_KEY sk-your_key_here

# Switch model provider any time
syriana model

# Start chatting
syriana chat

# Run gateway for Telegram / Discord
syriana gateway run

# Update to latest version
syriana update
```

---

## 📦 What's Included

| Component | Description |
|-----------|-------------|
| `syriana` CLI | Chat, config, skills, tools, gateway, cron |
| 450+ Skills | Pre-built capabilities for every domain |
| 30+ Plugins | Modular extensions for custom functionality |
| Messaging Gateway | Telegram, Discord, Slack, WhatsApp, Signal, Email |
| Desktop App | macOS, Windows, Linux (native) |
| Full Documentation | Docusaurus site with guides, API reference |
| 1,900+ Tests | Production-grade testing suite |

---

## 💬 Community & Support

- **Telegram Group:** [https://t.me/syriana_ai](https://t.me/syriana_ai) — Join us! Ask questions, share ideas, contribute
- **GitHub Issues:** Bug reports & feature requests
- **Updates:** `syriana update` pulls directly from this repository

---

## 🤝 Contributing

We welcome contributions from everyone! See our [Contributing Guide](CONTRIBUTING.md) to get started.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details. Free to use, modify, and distribute.

---

<br>

# <a name="arabic"></a> 🇸🇦 سيريانا أيجنت — الدليل الكامل بالعربية

<p align="center">
  <img src="assets/banner.gif" alt="Syriana Agent" width="100%">
</p>

## 🌟 ما هو سيريانا أيجنت؟

**سيريانا أيجنت (Syriana Agent)** هو وكيل ذكاء اصطناعي متطور مفتوح المصدر — مساعد مستقل يعمل في التيرمنال، تلغرام، دسكورد، أو سطح المكتب. على عكس روبوتات المحادثة التقليدية، سيريانا تملك **حلقة تعلم مدمجة**: تنشئ مهارات جديدة من التجارب، تحسّنها أثناء الاستخدام، تتذكر عبر المحادثات، وتزداد ذكاءً مع الوقت.

اعتبره **مهندسك الشخصي للذكاء الاصطناعي** — دائم الاستعداد، دائم التعلم، يعمل لأجلك.

---

## 🧠 يدعم كل مفاتيح API — استخدم أي مزود تريد

سيريانا **لا ترتبط بمزود معين**. أحضر مفتاح API الخاص بك من أي مزود واشتغل فوراً — لا إكراه، لا اشتراكات، لا رسوم خفية.

### 🔑 المزوّدات المدعومة (الرئيسية + المحلية)

| الفئة | المزوّدات |
|-------|-----------|
| ☁️ **سحابية** | OpenAI (GPT-4, GPT-4o), Anthropic (Claude 3.5/4), Google (Gemini 2.0+), OpenRouter (200+ نموذج), DeepSeek, Moonshot/Kimi, MiniMax, Z.AI/GLM, NVIDIA NIM, NovitaAI, Amazon Bedrock, Azure OpenAI, Google Vertex AI |
| 🏠 **نماذج محلية** | Ollama (Llama, Mistral, Qwen, DeepSeek محلي), LM Studio, vLLM, Text Generation WebUI |
| 🆓 **مجانية** | Google AI Studio, OpenRouter نماذج مجانية، نماذج محلية (بدون تكلفة) |
| 🔧 **مخصص** | أي endpoint متوافق مع OpenAI — استضف بنفسك، شبكة خاصة، معزول |

**لا يوجد ارتباط بمزوّد.** غيّر بين المزوّدات بأمر واحد: `syriana model`

---

## ✨ ما الذي يميز سيريانا عن غيرها؟

### 🔄 حلقة التعلم المدمجة (فريدة)
معظم وكلاء الذكاء الاصطناعي **عديمو الحالة** — بمجرد انتهاء المحادثة، يُنسى كل شيء. سيريانا مختلفة:
- **تنشئ مهارات** من تجاربها تلقائياً
- **تحسّن المهارات** أثناء الاستخدام بناءً على ما يعمل
- **تحفظ الذاكرة** عبر الجلسات — تتذكر من أنت
- **تبحث في المحادثات السابقة** للسياق عند الحاجة
- **تبني نموذجاً للمستخدم** لتفضيلاتك وأسلوبك مع الوقت

### 🛠️ نظام المهارات (450+ مهارة)
سيريانا تأتي مع **مكتبة غنية تضم أكثر من 450 مهارة مدمجة**:

| فئة المهارات | أمثلة |
|--------------|-------|
| 💻 **تطوير البرمجيات** | مراجعة الكود، تصحيح الأخطاء، TDD، تصميم معماري، إعادة هيكلة، Git |
| 🔒 **الأمن السيبراني** | اختبار الاختراق، OSINT، تحليل الثغرات، الطب الشرعي الرقمي |
| 📊 **علم البيانات** | تحليل البيانات، تصور بيانات، Jupyter، أنابيب ML |
| 📝 **الإنتاجية** | إدارة البريد الإلكتروني، تحرير المستندات، PDF، العروض التقديمية |
| 🌐 **البحث والويب** | بحث ويب، يوتيوب، أبحاث أكاديمية (arXiv)، متابعة أخبار |
| 🎨 **الإبداع** | توليد الصور، ASCII art، موسيقى، فيديو، مخططات معمارية |
| 🏢 **المال والأعمال** | تحليل أسواق، نمذجة مالية، Excel، عروض تقديمية |
| 🔗 **القنوات** | تلغرام، دسكورد، سلاك، واتساب، سيغنال، إيميل، SMS |

### 🌍 يعمل في أي مكان
| المنصة | الوضع |
|--------|-------|
| 💻 **التيرمنال (CLI)** | واجهة TUI كاملة مع تحرير متعدد الأسطر، أوامر مائلة، إخراج متدفق |
| 📱 **تلغرام** | دردش من هاتفك وسيريانا تعمل على سحابة VM |
| 💬 **دسكورد** | بوت متكامل مع أوامر مائلة |
| 🏢 **سلاك** | تعاون جماعي |
| 🖥️ **تطبيق سطح المكتب** | تطبيق أصلي لماك، ويندوز، لينكس |
| 🌐 **لوحة تحكم ويب** | واجهة متصفح |

### 🔌 بنية قابلة للتوسيع
- **أكثر من 30 بلجن** — وسّع الوظائف دون لمس النواة
- **أكثر من 450 مهارة** — مكتبة قدرات مدمجة
- **دعم خوادم MCP** — اتصال مع أي أداة متوافقة مع MCP
- **أدوات مخصصة** — اكتب أدواتك الخاصة بلغة Python

### 🖥️ متعدد المنصات
لينكس، ماك، ويندوز (أصلي)، أندرويد (Termux) — يعمل في أي مكان، حتى على VPS بـ 5$.

---

## 🚀 التثبيت السريع

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.sh | bash
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "iex (irm https://raw.githubusercontent.com/alwalid-khllo/syriana-agent/main/scripts/install.ps1)"
```

### ⚠️ هام لمستخدمي ويندوز العرب — ConEmu

> **مشكلة:** التيرمنال الافتراضي في ويندوز (Command Prompt / PowerShell) لا يدعم الكتابة باللغة العربية بشكل صحيح — الأحرف تظهر مقلوبة أو مشوهة.
>
> **الحل:** استخدم **ConEmu** — تيرمنال مجاني ومتطور يدعم العربية بشكل كامل.

1. حمّل ConEmu من الموقع الرسمي: [https://conemu.github.io](https://conemu.github.io)
2. ثبّته وشغّله
3. داخل ConEmu، شغّل أمر التثبيت الخاص بويندوز (أعلاه)

### Android (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
pip install syriana-agent --no-deps
```

---

## 🔧 بدء الاستخدام بعد التثبيت

```bash
# ضبط مفتاح API (من أي مزود)
syriana config set OPENROUTER_API_KEY مفتاحك_هنا

# أو استخدم OpenAI
syriana config set OPENAI_API_KEY sk-mفتاحك_هنا

# غيّر مزود النموذج في أي وقت
syriana model

# بدء المحادثة
syriana chat

# تشغيل gateway لـ تلغرام/دسكورد
syriana gateway run

# التحديث إلى آخر إصدار
syriana update
```

---

## 💬 انضم إلينا

**مجموعة التلغرام:** [https://t.me/syriana_ai](https://t.me/syriana_ai)

انضم إلى مجتمع سيريانا! شاركنا أفكارك، اسأل، ساهم في تطوير المشروع. نرحب بالجميع — مطورين، مستخدمين، ومهتمين.

---

## 📄 الترخيص

MIT — راجع ملف [LICENSE](LICENSE) للتفاصيل. مجاني للاستخدام والتعديل والنشر.

---

<p align="center">
  Made with ❤️ by <a href="https://fixology.dev">fixology Research</a> — Open source for everyone
</p>
