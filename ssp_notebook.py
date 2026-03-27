# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "numpy",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import marimo as mo

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Understanding Self-Play Red Teaming (SSP)
    ### An Interactive Simulation of the Paper "Be Your Own Red Teamer"

    Liu et al. (2025) · [arxiv:2601.10589](https://arxiv.org/abs/2601.10589)

    ---

    > **Note:** This notebook is a *conceptual simulation* designed to provide intuition for the Self-Play and Reflective Experience Replay (SSP) algorithm. It visualizes the core mechanics (zero-sum rewards, UCB sampling, reward dynamics) using synthetic data. It does **not** contain a real language model or a training loop.

    **What this notebook covers:**
    - The zero-sum reward structure coupling attacker and defender
    - The UCB-based experience replay logic for prioritizing hard cases
    - Simulated reward dynamics across training iterations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Background: Why Self-Play?

    Standard safety training teaches a model to refuse harmful requests — but it only trains on *known* attack patterns.
    Attackers can always craft new jailbreaks that bypass current defenses.

    **The core idea of SSP:** treat safety as an adversarial game between two roles.

    | Role | Input | Action |
    |------|-------|--------|
    | Attacker $\pi_\theta$ | Harmful goal $G$ | Generate jailbreak prompt $p_{\text{attack}}$ |
    | Defender $\pi_\theta$ | Jailbreak prompt $p_{\text{attack}}$ | Generate response $y$ |
    | Safety scorer | Response $y$ | Assign score $s \in \{1,2,3,4,5\}$ |

    Crucially, **attacker and defender share the same model weights** $\theta$.
    The model must simultaneously become harder to fool *and* better at refusing harmful prompts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zero-Sum Reward Structure

    Given safety score $s \in \{1, 2, 3, 4, 5\}$ where $s=1$ is most harmful and $s=5$ is safest:

    $$r_{\text{att}} = \frac{s - 1}{4} \qquad r_{\text{def}} = \frac{5 - s}{4}$$

    These rewards sum to exactly 1 for any score:

    $$r_{\text{att}} + r_{\text{def}} = \frac{s-1}{4} + \frac{5-s}{4} = 1$$

    So equivalently: $r_{\text{att}} = 1 - r_{\text{def}}$.

    When the attacker elicits a harmful response ($s$ low), it gets high reward and the defender gets low reward — and vice versa.
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    scores_axis = np.array([1, 2, 3, 4, 5])
    r_att_vals = (scores_axis - 1) / 4
    r_def_vals = (5 - scores_axis) / 4

    fig_rewards, ax_r = plt.subplots(figsize=(7, 3.5))
    ax_r.plot(scores_axis, r_att_vals, "o-", color="#e74c3c", label=r"$r_{\rm att} = (s-1)/4$", linewidth=2, markersize=8)
    ax_r.plot(scores_axis, r_def_vals, "s-", color="#2980b9", label=r"$r_{\rm def} = (5-s)/4$", linewidth=2, markersize=8)
    ax_r.axhline(0.5, linestyle="--", color="#888", alpha=0.6, label="Break-even (0.5)")
    ax_r.set_xlabel("Safety Score $s$")
    ax_r.set_ylabel("Reward")
    ax_r.set_xticks(scores_axis)
    ax_r.set_xticklabels(["1\n(harmful)", "2", "3", "4", "5\n(safe)"])
    ax_r.legend(loc="center right")
    ax_r.set_title("Zero-Sum Reward Coupling")
    ax_r.set_ylim(-0.05, 1.1)
    plt.tight_layout()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The SSP Training Loop

    The algorithm runs for $T$ iterations (paper uses $T=3$). Each iteration:

    1. **Sample** a batch of harmful goals $G$ from the dataset (5,000 goals from Jailbreak-R1)
    2. **Attack** — model generates a jailbreak prompt with chain-of-thought reasoning:
       ```
       <think> ... </think> <attack> {jailbreak prompt} </attack>
       ```
    3. **Defend** — same model responds to the jailbreak prompt
    4. **Score** — safety scorer assigns $s \in \{1..5\}$; compute $r_{\text{att}}$, $r_{\text{def}}$
    5. **Store** $(G,\, p_{\text{attack}},\, y,\, r_{\text{att}},\, r_{\text{def}})$ in experience pool $\mathcal{D}$
    6. **Sample** from $\mathcal{D}$ using UCB to prioritize hard cases (see below)
    7. **Update** $\theta$ via GRPO using sampled experiences

    The unified optimization objective:

    $$J_{\text{self-play}}(\theta) = \mathbb{E}_{\mathcal{D}}[r_{\text{att}}] + \mathbb{E}_{\mathcal{D}}[r_{\text{def}}]$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflective Experience Replay: UCB Sampling

    Naively replaying past experiences uniformly wastes compute on easy cases the model already handles.

    **UCB sampling** prioritizes goals that are:
    - **Hard** — the model gets low reward on them
    - **Underexplored** — sampled fewer times so far

    For goal $G_i$ with average reward $\bar{r}_i$ over $n_i$ samples, and $N = \sum_j n_j$ total:

    $$\text{UCB}(G_i) = \underbrace{(1 - \bar{r}_i)}_{\text{difficulty}} + \underbrace{c \sqrt{\frac{\ln N}{n_i}}}_{\text{exploration bonus}}$$

    The paper uses $c = \sqrt{2} \approx 1.41$. Goals are sampled proportional to their UCB score.

    **Adjust $c$ below** to see how exploration vs. exploitation trades off:
    """)
    return


@app.cell
def _(mo):
    c_slider = mo.ui.slider(start=0.0, stop=3.0, step=0.1, value=1.41, label="Exploration constant $c$")
    return (c_slider,)


@app.cell(hide_code=True)
def _(c_slider, mo):
    mo.hstack([c_slider], justify="start")
    return


@app.cell(hide_code=True)
def _(c_slider, np, plt):
    rng_ucb = np.random.default_rng(42)
    n_goals = 8
    goal_labels = [f"G{i+1}" for i in range(n_goals)]
    avg_rewards = rng_ucb.uniform(0.1, 0.9, n_goals)
    sample_counts = rng_ucb.integers(1, 20, n_goals)
    N_total = int(sample_counts.sum())
    c_val = c_slider.value

    difficulty = 1 - avg_rewards
    exploration = c_val * np.sqrt(np.log(N_total) / sample_counts)
    ucb_scores = difficulty + exploration
    probs = ucb_scores / ucb_scores.sum()

    x_pos = np.arange(n_goals)
    bar_w = 0.3

    fig_ucb, (ax_ucb, ax_prob) = plt.subplots(1, 2, figsize=(11, 4))

    ax_ucb.bar(x_pos - bar_w / 2, difficulty, bar_w, label="Difficulty $(1 - \\bar{r}_i)$", color="#e74c3c", alpha=0.85)
    ax_ucb.bar(x_pos + bar_w / 2, exploration, bar_w, label=f"Exploration $(c={c_val:.2f})$", color="#f39c12", alpha=0.85)
    for i, score in enumerate(ucb_scores):
        ax_ucb.text(i, max(difficulty[i], exploration[i]) + 0.04, f"{score:.2f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax_ucb.set_xticks(x_pos)
    ax_ucb.set_xticklabels(goal_labels)
    ax_ucb.set_ylabel("Score component")
    ax_ucb.set_title(f"UCB Score Components  (N={N_total})")
    ax_ucb.legend(fontsize=9)

    ax_prob.bar(x_pos, probs, color="#2980b9", alpha=0.85, edgecolor="white")
    ax_prob.set_xticks(x_pos)
    ax_prob.set_xticklabels(goal_labels)
    ax_prob.set_ylabel("Sampling probability")
    ax_prob.set_title("Resulting Sampling Distribution")

    plt.tight_layout()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simulated Self-Play: Reward Dynamics Over Iterations

    Let's simulate what happens to attacker and defender rewards across SSP iterations (no real LLM — synthetic scores).

    - **Early rounds**: attacker finds novel jailbreaks → defender reward drops temporarily
    - **Later rounds**: defender adapts → rewards stabilize, with defender ending stronger overall

    **Adjust the number of iterations:**
    """)
    return


@app.cell
def _(mo):
    iter_slider = mo.ui.slider(start=1, stop=10, step=1, value=3, label="Training iterations $T$")
    return (iter_slider,)


@app.cell(hide_code=True)
def _(iter_slider, mo):
    mo.hstack([iter_slider], justify="start")
    return


@app.cell(hide_code=True)
def _(iter_slider, np, plt):
    n_iter = iter_slider.value
    rng_sim = np.random.default_rng(0)
    batch_size = 20

    att_mean = []
    def_mean = []

    for t in range(n_iter):
        att_strength = min(0.75, 0.2 + t * 0.12)
        def_strength = min(0.90, 0.55 + t * 0.08)
        mu_score = np.clip(1 + 4 * (1 - att_strength) * def_strength, 1, 5)
        s_batch = np.clip(rng_sim.normal(mu_score, 0.7, batch_size), 1, 5)
        att_mean.append(((s_batch - 1) / 4).mean())
        def_mean.append(((5 - s_batch) / 4).mean())

    iters = np.arange(1, n_iter + 1)

    fig_sim, (ax_dyn, ax_hist) = plt.subplots(1, 2, figsize=(11, 4))

    ax_dyn.plot(iters, att_mean, "o-", color="#e74c3c", linewidth=2, markersize=7, label="Attacker $r_{\\rm att}$")
    ax_dyn.plot(iters, def_mean, "s-", color="#2980b9", linewidth=2, markersize=7, label="Defender $r_{\\rm def}$")
    ax_dyn.axhline(0.5, linestyle="--", color="#888", alpha=0.5)
    ax_dyn.set_xlabel("Iteration")
    ax_dyn.set_ylabel("Mean batch reward")
    ax_dyn.set_title("Reward Dynamics Across Iterations")
    ax_dyn.set_ylim(0, 1)
    ax_dyn.set_xticks(iters)
    ax_dyn.legend()

    att_strength_final = min(0.75, 0.2 + (n_iter - 1) * 0.12)
    def_strength_final = min(0.90, 0.55 + (n_iter - 1) * 0.08)
    mu_final = np.clip(1 + 4 * (1 - att_strength_final) * def_strength_final, 1, 5)
    s_final = np.clip(rng_sim.normal(mu_final, 0.7, 200), 1, 5)
    s_final_rounded = np.round(s_final).astype(int)

    ax_hist.hist(s_final_rounded, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], color="#2980b9", alpha=0.8, edgecolor="white")
    ax_hist.set_xlabel("Safety Score $s$")
    ax_hist.set_ylabel("Count")
    ax_hist.set_title(f"Score Distribution at Iteration {n_iter}")
    ax_hist.set_xticks([1, 2, 3, 4, 5])
    ax_hist.set_xticklabels(["1\nharmful", "2", "3", "4", "5\nsafe"])

    plt.tight_layout()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways

    - **Self-play eliminates the external attacker**: one model continuously finds its own blind spots
    - **Zero-sum coupling** prevents cheating: improving as attacker directly pressures the defender to adapt
    - **UCB replay** focuses compute on the hardest, least-explored goals rather than re-rehearsing easy wins
    - **Shared weights** mean every jailbreak found during training becomes a training signal to resist exactly that jailbreak

    The paper reports SSP reduces Attack Success Rate (ASR) by ~30–40% on Llama-3.1-8B-Instruct while leaving general capability (MT-Bench) unchanged.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notation Reference

    | Symbol | Description |
    |--------|-------------|
    | $G$ | Harmful goal (e.g., "explain how to synthesize X") |
    | $\pi_\theta$ | Shared LLM policy (both attacker and defender) |
    | $p_{\text{attack}}$ | Jailbreak prompt generated by attacker |
    | $y$ | Defender's response to the jailbreak |
    | $s$ | Safety score $\in \{1,2,3,4,5\}$ (1=harmful, 5=safe) |
    | $r_{\text{att}}$ | Attacker reward $= (s-1)/4$ |
    | $r_{\text{def}}$ | Defender reward $= (5-s)/4$ |
    | $\mathcal{D}$ | Experience pool (stores all past $(G, p, y, r)$ tuples) |
    | $n_i$ | Times goal $G_i$ has been sampled from $\mathcal{D}$ |
    | $\bar{r}_i$ | Average reward for goal $G_i$ |
    | $N$ | Total samples drawn: $\sum_i n_i$ |
    | $c$ | UCB exploration constant ($\sqrt{2}$ in the paper) |
    | $J_{\text{self-play}}(\theta)$ | Joint RL objective $= \mathbb{E}[r_{\text{att}}] + \mathbb{E}[r_{\text{def}}]$ |
    | $T$ | SSP training iterations (3 in the paper) |
    | ASR | Attack Success Rate — fraction of jailbreaks that elicit harmful responses |
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    This notebook, titled **"Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay,"** is an interactive demonstration of an AI safety technique. Here's a breakdown of what it contains:

    ### Core Concept: Self-Play and Zero-Sum Rewards

    The notebook introduces a method for making AI models safer by having them engage in "self-play." This involves two competing personas:

    *   An **Attacker**, which tries to find harmful or unsafe outputs.
    *   A **Defender**, which tries to make the model's outputs safe.

    The first plot, **"Zero-Sum Reward Coupling,"** illustrates the core mechanism. It shows that as the "Safety Score" of an output increases, the attacker's reward decreases while the defender's reward increases. This creates a zero-sum game that incentivizes the model to produce safer content over time.

    ### Mechanism: Reflective Experience Replay (UCB Sampling)

    The notebook then explains a specific technique called "Reflective Experience Replay," which uses **Upper Confidence Bound (UCB) sampling** to intelligently select which areas (or "goals") to focus on during training.

    The second plot, **"UCB Score Components,"** visualizes this process. It breaks down the UCB score into two parts:
    1.  **Difficulty**: How hard it is to achieve a specific goal.
    2.  **Exploration**: An incentive to explore less-tested goals, controlled by the interactive **"Exploration constant $c$"** slider.

    This plot shows how the UCB algorithm balances exploiting difficult goals and exploring new ones to create an efficient training strategy.

    ### Simulation: Reward Dynamics

    The main part of the notebook is a simulation that demonstrates how the self-play training works over multiple iterations. You can control the number of iterations with the **"Training iterations T"** slider.

    The final set of plots shows the results:
    *   **Reward Dynamics Across Iterations**: This line chart shows the average rewards for the attacker and defender over each training iteration, illustrating how their performance evolves.
    *   **Score Distribution**: This histogram shows the final distribution of safety scores after all training iterations are complete. This visualizes the overall safety of the model at the end of the simulation.

    In summary, this notebook provides an interactive and visual explanation of an advanced AI safety alignment technique, allowing you to see how competing internal models and intelligent sampling can lead to safer AI systems.
    """)
    return


if __name__ == "__main__":
    app.run()
