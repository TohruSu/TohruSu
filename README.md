<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="./assets/hero-mobile.png">
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/hero.png">
  <source media="(max-width: 600px)" srcset="./assets/hero-mobile.gif">
  <img src="./assets/hero.gif" width="960" alt="Tohru — Software Engineering / Hardware Verification. Waseda University · Kimura Lab. Focus: digital design, verification, optimization.">
</picture>

# Hi, I'm Tohru.

I'm a master's student at Graduate School of Information, Production and Systems, **Waseda University**, with a background in **Software Engineering at Xiamen University**.

I build and evaluate software across **Linux systems, backend engineering, and applied AI**. I care about reliable implementations, reproducible experiments, and tests that reveal both system behavior and its limitations. I'm currently learning **digital hardware design and verification** as I explore research-oriented engineering.

**Selected work:** [Linux Wake-up Latency Benchmark](https://github.com/TohruSu/linux-wakeup-latency-benchmark) · [PathReplay](https://github.com/TohruSu/PathReplay) · [RepoPort](https://github.com/TohruSu/RepoPort) · [RoomShelf](https://github.com/TohruSu/roomshelf-catalog-explorer) · [AdaptiveQueue](https://github.com/TohruSu/adaptivequeue)

**Connect:** [Email](mailto:suyanyu.cs@gmail.com) · [University email](mailto:yanyu.su@toki.waseda.jp) · [LinkedIn](https://www.linkedin.com/in/tohru-watanabe) · [ORCID](https://orcid.org/0009-0002-5960-6106)

## Current focus

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/prompt.svg">
  <img src="./assets/prompt.gif" width="24" height="16" alt="">
</picture> <strong>Currently</strong>

I'm strengthening my foundations in **hardware design and verification** while continuing work on **Linux performance measurement, backend systems, and reproducible experimental evaluation**.

## Experience

- **Rakuten Group · Software engineering intern** — Worked with Python/Flask and React/TypeScript on search features and the interface for a furniture discovery application.
- **DENSO · Automotive SoC internship** — Used C and measurement tools to investigate system wake-up timing and performance issues.
- **TokiTech · Web developer** — Worked on business applications with Java/Spring Boot, Vue.js, and databases.

## Featured projects

My portfolio focuses on **systems programming, developer tooling, full-stack engineering, and reproducible algorithm experiments**, with additional work in computer vision, robotics simulation, and data analysis.

### [Linux Wake-up Latency Benchmark](https://github.com/TohruSu/linux-wakeup-latency-benchmark)

*C11 · Linux/POSIX · Python · GitHub Actions*

A Linux toolkit for measuring application-observed wake-up lateness and analyzing the resulting CSV data.

- **Core implementation:** Absolute monotonic scheduling, checked timestamp arithmetic, and skipped-period accounting.
- **My work:** C collector and Python analysis pipeline with strict CSV validation, descriptive statistics, and visualizations.
- **Verification:** C/Python tests, ASan/UBSan, and GCC/Clang GitHub Actions.

### [RepoPort — Git Filename Portability Checker](https://github.com/TohruSu/RepoPort)

*Python 3.11+ · Git · Unicode · GitHub Actions*

A small, read-only CLI that flags potentially non-portable Git-tracked paths, including case/Unicode collisions and Windows-incompatible names.

- **Core implementation:** NUL-delimited Git index scanning, Unicode case/NFC checks, Windows filename rules, deterministic diagnostics, and CI-friendly exit codes.
- **My work:** MVP scoping and acceptance criteria, implementation review, regression testing, and release validation.
- **Verification:** 19 automated tests, Ubuntu/Windows CI with Python 3.11/3.14.

### [PathReplay — 2D Trajectory CSV Viewer](https://github.com/TohruSu/PathReplay)

*React · TypeScript · Vite · SVG · Vitest · GitHub Actions*

A browser-based tool for comparing and replaying 2D trajectories from local CSV files. [Try the live demo](https://tohrusu.github.io/PathReplay/).

- **Core implementation:** Local CSV validation and grouping, equal-scale SVG plotting, timestamp-based interpolation, and interactive replay for one or two trajectories.
- **My work:** MVP scoping and acceptance criteria, implementation review, regression verification, and browser-based release acceptance.
- **Verification:** 52 automated tests, successful CI and GitHub Pages deployment, and import of 14,342 synthetic simulator samples across 28 trajectory runs.

### [RoomShelf — Furniture Catalog Explorer](https://github.com/TohruSu/roomshelf-catalog-explorer)

*React 19 · TypeScript · Flask · SQLite · Playwright*

A full-stack furniture catalog for exploring products, comparing specifications, and saving favorites without an account.

- **Core implementation:** URL-driven catalog queries, product comparison, transactional SQLite shortlists, and signed sessions with CSRF/Origin checks.
- **My work:** Project scoping, technical design, feature development and review, testing, and documentation.
- **Verification:** 393 backend tests, 223 frontend tests, 40 Chromium browser tests, and GitHub Actions.

### [AdaptiveQueue — RL Job Scheduling](https://github.com/TohruSu/adaptivequeue)

*Python · Tabular Q-Learning · Scheduling Algorithms · pytest · GitHub Actions*

A scheduling simulator that explores when learned policy selection can improve on fixed rules under changing job workloads.

- **Core implementation:** Discrete-time task simulation, four deterministic scheduling baselines, and a tabular Q-Learning meta-scheduler.
- **My work:** Scheduling and reward design, implementation review, and reproducible benchmark analysis.
- **Verification:** 81 automated tests, Python 3.10/3.12 CI, and 720 seeded evaluation records across three workload scenarios.

### [Jetson Multimodal Emergency Detection](https://github.com/TohruSu/jetson-multimodal-emergency-detection)

*Python · Jetson Nano · Depth Anything V2 · Multiprocessing · PyQt5*

A university team prototype combining pose-based fall detection, speech help keywords, and relative depth for contextual alerts.

- **Core implementation:** Sensor and inference workers, event-fusion logic, and a PyQt5 monitoring interface.
- **My work:** Depth Anything V2 integration, person ROI processing, and pose-to-depth handoff.
- **Verification:** 132 automated tests, a synthetic five-worker smoke test, and GitHub Actions.

### [Autonomous Tractor Navigation Simulation](https://github.com/TohruSu/autonomous-tractor-navigation-sim)

*C# · .NET 10 · Stanley / Pure Pursuit · GitHub Actions*

A standalone toolkit for reproducible path tracking and controller evaluation on synthetic routes.

- **Core implementation:** Stanley and Pure Pursuit controllers, deterministic bicycle-model simulation, and steering constraints.
- **My work:** Seven synthetic scenarios, CSV evaluation metrics, and trajectory comparisons across four controller configurations.
- **Verification:** 61 automated tests, repeatable CSV/SVG outputs, and GitHub Actions.

### [Retail Customer Segmentation & Strategy](https://github.com/TohruSu/retail-customer-segmentation)

*Python · pandas · scikit-learn · PCA / KMeans · GitHub Actions*

From exploring shopping behavior to designing 「今日の食えらび編集室」, a meal-choice experience for food retail.

- **Core implementation:** Synthetic data generation, preprocessing, PCA/KMeans diagnostics, and an eight-stage analysis workflow.
- **My work:** Customer analysis, interpretation, and the original meal-choice retail strategy concept.
- **Verification:** 72 automated tests, eight executable notebooks, reproducible outputs, and Python 3.11–3.13 CI.

## Tools I use

### <img src="./assets/languages.svg" width="20" height="20" alt=""> Languages

**Most often:** Python · Java · JavaScript / TypeScript  
**Also:** C / C++ · C#

### <img src="./assets/web.svg" width="20" height="20" alt=""> Web development

Spring Boot · Flask · React · Vue.js  
MySQL · SQLite

### <img src="./assets/systems.svg" width="20" height="20" alt=""> Systems and tooling

Linux/POSIX · Git · GitHub Actions  
Performance measurement · Automated testing · Sanitizers

### <img src="./assets/applied.svg" width="20" height="20" alt=""> Other interests

Computer vision · Depth estimation · Multimodal sensing  
Reinforcement learning · Path-tracking simulation

## Outside of code

I play the piano, enjoy badminton, and occasionally spend far too much time editing music videos. I speak Chinese, Japanese, and English.

Thanks for visiting. If something here catches your eye, feel free to explore the code!
