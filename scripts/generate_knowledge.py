"""Generate engineering knowledge documents for EcoInfraMind AI.

Covers Nigerian and African infrastructure standards, civil engineering,
highway engineering, structural engineering, geotechnical engineering,
water resources, materials science, climate adaptation, and more.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.settings import settings

KB = settings.knowledge_dir
KB.mkdir(parents=True, exist_ok=True)

DOCUMENTS = {}

# ── 1. Nigerian Highway Manual ─────────────────────────────────────
DOCUMENTS["01_nigerian_highway_manual.md"] = """# Nigerian Highway Manual - Design Standards

## Design Speed Standards
- Rural highways (flat terrain): 100 km/h
- Rural highways (rolling terrain): 80 km/h
- Rural highways (mountainous terrain): 60 km/h
- Urban highways: 60-80 km/h
- Local roads: 30-50 km/h

## Pavement Design Parameters
- Design life: 20 years for flexible pavements
- Design life: 30-40 years for rigid pavements
- CBR design using 90th percentile of soaked CBR values
- Minimum base thickness: 150mm (light traffic), 200mm (medium), 250mm (heavy)
- Asphalt concrete surface: 40-50mm wearing course, 50-100mm binder course
- Subbase minimum thickness: 150mm (all traffic classes)

## Traffic Classification (ESA ranges)
- Light: < 0.5 million ESA
- Medium: 0.5 - 5 million ESA
- Heavy: 5 - 30 million ESA
- Very Heavy: > 30 million ESA

## Drainage Requirements
- Minimum longitudinal gradient: 0.5%
- Maximum longitudinal gradient: 8% for rural highways
- Side drain minimum depth: 450mm
- Culvert minimum diameter: 900mm for main roads
- Design return period: 50 years for culverts, 100 years for bridges
- Freeboard minimum: 0.5m above design flood level

## Geometric Standards
- Lane width: 3.5m for rural highways, 3.0m for urban
- Shoulder width: 2.5m paved, 3.0m unpaved
- Median width: 5.0m minimum for divided highways
- Minimum horizontal curve radius: based on design speed per AASHTO
- Superelevation: maximum 8%
- Stopping sight distance: based on design speed per AASHTO
- Overtaking sight distance: 2x stopping sight distance
- Vertical clearance: 5.0m minimum over roads, 5.5m over highways

## Materials Specifications
- Subgrade CBR: minimum 5% for highway construction
- Selected fill: CBR > 10%
- Subbase: CBR > 30%
- Base course: CBR > 80% (light traffic), 100% CBR (heavy traffic)
- Asphalt penetration grade: 60/70 for hot climate regions
- Asphalt softening point: minimum 48°C for tropical regions
- Concrete compressive strength: minimum 25 MPa for rigid pavements

## Road Classification
- Trunk A roads: Federal highways connecting states
- Trunk B roads: State highways connecting local governments
- Trunk C roads: Local government roads
- Urban roads: Streets within municipalities
"""

# ── 2. FERMA Guidelines ────────────────────────────────────────────
DOCUMENTS["02_ferma_guidelines.md"] = """# FERMA (Federal Roads Maintenance Agency) Guidelines

## Maintenance Categories
- Routine maintenance: Monthly/quarterly activities (clearing, pothole patching)
- Periodic maintenance: 3-5 year cycles (overlay, resealing)
- Emergency maintenance: Within 48 hours of defect detection
- Rehabilitation: Structural improvement every 15-20 years

## Pavement Distress Classification
- Cracking: Fatigue, block, edge, reflection, longitudinal, transverse
- Surface defects: Raveling, bleeding, polishing, stripping
- Deformation: Rutting, shoving, settlement, corrugation
- Potholes: Structural failure in localized areas
- Edge defects: Edge break, edge drop-off

## Condition Survey Rating
- Very Good (VG): 0-5% distress area, no structural defects
- Good (G): 5-15% distress, minor defects only
- Fair (F): 15-30% distress, some structural defects
- Poor (P): 30-50% distress, significant structural defects
- Very Poor (VP): >50% distress, requires reconstruction

## Maintenance Response Times
- Potholes on federal roads: Fill within 7 days of identification
- Shoulder erosion: Repair within 14 days
- Failed culverts: Replace within 30 days
- Vegetation clearance: Every 3 months during rainy season
- Drain cleaning: Monthly during rainy season
- Signage replacement: Within 14 days of damage report

## Quality Assurance
- All maintenance work must meet original design specifications
- Material testing every 500m for overlay projects
- Compaction testing: minimum 98% of maximum dry density
- Asphalt temperature at laying: 140-160°C for hot mix
- Surface tolerance: ±6mm under 3m straightedge
"""

# ── 3. Eurocodes for Structural Design ─────────────────────────────
DOCUMENTS["03_eurocodes_reference.md"] = """# Eurocodes - Reference for Structural Engineering

## Overview of Eurocodes
- EN 1990: Basis of structural design
- EN 1991: Actions on structures
- EN 1992: Design of concrete structures
- EN 1993: Design of steel structures
- EN 1994: Composite steel and concrete structures
- EN 1995: Design of timber structures
- EN 1996: Design of masonry structures
- EN 1997: Geotechnical design
- EN 1998: Design of structures for earthquake resistance
- EN 1999: Design of aluminium structures

## EN 1990 - Basis of Design
- Limit state design philosophy: Ultimate Limit State (ULS) and Serviceability Limit State (SLS)
- Design working life categories: 50 years for buildings, 100 years for bridges
- Partial factor method for all verifications
- Reliability classes: RC1, RC2, RC3 based on consequence class
- Consequence classes: CC1 (low), CC2 (medium), CC3 (high)

## EN 1992 - Concrete Design
- Concrete strength classes: C12/15 to C90/105
- Characteristic compressive strength fck (28 days)
- Design compressive strength fcd = fck / gamma_c
- Exposure classes: X0, XC1-4, XD1-3, XS1-3, XF1-4, XA1-3
- Minimum cover based on exposure class and structural class
- Crack width limits: 0.3mm for XC, 0.2mm for XD/XS
- Deflection limits: span/250 for quasi-permanent loads, span/500 for brittle finishes

## EN 1997 - Geotechnical Design
- Design approaches: DA1, DA2, DA3
- Partial factors for actions, materials, and resistances
- Bearing resistance verification using analytical or semi-empirical methods
- Serviceability limit state: settlements, heave, tilting
- Ultimate limit state: bearing failure, sliding, overturning, uplift
"""

# ── 4. Concrete Mix Design ─────────────────────────────────────────
DOCUMENTS["04_concrete_mix_design.md"] = """# Concrete Mix Design for Tropical Climates

## Materials Selection
- Cement: Ordinary Portland Cement (OPC) Grade 42.5 minimum
- Fine aggregate: River sand or crushed rock fines, zone 2 or 3 grading
- Coarse aggregate: Crushed granite or gravel, 20mm maximum size
- Water: Clean, potable water free from organic impurities, pH 6-8
- Admixtures: Plasticizers, retarders for hot weather concreting

## Mix Design Methods
- British Method (DOE): Most commonly used in Nigeria
- ACI Method: Suitable for large projects with aggregate data
- Trial mix method: For smaller projects

## Typical Mix Proportions (per m3 of concrete)
- Grade 20 (C16/20): Cement 300kg, Sand 800kg, Aggregate 1200kg, Water 180L (w/c 0.60)
- Grade 25 (C20/25): Cement 350kg, Sand 750kg, Aggregate 1150kg, Water 175L (w/c 0.50)
- Grade 30 (C25/30): Cement 400kg, Sand 700kg, Aggregate 1100kg, Water 170L (w/c 0.43)
- Grade 35 (C30/37): Cement 450kg, Sand 650kg, Aggregate 1050kg, Water 165L (w/c 0.37)
- Grade 40 (C35/45): Cement 500kg, Sand 600kg, Aggregate 1000kg, Water 160L (w/c 0.32)

## Hot Weather Concreting (Nigeria)
- Maximum concrete temperature at placing: 35°C
- Use chilled mixing water when ambient > 32°C
- Transport time limit: 60 minutes in tropical conditions
- Cover freshly placed concrete with wet burlap within 30 minutes
- Cure continuously for minimum 7 days
- Use retarder admixture when ambient > 35°C

## Quality Control
- Slump test: Target 25-75mm for reinforced concrete, 50-100mm for heavily reinforced
- Cube compressive strength: Test at 7 and 28 days
- Minimum 3 cubes per 50m3 or per day's pour
- Acceptance criteria: Mean - 1.64*stdev > characteristic strength
- Water-cement ratio shall not exceed design w/c by more than 0.02
"""

# ── 5. Asphalt & Bituminous Materials ──────────────────────────────
DOCUMENTS["05_asphalt_bituminous.md"] = """# Asphalt & Bituminous Materials for Tropical Roads

## Bitumen Grades for Tropical Climates
- Penetration grade 60/70: Standard for Nigerian highways
- Penetration grade 80/100: For high-altitude regions
- Polymer modified bitumen (PMB): For heavy traffic intersections and roundabouts
- Cutback bitumen: MC-30, MC-70 for prime coats and tack coats
- Emulsion: K1-60, K1-70 for surface dressing and slurry seal

## Hot Mix Asphalt (HMA) Design
- Marshall mix design method: Standard for tropical environments
- Marshall stability: minimum 8kN for heavy traffic, 5kN for light traffic
- Flow value: 2-4mm
- Air voids: 3-5% of mix volume
- Voids in mineral aggregate (VMA): minimum 14% for 19mm nominal maximum size
- Voids filled with bitumen (VFB): 65-78% for surface course
- Optimum bitumen content: typically 5.0-6.0% by weight of mix

## Asphalt Pavement Layers
- Wearing course: 40-50mm thick, dense graded, maximum aggregate size 12.5mm
- Binder course: 50-100mm thick, maximum aggregate size 19mm
- Base course: 100-200mm thick, maximum aggregate size 37.5mm
- Tack coat: 0.2-0.4 L/m2 residual bitumen between layers
- Prime coat: 0.6-1.0 L/m2 residual bitumen on granular base

## Hot Weather Laying Requirements
- Ambient temperature for laying: minimum 15°C, maximum 45°C
- Mix temperature at plant: 155-165°C for 60/70 pen bitumen
- Mix temperature at laying: minimum 140°C
- Compaction temperature: minimum 130°C
- Rolling pattern: 6-8 passes of vibratory roller (10-12 tonnes)
- Final rolling with tandem roller to remove roller marks
- Surface temperature before opening to traffic: < 40°C

## Quality Control Tests
- Bitumen penetration: ASTM D5, at 25°C, 100g, 5s
- Bitumen softening point: ASTM D36, ring and ball method
- Marshall stability and flow: ASTM D6927
- Bulk specific gravity: ASTM D2726
- Maximum theoretical specific gravity: ASTM D2041
- Air voids calculation: From bulk and maximum specific gravity
"""

# ── 6. Soil Mechanics & Geotechnical Engineering ──────────────────
DOCUMENTS["06_soil_mechanics.md"] = """# Soil Mechanics & Geotechnical Engineering for African Infrastructure

## Soil Classification Systems
- AASHTO Soil Classification: A-1 to A-7 groups
- Unified Soil Classification System (USCS): GW, GP, GM, GC, SW, SP, SM, SC, CL, ML, CH, MH
- Nigerian laterite soils: Special classification based on plasticity and grading
- Tropical red earths: Highly variable, require field identification

## Laboratory Testing
- Natural moisture content: Oven drying method, ASTM D2216
- Atterberg limits: Liquid limit, plastic limit, shrinkage limit
- Particle size distribution: Sieve analysis and hydrometer, ASTM D422
- Compaction test: Standard Proctor (2.5kg rammer, 305mm drop, 3 layers, 25 blows)
- Modified Proctor (4.5kg rammer, 457mm drop, 5 layers, 25 blows)
- California Bearing Ratio (CBR): Soaked and unsoaked, ASTM D1883
- Triaxial shear test: Unconsolidated undrained (UU), consolidated undrained (CU), consolidated drained (CD)
- Direct shear test: Quick and slow tests
- Consolidation test: One-dimensional oedometer, ASTM D2435

## Typical Soil Properties for Nigerian Soils
- Laterite (granular): MDD 1.9-2.2 g/cm3, OMC 10-15%, CBR 20-60%
- Laterite (clayey): MDD 1.6-1.9 g/cm3, OMC 15-25%, CBR 5-20%
- Sandy soil: MDD 1.7-2.0 g/cm3, OMC 8-12%, CBR 10-40%
- Clay soil: MDD 1.4-1.7 g/cm3, OMC 20-35%, CBR 2-8%
- Organic soil: Very poor engineering properties, avoid for structural fill

## Foundation Design Parameters
- Safe bearing capacity for rock: 1000-3000 kN/m2
- Safe bearing capacity for laterite: 200-500 kN/m2
- Safe bearing capacity for sand: 100-300 kN/m2
- Safe bearing capacity for clay: 50-150 kN/m2
- Minimum foundation depth: 1.0m in stable ground, 1.5m in expansive soils
- Minimum foundation depth below topsoil: 750mm

## Earthworks Specifications
- Topsoil stripping: 150-300mm depth, stockpile for landscaping
- Fill material: CBR > 5%, maximum particle size 150mm
- Embankment compaction: 95% MDD for lower layers, 98% for upper 500mm
- Maximum layer thickness before compaction: 200mm (loose)
- Compaction moisture content: OMC ± 2% for optimum results
- Field density test: Every 500m2 for embankments, every 250m2 for subgrade
"""

# ── 7. Drainage Design ─────────────────────────────────────────────
DOCUMENTS["07_drainage_design.md"] = """# Drainage Design for Infrastructure in Africa

## Hydrological Analysis
- Rainfall intensity-duration-frequency (IDF) curves for Nigerian cities
- Design return period: 10 years for urban drainage, 50 years for highways, 100 years for bridges
- Rational method: Q = CIA/360 (Q in m3/s, I in mm/hr, A in ha)
- Time of concentration: Kirpich formula, Manning's kinematic wave
- Runoff coefficient C: 0.90 for paved surfaces, 0.70 for gravel, 0.50 for grass, 0.30 for forest

## Drainage Structures Design
- Side drains: Trapezoidal shape, minimum depth 450mm, minimum width 600mm
- Lined drains: Concrete lining minimum 150mm thick for high velocities
- Culverts: Minimum diameter 900mm for main roads, 600mm for secondary
- Culvert length: Road width + 2x fill height + allowance for headwalls
- Headwalls and wingwalls: Required for all culverts to prevent scour
- Energy dissipators: Required for outlet velocities > 3m/s

## Hydraulic Design Criteria
- Drain velocity (minimum): 0.75 m/s to prevent sedimentation
- Drain velocity (maximum): 3.0 m/s for lined drains, 1.5 m/s for grassed
- Freeboard: 25% of design depth for open channels
- Manning's n: 0.015 for concrete, 0.025 for gravel, 0.035 for grass
- Culvert headwater depth: Limited to 1.2x culvert diameter

## Erosion Control
- Check dams: Every 50m on steep slopes (>5%)
- Gabion mattresses: For high-velocity channels
- Rip-rap protection: Around culvert outlets and bridge abutments
- Slope drains: Maximum 20m spacing between outlets
- Grassed waterways: For sheet flow and concentrated flow
- Silt fences: During construction to trap sediment

## Climate Adaptation
- Increase design rainfall intensity by 20% for climate change
- Design for 1-in-50 year storm for major infrastructure
- Overflow paths: Design for 1-in-100 year storm routed safely
- Permeable pavements: For parking areas and low-traffic roads
- Rain gardens and swales: For stormwater treatment in urban areas
"""

# ── 8. Bridge Engineering ──────────────────────────────────────────
DOCUMENTS["08_bridge_engineering.md"] = """# Bridge Engineering for African Infrastructure

## Bridge Types Common in Africa
- Reinforced concrete slab bridges: Span 5-15m, simple construction
- Reinforced concrete T-beam bridges: Span 15-30m
- Prestressed concrete I-girder bridges: Span 20-40m
- Steel truss bridges: Span 30-100m, for major river crossings
- Suspension bridges: Span > 100m, for major estuaries
- Bailey bridges: Military/prefabricated, span up to 60m for emergency use
- Culvert bridges: Box or pipe culverts for small spans (< 5m)

## Loading Standards
- HA loading (UK standard): 10 kN/m uniformly distributed, 100 kN knife edge load
- HB loading (UK standard): 45 units for Nigerian highways (450 kN total)
- Live load impact factor: 25% for reinforced concrete bridges
- Pedestrian loading: 5 kN/m2 on footways
- Wind loading: 1.0 kN/m2 on exposed surfaces, 1.5 kN/m2 for coastal areas

## Hydraulic Design
- Design flood: 100-year return period for major bridges
- Check flood: 200-year return period (scour check)
- Freeboard: 1.5m minimum above design flood level
- Scour depth: Calculate using Lacey-Inglis or Colorado State University formulas
- Afflux: Limited to 0.3m maximum to avoid upstream flooding
- Waterway area: Minimum 1.2x normal flow area

## Foundation Types for Bridges
- Spread footings: For rock or competent soil near surface
- Pile foundations: Bored cast-in-situ piles, diameter 600-1500mm
- Driven piles: Precast concrete or steel H-piles
- Pile cap: Minimum 1.5m thick, connecting all piles

## Bridge Deck Components
- Wearing surface: 50-75mm asphalt concrete
- Waterproofing membrane: Over entire deck surface
- Expansion joints: At every 30-40m for concrete bridges
- Bearings: Elastomeric bearings for spans < 30m
- Parapets/barriers: Minimum 1.1m height, designed to contain vehicles
- Drainage: Scuppers at 5m spacing, downpipes clear of structure
"""

# ── 9. Water Supply Engineering ────────────────────────────────────
DOCUMENTS["09_water_supply.md"] = """# Water Supply Engineering for African Communities

## Water Sources
- Groundwater: Boreholes (depth 30-200m), hand-dug wells (5-20m)
- Surface water: Rivers, lakes, dams, reservoirs
- Rainwater harvesting: Rooftop collection, storage tanks
- Spring water: Gravity-fed systems for hilly terrain

## Water Quality Standards
- WHO drinking water guidelines: Primary reference
- Nigerian Standard for Drinking Water Quality (NSDWQ)
- Turbidity: < 5 NTU (acceptable), < 1 NTU (desirable)
- pH: 6.5-8.5
- Total coliform: 0 CFU/100mL
- E. coli: 0 CFU/100mL
- Free residual chlorine: 0.2-0.5 mg/L at distribution point
- Iron: < 0.3 mg/L
- Manganese: < 0.1 mg/L
- Nitrate: < 50 mg/L
- Fluoride: 0.5-1.5 mg/L

## Water Treatment Processes
- Coagulation and flocculation: Alum dosage 10-50 mg/L
- Sedimentation: Surface loading rate 20-40 m3/m2/day
- Filtration: Rapid gravity filters, filtration rate 5-10 m/hr
- Disinfection: Chlorination, 2-5 mg/L dose, 30 min contact time
- pH adjustment: Lime dosage to achieve pH 7-8

## Water Distribution
- Minimum residual pressure: 10m head at farthest point
- Maximum velocity in pipes: 2.0 m/s
- Pipe materials: uPVC (for buried mains), HDPE (flexible), ductile iron (high pressure)
- Minimum pipe diameter: 75mm for distribution mains, 50mm for service lines
- Valve spacing: 200m maximum in distribution networks
- Fire hydrant spacing: 200m in urban areas, 100m in commercial zones

## Demand Estimation
- Urban domestic: 100-150 L/person/day
- Rural domestic: 30-60 L/person/day
- Public standpipe: 20-30 L/person/day
- Peak factor: 2.0-3.0 times average daily demand
- Design period: 20-25 years for major components, 10 years for pumps
"""

# ── 10. Structural Steel Design ────────────────────────────────────
DOCUMENTS["10_structural_steel.md"] = """# Structural Steel Design for Buildings and Bridges

## Steel Sections Commonly Used in Africa
- Universal beams (UB): Standard sections for beams and columns
- Universal columns (UC): Heavy sections for columns
- Channels (PFC): Bracing and secondary members
- Angles (L-sections): Bracing and truss members
- Circular hollow sections (CHS): Columns and trusses
- Rectangular hollow sections (RHS): Columns and beams
- Pipe sections: For handrails and bracing

## Design Standards
- BS 5950 (UK): Widely used in Nigerian practice
- Eurocode 3 (EN 1993): Increasing adoption
- Steel grade: S275 (standard), S355 (high strength) for structural applications
- Weldable reinforcing steel: Grade 460 for concrete reinforcement

## Connection Design
- Bolted connections: Grade 8.8 or 10.9 bolts, tension or shear
- Welded connections: Full penetration butt weld, fillet weld
- End plates: For beam-to-column connections
- Base plates: For column-to-foundation connections
- Cleat angles: For beam-to-beam connections

## Fire Protection
- Fire resistance periods: 30, 60, 90, 120 minutes per building regulations
- Intumescent paint: Up to 120 minutes fire resistance
- Board encasement: Plasterboard or vermiculite board
- Concrete encasement: 50-75mm minimum cover
- Sprinkler systems: May reduce required fire rating

## Corrosion Protection
- Hot-dip galvanizing: Standard for exposed steel in tropical environments
- Paint systems: Epoxy primer + polyurethane topcoat
- Weathering steel: Cor-ten for bridges (minimal maintenance)
- Cathodic protection: For steel in marine environments
- Zinc-rich primers: For shop-applied coatings

## Steel Bridges
- Plate girders: For spans 15-60m
- Truss girders: For spans 30-100m
- Arch bridges: For spans 50-200m
- Cable-stayed: For spans 100-500m
- Orthotropic decks: For long-span bridges (reduce weight)
"""

# ── 11. Environmental Impact Assessment ────────────────────────────
DOCUMENTS["11_environmental_impact.md"] = """# Environmental Impact Assessment (EIA) for Infrastructure Projects

## Legal Framework (Nigeria)
- NESREA Act 2007: National Environmental Standards and Regulations
- EIA Act (Cap E12 LFN 2004): Mandatory for major infrastructure
- NOSDRA: Oil spillage and environmental damage
- FMEnv: Federal Ministry of Environment oversight
- State environmental agencies: State-level EIA requirements

## EIA Process
- Screening: Determine if EIA is required
- Scoping: Identify key impacts and study areas
- Baseline study: Current environmental conditions
- Impact prediction: Assessment of project effects
- Mitigation measures: Actions to reduce negative impacts
- Environmental Management Plan (EMP): Implementation and monitoring
- Public participation: Stakeholder engagement and hearings
- EIA review: By FMEnv or designated agency
- Decision: Approval, conditional approval, or rejection

## Key Impact Categories
- Air quality: Construction dust, vehicle emissions, industrial emissions
- Water resources: Surface water quality, groundwater, drainage patterns
- Soil and land: Erosion, contamination, land use change
- Biodiversity: Habitat loss, species displacement, ecosystem disruption
- Noise and vibration: Construction and operational noise
- Visual impact: Landscape changes, lighting
- Socio-economic: Displacement, employment, community health
- Cultural heritage: Archaeological sites, sacred areas

## Mitigation Hierarchy
- Avoid: Design to avoid sensitive areas
- Minimize: Reduce impacts through design and construction methods
- Rectify: Restore damaged environments
- Reduce: Ongoing management to minimize impacts
- Compensate: Offsetting unavoidable impacts (e.g., tree planting)
"""

# ── 12. Project Management for Infrastructure ──────────────────────
DOCUMENTS["12_project_management.md"] = """# Project Management for Infrastructure Projects

## Project Lifecycle
- Conception: Needs assessment, feasibility study
- Planning: Design, budgeting, scheduling
- Execution: Construction, procurement, quality control
- Monitoring: Progress tracking, cost control, reporting
- Closeout: Handover, documentation, lessons learned

## Work Breakdown Structure (WBS)
- Level 1: Project name
- Level 2: Major phases (Design, Procurement, Construction)
- Level 3: Work packages (Site clearance, Earthworks, Drainage, Pavement)
- Level 4: Activities (Surveying, Clearing, Excavation, Compaction)
- Level 5: Tasks (Daily outputs, inspections, testing)

## Contract Types
- FIDIC Red Book: Conditions of Contract for Construction
- FIDIC Yellow Book: Design-Build
- FIDIC Silver Book: EPC/Turnkey
- Measured contract: Payment based on quantities
- Lump sum contract: Fixed price for defined scope
- Cost reimbursable: Payment based on actual costs plus fee

## Quality Management
- Quality plan: Project-specific quality requirements
- Inspection and test plans (ITP): For each work activity
- Hold points: Critical stages requiring inspection
- Material testing: Compliance with specifications
- Non-conformance reports (NCR): For defects and deviations
- Corrective action requests (CAR): For systemic issues

## Health and Safety
- HSE plan: Project-specific safety requirements
- Risk assessment: For all construction activities
- Method statement: Safe work procedures
- Personal protective equipment (PPE): Mandatory on all sites
- First aid: Minimum 1 trained person per 25 workers
- Emergency response: Evacuation plan, fire safety, accident reporting
"""

# ── 13. Traffic Engineering ────────────────────────────────────────
DOCUMENTS["13_traffic_engineering.md"] = """# Traffic Engineering and Transportation Planning

## Traffic Surveys
- Classified traffic counts: Vehicle classification (cars, buses, trucks, etc.)
- Origin-destination surveys: Trip patterns and movements
- Speed surveys: Spot speed, travel time, delay studies
- Parking surveys: Parking accumulation, duration, turnover
- Pedestrian counts: Volume and movement patterns

## Capacity Analysis (Highway Capacity Manual)
- Level of Service A: Free flow, low volumes
- Level of Service B: Reasonably free flow
- Level of Service C: Stable flow, at or near free flow
- Level of Service D: Approaching unstable flow
- Level of Service E: Unstable flow, at capacity
- Level of Service F: Forced or breakdown flow

## Intersection Design
- At-grade intersections: T-junctions, cross-roads, roundabouts
- Channelization: Islands and markings to guide traffic
- Traffic signals: Warrants for signal installation
- Roundabout capacity: Based on entry width, circulatory width, and inscribed diameter
- Grade separation: Interchanges for high-volume intersections

## Road Safety
- Black spot identification: High accident concentration locations
- Road safety audit: Systematic review of road safety performance
- Speed management: Speed humps, rumble strips, chicanes
- Signage and markings: Compliance with Nigerian Highway Code
- Street lighting: For urban roads and high-risk locations
- Barrier systems: Guardrails, crash barriers at hazardous locations
"""

# ── 14. Foundation Engineering ─────────────────────────────────────
DOCUMENTS["14_foundation_engineering.md"] = """# Foundation Engineering for African Soils

## Foundation Types
- Strip footing: For load-bearing walls, width 600-1500mm
- Pad footing: For columns, typically 1.0-3.0m square
- Combined footing: For closely spaced columns
- Raft foundation: For low bearing capacity, covers entire building area
- Pile foundation: For deep bearing stratum or high loads
- Pier foundation: For bridge abutments and heavy structures

## Bearing Capacity Calculation (Terzaghi)
- Ultimate bearing capacity (strip footing):
  qu = c*Nc + gamma*Df*Nq + 0.5*gamma*B*Ngamma
- Nc, Nq, Ngamma: Bearing capacity factors based on friction angle
- Allowable bearing capacity: qu / Factor of Safety (typically 3.0)

## Settlement Analysis
- Immediate settlement: Elastic deformation of soil
- Consolidation settlement: Time-dependent in clay soils
- Secondary settlement: Creep in organic soils
- Differential settlement: Must not exceed 25mm in buildings
- Total settlement: Typically limited to 50mm for buildings
- Angular distortion: Limited to 1/300 for framed structures

## Foundation in Expansive Soils
- Black cotton soil: Problematic in northern Nigeria
- Foundation depth: Below active zone (minimum 2.0m)
- Under-reamed piles: Bulb at base to resist uplift
- Soil replacement: Remove expansive soil, replace with granular fill
- Moisture barriers: Around foundation perimeter
- Flexible construction: Allow for movement without structural damage

## Pile Foundations
- Bored piles: Diameters 300-1500mm, depth 5-30m
- Driven piles: Precast concrete, steel H-piles, timber
- Pile capacity: End bearing + skin friction
- Pile spacing: Minimum 3x pile diameter (center to center)
- Pile cap: Minimum 1.0m thick, reinforced
- Pile load test: Static load test to 2x working load
- Integrity testing: Sonic echo or cross-hole sonic logging
"""

# ── 15. Construction Materials Testing ─────────────────────────────
DOCUMENTS["15_construction_materials.md"] = """# Construction Materials Testing & Quality Control

## Aggregate Testing
- Gradation: Sieve analysis (BS 812, ASTM C136)
- Specific gravity: Pycnometer method
- Water absorption: BS 812, limit < 2% for quality aggregate
- Aggregate crushing value (ACV): BS 812, limit < 30% for wearing course
- Aggregate impact value (AIV): BS 812, limit < 25% for wearing course
- Aggregate abrasion value (AAV): Los Angeles test, limit < 30% for base course
- Flakiness index: Limit < 30% for concrete aggregates
- Elongation index: Limit < 30% for concrete aggregates

## Concrete Testing
- Slump test: Workability measurement
- Compressive strength: Cube (150mm) or cylinder (150x300mm) at 7 and 28 days
- Flexural strength: Beam test for pavement concrete
- Indirect tensile strength: Splitting cylinder test
- Density: Fresh and hardened concrete
- Air content: For freeze-thaw resistance
- Chloride penetration: Rapid chloride permeability test
- Water absorption: Initial surface absorption test (ISAT)

## Soil Testing for Construction
- Moisture content: Oven drying method
- Atterberg limits: Casagrande method
- Particle size distribution: Wet and dry sieving
- Compaction: Standard and modified Proctor
- CBR: In-situ and laboratory, soaked and unsoaked
- Shear strength: Triaxial and direct shear
- Consolidation: Oedometer test for settlement

## Steel Reinforcement Testing
- Yield strength: BS 4449, minimum 500 N/mm2 for high-yield
- Ultimate tensile strength: BS 4449
- Elongation: Minimum 12% for ductility
- Bend test: 180-degree bend without cracking
- Rebar dimensions: Rib spacing, height, and pattern
- Chemical composition: Carbon equivalent limit
- Weldability: For welded connections
"""

# ── 16. Climate Adaptation for Infrastructure ──────────────────────
DOCUMENTS["16_climate_adaptation.md"] = """# Climate Adaptation for African Infrastructure

## Climate Projections for West Africa
- Temperature increase: 1.5-3°C by 2050 (RCP 4.5-8.5)
- Rainfall changes: Increased intensity, less frequent but more extreme events
- Sea level rise: 0.3-0.6m by 2100 along West African coast
- Increased frequency of extreme events: Floods, droughts, heatwaves
- Shift in rainfall patterns: Delayed onset, early cessation in many regions

## Flood Resilience Design
- Raise embankment height: 0.5m above 100-year flood level
- Adequate culvert capacity: Design for 50-year storm events
- Scour protection: At bridge abutments and culvert outlets
- Permeable pavements: For parking areas and low-traffic roads
- Rain gardens and bioswales: For stormwater management
- Flood barriers: Demountable barriers for critical infrastructure

## Heat Resilience
- Light-colored pavement surfaces: Reduce heat absorption by 20-30%
- High softening point asphalt: For tropical regions (minimum 55°C)
- Reflective coatings: On bridge decks and roofs
- Shade trees: Along urban road corridors, reduce pavement temperature by 5-10°C
- Thermal expansion joints: Accommodate increased temperature range
- Ventilation: For below-grade structures and tunnels

## Drought Resilience
- Water harvesting: From pavement runoff for non-potable uses
- Drought-resistant vegetation: For roadside landscaping
- Water-efficient construction: Recycle construction water
- Groundwater recharge: Through permeable shoulders and recharge pits
- Greywater systems: For maintenance facilities

## Coastal Infrastructure
- Sea walls and revetments: Protect coastal roads and facilities
- Mangrove restoration: Natural coastal defense
- Elevated structures: Above projected sea level rise
- Salt-resistant materials: For marine environment exposure
- Drainage: Prevent saltwater intrusion into freshwater systems
"""

# ── 17. Sustainable Construction ──────────────────────────────────
DOCUMENTS["17_sustainable_construction.md"] = """# Sustainable Construction Practices for Africa

## Green Building Materials
- Compressed earth blocks (CEB): Stabilized with 5-8% cement
- Bamboo: Renewable structural material for light construction
- Recycled aggregate: From construction and demolition waste, up to 30% replacement
- Reclaimed asphalt pavement (RAP): Up to 30% in new hot mix, 50% in cold mix
- Recycled concrete aggregate: In base and subbase layers
- Plastic-modified asphalt: Waste plastic in bitumen, up to 6% by weight

## Energy Efficiency
- Building orientation: North-south alignment to minimize solar gain
- Natural ventilation: Cross-ventilation design, window placement
- Solar water heating: For buildings and facilities
- LED lighting: For all road lighting and buildings
- Solar-powered street lights: Standalone with battery storage
- Energy-efficient pumps: Variable frequency drives for water pumping

## Water Conservation
- Rainwater harvesting: Rooftop collection with storage tanks, sizing for 30-day storage
- Water-efficient fixtures: Low-flow taps and toilets
- Greywater recycling: For landscape irrigation and flushing
- Erosion control: During and after construction
- Sediment basins: During construction to trap runoff

## Waste Management
- Construction waste segregation: Metal, wood, plastic, concrete
- Recycling: Target 50% diversion from landfill
- Proper disposal: Hazardous materials (paints, solvents, asbestos)
- Site cleanliness: Daily waste collection and disposal
- Temporary waste storage: Covered skips for recyclable materials
- Demolition planning: Selective demolition for maximum recovery

## Carbon Reduction
- Local materials: Reduce transport emissions
- Alternative cement: Up to 50% fly ash or slag replacement in concrete
- Low-carbon concrete: Geopolymer concrete for reduced carbon footprint
- Carbon sequestration: Tree planting on road verges
- Construction methods: Reduce fuel consumption and idling
- Maintenance planning: Extend asset life to spread carbon cost
"""

# ── 18. Highway Geometric Design ──────────────────────────────────
DOCUMENTS["18_highway_geometric_design.md"] = """# Highway Geometric Design

## Horizontal Alignment
- Circular curves: Minimum radius based on design speed and superelevation
- Transition curves: Clothoid spiral, length based on rate of change of lateral acceleration
- Superelevation: Runoff length on tangent-to-curve transition
- Sight distance: Horizontal sightline offset for horizontal curves
- Curve widening: On sharp curves to accommodate vehicle swept path

## Vertical Alignment
- Vertical curves: Parabolic shape for comfort and sight distance
- Crest curves: K-value based on stopping sight distance
- Sag curves: K-value based on headlight sight distance
- Maximum gradient: 8% for rural highways, 5% for urban
- Minimum gradient: 0.5% for drainage
- Critical length of grade: Based on truck speed reduction

## Cross Section Design
- Travel lane width: 3.5m minimum for highways
- Shoulder width: 2.5m paved or 3.0m unpaved
- Median width: 5.0m minimum for divided highways
- Side slope: 2:1 (H:V) maximum for fills, 1:1 for cuts
- Clear zone: Based on traffic volume and design speed
- Drainage swale: 3.0m minimum width beyond shoulder

## Intersection Design
- Channelization: Left-turn and right-turn lanes
- Acceleration lanes: For merging onto high-speed roads
- Deceleration lanes: For exiting high-speed roads
- Corner radius: Based on design vehicle turning path
- Sight triangles: Clear sight distance at intersections
- Roundabout geometry: Entry width, circulatory width, island diameter

## Roadside Safety
- Clear recovery zone: 9m for 100 km/h design speed
- Guardrails: W-beam, strong post, at embankments > 3m height
- Crash cushions: At fixed obstacles (bridge piers, sign supports)
- Breakaway supports: For signs and lighting within clear zone
- End treatments: Energy-absorbing guardrail terminals
- Median barriers: For divided highways with narrow medians
"""

# ── 19. Hydrological Modeling ──────────────────────────────────────
DOCUMENTS["19_hydrological_modeling.md"] = """# Hydrological Modeling for Infrastructure Design

## Catchment Characteristics
- Catchment area: Delineation from topographic maps or DEM
- Shape factor: Elongation ratio, circularity ratio
- Slope: Main channel slope, catchment slope
- Land use: Urban, agricultural, forest, water bodies
- Soil type: Hydrological soil groups (A, B, C, D)
- Antecedent moisture condition: Dry, moderate, wet (AMC I, II, III)

## Rainfall Analysis
- Annual rainfall: Nigeria ranges from 500mm (north) to 4000mm (south)
- Seasonal distribution: April-October rainy season
- Intensity-duration-frequency (IDF) curves: For design storms
- Design storm duration: Equal to time of concentration
- Design storm profile: SCS Type I, IA, II, III distribution
- Probable maximum precipitation (PMP): For dam spillway design

## Flood Estimation Methods
- Rational method: Q = CIA/360, for catchments < 50 ha
- SCS curve number method: For ungauged catchments
- Unit hydrograph: For gauged catchments with rainfall data
- Flood frequency analysis: Gumbel, Log-Pearson Type III distributions
- Regional flood equations: For specific regions in Nigeria
- Hydrologic modeling: HEC-HMS, SWMM for complex systems

## Design Flood Estimation
- Return period selection: Based on infrastructure importance and risk
- Minor structures (culverts): 10-25 year return period
- Major structures (bridges): 50-100 year return period
- Dams: 100-1000 year return period, PMF for high hazard
- Climate change factor: Increase flood by 10-30% for future scenarios

## Groundwater Hydrology
- Aquifer types: Confined, unconfined, perched
- Hydraulic conductivity: Typical range 10^-6 to 10^-2 m/s
- Transmissivity: K * aquifer thickness
- Storage coefficient: Specific yield for unconfined, storativity for confined
- Well yield: Specific capacity, safe yield
- Groundwater modeling: MODFLOW for regional studies
"""

# ── 20. Railway Engineering ────────────────────────────────────────
DOCUMENTS["20_railway_engineering.md"] = """# Railway Engineering for African Infrastructure

## Track Components
- Rails: Standard 40kg/m or 60kg/m for main lines
- Sleepers: Timber, concrete (monoblock or twin-block), steel
- Fastenings: Clips and baseplates, Pandrol or similar
- Ballast: Granite or other hard stone, 50mm grading
- Sub-ballast: 150mm granular layer below ballast
- Formation: Compacted subgrade, minimum CBR 5%

## Track Geometry Standards
- Gauge: 1067mm (Cape gauge) for most African railways
- Standard gauge (1435mm): For new high-speed lines
- Maximum gradient: 1.5% for main lines, 2.5% for secondary
- Minimum curve radius: 200m for main lines, 150m for secondary
- Cant (superelevation): Maximum 150mm for mixed traffic
- Cant deficiency: 75mm for passenger, 50mm for freight
- Transition curve minimum length: 50m for main lines

## Turnouts and Crossings
- Switch types: Split switch, stub switch
- Crossing angle: 1 in 8 to 1 in 12 for main lines
- Diamond crossing: For track intersections
- Double slip: For compact layouts
- Crossovers: Between parallel tracks

## Signaling Systems
- Absolute block: For single line working
- Automatic block: For double line working
- Interlocking: Mechanical or electronic at stations
- Level crossing protection: Gates, flashing lights, barriers
- Train control: Cab signaling or ERTMS for main lines

## Maintenance Standards
- Rail inspection: Ultrasonic testing every 6-12 months
- Track geometry measurement: Trolley or EMU-based, quarterly
- Ballast cleaning: Every 10-15 years
- Rail grinding: Preventive grinding every 30-60 MGT
- Sleeper replacement: As needed, timber 15-20 years, concrete 30-50 years
- Lubrication: On curves to reduce wear
"""

# ── 21. GIS in Infrastructure ─────────────────────────────────────
DOCUMENTS["21_gis_in_infrastructure.md"] = """# Geographic Information Systems (GIS) in Infrastructure

## GIS Applications
- Route alignment: Optimal path analysis, terrain analysis
- Catchment delineation: Watershed boundaries for drainage
- Environmental mapping: Vegetation, soils, land use
- Asset management: Road inventory, condition mapping
- Utility mapping: Water pipes, power lines, telecom
- Traffic analysis: Accident mapping, congestion analysis
- Flood mapping: Flood hazard zones for infrastructure

## Data Sources
- Satellite imagery: Landsat (30m), Sentinel (10m), Maxar (0.3m)
- Digital elevation models: SRTM (30m), ALOS (12.5m), LiDAR (1m)
- Topographic maps: Survey department, scale 1:50,000
- Administrative boundaries: National boundaries, states, LGAs
- Infrastructure data: Roads, railways, utilities from OSM or surveys
- Census data: Population distribution for demand analysis

## Spatial Analysis
- Least-cost path: Route optimization considering terrain, land use, cost
- Viewshed analysis: Visibility for tower and facility siting
- Buffer analysis: Impact zones around infrastructure
- Overlay analysis: Multi-criteria decision making
- Network analysis: Shortest path, service area, location-allocation
- Interpolation: Spline, kriging for rainfall, soil properties

## GIS Software (Open Source)
- QGIS: Desktop GIS for mapping and analysis
- GRASS GIS: Advanced raster and vector analysis
- SAGA GIS: Terrain and hydrological analysis
- PostGIS: Spatial database for storing and querying
- GDAL: Raster and vector data processing
- Leaflet/OpenLayers: Web mapping interfaces

## Standards
- OGC standards: WMS, WFS, WCS for data sharing
- ISO 19100 series: Geographic information standards
- SDI (Spatial Data Initiative): Nigerian NSDI framework
- Metadata: ISO 19115 for dataset documentation
- Coordinate systems: UTM zones (Zone 31-33 for Nigeria)
- Datum: WGS84, Minna (Nigeria) datum for local accuracy
"""

# ── 22. Construction Health and Safety ─────────────────────────────
DOCUMENTS["22_health_and_safety.md"] = """# Construction Health and Safety

## Legislation (Nigeria)
- Factories Act Cap F1 LFN 2004
- Labour Act Cap L1 LFN 2004
- Workmen's Compensation Act Cap W6 LFN 2004
- NESREA regulations on workplace safety
- State-specific safety regulations

## Hazard Identification
- Physical hazards: Working at height, excavation, moving machinery
- Chemical hazards: Cement dust, paints, solvents, asbestos
- Biological hazards: Insects, snakes, waterborne diseases
- Ergonomic hazards: Manual handling, repetitive work
- Psychosocial hazards: Stress, fatigue, long working hours

## High-Risk Activities
- Working at height: Fall protection above 2m, scaffolding inspection
- Excavation: Shoring for trenches > 1.2m deep, sloping, benching
- Lifting operations: Crane certification, lift plan, tag lines
- Confined spaces: Permit-to-work, gas monitoring, rescue plan
- Demolition: Engineering survey, sequential demolition, dust control
- Hot work: Welding permit, fire watch, fire extinguishers

## Required PPE
- Head protection: Hard hat on all construction sites
- Foot protection: Steel-toed boots
- Eye protection: Safety glasses for grinding and chipping
- Hearing protection: Earplugs above 85dB, earmuffs above 105dB
- Respiratory protection: N95 masks for dust, respirators for chemicals
- High-visibility clothing: On all live traffic sites
- Fall protection: Harness and lanyard for work above 2m

## Emergency Procedures
- First aid: Minimum 1 trained person per 25 workers
- Fire safety: Extinguishers every 200m2, fire hose reels
- Evacuation: Assembly point, roll call, designated marshals
- Medical emergency: Nearest hospital route, ambulance contact
- Accident reporting: Incident within 24 hours to authorities
- Rescue plan: For high-risk activities, practiced quarterly
"""

# ── 23. Geotechnical Investigation ────────────────────────────────
DOCUMENTS["23_geotechnical_investigation.md"] = """# Geotechnical Investigation for Infrastructure Projects

## Investigation Phases
- Desk study: Review existing data, geological maps, site history
- Reconnaissance: Site walkover, visual assessment, photography
- Preliminary investigation: Trial pits, shallow auger holes
- Detailed investigation: Boreholes, sampling, in-situ testing
- Construction verification: Foundation inspection, compaction testing

## Borehole Requirements
- Building foundations: Minimum 2 boreholes per structure, spacing 20-50m
- Bridge foundations: Minimum 1 borehole per abutment and pier
- Road projects: Boreholes every 500m, alternating sides, min 5m depth
- Retaining walls: Boreholes every 25-50m along wall alignment
- Minimum depth: 2x foundation width, or to rock if shallow
- Rock coring: NQ or PQ diamond core for bedrock confirmation

## Sampling
- Disturbed samples: Bulk bag samples for classification and compaction
- Undisturbed samples: Thin-wall tube (Shelby) for strength and consolidation
- Rock core: Continuous coring, core recovery and RQD logging
- Groundwater: Observation wells, piezometers for water level monitoring
- Sampling frequency: Every 1.5m in boreholes, minimum one sample per soil type

## In-Situ Testing
- Standard penetration test (SPT): Every 1.5m in boreholes, N-value for strength
- Cone penetration test (CPT): Continuous profile of tip resistance and friction
- Vane shear test: For in-situ undrained strength of clays
- Plate load test: For bearing capacity verification
- Permeability test: Falling head or constant head in boreholes
- Pressuremeter test: For modulus of deformation

## Reporting
- Borehole logs: Standard format with soil description, SPT N-values, water levels
- Soil profile: Geological cross-sections along alignment
- Laboratory results: Summary tables of all test results
- Foundation recommendations: Allowable bearing capacity, foundation type
- Pavement recommendations: Subgrade CBR, pavement thickness design
- Construction recommendations: Excavation, dewatering, compaction requirements
"""

# ── 24. Municipal Engineering ─────────────────────────────────────
DOCUMENTS["24_municipal_engineering.md"] = """# Municipal Engineering for African Cities

## Urban Road Design
- Local streets: 6-9m carriageway, 20-30km/h design speed
- Collector roads: 9-12m carriageway, 40-50km/h
- Arterial roads: 12-18m carriageway, 60-80km/h
- Pedestrian footways: minimum 1.5m width, 0.5m from carriageway
- Cycle lanes: 1.5-2.0m width, separate or marked on road
- Street furniture: Lighting, seating, signage, waste bins

## Solid Waste Management
- Collection frequency: Daily in commercial areas, weekly in residential
- Transfer stations: 10-20km radius of service area
- Landfill design: Liner system, leachate collection, gas management
- Recycling: Segregation at source, collection points, buy-back centers
- Composting: Organic waste processing for agricultural use
- Disposal: Engineered sanitary landfill with environmental controls

## Public Water Supply
- Distribution network: Looped system for reliability
- Storage tanks: Minimum 12-24 hours of average demand
- Pressure zones: Separate zones for high-rise and low-rise areas
- Non-revenue water: Target < 20% through leak detection and metering
- Disinfection: Continuous chlorination, residual monitoring
- Water quality: Regular testing at treatment works and distribution points

## Sewerage Systems
- Separate system: Stormwater and sewage in separate pipes
- Combined system: For older urban areas
- Minimum pipe diameter: 150mm for sewers
- Minimum slope: 1:100 for 150mm, 1:80 for 100mm
- Manhole spacing: Maximum 100m on straight runs
- Treatment: Stabilization ponds for tropical climates, extended aeration
"""

# ── 25. Infrastructure Asset Management ───────────────────────────
DOCUMENTS["25_asset_management.md"] = """# Infrastructure Asset Management

## Asset Types
- Roads: Pavement, bridges, culverts, drainage, signage, lighting
- Water supply: Treatment plants, reservoirs, pipes, valves, hydrants
- Wastewater: Treatment plants, sewers, pumping stations, manholes
- Buildings: Administrative, maintenance, storage, residential
- Equipment: Vehicles, plant, tools, IT systems

## Asset Register
- Unique ID: Barcode or RFID tag for each asset
- Location: GPS coordinates, route/chainage for linear assets
- Description: Type, dimensions, material, capacity
- Condition: Rating scale (1-5), inspection date
- Valuation: Replacement cost, depreciated value
- Maintenance history: Date, type, cost, contractor

## Condition Assessment
- Visual inspection: Routine (monthly to annual) depending on asset type
- Detailed inspection: Specialist, every 3-5 years
- Non-destructive testing: For critical assets (GPR, ultrasonic)
- Condition rating: 1 (excellent) to 5 (failed) scale
- Residual life: Estimate based on condition and deterioration curve
- Risk rating: Likelihood × consequence for prioritization

## Maintenance Strategies
- Reactive maintenance: Fix when broken (unplanned)
- Preventive maintenance: Scheduled activities (time-based)
- Predictive maintenance: Condition-based, triggered by monitoring
- Reliability-centered maintenance (RCM): For critical assets
- Lifecycle costing: Optimize replacement vs. repair
- Maintenance prioritization: Based on risk, criticality, and budget

## Budgeting and Planning
- Annual maintenance plan: Prioritized list with costs
- Three-year rolling program: Medium-term planning
- Lifecycle cost analysis: Least-cost over asset life
- Value management: Optimize function vs. cost
- Performance indicators: Condition targets, response times, cost per unit
- Reporting: Quarterly and annual performance reports to stakeholders
"""

# ── 26. Concrete Repair and Rehabilitation ────────────────────────
DOCUMENTS["26_concrete_repair.md"] = """# Concrete Repair and Rehabilitation

## Causes of Concrete Deterioration
- Carbonation: CO2 penetration reduces pH, leading to reinforcement corrosion
- Chloride ingress: From marine environment or de-icing salts
- Sulfate attack: From soil or groundwater containing sulfates
- Alkali-aggregate reaction (AAR): Reactive silica in aggregate
- Freeze-thaw damage: In high-altitude regions
- Mechanical damage: Overloading, impact, abrasion
- Fire damage: Spalling and strength loss at high temperatures
- Poor construction: Inadequate cover, compaction, curing

## Condition Assessment
- Visual inspection: Cracks, spalling, staining, exposed reinforcement
- Half-cell potential: ASTM C876, corrosion probability mapping
- Carbonation depth: Phenolphthalein indicator spray
- Chloride profile: Acid-soluble chloride content at various depths
- Cover measurement: Covermeter survey
- Core sampling: Compressive strength, petrographic analysis
- Pull-off test: Bond strength of repairs and coatings

## Repair Methods
- Crack injection: Epoxy for structural cracks, polyurethane for water stops
- Surface repair: Patch repair with polymer-modified cement mortar
- Shotcrete/gunite: For large-area repairs
- Cathodic protection: Impressed current or sacrificial anode
- Corrosion inhibitors: Migrating corrosion inhibitors for reinforced concrete
- Electrochemical realkalization: For carbonated concrete
- Chloride extraction: Electrochemical for chloride-contaminated concrete

## Protective Coatings
- Anti-carbonation coatings: Breathable, UV-resistant for exposed surfaces
- Water repellents: Silane/siloxane for hydrophobic treatment
- Epoxy coatings: For chemical resistance
- Acrylic coatings: For decorative and protective finish
- Sacrificial coatings: Zinc-rich primers for steel
- Fire-resistant coatings: Intumescent for structural steel
"""

# ── 27. Tender and Procurement ────────────────────────────────────
DOCUMENTS["27_tendering_procurement.md"] = """# Tender and Procurement for Infrastructure Projects

## Procurement Methods
- Open tender: Public advertisement, any qualified contractor can bid
- Selective tender: Pre-qualified contractors invited to bid
- Negotiated contract: Direct negotiation with single contractor
- Design-build: Contractor responsible for both design and construction
- PPP (Public-Private Partnership): Private finance and operation
- EPC (Engineering, Procurement, Construction): Turnkey delivery

## Bidding Documents
- Invitation to tender: Project description, eligibility, submission deadline
- Instructions to tenderers: Bid preparation, submission, evaluation criteria
- Form of tender: Bid price, validity period, signature
- Conditions of contract: General and particular conditions
- Specifications: Technical requirements, standards, testing
- Bill of quantities (BOQ): Measured quantities with unit rates
- Drawings: Design drawings, typical details
- Addenda: Clarifications issued during tender period

## Tender Evaluation
- Responsiveness: Compliance with submission requirements
- Technical evaluation: Methodology, experience, personnel, equipment
- Financial evaluation: Bid price comparison, arithmetical checks
- Post-qualification: Verification of claims and references
- Best value: Quality/price ratio, not just lowest price
- Negotiation: With preferred bidder for final terms

## Contract Award
- Letter of acceptance: Formal notification to successful bidder
- Performance bond: 5-10% of contract value for performance guarantee
- Advance payment bond: For mobilization advance, up to 15% of contract
- Defects liability period: 6-12 months for infrastructure projects
- Retention: 5-10% withheld, released after defects period
- Insurance: All-risk, third party, workmen's compensation
"""

# ── 28. Materials for Low-Cost Housing ────────────────────────────
DOCUMENTS["28_low_cost_housing.md"] = """# Materials for Low-Cost Housing in Africa

## Alternative Wall Materials
- Compressed stabilized earth blocks (CSEB): 5-8% cement, 40% cheaper than sandcrete
- Interlocking stabilized soil blocks (ISSB): No mortar required, faster construction
- Hydraform blocks: Interlocking, machine-pressed, cement-stabilized
- Sandcrete blocks: 225x225x450mm for load-bearing walls
- Expanded polystyrene (EPS) panels: Lightweight, insulated
- Bamboo reinforced panels: Renewable, seismic-resistant

## Roofing Options
- Corrugated iron sheets: Most common, affordable, 0.3-0.5mm gauge
- Clay/concrete tiles: Durable, good thermal performance
- Thatched roofing: Traditional, good insulation, limited lifespan (5-10 years)
- Polycarbonate sheets: For daylighting and covered areas
- Recycled roofing tiles: From waste plastic and fiber

## Foundation Systems
- Strip footings: For load-bearing walls, 600mm wide, 1.0m deep (minimum)
- Raft foundation: For poor soil, covers entire building footprint
- Stub columns: With ground beams for sloping sites
- Pier and beam: For steep slopes and flood-prone areas
- Rammed earth plinth: For low-cost, low-rise buildings

## Cost-Saving Techniques
- Local materials: Reduce transport costs by 30-50%
- Simple designs: Rectangular plan, standard window/door sizes
- Owner-built: Self-help construction with technical supervision
- Incremental construction: Build core house, expand over time
- Community labor: Harnessing local workforce for non-specialist tasks
- Standardized components: Pre-cast lintels, stairs, window frames
"""

# ── 29. Structural Analysis Methods ───────────────────────────────
DOCUMENTS["29_structural_analysis.md"] = """# Structural Analysis Methods

## Analysis Methods
- Elastic analysis: Linear stress-strain, serviceability checks
- Plastic analysis: Ultimate limit state, collapse mechanisms
- Second-order analysis: P-Delta effects for slender frames
- Finite element analysis (FEA): For complex geometries and stress analysis
- Dynamic analysis: Modal, response spectrum, time history
- Nonlinear analysis: Material and geometric nonlinearity
- Buckling analysis: Linear and nonlinear for slender members

## Load Combinations (BS 8110)
- Dead load + Imposed load: 1.4DL + 1.6IL (ULS)
- Dead load + Wind load: 1.4DL + 1.4WL
- Dead load + Imposed + Wind: 1.2DL + 1.2IL + 1.2WL
- Serviceability: 1.0DL + 1.0IL
- Accidental: 1.0DL + 0.33IL + 1.0AD

## Design Loads for Buildings (BS 6399)
- Imposed floor loads: 1.5 kN/m2 (domestic), 3.0 kN/m2 (offices), 5.0 kN/m2 (retail)
- Imposed roof loads: 0.75 kN/m2 (accessible), 1.5 kN/m2 (with storage)
- Wind loads: Based on basic wind speed, topography, building height
- Seismic loads: For earthquake zones (limited in West Africa)
- Thermal loads: For restrained structures
- Settlement loads: For differential foundation movement

## Structural Framing Systems
- Moment-resisting frames: Rigid beam-column connections
- Braced frames: With lateral bracing for wind resistance
- Shear walls: Reinforced concrete walls for lateral stability
- Tube structures: For tall buildings, perimeter moment frame
- Space frames: Three-dimensional truss systems for large spans
- Portal frames: Single-story, pinned or fixed base for industrial buildings

## Software Tools
- Prokon: Popular in African consulting for structural analysis and design
- ETABS: For building analysis and design
- SAP2000: General-purpose finite element analysis
- STAAD Pro: For structural analysis of frames and bridges
- Robot Structural Analysis: BIM-integrated analysis
- Tekla Structural Designer: For steel and concrete design
"""
# ── 30. Irrigation Engineering ────────────────────────────────────
DOCUMENTS["30_irrigation_engineering.md"] = """# Irrigation Engineering for African Agriculture

## Irrigation Methods
- Surface irrigation: Border, furrow, basin for suitable topography
- Sprinkler irrigation: Center pivot, lateral move, hand move
- Drip irrigation: Most efficient (90-95%), for high-value crops
- Micro-irrigation: Drip, micro-sprinklers for orchards and vegetables
- Manual irrigation: Bucket and watering can for small gardens

## Water Requirements
- Crop evapotranspiration (ETc): Reference ET × crop coefficient (Kc)
- Reference ET (ETo): Penman-Monteith or Pan evaporation method
- Net irrigation requirement: ETc - effective rainfall
- Gross irrigation requirement: Net / application efficiency
- Irrigation interval: Based on soil moisture depletion
- Application depth: Root zone depth × field capacity deficit

## Irrigation System Design
- Pump capacity: Based on flow rate and total dynamic head
- Pipe sizing: Friction loss < 15% of operating pressure
- Sprinkler spacing: Based on wind speed and nozzle pattern
- Drip line spacing: Based on crop row spacing and soil type
- Filtration: Screen, disc, or sand media for drip systems
- Fertigation: Fertilizer injection through irrigation system

## Water Sources
- Rivers and streams: With abstraction license
- Groundwater: Boreholes with pump test
- Reservoirs: Small dams for dry season irrigation
- Rainwater harvesting: Storage ponds and tanks
- Wastewater treatment: Treated effluent for irrigation

## Soil-Water Relationships
- Field capacity: Soil moisture after free drainage (typically -33 kPa)
- Permanent wilting point: Soil moisture beyond plant recovery (-1500 kPa)
- Available water capacity: Field capacity - wilting point
- Saturation: All pore spaces filled with water
- Infiltration rate: Varies by soil type (5-50 mm/hr)
- Deep percolation: Water beyond root zone, represents loss
"""

# ── 31. Land Surveying ───────────────────────────────────────────
DOCUMENTS["31_land_surveying.md"] = """# Land Surveying for Infrastructure Projects

## Survey Types
- Control survey: Establishing primary and secondary control points
- Topographic survey: Contours, features, boundaries for design
- Route survey: For linear infrastructure (roads, pipelines, power lines)
- Hydrographic survey: Water depth, bed levels for bridges and ports
- Cadastral survey: Property boundaries for land acquisition
- Construction survey: Setting-out, as-built, monitoring
- GPS/GNSS survey: Real-time kinematic (RTK) for high accuracy

## Equipment
- Total station: Electronic distance measurement (EDM), angles, coordinates
- Level: Automatic or digital, for heights and contours
- GPS receiver: GNSS for control and topographic surveys
- Drone/UAV: Aerial photography, photogrammetry, LiDAR
- 3D scanner: Terrestrial laser scanning for detailed surveys
- Measuring tape: For short distances and offsets

## Survey Accuracy Standards
- Primary control: 1:100,000 or better
- Secondary control: 1:50,000
- Topographic survey: 1:2,500 to 1:10,000 scale
- Contour interval: 0.5m for flat terrain, 1.0m for rolling terrain, 2.0m for steep
- Spot heights: Minimum 15 per hectare for detailed design
- Cross-sections: Every 20m for road design, 10m for complex terrain

## Coordinate Systems
- UTM (Universal Transverse Mercator): Standard for mapping
- Local grid: For small projects, arbitrary datum
- Geodetic datum: WGS84, Minna (Nigeria) datum
- Height datum: Mean sea level (MSL) via tide gauge
- Projection: UTM zones 31-33 for Nigeria
- Transformation: Between datums using 7-parameter Helmert
"""

# ── 32. Erosion and Sediment Control ──────────────────────────────
DOCUMENTS["32_erosion_control.md"] = """# Erosion and Sediment Control for Construction Sites

## Erosion Processes
- Sheet erosion: Uniform removal of thin layer of soil
- Rill erosion: Small channels formed by concentrated flow
- Gully erosion: Deep channels, major concern in southeastern Nigeria
- Streambank erosion: Along rivers and drainage channels
- Wind erosion: In northern Nigeria during dry season
- Coastal erosion: Along Atlantic coast, up to 30m/year in some areas

## Erosion Control Measures
- Vegetation: Grass cover, trees, shrubs for slope stabilization
- Mulching: Straw, wood chips, or geotextile for bare soil
- Erosion control blankets: Biodegradable mats for slopes
- Hydroseeding: Spray application of seed, fertilizer, and mulch
- Terracing: Step-like construction on steep slopes
- Check dams: Small structures across drainage channels

## Sediment Control
- Silt fences: Along site perimeter, filter sediment from runoff
- Sediment basins: Temporary ponds to settle suspended solids
- Sediment traps: Small check dams with gravel outlet
- Inlet protection: Around storm drain inlets
- Stabilized construction entrance: Rock pad to prevent mud tracking
- Street sweeping: Regular cleaning of paved areas

## Construction Sequence
- Phase 1: Install perimeter controls before earthworks
- Phase 2: Clear and grub in stages, not entire site at once
- Phase 3: Grade and stabilize slopes immediately
- Phase 4: Install drainage structures concurrently
- Phase 5: Revegetate disturbed areas within 14 days of final grade
- Phase 6: Remove temporary controls only after permanent stabilization

## Regulatory Requirements
- NESREA: National guidelines for erosion and sediment control
- State regulations: Additional requirements in some states
- Stormwater pollution prevention plan (SWPPP): For large projects
- Inspections: Weekly and within 24 hours of > 25mm rainfall
- Maintenance: Repair controls within 48 hours of damage
- Record keeping: Inspection logs, maintenance records, photo documentation
"""

# ── 33. Quality Assurance in Construction ─────────────────────────
DOCUMENTS["33_quality_assurance.md"] = """# Quality Assurance and Quality Control in Construction

## QA/QC Definitions
- Quality Assurance: Systematic processes to ensure quality requirements are met
- Quality Control: Inspection and testing to verify compliance
- Quality Management System (QMS): Documented policies and procedures
- ISO 9001: International standard for quality management

## Quality Documentation
- Project Quality Plan (PQP): Overall quality approach for the project
- Inspection and Test Plan (ITP): Specific inspections for each activity
- Method Statement: Detailed work procedure for each activity
- Quality Records: Completed inspection forms, test results, certificates
- Non-Conformance Report (NCR): For work not meeting specifications
- Corrective Action Request (CAR): For systemic quality issues

## Hold Points and Witness Points
- Hold point: Work cannot proceed without inspection
- Witness point: Inspection required, but work can proceed if inspector absent
- Review point: Document review required before proceeding
- Typical hold points: Foundation concrete, steel erection, pressure testing
- Notification period: Minimum 24-48 hours for hold points

## Testing Frequency
- Concrete: 1 compressive strength test per 50m3 or per day's pour
- Steel reinforcement: 1 tensile test per 10 tonnes
- Asphalt: 1 Marshall test per 500m2
- Soil compaction: 1 density test per 250m2 for subgrade, per 500m3 for fill
- Welding: 100% visual, 10% radiographic for critical welds
- Piling: 1 load test per 100 piles, integrity test per 10 piles

## Common Defects and Prevention
- Honeycombing in concrete: Improve vibration, correct mix design
- Cracking: Proper curing, control joints, reinforcement detailing
- Segregation: Reduce drop height, correct mix proportions
- Poor compaction: Correct moisture content, adequate passes
- Reinforcement displacement: Secure spacers, proper tying
- Surface defects: Proper formwork, release agent, curing
"""

# ── 34. Road Construction Methods ─────────────────────────────────
DOCUMENTS["34_road_construction.md"] = """# Road Construction Methods

## Earthworks
- Clearing and grubbing: Remove vegetation, topsoil (150-300mm)
- Cut and fill: Balance earthwork quantities to minimize haulage
- Excavation: In cuts, benched slopes for stability
- Embankment construction: Layer placement, maximum 200mm loose thickness
- Compaction: 95-98% MDD, moisture content OMC ± 2%
- Proof rolling: For subgrade verification before pavement layers

## Subgrade Preparation
- Subgrade formation: Shape to design cross-fall (2.5-3%)
- Subgrade improvement: Lime or cement stabilization for poor soils (CBR < 5%)
- Geotextile separation: Between subgrade and subbase for weak soils
- Drainage layer: 150mm granular layer below subgrade in wet areas
- Subgrade testing: CBR, density, moisture content every 250m

## Pavement Construction
- Subbase: Granular material, 150-300mm thick, compacted in layers
- Base course: Crushed stone or cement-stabilized, 150-250mm thick
- Prime coat: MC-30 cutback bitumen, 0.6-1.0 L/m2 on granular base
- Binder course: Asphalt concrete, 50-100mm thick
- Wearing course: Asphalt concrete, 40-50mm thick
- Tack coat: Between asphalt layers, 0.2-0.4 L/m2 residual bitumen

## Asphalt Paving
- Paver speed: 2-5 m/min for uniform mat
- Rolling temperature: Start at 140-150°C, finish above 110°C
- Breakdown rolling: Vibratory roller, 6-8 passes
- Intermediate rolling: Pneumatic tire roller for densification
- Finish rolling: Tandem roller to remove roller marks
- Joint construction: Hot longitudinal joint, transverse joint treatment

## Rigid Pavement Construction
- Slab thickness: 200-300mm (jointed reinforced concrete)
- Joint spacing: 4-6m for contraction joints, 15-30m for expansion joints
- Dowel bars: At contraction joints for load transfer, 25-32mm diameter
- Tie bars: At longitudinal joints, 12-16mm diameter
- Concrete placing: Slip-form paver or fixed formwork
- Curing: Wet curing or curing compound for minimum 7 days
"""

# ── 35. Temporary Works in Construction ──────────────────────────
DOCUMENTS["35_temporary_works.md"] = """# Temporary Works in Construction

## Types of Temporary Works
- Formwork: For concrete construction (columns, slabs, walls, beams)
- Falsework: Temporary support for structures during construction
- Scaffolding: For access and working platforms
- Shoring: For excavation support and existing structure support
- Cofferdams: For construction in water
- Haul roads: Temporary access routes for construction traffic

## Formwork Design
- Loads: Concrete pressure (self-weight + hydrostatic), live load, wind
- Concrete pressure: P = 23h (kPa) for normal vibration, h = height of pour
- Form materials: Plywood (18mm minimum), timber, steel, or aluminum
- Form ties: Spacing based on concrete pressure, 450-600mm typical
- Release agent: Applied before each pour to prevent sticking
- Stripping time: 24 hours for sides, 7 days for soffits, 14 days for props
- Tolerances: ±3mm for dimensions, ±5mm for alignment

## Scaffolding
- Tube and coupler: Standard system, 48mm diameter tubes
- System scaffold: Cuplock, ringlock, or similar prefabricated systems
- Mobile scaffold: For low-height work, height/width ratio < 3.5
- Loading: Light duty (0.75 kN/m2), general (1.5 kN/m2), heavy (3.0 kN/m2)
- Ties: At every other lift, every 4m horizontally
- Guardrails: Top rail at 1.0m, mid-rail, toe board
- Inspection: Weekly and after adverse weather

## Excavation Support
- Shoring types: Timber, soldier piles + lagging, sheet piles, secant piles
- Depth limits: < 1.2m unsupported in stable soil
- Trench boxes: For utility trenches in confined spaces
- Dewatering: Sumps, wellpoints, deep wells for groundwater control
- Monitoring: Settlement points, inclinometers for adjacent structures
- Backfill: Granular material, compacted in 200mm layers

## Traffic Management
- Temporary traffic control: Signs, cones, barriers, flaggers
- Lane closures: Night work preferred for high-volume roads
- Detours: Signed alternate routes, minimum 2 weeks advance notice
- Pedestrian protection: Segregated walkways, covered where necessary
- Site access: Clearly marked entry/exit points for construction vehicles
- Emergency access: Maintained at all times for emergency vehicles
"""

# Generate all files
print(f"Generating {len(DOCUMENTS)} knowledge documents in {KB}...")
for filename, content in DOCUMENTS.items():
    path = KB / filename
    path.write_text(content.strip())
    print(f"  Created: {filename} ({len(content)} chars)")

print(f"\nDone! Generated {len(DOCUMENTS)} engineering knowledge documents.")
