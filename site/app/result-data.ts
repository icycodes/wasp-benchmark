// pochi + gemini 3 flash
import resultData0308 from "@/jobs/2026-03-08__16-54-33/result.json"
// builtin + codex
import resultData0309_1 from "@/jobs/2026-03-09__10-20-21/result.json"
// pochi + glm
import resultData0309_2 from "@/jobs/2026-03-09__12-08-37/result.json"
// pochi + glm-flash
import resultData0310 from "@/jobs/2026-03-10__13-59-33/result.json"

export default {
  startedAt: resultData0310.started_at,
  evals: {
    ...resultData0308.stats.evals,
    ...resultData0309_1.stats.evals,
    ...resultData0309_2.stats.evals,
    ...resultData0310.stats.evals,
  }
}
