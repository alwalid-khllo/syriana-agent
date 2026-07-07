<p align="center">
  <img src="assets/banner.gif" alt="Syriana Agent" width="100%">
</p>

# Syriana Agent ☤

<p align="center">
  <a href="https://github.com/fixology/syriana-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://t.me/syriana_ai"><img src="https://img.shields.io/badge/Telegram-Syriana_AI-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"></a>
  <a href="#-arabic-عربي"><img src="https://img.shields.io/badge/Lang-العربية-red?style=for-the-badge" alt="Arabic"></a>
</p>

---

## 🌟 Overview

**Syriana Agent** is a powerful, open-source AI agent platform that runs anywhere — your terminal, Telegram, Discord, or desktop. It supports any AI model provider (OpenAI, OpenRouter, local models, and more) and features a unique **built-in learning loop** that creates skills from experience, remembers across conversations, and improves over time.

Whether you're a developer, power user, or AI enthusiast, Syriana gives you a production-grade AI assistant that you can install, configure, and use in minutes.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Provider** | Works with OpenAI, OpenRouter, Anthropic, Google, local models, and 20+ providers |
| 📍 **Anywhere** | CLI, Telegram, Discord, Slack, WhatsApp, Signal, Email, Desktop |
| 🔄 **Learning Loop** | Creates skills from experience, improves them during use, persists memory |
| 🔌 **Extensible** | Plugins, Skills, MCP servers — extend without touching core |
| 🖥️ **Cross-Platform** | Linux, macOS, Windows, Android (Termux) |
| 🆓 **Free & Open Source** | MIT License — self-host, modify, share |
| 🌐 **Arabic Support** | Full Arabic terminal support via ConEmu on Windows |

---

## 🚀 Quick Install

### Linux / macOS / WSL

```bash
curl -fsSL https://raw.githubusercontent.com/fixology/syriana-agent/main/scripts/install.sh | bash
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "iex (irm https://raw.githubusercontent.com/fixology/syriana-agent/main/scripts/install.ps1)"
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
# Set your API key (OpenAI, OpenRouter, etc.)
syriana config set OPENROUTER_API_KEY your_key_here

# Start chatting
syriana chat

# Or run the gateway for Telegram/Discord
syriana gateway run
```

---

## 📦 What's Included

| Component | Description |
|-----------|-------------|
| `syriana` | CLI — chat, config, skills, tools |
| `gateway/` | Messaging gateway (Telegram, Discord, Slack...) |
| `plugins/` | 30+ plugins extending functionality |
| `skills/` | Built-in skills library |
| `apps/` | Desktop app (macOS/Windows/Linux) |
| `website/` | Documentation site (Docusaurus) |
| `tests/` | 1,900+ tests |

---

## 💬 Community & Support

- **Telegram Group:** [https://t.me/syriana_ai](https://t.me/syriana_ai) — Join us! Ask questions, share ideas, contribute
- **GitHub Issues:** Bug reports & feature requests
- **Documentation:** Full docs at [syriana-agent.fixology.dev](https://syriana-agent.fixology.dev)

---

## 🤝 Contributing

We welcome contributions from everyone! See our [Contributing Guide](CONTRIBUTING.md) to get started.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<br>

# <a name="arabic"></a> 🇸🇦 سيريانا أيجنت — الدليل الكامل بالعربية

<p align="center">
  <img src="assets/banner.gif" alt="Syriana Agent" width="100%">
</p>

## 🌟 نظرة عامة

**سيريانا أيجنت (Syriana Agent)** هو وكيل ذكاء اصطناعي مفتوح المصدر، يعمل في أي مكان — في التيرمنال، تلغرام، دسكورد، أو سطح المكتب. يدعم أي مزود نماذج ذكاء اصطناعي (OpenAI، OpenRouter، نماذج محلية، وغيرها)، ويتميز بـ **حلقة تعلم مدمجة** تنشئ مهارات جديدة من التجارب، تتذكر عبر المحادثات، وتتحسن مع الوقت.

سواء كنت مطوراً أو مستخدماً متقدماً أو مهتماً بالذكاء الاصطناعي، سيريانا تعطيك وكيلاً احترافياً يمكنك تثبيته وتشغيله في دقائق.

### ✨ المميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 🧠 **مزوّدات متعددة** | يدعم OpenAI، OpenRouter، Anthropic، Google، نماذج محلية، وأكثر |
| 📍 **يعمل في أي مكان** | تيرمنال، تلغرام، دسكورد، سلاك، واتساب، سيغنال، إيميل، سطح مكتب |
| 🔄 **حلقة تعلم** | ينشئ مهارات من التجارب، يحسّنها أثناء الاستخدام، يحفظ الذاكرة |
| 🔌 **قابل للتوسيع** | بلجنز، مهارات، خوادم MCP — وسّع دون لمس النواة |
| 🖥️ **متعدد المنصات** | لينكس، ماك، ويندوز، أندرويد (Termux) |
| 🆓 **مجاني ومفتوح المصدر** | رخصة MIT — استضف بنفسك، عدّل، شارك |

---

## 🚀 التثبيت السريع

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/fixology/syriana-agent/main/scripts/install.sh | bash
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "iex (irm https://raw.githubusercontent.com/fixology/syriana-agent/main/scripts/install.ps1)"
```

### ⚠️ هام لمستخدمي ويندوز العرب — ConEmu

> **مشكلة:** التيرمنال الافتراضي في ويندوز (Command Prompt / PowerShell) لا يدعم الكتابة باللغة العربية بشكل صحيح — الأحرف تظهر مقلوبة أو مشوهة.
>
> **الحل:** استخدم **ConEmu** — تيرمنال مجاني ومتطور يدعم العربية بشكل كامل.

**طريقة التثبيت:**

1. حمّل ConEmu من الموقع الرسمي: [https://conemu.github.io](https://conemu.github.io)
2. ثبّته وشغّله
3. داخل ConEmu، شغّل أمر التثبيت الخاص بويندوز (أعلاه)

ConEmu سيعرض لك العربية بشكل صحيح مع دعم كامل للـ RTL.

### Android (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
pip install syriana-agent --no-deps
```

---

## 🔧 بدء الاستخدام بعد التثبيت

```bash
# ضبط مفتاح API (OpenRouter, OpenAI الخ)
syriana config set OPENROUTER_API_KEY مفتاحك_هنا

# بدء المحادثة
syriana chat

# أو تشغيل gateway لـ تلغرام/دسكورد
syriana gateway run
```

---

## 💬 انضم إلينا

**مجموعة التلغرام:** [https://t.me/syriana_ai](https://t.me/syriana_ai)

انضم إلى مجتمع سيريانا! شاركنا أفكارك، اسأل، ساهم في تطوير المشروع. نرحب بالجميع — مطورين، مستخدمين، ومهتمين.

---

## 📄 الترخيص

MIT — راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

<p align="center">
  Made with ❤️ by <a href="https://fixology.dev">fixology Research</a> — Open source for everyone
</p>
