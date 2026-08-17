# EcoInfraMind AI - Competition Demo Script (ADTC 2026)
# ======================================================
# Run with: powershell -ExecutionPolicy Bypass -File demo.ps1
# Requires: Server running on port 8432, knowledge base indexed
# Time estimate: ~15 minutes for all 10 questions (due to CPU inference speed)

$API = "http://localhost:8432/api/v1"
$PASS = 0
$FAIL = 0
$TIMEOUT_SEC = 180

function Test-Step {
    param($Name, $ScriptBlock)
    Write-Host "`n=== $Name ===" -ForegroundColor Cyan
    try {
        $result = & $ScriptBlock
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "Exit code: $LASTEXITCODE" }
        Write-Host "  PASS" -ForegroundColor Green
        $script:PASS++
    } catch {
        Write-Host "  FAIL: $_" -ForegroundColor Red
        $script:FAIL++
    }
}

# ==========================================
# SECTION 1: SYSTEM VERIFICATION
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  EcoInfraMind AI - ADTC 2026 Demo" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "Started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

Test-Step "1.1 - Server Health Check" {
    $r = Invoke-RestMethod -Uri "$API/health" -TimeoutSec 10
    if ($r.status -ne "ok") { throw "Status: $($r.status)" }
    Write-Host "  Model loaded: $($r.model_loaded)" -ForegroundColor Gray
    Write-Host "  CPU: $($r.cpu_percent)%  RAM: $($r.ram_gb) GB" -ForegroundColor Gray
}

Test-Step "1.2 - Knowledge Base Stats" {
    $r = Invoke-RestMethod -Uri "$API/knowledge/stats" -TimeoutSec 10
    if ($r.total_chunks -eq 0) { throw "Knowledge base empty - run /api/v1/knowledge/index-all first" }
    Write-Host "  Chunks: $($r.total_chunks)" -ForegroundColor Gray
}

Test-Step "1.3 - Available Expert Types" {
    $r = Invoke-RestMethod -Uri "$API/experts" -TimeoutSec 10
    $experts = $r.experts -join ", "
    Write-Host "  $experts" -ForegroundColor Gray
    if ($r.experts.Count -ne 4) { throw "Expected 4 expert types, got $($r.experts.Count)" }
}

Test-Step "1.4 - System Metrics" {
    $r = Invoke-RestMethod -Uri "$API/metrics" -TimeoutSec 10
    Write-Host "  RAM: $($r.ram_gb) GB / $($r.ram_percent)%" -ForegroundColor Gray
    Write-Host "  Cache: $($r.cache_size) entries" -ForegroundColor Gray
    Write-Host "  Knowledge: $($r.knowledge_stats.total_chunks) chunks" -ForegroundColor Gray
}

# ==========================================
# SECTION 2: BENCHMARK QUESTIONS (10)
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  10 Engineering Benchmark Questions" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

$questions = @(
    @{
        id = "Q1 - Pavement Design"
        q = "What is the standard pavement structure for a rural road in Nigeria according to the Nigerian Highway Manual? Describe the typical layers and their thickness."
        check = @("subgrade", "base", "subbase", "wearing", "thickness", "mm")
        min_tokens = 50
    },
    @{
        id = "Q2 - Concrete Mix Design"
        q = "Explain the process of concrete mix design. What are the key factors that determine the proportions of cement, sand, aggregate, and water?"
        check = @("cement", "water", "aggregate", "ratio", "strength")
        min_tokens = 50
    },
    @{
        id = "Q3 - Drainage Design"
        q = "Describe the Rational Method for calculating stormwater runoff. What parameters are needed and how is the peak flow rate determined?"
        check = @("runoff", "coefficient", "intensity", "area", "flow")
        min_tokens = 50
    },
    @{
        id = "Q4 - Bearing Capacity"
        q = "Explain Terzaghi's bearing capacity theory. What are the three components that contribute to the ultimate bearing capacity of a shallow foundation?"
        check = @("cohesion", "friction", "overburden", "bearing", "Terzaghi")
        min_tokens = 40
    },
    @{
        id = "Q5 - Environmental Impact Assessment"
        q = "What are the key steps in conducting an Environmental Impact Assessment (EIA) for a road project in West Africa?"
        check = @("screening", "scoping", "impact", "mitigation", "EIA")
        min_tokens = 60
    },
    @{
        id = "Q6 - Soil Compaction"
        q = "Explain the Proctor compaction test. What is the relationship between moisture content and dry density, and why is it important in road construction?"
        check = @("moisture", "density", "optimum", "compaction", "Proctor")
        min_tokens = 50
    },
    @{
        id = "Q7 - Traffic Engineering"
        q = "How is Annual Average Daily Traffic (AADT) calculated from short-term traffic counts? What adjustment factors are typically applied?"
        check = @("AADT", "factor", "count", "traffic", "adjustment")
        min_tokens = 40
    },
    @{
        id = "Q8 - Climate Adaptation"
        q = "What climate adaptation measures should be considered in the design of road infrastructure in flood-prone areas?"
        check = @("flood", "drainage", "climate", "elevation", "design")
        min_tokens = 50
    },
    @{
        id = "Q9 - Foundation Engineering"
        q = "What are the main types of shallow foundations and how does an engineer select the appropriate type for a given site condition?"
        check = @("strip", "spread", "raft", "soil", "bearing")
        min_tokens = 50
    },
    @{
        id = "Q10 - Construction Quality Assurance"
        q = "Describe the key quality control tests required during road construction, including tests for materials, compaction, and pavement layers."
        check = @("compaction", "test", "density", "quality", "material")
        min_tokens = 50
    }
)

foreach ($q in $questions) {
    $body = @{ message = $q.q; history = @() } | ConvertTo-Json
    $response = $null
    $elapsed = 0
    try {
        $t0 = [DateTime]::UtcNow
        $response = Invoke-RestMethod -Uri "$API/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec $TIMEOUT_SEC
        $elapsed = ([DateTime]::UtcNow - $t0).TotalSeconds
    } catch {
        Write-Host "  FAIL ($($q.id)): HTTP/network error - $_" -ForegroundColor Red
        $script:FAIL++
        continue
    }

    $text = $response.response
    $tokens = $response.tokens
    $tps = if ($tokens -gt 0 -and $elapsed -gt 0) { "{0:N1}" -f ($tokens / $elapsed) } else { "?" }

    $checks = $q.check | ForEach-Object { if ($text -match [regex]::Escape($_)) { 1 } else { 0 } }
    $checkCount = ($checks | Measure-Object -Sum).Sum
    $totalChecks = $q.check.Count
    $lengthOk = ($tokens -ge $q.min_tokens)

    if ($checkCount -ge ($totalChecks * 0.6) -and $lengthOk) {
        $pct = "{0:N0}" -f ($checkCount / $totalChecks * 100)
        Write-Host "  PASS ($($q.id)): $tokens tokens in $("{0:N1}" -f $elapsed)s ($tps tok/s) - $pct% keywords" -ForegroundColor Green
        $script:PASS++
    } else {
        Write-Host "  FAIL ($($q.id)): tokens=$tokens ($("{0:N1}" -f $elapsed)s) keywords=$checkCount/$totalChecks min_tokens=$($q.min_tokens)" -ForegroundColor Red
        Write-Host "    Partial response: $($text.Substring(0, [Math]::Min(200, $text.Length)))" -ForegroundColor Gray
        $script:FAIL++
    }
}

# ==========================================
# SECTION 3: CALCULATOR TESTS
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  Calculator Tests" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

$calculatorTests = @(
    @{ name = "Concrete Mix"; endpoint = "concrete_mix"; params = @{cement=350; sand=700; aggregate=1400; water=175}; check = "ratio" }
    @{ name = "Pavement Thickness"; endpoint = "pavement_thickness"; params = @{cbr=15; traffic_esa=5000000; reliability=90}; check = "thickness" }
    @{ name = "Drainage Flow"; endpoint = "drainage"; params = @{area_ha=50; runoff_coefficient=0.6; rainfall_intensity_mm_hr=50}; check = "flow" }
    @{ name = "Bearing Capacity"; endpoint = "bearing_capacity"; params = @{cohesion=25; unit_weight=18; phi_deg=30; width=1.5; depth=1.0; safety_factor=3.0}; check = "capacity" }
    @{ name = "Earthwork Volume"; endpoint = "earthwork"; params = @{length=100; width=8; depth=0.5; swell_factor=1.25}; check = "volume" }
)

foreach ($ct in $calculatorTests) {
    Test-Step "3.0 - $($ct.name)" {
        $body = @{ calculator = $ct.endpoint; params = $ct.params } | ConvertTo-Json
        $r = Invoke-RestMethod -Uri "$API/calculator" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 15
        $resultStr = ($r.result | ConvertTo-Json -Compress)
        if ($resultStr -match $ct.check) {
            Write-Host "  Result: $resultStr" -ForegroundColor Gray
        } else {
            throw "Result missing expected key '$($ct.check)': $resultStr"
        }
    }
}

# ==========================================
# SECTION 4: EXPERT MODE TEST
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  Expert Assistant Mode Test" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

Test-Step "4.0 - Expert Mode (proposal)" {
    $body = @{
        message = "Generate a method statement outline for road pavement construction"
        expert_type = "proposal"
        history = @()
    } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "$API/expert" -Method Post -Body $body -ContentType "application/json" -TimeoutSec $TIMEOUT_SEC
    if ($r.response.Length -lt 100) { throw "Response too short: $($r.response.Length) chars" }
    if ($r.expert_type -ne "proposal") { throw "Wrong expert type: $($r.expert_type)" }
    Write-Host "  Expert: $($r.expert_type), Tokens: $($r.tokens), Time: $($r.response_time_s)s" -ForegroundColor Gray
    Write-Host "  Excerpt: $($r.response.Substring(0, [Math]::Min(150, $r.response.Length)))" -ForegroundColor Gray
}

# ==========================================
# SECTION 5: CACHE TEST
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  Cache Hit Test" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

Test-Step "5.0 - Repeated query cache (should be faster)" {
    $body = @{ message = "What is pavement thickness?"; history = @() } | ConvertTo-Json
    $t0 = [DateTime]::UtcNow
    $r1 = Invoke-RestMethod -Uri "$API/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec $TIMEOUT_SEC
    $t1 = ([DateTime]::UtcNow - $t0).TotalSeconds

    $t0 = [DateTime]::UtcNow
    $r2 = Invoke-RestMethod -Uri "$API/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 30
    $t2 = ([DateTime]::UtcNow - $t0).TotalSeconds

    Write-Host "  First: $("{0:N1}" -f $t1)s, Cached: $("{0:N2}" -f $t2)s" -ForegroundColor Gray
    if ($t2 -gt $t1 * 0.5) {
        Write-Host "  (Cache may not have been populated yet)" -ForegroundColor Yellow
    }
}

# ==========================================
# SUMMARY
# ==========================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "  Demo Complete" -ForegroundColor Yellow
Write-Host "  Completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Yellow
$total = $PASS + $FAIL
if ($FAIL -eq 0) {
    Write-Host "  RESULT: ALL $PASS / $total TESTS PASSED" -ForegroundColor Green
} else {
    Write-Host "  RESULT: $PASS PASSED, $FAIL FAILED (out of $total)" -ForegroundColor Red
    exit 1
}
