# marimo for AI and ML Development

Workshop materials for the O'Reilly Live course **marimo for AI and ML Development**.

**Subtitle:** Enable reactive execution and predictable AI workflows

This repository contains the slides, notebooks, and supporting materials used for the live workshop. The course introduces **marimo**, a next-generation Python programming environment for AI and ML, and shows how to build interactive, reproducible, and reusable workflows that improve on traditional notebook-based development.

## What you'll learn

By working through these materials, participants will learn how to:

- articulate why reactive, dependency-aware execution prevents the reproducibility failures endemic to notebooks like Jupyter
- build and share reproducible AI/ML experiments using modern environment and dependency tooling alongside marimo's controlled execution model
- develop interactive data exploration and model evaluation workflows with reactive visualizations
- apply AI coding agents as active development partners to accelerate prototyping, debug models, and iterate faster across the full ML workflow
- package and deploy marimo notebooks as standalone scripts, shareable web apps, or importable Python modules without rewriting code

## Course description

Interactive programming environments are central to modern AI development, but traditional ones like Jupyter notebooks don't quite fit the bill. This workshop provides a hands-on introduction to marimo, a programming environment designed specifically for AI and ML.

The materials in this repository are organized to show how to do serious computational work in a reproducible environment while also making data, models, and visual feedback work together in a more connected way. The workflow emphasizes faster iteration, more trustworthy execution, and a clearer path from experimentation to reusable systems.

## Who this is for

This workshop is designed for people who:

- are AI or ML engineers, data scientists, or data practitioners who write Python and build models
- work with experiments, notebooks, and ML workflows in real development settings
- are curious about marimo and want to understand how it improves on traditional notebooks

## Prerequisites

- a computer with marimo installed, or access to marimo's free cloud-hosted notebook workspace, Molab
- intermediate Python proficiency
- basic familiarity with data science or ML workflows
- prior experience with Jupyter notebooks or similar interactive environments

## Repository structure

- [`Module_1`](./Module_1): why interactive programming environments matter, where traditional notebooks break, and how reactive execution works
- [`Module_2`](./Module_2): reproducibility, dependency management, and reviewable experiments
- [`Module_3`](./Module_3): interactive AI/ML workflows and live experimentation
- [`Module_4`](./Module_4): AI coding agents for AI/ML development
- [`Module_5`](./Module_5): turning interactive work into reusable systems
- [`booklet_complete.md`](./booklet_complete.md): long-form workshop narrative and supporting written material

## Workshop schedule

### Module 1: Why interactive programming environments matter for AI and ML

- Presentation: interactive environments in the modern AI/ML stack; execution order and state in notebooks; how marimo enables reactive execution and predictable workflows
- Group discussion: issues that undermine correctness, reproducibility, and iteration speed
- Hands-on exercise: predictable execution and connected data and computation

### Module 2: Reproducibility as a baseline for trustworthy AI

- Presentation: the "it works on my machine" problem; why reproducibility must be built into the environment itself
- Hands-on exercise: identifying hidden dependency and environment assumptions; examining how libraries, system settings, and execution context affect results; making dependencies explicit and controlled

### Module 3: Why interactivity accelerates AI discovery

- Presentation: interactive computation as a unified system; data, models, visualizations, and user input working together in a single system that updates automatically
- Hands-on exercise: building interactive computations where data, model outputs, and visualizations stay connected

### Module 4: How to use AI coding agents for AI/ML development

- Presentation: AI coding agents integrated directly into the development environment; when to trust AI assistance and where it adds value
- Hands-on exercise: generating, modifying, and extending code with AI agents while providing the right execution context

### Module 5: From interactive work to reusable systems

- Presentation: moving from private experimentation to work others can run, inspect, and build upon
- Hands-on exercise: turning interactive code into scripts, apps, artifacts, and reusable Python modules


