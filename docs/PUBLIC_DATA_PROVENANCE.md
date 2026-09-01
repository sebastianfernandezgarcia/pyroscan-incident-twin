# Public data provenance

PyroScan deliberately separates **public historical/geographic context** from its **synthetic exercise model**. The public layers make the La Palma surface authentic and auditable; they are never presented as a live incident feed, forecast, or simulator input.

## Bundled layers

### Copernicus EMSR671 · July 2023 wildfire

- **Visible use:** toggleable blue historical burn-scar reference on the shared map; compact provenance returned by `read_incident_board` and `inspect_zone`.
- **Official activation:** [Copernicus Emergency Management Service, EMSR671](https://mapping.emergency.copernicus.eu/activations/EMSR671/).
- **Product:** `EMSR671_AOI01_DEL_PRODUCT v2`, corrected delineation for Puntagorda.
- **Observation:** Pleiades image acquired 16 July 2023 at 11:46 UTC; geometry produced by photo-interpretation.
- **Geometry:** two observed burned-area features totaling **2,117.126 ha** in the source GeoJSON.
- **Source package:** [official vector ZIP](https://rapidmapping.emergency.copernicus.eu/backend/EMSR671/AOI01/DEL_PRODUCT/EMSR671_AOI01_DEL_PRODUCT_v2.zip).
- **Source SHA-256:** `60a1b6bc1222ff92a930ccd30455e0df9d4e4686af85be65e3d45d55d557dbab`.
- **GeoJSON SHA-256:** `76a2e174e6f4f70dedb3f61375faae4636b307dc85bb3750da3c11a62ce40f14`.
- **Attribution:** Copernicus Emergency Management Service (© 2023 European Union), EMSR671.

The browser asset is a deterministic SVG projection of the source polygons into the same geographic bounds as the La Palma coastline. It is simplified only for display and remains labeled **historical reference**.

### SITCAN / GRAFCAN · La Palma terrain

- **Visible use:** hillshade inside the La Palma coastline; compact provenance returned by `read_incident_board` and `inspect_zone`.
- **Official dataset:** [Modelo Digital de Terreno 25 × 25 m — La Palma](https://opendata.sitcan.es/dataset/modelo-digital-de-terreno-mdt-de-25x25-metros/resource/90d97840-9bc9-4e31-a470-3cb631806fd5).
- **Resolution:** 25 metres.
- **Dataset update shown by the catalogue:** 4 February 2021.
- **Source SHA-256:** `331915203d2d120c4a9cc83a64fad4a736b3f9636c79a582e4420a2b49437350`.
- **Derived hillshade SHA-256:** `a4c30c772944ce61f610d9bdee92349f2f093aac8e9c2d70bfcc3229d40cf940`.
- **Attribution:** GRAFCAN / Gobierno de Canarias. Reused under the catalogue's attribution terms; no endorsement is implied.

The committed PNG is a locally derived north-west illuminated hillshade. Elevation values are not sent to the agent and do not influence spread or response scoring.

### OpenStreetMap · island boundary

- **Visible use:** locally embedded La Palma coastline.
- **Source:** OpenStreetMap relation `11775386`.
- **Attribution:** [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL.

## Rebuild

The transformation is reproducible and outside the app build:

```bash
python3 scripts/derive_public_reference.py
```

The script downloads the exact official products, verifies their deterministic hashes in generated metadata, rebuilds `src/domain/publicReference.ts`, and writes `src/assets/la-palma-hillshade.png`. Python, Pillow and NumPy are required only for this optional provenance rebuild—not to install, test or run the web app.

## Safety boundary

| Layer | Status | Drives simulation? |
| --- | --- | --- |
| La Palma coastline | Public geography | No |
| SITCAN terrain hillshade | Public geography | No |
| EMSR671 burn scar | Public historical observation | No |
| Ignition, wind, attention contours, risk score | Synthetic exercise fixture | Yes, within the deterministic rehearsal only |
| Response rankings and staged actions | Synthetic exercise output | Yes, within the rehearsal only |

The app has no live incident, weather, sensor, dispatch, alerting, or emergency-decision integration.
