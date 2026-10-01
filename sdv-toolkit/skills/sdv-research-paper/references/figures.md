# Figures

Check the **rendered PDF**, not the source plot. Paper A's vector PDFs existed
but the build embedded PNGs.

## Checks (each one a FAIL)

1. **Vector embed.** Figures are embedded as PDF/SVG where a vector export
   exists. `pdfimages -list paper.pdf` lists raster embeds.
2. **No overprint.** In multi-panel figures, no label, tick or legend overlaps
   another panel. Use `constrained_layout=True` or explicit `wspace`.
3. **Size floor.** Nothing is under 7 pt at final printed size. A 10-pt label
   on a figure scaled to 66% prints at 6.6 pt.
4. **Color isn't the only cue.** Sign and series are also told apart by
   marker, line style or label. One color means one thing across the whole
   paper: never red = Ridge in one figure and red = the open model in another.
5. **The claim is visible.** Every sentence that cites a figure describes
   something a reader can see in it.
6. **The test is shown.** The paper's decisive comparison, usually the
   holdout, appears in a figure or table.
7. **Counts on calibration plots.** Reliability diagrams show the n per bin.
8. **Tables and figures agree.** The same quantity shows the same value in a
   table and a figure, with the same grouping.
9. **Captions stand alone.** A caption names the metric, sample, interval
   method and n. Alt text exists if the venue renders HTML.
10. **Nothing leaves the machine.** No draft figure, data or text is sent to an
    image or LLM generation service (several installed skills do this). Draw
    diagrams locally: matplotlib, Mermaid, TikZ, Graphviz.
