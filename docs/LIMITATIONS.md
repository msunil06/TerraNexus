# TerraNexus Limitations & Scope Documentation

In adherence to truthfulness and software integrity standards, this document outlines known current limitations, technical boundaries, and planned future expansions.

---

## 1. Cartographic Scope

1. **Simplified Vector Polygons**: At the initial release, boundary geometries for world countries are loaded in simplified GeoJSON format (`static/data/world_countries.json`) to guarantee 60fps rendering across mobile smartphones and low-bandwidth connections. Highly detailed sub-meter boundary vectors are loaded progressively on detailed zoom levels.
2. **Marine Polygons**: While points, sounding depths, and littoral countries for oceans and seas are fully cataloged and searchable, arbitrary oceanic polygonal outlines are avoided because open ocean boundaries lack physical surface walls and follow dynamic international agreements (IHO S-23 limits).

---

## 2. Sub-National Administrative Divisions

1. **Hierarchy Depth**: Administrative hierarchies differ vastly across countries:
   - India: States / Union Territories & Districts are actively modeled.
   - United States: States are actively modeled.
   - Japan: Prefectures are actively modeled.
   - Germany: Bundesländer are actively modeled.
   Smaller nations or territories whose statistical bureaus publish limited open shapefiles display top-level divisions only.

---

## 3. Dynamic Live Currency Rates

- Currency codes, names, and symbols are statically cataloged per ISO 4217. Real-time forex trading quotes require an optional external exchange rate provider API key.
