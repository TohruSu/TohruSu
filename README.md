<picture>
  <source media="(max-width: 600px)" srcset="./assets/hero-mobile.svg">
  <img src="./assets/hero.svg" width="960" alt="Tohru — software, systems, and applied AI. A navy engineering panel with an abstract signal trace.">
</picture>

# Hi, I'm Tohru.

**Software engineering, with a systems mindset.**

Master's student at **Waseda University**, Graduate School of Information, Production and Systems · Expected graduation: **March 2028**.

[Featured projects](#featured-projects) · [Experience](#experience-highlights) · [Toolkit](#technical-toolkit) · [Beyond the code](#beyond-the-code)

## About me

I enjoy building backend services and web applications, then looking closer at how they behave: timing on Linux, data flowing between components, and the boundaries of an AI prototype. I care about clear interfaces, reproducible tests, and documentation that makes the results easy to inspect.

My background spans software engineering, computer vision, multimodal sensing, and control simulation. I hold a **Bachelor of Engineering in Software Engineering from Xiamen University**.

## Now exploring

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/prompt.svg">
  <img src="./assets/prompt.gif" width="24" height="16" alt="">
</picture> <strong>Learning focus</strong>

**Deepening:** systems programming, performance analysis, and backend design.<br>
**Exploring:** applied AI, hardware-aware computing, and hardware design, verification, and optimization.

## Experience highlights

- **Rakuten Group · Software engineering internship** — Python/Flask backend features and search logic; React/TypeScript UI improvements for a furniture combination search app.
- **DENSO · Automotive SoC performance evaluation** — C programming, experimental measurements, and issue analysis.
- **TokiTech · Web system development** — Business web systems using Java/Spring Boot, Vue.js, and databases.

## Featured projects

Three ways I approach engineering: measure a system, model its behavior, and connect its components.

### [Linux Wake-up Latency Benchmark](https://github.com/TohruSu/linux-wakeup-latency-benchmark)

*C11 · Linux/POSIX · Python · GitHub Actions*

A Linux toolkit for measuring application-observed wake-up lateness and analyzing the resulting CSV data.

- **Core implementation:** Absolute monotonic scheduling, checked timestamp arithmetic, and skipped-period accounting.
- **My contribution:** C collector and Python analysis pipeline with strict CSV validation, descriptive statistics, and optional visualizations.
- **Validation:** C/Python unit and integration tests, ASan/UBSan, and GCC/Clang GitHub Actions; measurements describe application observations.

**[Explore the project →](https://github.com/TohruSu/linux-wakeup-latency-benchmark)**

### [Autonomous Tractor Navigation Simulation](https://github.com/TohruSu/autonomous-tractor-navigation-sim)

*C# · .NET 10 · Stanley / Pure Pursuit · GitHub Actions*

A standalone toolkit for reproducible path tracking and controller evaluation on synthetic routes.

- **Core implementation:** Stanley and Pure Pursuit controllers, deterministic kinematic bicycle simulation, and steering constraints.
- **My contribution:** Seven synthetic scenarios, CSV evaluation metrics, and reproducible trajectory comparisons across four controller configurations.
- **Validation:** 61 automated tests, repeatable CSV/SVG outputs, and GitHub Actions; synthetic results do not establish real-vehicle performance.

**[Explore the project →](https://github.com/TohruSu/autonomous-tractor-navigation-sim)**

### [Jetson Multimodal Emergency Detection](https://github.com/TohruSu/jetson-multimodal-emergency-detection)

*Python · Jetson Nano · Depth Anything V2 · Multiprocessing · PyQt5*

A university team prototype combining pose-based fall detection, speech help keywords, and relative depth for contextual alerts.

- **Core implementation:** Team-developed sensor/inference workers, an event-fusion state machine, and a PyQt5 monitoring interface.
- **My contribution:** Depth Anything V2 integration, person ROI processing, relative-depth classification, and pose-to-depth handoff.
- **Validation:** 132 automated tests, a five-worker synthetic smoke test, and GitHub Actions; real-hardware accuracy and performance remain unverified.

**[Explore the project →](https://github.com/TohruSu/jetson-multimodal-emergency-detection)**

## Technical toolkit

### <img src="./assets/languages.svg" width="20" height="20" alt=""> Languages

**Primary:** Python · Java · JavaScript / TypeScript<br>
**Also used:** C / C++ · C#

### <img src="./assets/web.svg" width="20" height="20" alt=""> Backend & web

Spring Boot · Flask · React · Vue.js<br>
MySQL · SQLite

### <img src="./assets/systems.svg" width="20" height="20" alt=""> Systems & tools

Linux/POSIX · Git · GitHub Actions<br>
Performance measurement · Automated testing · Sanitizers

### <img src="./assets/applied.svg" width="20" height="20" alt=""> Applied engineering

Computer vision · Relative depth estimation · Multimodal sensing<br>
Reinforcement learning · Path-tracking simulation

## On GitHub

[Browse my repositories](https://github.com/TohruSu?tab=repositories) · [See contribution activity](https://github.com/TohruSu?tab=overview)

## Beyond the code

Away from the terminal, you'll find me at the piano, on a badminton court, or working on a music or video edit. I communicate in **Chinese, Japanese, and English**.

Thanks for stopping by. Pick a project above and take a look at how it works.
