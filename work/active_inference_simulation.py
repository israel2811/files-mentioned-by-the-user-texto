#!/usr/bin/env python3
"""Active Inference Simulation for CCA Pareidolia Model (stdlib-only).

Implements the generative model from Scientific Evolution Loop Cycle 3
using only Python standard library (no numpy/matplotlib required).
Outputs CSV data with convergence trajectories.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent / "outputs" / "active_inference_simulation"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def simulate(
    pi_s: float,
    pi_p: float,
    mu_prior: float,
    T: float = 2.0,
    dt: float = 0.001,
    noise_amp: float = 0.02,
    seed: int = 42,
) -> list[tuple[float, float]]:
    random.seed(seed)
    steps = int(T / dt)
    mu = 0.5
    trajectory = []

    for i in range(steps):
        t = i * dt
        # CNG-like noise: periodic 300Hz component + random
        cng = 0.005 * math.sin(2 * math.pi * 300 * t)
        y = cng + noise_amp * random.gauss(0, 1)

        g_mu = mu
        eps_s = y - g_mu
        eps_p = mu - mu_prior
        # Free energy gradient: minimize both prediction errors
        # sensory term pulls mu toward sensory data
        # prior term pulls mu toward mu_prior
        d_mu = pi_s * eps_s - pi_p * eps_p
        mu = mu + dt * d_mu
        mu = max(0.0, min(1.0, mu))

        # Record every 10th step for output
        if i % 10 == 0:
            trajectory.append((t * 1000, mu))  # time in ms

    return trajectory


def main():
    print("Running Active Inference simulations (stdlib-only)...")

    regimes = [
        {"pi_s": 5.0, "pi_p": 1.0, "mu_prior": 0.5,
         "label": "Healthy_Control",
         "desc": "High sensory precision, low prior, neutral expectation"},
        {"pi_s": 0.5, "pi_p": 1.0, "mu_prior": 0.5,
         "label": "Hearing_Loss_Only",
         "desc": "Low sensory precision, low prior (neuropathy only)"},
        {"pi_s": 5.0, "pi_p": 15.0, "mu_prior": 1.0,
         "label": "Strong_Prior_Only",
         "desc": "High sensory precision, high prior (anxiety/trauma only)"},
        {"pi_s": 0.1, "pi_p": 15.0, "mu_prior": 1.0,
         "label": "CCA_Vulnerable",
         "desc": "Low sensory + high prior (DOUBLE FAILURE)"},
        {"pi_s": 0.1, "pi_p": 30.0, "mu_prior": 1.0,
         "label": "CCA_Severe",
         "desc": "Very low sensory + very high prior"},
    ]

    summary_lines = ["label,time_to_090_ms,final_belief,description"]

    for regime in regimes:
        label = regime["label"]
        desc = regime["desc"]
        traj = simulate(
            pi_s=regime["pi_s"],
            pi_p=regime["pi_p"],
            mu_prior=regime["mu_prior"],
        )

        # Save full trajectory
        traj_path = OUT_DIR / f"trajectory_{label}.csv"
        with traj_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time_ms", "belief_mu"])
            for t_ms, mu in traj:
                writer.writerow([f"{t_ms:.1f}", f"{mu:.6f}"])

        # Summary
        final_mu = traj[-1][1]
        t_090 = next((t for t, mu in traj if mu >= 0.9), -1.0)
        summary_lines.append(f"{label},{t_090:.1f},{final_mu:.4f},{desc}")

        if t_090 > 0:
            print(f"  {label}: final mu = {final_mu:.4f}, time to 0.9 = {t_090:.0f} ms")
        else:
            print(f"  {label}: final mu = {final_mu:.4f}, never reached 0.9")

    # Save summary
    summary_path = OUT_DIR / "simulation_summary.csv"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"\nSummary saved to: {summary_path}")
    print(f"Individual trajectories saved to: {OUT_DIR}")
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
