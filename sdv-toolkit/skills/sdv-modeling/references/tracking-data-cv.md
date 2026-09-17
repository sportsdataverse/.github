# Tracking data and computer vision for sports models

> Reference file of the `sdv-modeling` skill. Covers **player/ball tracking
> data** — whether delivered by a vendor (SkillCorner, Second Spectrum, NGS,
> Hawk-Eye) or produced from video — and the computer-vision pipeline that
> produces it. Not to be confused with `tracking.md`, which is *experiment*
> tracking (fingerprints, lineage, the ledger).

Tracking data fails in a different way from play-by-play. Play-by-play is wrong
in *values*; tracking data is wrong in **frames of reference** — which way the
court faces, which end a team attacks, which frame an event id points at, where
the letterbox padding went. Every one of those produces a clean, plausible,
completely wrong feature, and none of them raises.

Every entry: **the trap · why it never errors · the detection test · a real
citation** where this ecosystem has one.

**Contents**

1. The pipeline and where each stage fails
2. Frames of reference — normalize direction before anything else
3. Time — events, frames, and ids that point the wrong way
4. Detection → pixel coordinates: the letterbox inverse
5. Pixels → court: homography and its error budget
6. Tracks: continuity, id switches, and frame sampling
7. Kinematics: velocity and acceleration from noisy positions
8. Features that carry signal
9. Validation and augmentation on tracking data
10. Libraries, licences, and which installed skill to reach for

---

## 1. The pipeline and where each stage fails

```
video ─► detect ─► track ─► project (homography) ─► normalize ─► features ─► model
          §4        §6          §5                     §2           §7-8         §9
```

Vendor tracking data enters at *normalize*: someone else ran the first three
stages, which means their errors are baked in and undocumented. **Validate a
vendor's frame of reference exactly as you would your own** (§2) — the most
important geometric fact in the hoopsq data was documented nowhere.

The downstream model metric is the gate. Detection mAP and tracking HOTA are
diagnostics for the upstream stages; a pipeline can improve both and still
degrade the model if it shifts the coordinate frame.

---

## 2. Frames of reference — normalize direction before anything else

**Trap.** Coordinates are in a fixed arena frame, but teams switch ends. A
"distance to goal" or "shot from the left" feature computed in the arena frame
means opposite things in alternating periods.

**Why invisible.** The feature is continuous, finite, and correlated with the
target *on average* — just much more weakly than it should be.

**Real citations.**
- **NHL xG.** `x_fixed` is not direction-normalized; its sign splits about 50/50,
  so raw `x_shot` scores **exactly 0.5000 AUC alone**. `89 − |x|` (distance from
  the goal line) is the usable form. The same reason makes raw `sign(y)` useless
  for handedness: a team's left wing flips ends, so the working feature is the
  direction-normalized side `sign(y) · sign(x)`.
- **hoopsq (SkillCorner ACB).** Raw tracking is in **broadcast orientation**, but
  event `location`s are **normalized** (offense toward negative x). Mixing the two
  silently mirrors half the possessions. The flip is keyed on
  `possessions.leftHoop` (`needs_flip = not left_hoop`) and was validated
  **135/135** against geometry. The hoop sits at **(−40.75, 0) ft** — FIBA-exact,
  and documented nowhere in the vendor docs.

**Detection test — a normalization must put attacks at the attacking end.** After
normalizing, nearly every shot should be closer to the target it attacks than to
the other one. A mirrored period drags that fraction toward 0.5.

```python
import numpy as np

def assert_direction_normalized(shot_x, shot_y, target=(-40.75, 0.0),
                                other=(40.75, 0.0), min_frac=0.95):
    """All shots should be nearer the attacked target after normalization.

    Defaults are hoopsq's FIBA court in feet; pass the real target for the sport.
    A result near 0.5 means half the possessions are mirrored.
    """
    x, y = np.asarray(shot_x, float), np.asarray(shot_y, float)
    d_t = np.hypot(x - target[0], y - target[1])
    d_o = np.hypot(x - other[0], y - other[1])
    frac = float((d_t < d_o).mean())
    assert frac >= min_frac, (
        f"only {frac:.1%} of shots are nearer the attacked target: direction is "
        "not normalized (expect ~50% if half the periods are mirrored)"
    )
    return frac
```

**The solo-AUC tell.** A positional feature that scores ~0.50 alone, when it
obviously should matter, is the signature of an un-normalized frame. Run
`competition.md` §1b over the raw coordinate columns and look for exactly that.

---

## 3. Time — events, frames, and ids that point the wrong way

**Trap 1 — event ids that link backwards.** An id joining an event table to the
tracking stream refers to the *previous* or *interrupted* event, so a "pre-event"
feature is built from what happened after.

**Real citation.** hoopsq: `timeouts.chanceId` names the chance the timeout
*interrupted* — 56 of 65 timeout frames fall after that chance ends, none before
it starts. An `after_timeout` flag built on it tagged 55 shots, 51 of them made,
and produced a **−0.012 log-loss improvement that was pure outcome leakage**. The
guard is `competition.md` §1d (`assert_sources_precede_event`); run it on every
feature that joins across tables.

**Trap 2 — post-outcome categories in a pre-event field.** A label that looks
descriptive is partly determined by the outcome.

**Real citation.** hoopsq: `contestLevel` includes **`blocked`**, which can only be
known after the shot — recoded to the strongest pre-shot level (`plus`). And
contest level is **not monotone in defender distance** (pooled medians: plus
2.77 ft < light 4.13 < average 4.48 < open 5.98), so it is not a proxy you can
replace with distance alone.

**Trap 3 — windows that can never fire.** Video-frame gaps around stoppages are
long. hoopsq's gaps around a timeout are **≥ 80 s**, so a "within 20 s of a
timeout" feature is all-False. Assert a non-zero True-count on real data
(`competition.md` §1c).

**Rule.** Build every feature with an explicit `as_of_frame` and assert
`consumed_frame < event_start_frame`. For windowed features, assert the window is
satisfiable on real data before trusting its importance.

---

## 4. Detection → pixel coordinates: the letterbox inverse

**Trap.** A detector is run on a resized-and-padded (letterboxed) frame, then
boxes are mapped back by dividing by the scale — **without removing the padding
offset**. Every coordinate is shifted by `pad / scale` along the padded axis.

**Why invisible.** Every box is shifted by the same amount along the padded axis,
so the *pattern* of detections still looks right — and a constant shift becomes a
constant court-position bias after homography. The shift is not small: on
1920×1080 video letterboxed to 640, it is **420 px** vertically (`pad_h / scale`
= 140 / 0.333), measured. A widely installed CV skill ships exactly this bug
(surveyed 2026-09-16). It only looks right on square input, where the padding is
zero.

**Correct inverse.** Subtract the pad, *then* divide by the scale.

```python
def letterbox_params(h, w, target=640):
    scale = target / max(h, w)
    new_w, new_h = int(round(w * scale)), int(round(h * scale))
    return scale, (target - new_w) // 2, (target - new_h) // 2

def boxes_to_original(boxes_xyxy, scale, pad_w, pad_h):
    """boxes in letterboxed coordinates -> original frame coordinates."""
    b = np.asarray(boxes_xyxy, float).copy()
    b[:, [0, 2]] = (b[:, [0, 2]] - pad_w) / scale
    b[:, [1, 3]] = (b[:, [1, 3]] - pad_h) / scale
    return b
```

**Detection test — the round trip must be exact.**

```python
def assert_letterbox_round_trip(h, w, target=640, tol=1.0):
    scale, pad_w, pad_h = letterbox_params(h, w, target)
    orig = np.array([[0.0, 0.0, w, h], [w * 0.25, h * 0.5, w * 0.75, h * 0.9]])
    boxed = orig.copy()
    boxed[:, [0, 2]] = boxed[:, [0, 2]] * scale + pad_w
    boxed[:, [1, 3]] = boxed[:, [1, 3]] * scale + pad_h
    back = boxes_to_original(boxed, scale, pad_w, pad_h)
    err = float(np.abs(back - orig).max())
    assert err <= tol, f"letterbox inverse is off by {err:.1f}px on a {w}x{h} frame"
    return err
```

Most current detector APIs letterbox internally and already return boxes in
original coordinates. **Only apply an inverse if you letterboxed yourself** —
doing it twice is the same bug in the other direction. Confirm by drawing one
frame's boxes.

---

## 5. Pixels → court: homography and its error budget

A planar homography maps image points on the playing surface to court
coordinates from ≥ 4 known landmarks (line intersections, key corners, pitch
keypoints). `roboflow/sports`' `ViewTransformer` is the reference implementation:
`cv2.findHomography(source, target)` then `cv2.perspectiveTransform`.

**Traps.**
- **Only the ground plane is valid.** A homography maps the *floor*. Project each
  player's **foot point** (bottom-centre of the box), never the box centre — the
  torso projects metres away. A ball in the air cannot be projected at all without
  height.
- **Broadcast cameras pan and zoom**, so one homography per game is wrong. Refit
  per frame (or per shot) from detected keypoints.
- **Few or collinear landmarks** produce a numerically valid, geometrically absurd
  matrix.

**Detection test — reprojection error on held-out landmarks.** Fit on some
landmarks, measure error on the rest, in real-world units.

```python
import cv2

def homography_reprojection_error(img_pts, court_pts, holdout=2):
    """Fit on all but `holdout` landmarks; report error on the held-out ones.

    Units are the court units (feet/metres). Rejects a fit whose held-out error
    is not small relative to the feature it will feed.
    """
    img, court = np.asarray(img_pts, np.float32), np.asarray(court_pts, np.float32)
    assert len(img) >= 4 + holdout, "need >= 4 fit landmarks plus held-out ones"
    H, _ = cv2.findHomography(img[:-holdout], court[:-holdout])
    assert H is not None, "homography failed: landmarks degenerate or collinear"
    proj = cv2.perspectiveTransform(img[-holdout:].reshape(-1, 1, 2), H).reshape(-1, 2)
    return float(np.linalg.norm(proj - court[-holdout:], axis=1).max())
```

A held-out error of 1–2 ft is invisible for "which zone" features and
disqualifying for "closest defender distance" features. **Pick the tolerance from
the feature, not from the geometry.**

---

## 6. Tracks: continuity, id switches, and frame sampling

**Trap 1 — frame skipping on fast motion.** Generic video-pipeline advice is to
process every Nth frame because adjacent frames are redundant. That is right for
slow scenes and **wrong for sports**: a player can cross the association radius
between sampled frames, the tracker swaps identities, and velocity is computed
across a gap it does not know about.

**Trap 2 — id switches.** Two players crossing trade track ids. Aggregates per
"player" silently mix two people.

**Trap 3 — entity aliases.** The same person under two ids. hoopsq found **9
players carrying two ids**; features and CV groups must use a canonical id.

**Detection tests.**

```python
def assert_consistent_sampling(frame_times, expected_dt, max_gap_frac=0.02,
                               gap_factor=1.5):
    """frame_times: timestamps (s) for ONE track, sorted. Flags dropped frames."""
    dt = np.diff(np.asarray(frame_times, float))
    gaps = dt > expected_dt * gap_factor
    assert gaps.mean() <= max_gap_frac, (
        f"{gaps.mean():.1%} of steps exceed {gap_factor}x the frame interval: "
        "compute kinematics from timestamps and break tracks at gaps"
    )

def id_switch_candidates(track_xy, track_t, max_speed):
    """Indices where implied speed exceeds what a player can do -> likely swap."""
    xy, t = np.asarray(track_xy, float), np.asarray(track_t, float)
    speed = np.linalg.norm(np.diff(xy, axis=0), axis=1) / np.diff(t)
    return np.flatnonzero(speed > max_speed) + 1
```

Physical ceilings make good tolerances: elite sprinters top out around 12–13 m/s,
so an implied speed well above that between two frames is a swap or a projection
glitch, not a player.

**Tracking metrics.** Report **HOTA** (balances detection and association),
**IDF1** (identity preservation — the one that matters for per-player features)
and **MOTA** (detection-dominated; it can look good while identities are
scrambled). Prefer IDF1 when the model aggregates by player.

---

## 7. Kinematics: velocity and acceleration from noisy positions

**Trap.** Finite differences on raw positions amplify noise: velocity is noisy,
acceleration is mostly noise.

**Rules.**
- Differentiate against **timestamps**, not frame indices, so a dropped frame does
  not read as a burst of speed (§6).
- Smooth before differentiating — a Savitzky–Golay filter
  (`scipy.signal.savgol_filter`, with `deriv=1` for velocity) estimates the
  derivative from a local polynomial fit instead of differencing noise. Choose the
  window from the physics (a few tenths of a second), not by tuning on the target.
- **Break tracks at gaps** before smoothing; a filter window spanning a gap blends
  two unrelated segments.
- Vendor tracking often carries a per-point uncertainty (SkillCorner's
  `predError`). Use it to **weight or mask**, not to jitter: hoopsq found jitter at
  the `predError` scale **hurt** log loss by +0.006 (§9).

```python
from scipy.signal import savgol_filter

def velocity_from_positions(xy, t, window_s=0.4):
    """Smoothed velocity (units/s) for one gap-free, uniformly sampled segment."""
    xy, t = np.asarray(xy, float), np.asarray(t, float)
    dt = float(np.median(np.diff(t)))
    w = max(5, int(round(window_s / dt)) | 1)          # odd, >= 5
    w = min(w, len(xy) - (1 - len(xy) % 2))            # fit inside the segment
    return savgol_filter(xy, w, polyorder=2, deriv=1, delta=dt, axis=0)
```

---

## 8. Features that carry signal

Tracking data invites hundreds of geometric features that re-express the same
thing. The lesson from both NHL and hoopsq is the same: **reparameterizations of
geometry the model already has do not help; new information does.**

- **Reparameterization is a no-op for trees.** NHL `dx_goal = 89 − |x|`,
  `|y|`, and `behind_net` scored 0.7762 against 0.7769 — `shot_distance ==
  hypot(89 − |x|, |y|)` to 0.023 ft on 100% of rows, so the trees had already
  found those boundaries.
- **Information the event feed lacks is what moves the score.** Handedness
  (+0.0021, 16/16 seasons) on NHL; on basketball tracking, the analogous candidates
  are pre-shot state that event data cannot carry — closest-defender distance and
  closing speed at release, help-defender positions, passer location, the shooter's
  own velocity and direction into the shot, and time since the catch.
- **Defender features need a frame.** "Closest defender" at the *release* frame,
  not the event's logged frame, which may be seconds later.
- **Spatial encodings.** Zone one-hots, distance/angle to target, and a smoothed
  2-D spatial prior (a kernel density of league outcomes by location) are strong
  low-variance baselines before per-player spatial models.

Run every new feature through `competition.md` §1 before trusting its importance.

---

## 9. Validation and augmentation on tracking data

- **Group by game, at least.** Frames within a possession are nearly identical;
  possessions within a game share lineups and fatigue. hoopsq validated
  **leave-one-game-out** over 10 games.
- **Small game counts make per-game spread large.** Report per-game wins and a
  sign test (`competition.md` §11), not only the mean.
- **Reflection is the natural label-preserving augmentation.** A court mirrored
  across its long axis is the same play. In hoopsq it was the **only**
  augmentation that helped — **−0.003 log loss, 9 of 10 games** — while
  `predError`-scale jitter hurt (+0.006). Reflect in-fold only, and swap the
  left/right vocabulary (`left_corner` ↔ `right_corner`) along with the coordinate.
- **Reflection breaks for asymmetric facts.** Handedness is not symmetric under
  reflection: mirror the shooter's side and the off-wing relationship flips unless
  handedness flips with it. Decide explicitly, per feature, what a mirror means.

---

## 10. Libraries, licences, and which installed skill to reach for

**Licence first.** SportsDataverse packages are MIT. A copyleft dependency changes
what an open-source entry or package can ship — check before wiring one in.

| Library | Role | Licence (verified 2026-09-16) |
|---|---|---|
| `roboflow/supervision` | detections, annotators, zones, keypoints | MIT |
| `roboflow/trackers` | ByteTrack/SORT-family tracker re-implementations (split out of supervision) | Apache-2.0 |
| `roboflow/sports` | sports CV reference: pitch keypoints, `ViewTransformer` homography | MIT |
| OpenCV (`cv2.findHomography`, `perspectiveTransform`) | homography | Apache-2.0 |
| `ultralytics` | YOLO detection / pose / segmentation (YOLO11 → YOLO27) | **AGPL-3.0** |
| `boxmot` | pluggable multi-object trackers | **AGPL-3.0** |
| `scipy.signal.savgol_filter` | smoothed derivatives | BSD-3 |

The two AGPL libraries are excellent and widely used; the point is to choose them
knowingly, not to find out at release time.

**Installed skills — scope and caveats.**

| Skill | Use it for | Caveat |
|---|---|---|
| `computer-vision-pipeline` | detection → tracking pipeline structure, NMS tuning, batching | calls YOLOv8 current (it is not); frame-skipping advice is wrong for sports (§6); its letterbox inverse omits the padding offset (§4) |
| `roboflow-inference` | choosing Roboflow deployment (serverless, dedicated, self-hosted, batch) and Workflow execution | deployment operations, not modeling |
| `engineering-skills:senior-computer-vision` | architectures, training, ONNX/TensorRT export | general-purpose; no sports frame-of-reference guidance |

---

## Provenance

The frame-of-reference, timing, feature and augmentation findings are this
ecosystem's own: the hoopsq SkillCorner shot-quality entry (2026-09-14/15) and the
NHL xG leave-one-season-out search (2026-09-03). The surveyed public CV skills —
`curiositech/some_claude_skills@computer-vision-pipeline` (MIT) and
`roboflow/computer-vision-skills@roboflow-inference` (Apache-2.0) — informed the
pipeline outline in §1; no text was copied, and §4 and §6 correct defects found in
the surveyed version. Library roles and licences were read from each repository on
2026-09-16.
