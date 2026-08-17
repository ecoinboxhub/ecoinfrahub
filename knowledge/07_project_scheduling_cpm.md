# Project Scheduling and CPM

## Project Planning Fundamentals
- Work Breakdown Structure (WBS): Hierarchical decomposition of project work
- Activity definition: Each work package decomposed into individual activities
- Activity sequencing: Logical relationships between activities
- Duration estimation: Historical data, expert judgment, parametric estimation
- Resource allocation: Labor, plant, materials assigned to activities

## Activity Relationships
- Finish-to-start (FS): Most common, predecessor must finish before successor starts
- Start-to-start (SS): Activities can start concurrently with a lag
- Finish-to-finish (FF): Activities must finish together or within a lag
- Start-to-finish (SF): Rare, successor cannot finish until predecessor starts
- Lag time: Waiting period between linked activities
- Lead time: Overlap between activities, negative lag value

## Critical Path Method (CPM)
- Forward pass: Earliest start (ES) and earliest finish (EF) for each activity
- Backward pass: Latest start (LS) and latest finish (LF) for each activity
- Total float: LS - ES or LF - EF, time an activity can slip without delaying project
- Free float: Minimum ES of successors - EF of current activity
- Critical path: Sequence of activities with zero total float, longest path through network
- Near-critical paths: Activities with small float, may become critical during execution
- Float calculation example: Activity duration 5 days, ES=10, EF=15, LS=12, LF=17, Total float=2 days

## Network Diagrams
- Activity-on-node (AON): Nodes represent activities, arrows show dependencies
- Activity-on-arrow (AOA): Arrows represent activities, nodes show events
- Precedence diagramming method (PDM): AON with all relationship types and lags
- Arrow diagramming method (ADM): AOA with dummy activities for proper logic
- Milestone chart: Key deliverables and decision points on timeline

## Duration Estimation Techniques
- Three-point estimation (PERT): Optimistic (O), Most likely (M), Pessimistic (P)
- Expected duration: (O + 4M + P) / 6 using beta distribution
- Standard deviation: (P - O) / 6 for each activity
- Variance: ((P - O) / 6)^2 for calculating project completion probability
- Probability of completion: Z = (Target - Expected) / Project standard deviation
- Parametric estimation: Productivity rates, m3/day for earthworks, m2/day for paving

## Resource Management
- Resource histogram: Daily resource requirements plotted against time
- Resource leveling: Adjust schedule to keep resource usage within limits
- Resource smoothing: Adjust float without extending project duration
- Resource loading: Total quantity of each resource per activity
- Critical chain: Buffer management, feeding buffers protect critical path

## Schedule Compression
- Crashing: Add resources to reduce duration, cost-time trade-off analysis
- Crashing cost slope: (Crash cost - Normal cost) / (Normal duration - Crash duration)
- Fast tracking: Overlap activities normally done sequentially, rework risk
- Overtime: 50-100% productivity for overtime hours, limited duration before fatigue
- Phased construction: Early completion of sections for beneficial use

## Progress Monitoring
- S-curves: Planned vs actual cumulative work (cost, hours, quantities)
- Earned Value Management (EVM): BCWS (planned), BCWP (earned), ACWP (actual)
- Schedule variance: SV = BCWP - BCWS, negative means behind schedule
- Cost variance: CV = BCWP - ACWP, negative means over budget
- Performance indices: SPI = BCWP/BCWS, CPI = BCWP/ACWP
- Look-ahead schedules: 3-6 week rolling window for short-term planning
- Schedule updates: Monthly progress update, logic and duration adjustments

## Software Tools
- Microsoft Project: Gantt charts, resource management, earned value analysis
- Primavera P6: Enterprise level, multi-project, role-based resource allocation
- Open source: ProjectLibre, GanttProject for small to medium projects
- BIM 4D: 3D model linked to schedule for construction sequence visualization
- Excel: Basic scheduling with formulas for small projects
