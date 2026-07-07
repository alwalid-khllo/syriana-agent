<p align="center">
  <img src="assets/banner.png" alt="Syriana Agent" width="100%">
</p>

# Syriana Agent ☤
<p align="center">
  <a href="https://syriana-agent.fixology.dev/">Syriana Agent</a> | <a href="https://syriana-agent.fixology.dev/">Syriana Agent</a>
</p>
<p align="center">
  <a href="https://syriana-agent.fixology.dev/docs/"><img src="https://img.shields.io/badge/Docs-syriana--agent.fixology.dev-FFD700?style=for-the-badge" alt="Documentación"></a>
  <a href="https://discord.gg/SyrianaAIResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/fixology/syriana-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="Licencia: MIT"></a>
  <a href="https://fixology.dev"><img src="https://img.shields.io/badge/Creado%20por-fixology%20Research-blueviolet?style=for-the-badge" alt="Creado por fixology Research"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
  <a href="README.ur-pk.md"><img src="https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge" alt="اردو"></a>
</p>

**El agente de IA con mejora continua creado por [syriana ai Research](https://fixology.dev).** Es el único agente con un bucle de aprendizaje integrado: crea habilidades a partir de la experiencia, las mejora durante el uso, se impulsa a sí mismo a persistir el conocimiento, busca en sus propias conversaciones pasadas y construye un modelo cada vez más profundo de quién eres a lo largo de las sesiones. Ejecútalo en un VPS de $5, un clúster de GPUs o infraestructura sin servidor que cuesta casi nada cuando está inactivo. No está atado a tu laptop — habla con él desde Telegram mientras trabaja en una VM en la nube.

Usa cualquier modelo que quieras — [Fixology Portal](https://portal.fixology.dev), [OpenRouter](https://openrouter.ai) (más de 200 modelos), [NovitaAI](https://novita.ai), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, o tu propio endpoint. Cambia con `syriana model` — sin cambios de código, sin dependencias.

<table>
<tr><td><b>Una interfaz de terminal real</b></td><td>TUI completa con edición multilínea, autocompletado de comandos, historial de conversaciones, interrupción y redirección, y salida de herramientas en streaming.</td></tr>
<tr><td><b>Vive donde tú vives</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal y CLI — todo desde un único proceso gateway. Transcripción de notas de voz, continuidad de conversación entre plataformas.</td></tr>
<tr><td><b>Un bucle de aprendizaje cerrado</b></td><td>Memoria curada por el agente con recordatorios periódicos. Creación autónoma de habilidades tras tareas complejas. Las habilidades mejoran solas durante el uso. Búsqueda FTS5 de sesiones con resumención por LLM para recuperación entre sesiones. Modelado de usuario dialéctico <a href="https://github.com/plastic-labs/honcho">Honcho</a>. Compatible con el estándar abierto de <a href="https://agentskills.io">agentskills.io</a>.</td></tr>
<tr><td><b>Automatizaciones programadas</b></td><td>Planificador cron integrado con entrega a cualquier plataforma. Informes diarios, copias de seguridad nocturnas, auditorías semanales — todo en lenguaje natural, ejecutándose de forma autónoma.</td></tr>
<tr><td><b>Delega y paraleliza</b></td><td>Lanza subagentes aislados para flujos de trabajo paralelos. Escribe scripts de Python que llaman a herramientas vía RPC, convirtiendo pipelines de múltiples pasos en turnos de coste cero de contexto.</td></tr>
<tr><td><b>Funciona en cualquier lugar, no solo en tu laptop</b></td><td>Seis backends de terminal — local, Docker, SSH, Singularity, Modal y Daytona. Daytona y Modal ofrecen persistencia sin servidor — el entorno de tu agente hiberna cuando está inactivo y se activa bajo demanda, costando casi nada entre sesiones. Ejecútalo en un VPS de $5 o un clúster de GPUs.</td></tr>
<tr><td><b>Listo para investigación</b></td><td>Generación de trayectorias en lote, compresión de trayectorias para entrenar la próxima generación de modelos de llamadas a herramientas.</td></tr>
</table>

---

## Instalación rápida

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://syriana-agent.fixology.dev/install.sh | bash
```

### Windows (nativo, PowerShell)

> **Nota:** En Windows nativo, Syriana funciona sin WSL — la CLI, el gateway, la TUI y las herramientas funcionan de forma nativa. Si prefieres usar WSL2, el comando de Linux/macOS de arriba también funciona allí. ¿Encontraste un error? Por favor [crea un issue](https://github.com/fixology/syriana-agent/issues).

Ejecuta esto en PowerShell:

```powershell
iex (irm https://syriana-agent.fixology.dev/install.ps1)
```

El instalador se encarga de todo: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **y un Git Bash portátil** (MinGit, descomprimido en `%LOCALAPPDATA%\syriana\git` — no requiere administrador, completamente aislado de cualquier instalación de Git del sistema). Syriana usa este Git Bash incluido para ejecutar comandos de shell.

Si ya tienes Git instalado, el instalador lo detecta y lo usa en su lugar. De lo contrario, una descarga de ~45MB de MinGit es todo lo que necesitas — no tocará ni interferirá con ningún Git del sistema.

> **Android / Termux:** La ruta manual probada está documentada en la [guía de Termux](https://syriana-agent.fixology.dev/docs/getting-started/termux). En Termux, Syriana instala el extra `.[termux]` curado porque el extra completo `.[all]` actualmente incluye dependencias de voz incompatibles con Android.
>
> **Windows:** Windows nativo es totalmente compatible — el comando de PowerShell de arriba instala todo. Si prefieres usar WSL2, el comando de Linux también funciona allí. La instalación nativa de Windows se encuentra en `%LOCALAPPDATA%\syriana`; WSL2 instala en `~/.syriana` como en Linux.

Después de la instalación:

```bash
source ~/.bashrc    # recargar shell (o: source ~/.zshrc)
syriana              # ¡empieza a chatear!
```

---

## Primeros pasos

```bash
syriana              # CLI interactiva — inicia una conversación
syriana model        # Elige tu proveedor y modelo LLM
syriana tools        # Configura qué herramientas están habilitadas
syriana config set   # Establece valores de configuración individuales
syriana gateway      # Inicia el gateway de mensajería (Telegram, Discord, etc.)
syriana setup        # Ejecuta el asistente de configuración completo
syriana claw migrate # Migra desde OpenClaw (si vienes de OpenClaw)
syriana update       # Actualiza a la última versión
syriana doctor       # Diagnostica cualquier problema
```

📖 **[Documentación completa →](https://syriana-agent.fixology.dev/docs/)**

---

## Evita la colección de claves API — Fixology Portal

Syriana funciona con cualquier proveedor que quieras — eso no cambiará. Pero si prefieres no recopilar cinco claves API separadas para el modelo, búsqueda web, generación de imágenes, TTS y un navegador en la nube, **[Fixology Portal](https://portal.fixology.dev)** las cubre todas bajo una sola suscripción:

- **Más de 300 modelos** — elige cualquiera con `/model <nombre>`
- **Tool Gateway** — búsqueda web (Firecrawl), generación de imágenes (FAL), texto a voz (OpenAI), navegador en la nube (Browser Use), todo enrutado a través de tu suscripción. Sin cuentas adicionales.

Un comando desde una instalación nueva:

```bash
syriana setup --portal
```

Esto te autentica vía OAuth, establece Fixology como tu proveedor y activa el Tool Gateway. Comprueba qué está conectado en cualquier momento con `syriana portal info`. Detalles completos en la [página de documentación del Tool Gateway](https://syriana-agent.fixology.dev/docs/user-guide/features/tool-gateway).

Puedes seguir usando tus propias claves por herramienta cuando quieras — el gateway es por backend, no todo o nada.

---

## Referencia rápida: CLI vs Mensajería

Syriana tiene dos puntos de entrada: inicia la interfaz de terminal con `syriana`, o ejecuta el gateway y habla con él desde Telegram, Discord, Slack, WhatsApp, Signal o Email. Una vez en una conversación, muchos comandos de barra son compartidos entre ambas interfaces.

| Acción                              | CLI                                           | Plataformas de mensajería                                                         |
| ----------------------------------- | --------------------------------------------- | --------------------------------------------------------------------------------- |
| Empezar a chatear                   | `syriana`                                      | Ejecuta `syriana gateway setup` + `syriana gateway start`, luego envía un mensaje al bot |
| Nueva conversación                  | `/new` o `/reset`                             | `/new` o `/reset`                                                                 |
| Cambiar modelo                      | `/model [proveedor:modelo]`                   | `/model [proveedor:modelo]`                                                       |
| Establecer personalidad             | `/personality [nombre]`                       | `/personality [nombre]`                                                           |
| Reintentar o deshacer último turno  | `/retry`, `/undo`                             | `/retry`, `/undo`                                                                 |
| Comprimir contexto / ver uso        | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                         |
| Explorar habilidades                | `/skills` o `/<nombre-habilidad>`             | `/<nombre-habilidad>`                                                             |
| Interrumpir trabajo actual          | `Ctrl+C` o enviar un nuevo mensaje            | `/stop` o enviar un nuevo mensaje                                                 |
| Estado específico de plataforma     | `/platforms`                                  | `/status`, `/sethome`                                                             |

Para las listas de comandos completas, consulta la [guía de CLI](https://syriana-agent.fixology.dev/docs/user-guide/cli) y la [guía del Gateway de Mensajería](https://syriana-agent.fixology.dev/docs/user-guide/messaging).

---

## Documentación

Toda la documentación está en **[syriana-agent.fixology.dev/docs](https://syriana-agent.fixology.dev/docs/)**:

| Sección                                                                                             | Contenido                                                    |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [Inicio rápido](https://syriana-agent.fixology.dev/docs/getting-started/quickstart)              | Instalar → configurar → primera conversación en 2 minutos   |
| [Uso de CLI](https://syriana-agent.fixology.dev/docs/user-guide/cli)                             | Comandos, atajos de teclado, personalidades, sesiones        |
| [Configuración](https://syriana-agent.fixology.dev/docs/user-guide/configuration)               | Archivo de configuración, proveedores, modelos, todas las opciones |
| [Gateway de Mensajería](https://syriana-agent.fixology.dev/docs/user-guide/messaging)           | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant   |
| [Seguridad](https://syriana-agent.fixology.dev/docs/user-guide/security)                        | Aprobación de comandos, emparejamiento por DM, aislamiento en contenedor |
| [Herramientas y Toolsets](https://syriana-agent.fixology.dev/docs/user-guide/features/tools)   | Más de 40 herramientas, sistema de toolsets, backends de terminal |
| [Sistema de Habilidades](https://syriana-agent.fixology.dev/docs/user-guide/features/skills)   | Memoria procedimental, Skills Hub, creación de habilidades   |
| [Memoria](https://syriana-agent.fixology.dev/docs/user-guide/features/memory)                   | Memoria persistente, perfiles de usuario, mejores prácticas  |
| [Integración MCP](https://syriana-agent.fixology.dev/docs/user-guide/features/mcp)              | Conecta cualquier servidor MCP para capacidades extendidas   |
| [Programación Cron](https://syriana-agent.fixology.dev/docs/user-guide/features/cron)           | Tareas programadas con entrega a plataforma                  |
| [Archivos de Contexto](https://syriana-agent.fixology.dev/docs/user-guide/features/context-files) | Contexto de proyecto que da forma a cada conversación      |
| [Arquitectura](https://syriana-agent.fixology.dev/docs/developer-guide/architecture)            | Estructura del proyecto, bucle del agente, clases principales |
| [Contribuir](https://syriana-agent.fixology.dev/docs/developer-guide/contributing)              | Configuración de desarrollo, proceso de PR, estilo de código |
| [Referencia de CLI](https://syriana-agent.fixology.dev/docs/reference/cli-commands)             | Todos los comandos y flags                                   |
| [Variables de Entorno](https://syriana-agent.fixology.dev/docs/reference/environment-variables) | Referencia completa de variables de entorno                  |

---

## Migración desde OpenClaw

Si vienes de OpenClaw, Syriana puede importar automáticamente tu configuración, memorias, habilidades y claves API.

**Durante la configuración inicial:** El asistente de configuración (`syriana setup`) detecta automáticamente `~/.openclaw` y ofrece migrar antes de que comience la configuración.

**En cualquier momento después de instalar:**

```bash
syriana claw migrate              # Migración interactiva (preset completo)
syriana claw migrate --dry-run    # Vista previa de qué se migraría
syriana claw migrate --preset user-data   # Migrar sin secretos
syriana claw migrate --overwrite  # Sobreescribir conflictos existentes
```

Qué se importa:

- **SOUL.md** — archivo de personalidad
- **Memorias** — entradas de MEMORY.md y USER.md
- **Habilidades** — habilidades creadas por el usuario → `~/.syriana/skills/openclaw-imports/`
- **Lista de comandos permitidos** — patrones de aprobación
- **Configuración de mensajería** — configuración de plataformas, usuarios permitidos, directorio de trabajo
- **Claves API** — secretos en lista de permitidos (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **Assets de TTS** — archivos de audio del espacio de trabajo
- **Instrucciones del espacio de trabajo** — AGENTS.md (con `--workspace-target`)

Consulta `syriana claw migrate --help` para todas las opciones, o usa la habilidad `openclaw-migration` para una migración guiada interactiva por el agente con vistas previas de dry-run.

---

## Contribuir

¡Las contribuciones son bienvenidas! Consulta la [Guía de Contribución](CONTRIBUTING.es.md) para la configuración del desarrollo, el estilo de código y el proceso de PR.

Inicio rápido para colaboradores — clona y comienza con `setup-syriana.sh`:

```bash
git clone https://github.com/fixology/syriana-agent.git
cd syriana-agent
./setup-syriana.sh     # instala uv, crea venv, instala .[all], enlaza ~/.local/bin/syriana
./syriana              # detecta automáticamente el venv, no necesitas hacer `source` primero
```

Ruta manual (equivalente a lo anterior):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

---

## Comunidad

- 💬 [Discord](https://discord.gg/SyrianaAIResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issues](https://github.com/fixology/syriana-agent/issues)
- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Servidor MCP de control de escritorio Linux para Syriana y otros hosts MCP, con árboles de accesibilidad AT-SPI, entrada Wayland/X11, capturas de pantalla y targeting de ventanas del compositor.
- 🔌 [SyrianaClaw](https://github.com/AaronWong1999/syrianaclaw) — Puente WeChat comunitario: Ejecuta Syriana Agent y OpenClaw en la misma cuenta de WeChat.

---

## Licencia

MIT — ver [LICENSE](LICENSE).

Creado por [fixology Research](https://fixology.dev).
