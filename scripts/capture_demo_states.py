"""Capture deterministic PyroScan frames by exercising the real WebMCP handlers.

The init script provides the browser's tiny registration surface only; every
tool definition and execute callback comes from the production application.
This makes reproducible submission media possible outside the ChatGPT browser.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from playwright.async_api import async_playwright
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "videos" / "pyroscan-challenge-film" / "product-states"
CHROME = Path.home() / "Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
URL = os.environ.get("PYROSCAN_CAPTURE_URL", "http://127.0.0.1:4174/")
CAPTURE_SCALE = int(os.environ.get("PYROSCAN_CAPTURE_SCALE", "2"))

if CAPTURE_SCALE not in {1, 2, 3}:
    raise SystemExit("PYROSCAN_CAPTURE_SCALE must be 1, 2, or 3")

POLYFILL = """
window.__pyroTools = {};
Object.defineProperty(document, 'modelContext', {
  configurable: true,
  value: {
    registerTool: async (tool) => {
      window.__pyroTools[tool.name] = tool;
    },
  },
});
"""


async def invoke(page, name: str, arguments: dict) -> dict:
    return await page.evaluate(
        """async ({name, arguments}) => {
          const tool = window.__pyroTools[name];
          if (!tool) throw new Error(`Tool not registered: ${name}`);
          return await tool.execute(arguments, {signal: new AbortController().signal});
        }""",
        {"name": name, "arguments": arguments},
    )


async def shot(page, filename: str) -> None:
    await page.screenshot(path=OUTPUT / filename, animations="disabled")


def build_contact_sheet() -> None:
    files = sorted(OUTPUT.glob("0*.png"))
    sheet = Image.new("RGB", (1200, 1290), "#090b0a")
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        image.thumbnail((600, 400), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (600, 430), "#0b0e0c")
        tile.paste(image, ((600 - image.width) // 2, 0))
        ImageDraw.Draw(tile).text((14, 405), path.name, fill="#d7f85d")
        sheet.paste(tile, ((index % 2) * 600, (index // 2) * 430))
    sheet.save(OUTPUT / "contact-sheet.jpg", quality=90, optimize=True)


async def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    transcript: list[dict] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=str(CHROME),
            headless=True,
            args=["--font-render-hinting=none"],
        )
        # Keep the CSS viewport identical to the judged product state while
        # capturing extra physical pixels for legible video crops and 4K delivery.
        page = await browser.new_page(
            viewport={"width": 1800, "height": 1200},
            device_scale_factor=CAPTURE_SCALE,
        )
        await page.add_init_script(POLYFILL)
        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_function("Object.keys(window.__pyroTools || {}).length === 6")

        await page.get_by_role("button", name="How it works").click()
        await shot(page, "01-how-it-works.png")
        await page.get_by_role("button", name="Close how it works").click()

        result = await invoke(page, "inspect_zone", {"zoneId": "el-paso"})
        transcript.append({"tool": "inspect_zone", "input": {"zoneId": "el-paso"}, "result": result})
        await shot(page, "02-inspect-zone.png")

        annotation_input = {
            "type": "blocked-road",
            "zoneId": "el-paso",
            "note": "LP-3 checkpoint closed in this exercise; validate the western access route before staging.",
        }
        result = await invoke(page, "add_board_annotation", annotation_input)
        transcript.append({"tool": "add_board_annotation", "input": annotation_input, "result": result})
        await shot(page, "03-human-context.png")

        simulation_input = {"horizonMinutes": 60, "windPreset": "northeast-shift"}
        result = await invoke(page, "simulate_spread", simulation_input)
        transcript.append({"tool": "simulate_spread", "input": simulation_input, "result": result})
        await shot(page, "04-simulate-spread.png")

        comparison_input = {"optionIds": ["ridge-hold", "dual-protection"]}
        result = await invoke(page, "compare_response_options", comparison_input)
        transcript.append({"tool": "compare_response_options", "input": comparison_input, "result": result})
        await shot(page, "05-compare-options.png")

        board = await invoke(page, "read_incident_board", {})
        transcript.append({"tool": "read_incident_board", "input": {}, "result": board})
        stage_input = {
            "boardVersion": board["exercise"]["boardVersion"],
            "scenarioId": board["activeScenario"]["id"],
            "optionId": "dual-protection",
            "rationale": "Broad reversible coverage while the exercise director validates the recorded LP-3 access constraint.",
        }
        result = await invoke(page, "stage_response_plan", stage_input)
        transcript.append({"tool": "stage_response_plan", "input": stage_input, "result": result})
        await shot(page, "06-staged-plan.png")

        (OUTPUT / "tool-transcript.json").write_text(json.dumps(transcript, indent=2), encoding="utf-8")
        await browser.close()
    build_contact_sheet()


if __name__ == "__main__":
    asyncio.run(main())
