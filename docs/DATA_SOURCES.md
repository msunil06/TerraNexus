# TerraNexus Data Sources & Licensing Documentation

TerraNexus is committed to factual veracity, provenance tracking, and open-source licensing compliance. We integrate datasets from official intergovernmental bodies and public-domain cartographic repositories.

---

## 1. Primary Sources & Licenses

| Source | Organization | Primary Use | License |
| :--- | :--- | :--- | :--- |
| **Natural Earth** | NACIS / Free Software Foundation | Vector boundaries, coastlines, centroids | **Public Domain (CC0)** |
| **GeoNames** | GeoNames Foundation | Placenames, alternate spellings, coordinates | **Creative Commons Attribution 4.0 (CC BY 4.0)** |
| **World Bank Open Data** | The World Bank Group | GDP, population, urban percentage | **Creative Commons Attribution 4.0 (CC BY 4.0)** |
| **Limits of Oceans and Seas (S-23)** | International Hydrographic Organization (IHO) | Marine divisions, named seas, straits | **Official Standard / Open Data** |
| **GEBCO** | IHO & IOC UNESCO | Bathymetric soundings and ocean trench depths | **Open Scientific Data** |
| **UN Statistics Division** | United Nations | Standard country and currency codes (M49) | **Open Public Data** |

---

## 2. Integrity and Non-Fabrication Rules

1. **No Extrapolated Fictions**: If an elevation or coastline statistic is unmeasured or ambiguous, TerraNexus records `None` / `N/A` rather than fabricating values or defaulting to zero.
2. **Provenance Stamps**: Every changing socio-economic statistic records its reference year (e.g., World Bank 2024).
3. **Disputed Boundaries**: Borders shown on interactive map tiles represent de facto cartographic lines for educational visualization and do not constitute political recognition of sovereignty.
