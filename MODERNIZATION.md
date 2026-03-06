# LDAR-Sim Modernization

Integrates LDAR-Sim into the EIP NX monorepo as a browser-based feature: configure simulations with sensible defaults, submit async jobs, and explore results in an interactive dashboard.

**Guiding constraint:** the existing Python simulation code is untouched — everything wraps it.

---

## What I Changed

### LDAR-Sim repo — new files only

```
LDAR_Sim/worker/
├── worker_main.py        SQS long-poll loop with graceful SIGTERM shutdown
├── job_handler.py        Full job lifecycle orchestrator (S3 → YAML → simulate → POST)
├── config_generator.py   Converts stored JSON config into 4 YAML files for ldar_sim_main.py
├── result_parser.py      Parses timeseries/leaks/sites CSVs into structured dicts
├── s3_client.py          Downloads input files (facilities CSV, weather NetCDF) from S3
├── api_client.py         POSTs results and status updates to the NestJS internal API
├── requirements.txt      boto3, requests, pyyaml, pandas
└── Dockerfile            Containerised worker image
```

No existing simulation files were modified.

---

### Monorepo — new files

**Database schema** (`libs/db/src/schema/ldar-sim.ts`)

Five new Drizzle/PostgreSQL tables:

| Table | Purpose |
|---|---|
| `ldar_sim_config` | Stores the full 4-level config as JSONB, scoped to a Clerk org |
| `ldar_sim_run` | Job record with status (`pending → running → completed → failed`) |
| `ldar_sim_timeseries` | Daily timeseries rows per program per simulation index |
| `ldar_sim_leaks` | One row per leak per program per simulation index |
| `ldar_sim_sites` | One row per site per program per simulation index |

**Migration** (`libs/db/src/migration/20260218172558_add_ldar_sim.sql`)

Generated automatically by `pnpm drizzle-kit generate`. Creates all five tables with foreign-key constraints and indexes.

**Shared models** (`libs/models/src/ldar-sim.ts`)

- Zod schemas for the full 4-level config tree (simulation settings, virtual world, programs, methods)
- `LdarSimConfigDefaults` — hardcoded defaults sourced from `src/default_parameters/*.yml`
- `LdarSimRunStatus` enum (`pending | running | completed | failed`)
- Request/response types for every API endpoint
- `LdarSimJobMessage` schema for the SQS payload

**NestJS module** (`apps/api-nest/src/app/modules/ldar-sim/`)

| File | Purpose |
|---|---|
| `ldar-sim.module.ts` | Module definition; imports `ClerkModule`, `DrizzleModule`, and `PrimaryCollectionModule` |
| `ldar-sim.controller.ts` | 16 REST endpoints with `AuthGuard` + `PermissionGuard` + `AuthInterceptor` |
| `ldar-sim.service.ts` | Business logic; SQS submission stubbed with logger (TODO comment) |
| `ldar-sim.repository.ts` | All Drizzle queries — no raw SQL |

**Next.js pages** (`apps/eip-next/src/app/(app)/ldar-sim/`)

| Route | Page |
|---|---|
| `/ldar-sim` | Dashboard — run counts, recent runs list |
| `/ldar-sim/configs` | Saved configs list with Run / Edit / Delete per card |
| `/ldar-sim/configs/new` | 4-step config wizard pre-populated from `LdarSimConfigDefaults` |
| `/ldar-sim/configs/[id]/edit` | Same wizard, seeded with stored config |
| `/ldar-sim/runs` | All runs with status badges |
| `/ldar-sim/runs/[id]` | Run detail: status banner + results dashboard |

The results dashboard (`RunResultsDashboard`) is a client component that:
- Auto-polls the API every 5 s while the run is `pending` or `running`
- Renders a daily-emissions line chart and an active-leaks line chart (Recharts via `@eip-mono/ui`)
- Shows a paginated leak analysis table

The config wizard Step 2 (**Virtual World**) connects to the primary site database:
- Loads filter options (assets, basins, operators) from `GET /ldar-sim/site-filter-options` on mount
- Scrollable checkbox lists let the user narrow down which sites to include
- Optional year filter restricts to sites active during a given year (via `acquiredAt`/`decommissionedAt`)
- **Prepare Facilities** button calls `POST /ldar-sim/prepare-facilities` → generates the CSV in-memory and uploads it to S3; stores the returned key as `infrastructure_file` in the config
- Weather file selector auto-populates from `GET /ldar-sim/weather-files` (falls back to a manual text input when no files are present in S3)

---

### Monorepo — modified files

| File | Change |
|---|---|
| `libs/db/src/schema/index.ts` | Added `export * from './ldar-sim'` |
| `libs/models/src/index.ts` | Added `export * from './ldar-sim'` |
| `apps/api-nest/src/app/app.module.ts` | Added `LdarSimModule` to the imports array |

---

## API Endpoints

All endpoints are prefixed `/api/ldar-sim` and require a valid Clerk session.

| Method | Path | Description |
|---|---|---|
| `POST` | `/configs` | Save a configuration |
| `GET` | `/configs` | List configs for the authenticated org |
| `GET` | `/configs/:id` | Get a single config |
| `PUT` | `/configs/:id` | Update a config |
| `DELETE` | `/configs/:id` | Delete a config |
| `POST` | `/runs` | Submit a simulation job |
| `GET` | `/runs` | List runs for the org |
| `GET` | `/runs/:id` | Run status + metadata |
| `GET` | `/runs/:id/timeseries` | Paginated timeseries rows (`?limit=&offset=`) |
| `GET` | `/runs/:id/sites` | Site-level results |
| `GET` | `/runs/:id/leaks` | Leak-level results |
| `POST` | `/runs/:id/results` | **Internal** — worker posts parsed results here |
| `GET` | `/upload-url` | S3 pre-signed upload URL (`?filename=`) |
| `POST` | `/prepare-facilities` | Filter sites from primary DB → generate CSV → upload to S3 |
| `GET` | `/weather-files` | List `.nc` files available in S3 under `ldar-sim/weather/` |
| `GET` | `/site-filter-options` | Distinct asset / basin / operator values for the org's collection |

### `POST /prepare-facilities` body

```json
{
  "filters": {
    "assets":      ["Permian Basin"],
    "basins":      ["Delaware"],
    "operators":   ["Operator A"],
    "siteGroups":  [],
    "year":        2022,
    "operatedOnly": true
  },
  "defaults": {
    "subtypeCode":      999,
    "equipmentGroups":  1
  }
}
```

All filter arrays are optional — omit them (or send an empty array) to include all values.
`operatedOnly` defaults to `true`. `year` filters by `acquiredAt ≤ year-end` AND (`decommissionedAt IS NULL` OR `decommissionedAt ≥ year-start`).

Response: `{ "s3Key": "ldar-sim/org_xxx/facilities/uuid.csv", "siteCount": 412 }`

The returned `s3Key` is stored as `virtual_world.infrastructure_file` in the config.

---

## Worker Job Flow

```
SQS message { runId, configId, orgId, config }
        │
        ▼
PATCH  /runs/:id/status  →  running
        │
        ▼
Download  s3://<bucket>/<infrastructure_key>  →  /tmp/.../inputs/facilities.csv
Download  s3://<bucket>/<weather_key>         →  /tmp/.../inputs/weather.nc
        │
        ▼
config_generator.py  →  /tmp/.../params/{simulation_settings,virtual_world,P_*.yaml,M_*.yaml}
        │
        ▼
python ldar_sim_main.py --in_dir /tmp/.../params --out_dir /tmp/.../outputs
        │
        ▼
result_parser.py  →  parse timeseries/leaks/sites CSVs
        │
        ▼
POST  /runs/:id/results  →  NestJS writes to DB, marks run completed
        │
        ▼
shutil.rmtree( /tmp/... )
```

On any exception the worker PATCHes the run to `failed` with the error message truncated to 1000 chars, then re-raises so the SQS message remains invisible until its visibility timeout expires (default 2 h, configurable via `LDAR_SIM_VISIBILITY_TIMEOUT`).

---

## Worker Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LDAR_SIM_QUEUE_URL` | yes | — | SQS queue URL |
| `LDAR_SIM_S3_BUCKET` | yes | — | S3 bucket containing input files |
| `LDAR_SIM_API_BASE_URL` | yes | `http://localhost:3999` | NestJS API base URL |
| `LDAR_SIM_INTERNAL_TOKEN` | yes | — | Bearer token for the internal results endpoint |
| `AWS_REGION` | no | `us-east-1` | AWS region |
| `LDAR_SIM_POLL_WAIT_SECONDS` | no | `20` | SQS long-poll wait time |
| `LDAR_SIM_MAX_MESSAGES` | no | `1` | Messages per poll (keep at 1; simulations are CPU-heavy) |
| `LDAR_SIM_VISIBILITY_TIMEOUT` | no | `7200` | Seconds a message stays invisible while processing |

---

## How to Test

### 1 — TypeScript compilation (instant, no services needed)

```bash
cd /home/ian/highwood/mono

pnpm nx run models:build
pnpm nx run db:build
pnpm nx run api-nest:build
```

A clean build means all types, imports, and Zod schemas are consistent.

---

### 2 — Python worker unit tests (no AWS, no DB needed)

Create the test directory and files:

```bash
mkdir -p /home/ian/highwood/LDAR_Sim/worker/tests
```

**`worker/tests/test_config_generator.py`**

```python
import os, sys, tempfile, yaml
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config_generator import generate_yaml_files

CONFIG = {
    "simulation_settings": {
        "n_simulations": 1, "n_processes": 1,
        "start_date": [2017, 1, 1], "end_date": [2021, 12, 31],
        "pregenerate_leaks": True, "preseed_random": True,
        "outputs": {"leaks": True, "sites": True, "timeseries": True},
    },
    "virtual_world": {
        "infrastructure_file": "facilities_Perm.csv",
        "weather_file": "ERA5_2017_2019_Perm.nc",
        "weather_is_hourly": True, "NRd": 365,
        "emissions": {
            "LPR": 0.013, "max_leak_rate": 100000,
            "leak_dist_params": [-1.79, 2.17], "consider_venting": False,
        },
    },
    "programs": [{"program_name": "P_OGI", "method_labels": ["OGI"], "economics": {}}],
    "methods": [{
        "label": "OGI", "deployment_type": "mobile",
        "measurement_scale": "component",
        "sensor": {"type": "OGI_camera_zim", "MDL": [0.24, 0.39]},
        "cost": {"per_day": 0, "per_site": 500},
        "is_follow_up": False, "RS": 4, "time": 120,
    }],
}

with tempfile.TemporaryDirectory() as tmp:
    generate_yaml_files(CONFIG, tmp, "/inputs", "/outputs",
                        "facilities_Perm.csv", "ERA5_2017_2019_Perm.nc")

    files = os.listdir(tmp)
    assert "simulation_settings.yaml" in files, "Missing simulation_settings.yaml"
    assert "virtual_world.yaml" in files,       "Missing virtual_world.yaml"
    assert "P_OGI.yaml" in files,               "Missing P_OGI.yaml"
    assert "M_OGI.yaml" in files,               "Missing M_OGI.yaml"

    ss = yaml.safe_load(open(f"{tmp}/simulation_settings.yaml"))
    assert ss["parameter_level"] == "simulation_settings"
    assert ss["n_simulations"] == 1
    assert ss["start_date"] == [2017, 1, 1]

    vw = yaml.safe_load(open(f"{tmp}/virtual_world.yaml"))
    assert vw["parameter_level"] == "virtual_world"
    assert vw["emissions"]["LPR"] == 0.013

    prog = yaml.safe_load(open(f"{tmp}/P_OGI.yaml"))
    assert prog["program_name"] == "P_OGI"
    assert "OGI" in prog["method_labels"]

    meth = yaml.safe_load(open(f"{tmp}/M_OGI.yaml"))
    assert meth["label"] == "OGI"
    assert meth["sensor"]["type"] == "OGI_camera_zim"

print("config_generator: PASS")
```

**`worker/tests/test_result_parser.py`**

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from result_parser import parse_all_results

EXPECTED_OUT = (
    "/home/ian/highwood/LDAR_Sim/LDAR_Sim/testing/end_to_end_testing"
    "/test_suite/basic_test_LPRx2/expected_outputs"
)

results = parse_all_results(EXPECTED_OUT)

assert len(results["timeseries"]) > 0, "No timeseries rows parsed"
assert len(results["leaks"]) > 0,      "No leak rows parsed"
assert len(results["sites"]) > 0,      "No site rows parsed"

ts = results["timeseries"][0]
for key in ("programName", "simIndex", "date", "dailyEmissionsKg", "activeLeaks"):
    assert key in ts, f"Missing key: {key}"

leak = results["leaks"][0]
assert leak["rateGs"] is None or isinstance(leak["rateGs"], float)
assert leak["programName"] == "P_OGI"

print(
    f"result_parser: PASS  "
    f"({len(results['timeseries'])} timeseries, "
    f"{len(results['leaks'])} leaks, "
    f"{len(results['sites'])} sites)"
)
```

Run them:

```bash
cd /home/ian/highwood/LDAR_Sim
pip install pyyaml pandas

python worker/tests/test_config_generator.py
python worker/tests/test_result_parser.py
```

---

### 3 — NestJS service unit test

Create the spec file:

**`apps/api-nest/src/app/modules/ldar-sim/ldar-sim.service.spec.ts`**

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { ConfigService } from '@nestjs/config';
import { NotFoundException } from '@nestjs/common';
import { LdarSimService } from './ldar-sim.service';
import { LdarSimRepository } from './ldar-sim.repository';

const mockRepo = {
  createConfig: jest.fn(),
  listConfigs: jest.fn(),
  getConfig: jest.fn(),
  updateConfig: jest.fn(),
  deleteConfig: jest.fn(),
  createRun: jest.fn(),
  listRuns: jest.fn(),
  getRun: jest.fn(),
  getRunById: jest.fn(),
  updateRunStatus: jest.fn(),
  insertResults: jest.fn(),
  getTimeseries: jest.fn(),
  getSites: jest.fn(),
  getLeaks: jest.fn(),
};

describe('LdarSimService', () => {
  let service: LdarSimService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        LdarSimService,
        { provide: LdarSimRepository, useValue: mockRepo },
        { provide: ConfigService, useValue: { get: jest.fn() } },
      ],
    }).compile();
    service = module.get(LdarSimService);
    jest.clearAllMocks();
  });

  it('createConfig delegates to repository', async () => {
    const body = { name: 'Test', config: {} as any };
    mockRepo.createConfig.mockResolvedValue({ id: 1, ...body });
    const result = await service.createConfig('org_1', body);
    expect(mockRepo.createConfig).toHaveBeenCalledWith('org_1', body);
    expect(result.id).toBe(1);
  });

  it('getConfig throws NotFoundException when missing', async () => {
    mockRepo.getConfig.mockResolvedValue(null);
    await expect(service.getConfig('org_1', 99)).rejects.toThrow(NotFoundException);
  });

  it('createRun throws NotFoundException when config not found', async () => {
    mockRepo.getConfig.mockResolvedValue(null);
    await expect(service.createRun('org_1', { configId: 42 })).rejects.toThrow(NotFoundException);
  });

  it('createRun creates run and logs SQS payload', async () => {
    mockRepo.getConfig.mockResolvedValue({ id: 1, config: {}, orgId: 'org_1' });
    mockRepo.createRun.mockResolvedValue({ id: 5, configId: 1, status: 'pending' });
    const result = await service.createRun('org_1', { configId: 1 });
    expect(mockRepo.createRun).toHaveBeenCalledWith('org_1', 1);
    expect(result.id).toBe(5);
    expect(result.status).toBe('pending');
  });

  it('ingestResults inserts data and marks run completed', async () => {
    mockRepo.getRunById.mockResolvedValue({ id: 3, status: 'running' });
    mockRepo.insertResults.mockResolvedValue(undefined);
    mockRepo.updateRunStatus.mockResolvedValue({ id: 3, status: 'completed' });
    await service.ingestResults(3, { timeseries: [], leaks: [], sites: [] });
    expect(mockRepo.insertResults).toHaveBeenCalledWith(3, expect.any(Object));
    expect(mockRepo.updateRunStatus).toHaveBeenCalledWith(
      3, 'completed', expect.objectContaining({ completedAt: expect.any(String) })
    );
  });
});
```

Run it:

```bash
cd /home/ian/highwood/mono
pnpm nx run api-nest:test --testPathPattern=ldar-sim.service.spec
```

---

### 4 — Update the service unit test mock

The `LdarSimService` now requires `PrimaryCollectionService` as a third constructor argument. Update the `providers` array in `ldar-sim.service.spec.ts`:

```typescript
{ provide: PrimaryCollectionService,
  useValue: { findByClerkId: jest.fn().mockResolvedValue({ collectionId: 1 }) } },
```

Add `PrimaryCollectionService` to the imports at the top of the spec file:

```typescript
import { PrimaryCollectionService } from '../primary/collection/collection.service';
```

---

### 5 — Apply the migration and test the API manually

```bash
# Start the database (if not already running)
cd /home/ian/highwood/mono
docker compose up db -d

# Apply the new migration
pnpm drizzle-kit migrate

# Start the API
pnpm nx run api-nest:serve
```

Then in another terminal, grab a Clerk JWT (from browser dev tools on any authenticated page, or from `.env`'s `API_TEST_USER_TOKEN`) and:

```bash
TOKEN="your-clerk-jwt"
BASE="http://localhost:3999/api"

# 1. Create a config
curl -s -X POST $BASE/ldar-sim/configs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick test",
    "config": {
      "simulation_settings": {
        "n_simulations": 1, "n_processes": 1,
        "start_date": [2017,1,1], "end_date": [2019,12,31],
        "pregenerate_leaks": false, "preseed_random": false,
        "outputs": {"leaks": true, "sites": true, "timeseries": true}
      },
      "virtual_world": {
        "infrastructure_file": "facilities_Perm.csv",
        "weather_file": "ERA5_2017_2019_Perm.nc",
        "weather_is_hourly": true, "NRd": 365,
        "emissions": {"LPR": 0.013, "max_leak_rate": 100000,
                      "leak_dist_params": [-1.79, 2.17], "consider_venting": false}
      },
      "programs": [{"program_name":"P_OGI","method_labels":["OGI"],"economics":{}}],
      "methods": [{
        "label":"OGI","deployment_type":"mobile","measurement_scale":"component",
        "sensor":{"type":"OGI_camera_zim","MDL":[0.24,0.39]},
        "cost":{"per_day":0,"per_site":500},
        "is_follow_up":false,"RS":4,"time":120
      }]
    }
  }' | jq .

# 2. List configs
curl -s $BASE/ldar-sim/configs -H "Authorization: Bearer $TOKEN" | jq .

# 3. Submit a run (replace 1 with the id returned above)
curl -s -X POST $BASE/ldar-sim/runs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"configId": 1}' | jq .

# 4. Check run status
curl -s $BASE/ldar-sim/runs/1 -H "Authorization: Bearer $TOKEN" | jq .

# 5. Simulate the worker posting results back
curl -s -X POST $BASE/ldar-sim/runs/1/results \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timeseries": [{"programName":"P_OGI","simIndex":0,"date":"2017-01-01",
                    "activeLeaks":10,"newLeaks":2,"nTags":1,
                    "dailyEmissionsKg":500.0,"totalDailyCost":1500.0,
                    "repairCost":0.0,"methodCost":1500.0}],
    "leaks": [{"programName":"P_OGI","simIndex":0,"leakId":"leak_001",
               "facilityId":"fac_001","rateGs":0.05,"volumeKg":12.3,
               "status":"repaired","daysActive":45,"dateBegan":"2017-01-01",
               "dateTagged":"2017-02-01","dateRepaired":"2017-02-15",
               "taggedByMethod":"OGI"}],
    "sites": [{"programName":"P_OGI","simIndex":0,"facilityId":"fac_001",
               "lat":32.0,"lon":-102.0,"totalEmissionsKg":1234.5,
               "activeLeakCount":2,"repairedLeakCount":5,"surveysConducted":3}]
  }' | jq .

# 6. Verify results were stored
curl -s "$BASE/ldar-sim/runs/1/timeseries" -H "Authorization: Bearer $TOKEN" | jq .
curl -s "$BASE/ldar-sim/runs/1/leaks"      -H "Authorization: Bearer $TOKEN" | jq .
curl -s "$BASE/ldar-sim/runs/1/sites"      -H "Authorization: Bearer $TOKEN" | jq .
```

The run status should flip to `completed` after step 5, and steps 6–8 should return the rows you posted.

**Test the facilities-from-DB endpoints** (requires the org to have a primary collection with site data):

```bash
# Check what filter options are available
curl -s "$BASE/ldar-sim/site-filter-options" \
  -H "Authorization: Bearer $TOKEN" | jq .

# List weather files in S3
curl -s "$BASE/ldar-sim/weather-files" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Prepare a facilities CSV from the primary DB
curl -s -X POST "$BASE/ldar-sim/prepare-facilities" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": { "operatedOnly": true },
    "defaults": { "subtypeCode": 999, "equipmentGroups": 1 }
  }' | jq .
# → { "s3Key": "ldar-sim/org_xxx/facilities/uuid.csv", "siteCount": N }
```

Use the returned `s3Key` as `virtual_world.infrastructure_file` when creating a config.

---

### 5 — End-to-end worker test (no SQS, no S3)

Invoke `job_handler.py` directly using the existing test simulation data:

```bash
cd /home/ian/highwood/LDAR_Sim
pip install -r worker/requirements.txt

# Make sure the API is running (step 4 above) and a run with id=1 exists
export LDAR_SIM_API_BASE_URL=http://localhost:3999/api
export LDAR_SIM_INTERNAL_TOKEN=$TOKEN
export LDAR_SIM_S3_BUCKET=   # empty = skip S3 download

python - << 'EOF'
import sys, os, shutil, tempfile
sys.path.insert(0, 'worker')
sys.path.insert(0, 'LDAR_Sim/src')
sys.path.insert(0, 'LDAR_Sim/external_sensors')

# Patch job_handler to copy test input files instead of downloading from S3
import s3_client
TEST_INPUTS = "LDAR_Sim/testing/end_to_end_testing/test_suite/basic_test_LPRx2/inputs"

def fake_download(bucket, infrastructure_key, weather_key, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    for fname in os.listdir(TEST_INPUTS):
        if fname.endswith('.csv') or fname.endswith('.nc'):
            shutil.copy(os.path.join(TEST_INPUTS, fname),
                        os.path.join(dest_dir, fname))
    return {
        "infrastructure_file": os.path.join(dest_dir, "facilities_Perm.csv"),
        "weather_file":        os.path.join(dest_dir, "ERA5_2017_2019_Perm.nc"),
    }

s3_client.download_input_files = fake_download

from job_handler import handle_job

handle_job({
    "runId": 1,
    "configId": 1,
    "orgId": "org_test",
    "config": {
        "simulation_settings": {
            "n_simulations": 1, "n_processes": 1,
            "start_date": [2017, 1, 1], "end_date": [2019, 12, 31],
            "pregenerate_leaks": True, "preseed_random": True,
            "outputs": {"leaks": True, "sites": True, "timeseries": True},
        },
        "virtual_world": {
            "infrastructure_file": "facilities_Perm.csv",
            "weather_file": "ERA5_2017_2019_Perm.nc",
            "weather_is_hourly": True, "NRd": 365,
            "emissions": {
                "LPR": 0.013, "max_leak_rate": 100000,
                "leak_dist_params": [-1.79, 2.17], "consider_venting": False,
            },
        },
        "programs": [{"program_name": "P_OGI", "method_labels": ["OGI"], "economics": {}}],
        "methods": [{
            "label": "OGI", "deployment_type": "mobile",
            "measurement_scale": "component",
            "sensor": {"type": "OGI_camera_zim", "MDL": [0.24, 0.39]},
            "cost": {"per_day": 0, "per_site": 500},
            "is_follow_up": False, "RS": 4, "time": 120,
        }],
    },
})
print("job_handler: PASS — check /ldar-sim/runs/1/timeseries for results")
EOF
```

After this completes, hitting `GET /api/ldar-sim/runs/1/timeseries` should return real simulation rows.

---

### Quick-start order

| # | Command | Checks |
|---|---------|--------|
| 1 | `pnpm nx run models:build && pnpm nx run api-nest:build` | Types compile |
| 2 | `python worker/tests/test_config_generator.py` | YAML generation |
| 3 | `python worker/tests/test_result_parser.py` | CSV parsing against real fixtures |
| 4 | `pnpm nx run api-nest:test --testPathPattern=ldar-sim.service.spec` | Service logic |
| 5 | `docker compose up db -d && pnpm drizzle-kit migrate` | Schema applies cleanly |
| 6 | `curl` scripts above | REST endpoints end-to-end + facilities/weather endpoints |
| 7 | `python` job_handler script above | Full simulation → results pipeline |
