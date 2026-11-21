# Charts for the Agentic Engineering Worklog presentation.
# Every number is copied from a saved notebook run (lesson 4, Step 7: "Text the model read on each turn").
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe

GREEN = "#2E6A4C"; INK = "#1F1B18"; MUTED = "#5F5852"; GRID = "#E6DED6"; LIGHT = "#FAF8F5"; DARK = "#1F1B18"; GLOW = "#6FBF94"
plt.rcParams.update({"font.family": "Inter", "font.size": 15})

tokens = [573, 652, 741, 772, 931]   # lesson 4, saved output
turns = ["Log an hour\non Herd Planner", "Actually, make\nthat two hours", "What project\nwas that for?", "How many hours\ntoday?", "What's the capital\nof Colorado?"]

# --- Token growth chart: 1000 x 540 on the slide, drawn at 2x ---
fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
fig.patch.set_facecolor(LIGHT); ax.set_facecolor(LIGHT)
x = range(1, 6)
ax.plot(x, tokens, color=GREEN, lw=3.2, solid_capstyle="round", zorder=3)
ax.scatter(x, tokens, s=70, color=GREEN, edgecolor=LIGHT, linewidth=2.2, zorder=4)
for i, t in enumerate(tokens):
    bold = i in (0, 4)
    ax.annotate(f"{t}", (i + 1, t), xytext=(0, 14), textcoords="offset points", ha="center",
                fontsize=17 if bold else 14, fontweight="bold" if bold else "normal", color=INK if bold else MUTED)
ax.set_xticks(list(x)); ax.set_xticklabels([f"Turn {i}\n{t}" for i, t in zip(x, turns)], fontsize=12.5, color=MUTED, linespacing=1.3)
ax.set_ylim(0, 1050); ax.set_xlim(0.6, 5.4)
ax.set_yticks([0, 250, 500, 750, 1000]); ax.tick_params(axis="y", colors=MUTED, labelsize=13, length=0)
ax.tick_params(axis="x", length=0, pad=10)
ax.grid(axis="y", color=GRID, lw=1); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED)
ax.set_ylabel("Tokens the model read", color=MUTED, fontsize=13)
fig.tight_layout()
fig.savefig("tokens.png", facecolor=LIGHT)

# --- Cover backdrop: the same five turns as a glowing line, 3840 x 2160 ---
fig = plt.figure(figsize=(19.2, 10.8), dpi=200)
fig.patch.set_facecolor(DARK)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_facecolor(DARK); ax.axis("off")
xs = [0.30, 0.47, 0.64, 0.80, 0.97]
ys = [0.18 + (t - 573) / (931 - 573) * 0.42 for t in tokens]
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
for w, a in [(28, 0.05), (18, 0.08), (10, 0.15)]:
    ax.plot(xs, ys, color=GLOW, lw=w, alpha=a, solid_capstyle="round", solid_joinstyle="round")
ax.plot(xs, ys, color=GLOW, lw=4, alpha=0.55, solid_capstyle="round", solid_joinstyle="round")
for r, a in [(1400, 0.06), (700, 0.12)]:
    ax.scatter(xs, ys, s=r, color=GLOW, alpha=a, linewidths=0)
ax.scatter(xs, ys, s=160, color=GLOW, alpha=0.65, linewidths=0)
fig.savefig("cover_backdrop.png", facecolor=DARK)
print("ok")
