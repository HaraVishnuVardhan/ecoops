import { useState } from "react";
import "./App.css";

function App() {
  const [page, setPage] = useState("overview");

  const [metric, setMetric] = useState("energy");
  const [location, setLocation] = useState("Academic Block A");
  const [currentValue, setCurrentValue] = useState(12500);
  const [baselineValue, setBaselineValue] = useState(10870);

  const [eventToday, setEventToday] = useState(false);
  const [sensorRecentlyReplaced, setSensorRecentlyReplaced] =
    useState(false);

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // --------------------------------------------------
  // ANALYZE ANOMALY
  // --------------------------------------------------

  const analyzeAnomaly = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8080/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            metric,
            location,
            current_value: Number(currentValue),
            baseline_value: Number(baselineValue),
            timestamp: new Date().toISOString(),
            event_today: eventToday,
            sensor_recently_replaced: sensorRecentlyReplaced,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();

      setResult(data);

      setHistory((previous) => [
        {
          id: Date.now(),
          location: data.location,
          metric: data.metric,
          change: data.change_percent,
          severity: data.severity,
          confidence: data.confidence,
          decision: data.decision,
        },
        ...previous,
      ]);

      setPage("analyze");
    } catch (err) {
      setError(
        "Could not connect to EcoOps backend. Make sure FastAPI is running on port 8080."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // LOAD DEMO SCENARIO
  // --------------------------------------------------

  const loadScenario = (scenario) => {
    setResult(null);
    setError("");

    if (scenario === "academic") {
      setMetric("energy");
      setLocation("Academic Block A");
      setCurrentValue(12500);
      setBaselineValue(10870);
      setEventToday(false);
      setSensorRecentlyReplaced(false);
    }

    if (scenario === "hostel") {
      setMetric("water");
      setLocation("Hostel C");
      setCurrentValue(15000);
      setBaselineValue(11100);
      setEventToday(true);
      setSensorRecentlyReplaced(false);
    }

    if (scenario === "chemistry") {
      setMetric("energy");
      setLocation("Chemistry Lab");
      setCurrentValue(28000);
      setBaselineValue(5800);
      setEventToday(false);
      setSensorRecentlyReplaced(false);
    }

    setPage("analyze");
  };

  const confidencePercent = result
    ? Math.round(result.confidence * 100)
    : 0;

  const escalatedCount = history.filter(
    (item) => item.decision === "ESCALATE"
  ).length;

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="sidebar-brand">

          <div className="brand-mark">E</div>

          <div>
            <div className="brand">
              ECOOPS <span>2.0</span>
            </div>

            <div className="brand-subtitle">
              CAMPUS INTELLIGENCE
            </div>
          </div>

        </div>


        <nav className="navigation">

          <button
            className={
              page === "overview"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setPage("overview")}
          >
            <span>⌂</span>
            Overview
          </button>


          <button
            className={
              page === "analyze"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setPage("analyze")}
          >
            <span>⌁</span>
            Analyze
          </button>


          <button
            className={
              page === "alerts"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setPage("alerts")}
          >
            <span>⚠</span>
            Alerts

            {escalatedCount > 0 && (
              <span className="alert-count">
                {escalatedCount}
              </span>
            )}
          </button>


          <button
            className={
              page === "audit"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setPage("audit")}
          >
            <span>≡</span>
            Audit Trail
          </button>

        </nav>


        <div className="sidebar-bottom">

          <div className="architecture-mini">

            <div className="mini-title">
              SYSTEM STACK
            </div>

            <div>● LangGraph</div>
            <div>● MCP Tools</div>
            <div>● Policy RAG</div>
            <div>● Safety Router</div>

          </div>


          <div className="human-loop">

            <span className="status-dot"></span>

            HUMAN-IN-THE-LOOP

          </div>

        </div>

      </aside>


      {/* ================= MAIN AREA ================= */}

      <div className="main-area">

        {/* TOP BAR */}

        <header className="topbar">

          <div>

            <div className="page-label">
              {page.toUpperCase()}
            </div>

            <div className="page-description">
              Confidence-aware sustainability intelligence
            </div>

          </div>


          <div className="system-status">

            <span className="status-dot"></span>

            SYSTEM OPERATIONAL

          </div>

        </header>


        {/* =====================================================
            OVERVIEW
        ===================================================== */}

        {page === "overview" && (

          <main className="content">

            <section className="welcome">

              <div>

                <p className="eyebrow">
                  CAMPUS INTELLIGENCE
                </p>

                <h1>
                  See the anomaly.
                  <br />
                  Understand the uncertainty.
                </h1>

                <p>
                  EcoOps detects abnormal resource consumption,
                  grounds decisions in policy, and knows when
                  human intervention is required.
                </p>

              </div>


              <button
                className="primary-button"
                onClick={() => setPage("analyze")}
              >
                START ANALYSIS →
              </button>

            </section>


            {/* CAMPUS METRICS */}

            <section className="overview-grid">

              <div className="overview-card">

                <span>ENERGY</span>

                <strong>12.5k</strong>

                <small>
                  kWh · Academic Block A
                </small>

                <div className="metric-change">
                  +15.0%
                </div>

              </div>


              <div className="overview-card">

                <span>WATER</span>

                <strong>15.0k</strong>

                <small>
                  L · Hostel C
                </small>

                <div className="metric-change warning">
                  +35.1%
                </div>

              </div>


              <div className="overview-card">

                <span>ESCALATED ALERTS</span>

                <strong>
                  {escalatedCount}
                </strong>

                <small>
                  Require human investigation
                </small>

                <div className="metric-change danger">
                  SAFETY
                </div>

              </div>

            </section>


            {/* DEMO SCENARIOS */}

            <section className="dashboard-panel">

              <div className="panel-header">

                <div>

                  <p className="eyebrow">
                    DEMO SCENARIOS
                  </p>

                  <h2>
                    Campus Resource Intelligence
                  </h2>

                </div>


                <span className="live-pill">
                  ● LIVE ENGINE
                </span>

              </div>


              <div className="scenario-list">

                <Scenario
                  location="Academic Block A"
                  metric="Energy"
                  change="+15.0%"
                  severity="LOW"
                  confidence="89%"
                  decision="RECOMMEND"
                  onClick={() =>
                    loadScenario("academic")
                  }
                />


                <Scenario
                  location="Hostel C"
                  metric="Water"
                  change="+35.14%"
                  severity="MEDIUM"
                  confidence="75%"
                  decision="MONITOR"
                  onClick={() =>
                    loadScenario("hostel")
                  }
                />


                <Scenario
                  location="Chemistry Lab"
                  metric="Energy"
                  change="+382.76%"
                  severity="EXTREME"
                  confidence="45%"
                  decision="ESCALATE"
                  onClick={() =>
                    loadScenario("chemistry")
                  }
                />

              </div>

            </section>

          </main>

        )}


        {/* =====================================================
            ANALYZE
        ===================================================== */}

        {page === "analyze" && (

          <main className="content">

            <section className="dashboard-panel">

              <div className="panel-header">

                <div>

                  <p className="eyebrow">
                    RESOURCE ANALYSIS
                  </p>

                  <h2>
                    Analyze Campus Resource
                  </h2>

                </div>


                <span className="live-pill">
                  ● MCP + LANGGRAPH
                </span>

              </div>


              {/* FORM */}

              <div className="form-grid">

                <div className="field">

                  <label>
                    RESOURCE TYPE
                  </label>

                  <select
                    value={metric}
                    onChange={(e) =>
                      setMetric(e.target.value)
                    }
                  >

                    <option value="energy">
                      Energy
                    </option>

                    <option value="water">
                      Water
                    </option>

                    <option value="waste">
                      Waste
                    </option>

                  </select>

                </div>


                <div className="field">

                  <label>
                    LOCATION
                  </label>

                  <select
                    value={location}
                    onChange={(e) =>
                      setLocation(e.target.value)
                    }
                  >

                    <option>
                      Academic Block A
                    </option>

                    <option>
                      Hostel C
                    </option>

                    <option>
                      Chemistry Lab
                    </option>

                  </select>

                </div>


                <div className="field">

                  <label>
                    CURRENT VALUE
                  </label>

                  <input
                    type="number"
                    value={currentValue}
                    onChange={(e) =>
                      setCurrentValue(e.target.value)
                    }
                  />

                </div>


                <div className="field">

                  <label>
                    BASELINE VALUE
                  </label>

                  <input
                    type="number"
                    value={baselineValue}
                    onChange={(e) =>
                      setBaselineValue(e.target.value)
                    }
                  />

                </div>


                {/* CONTEXT */}

                <div className="context-fields">

                  <label className="context-title">
                    OPERATIONAL CONTEXT
                  </label>


                  <label className="checkbox-row">

                    <input
                      type="checkbox"
                      checked={eventToday}
                      onChange={(e) =>
                        setEventToday(
                          e.target.checked
                        )
                      }
                    />

                    Campus event today

                  </label>


                  <label className="checkbox-row">

                    <input
                      type="checkbox"
                      checked={
                        sensorRecentlyReplaced
                      }
                      onChange={(e) =>
                        setSensorRecentlyReplaced(
                          e.target.checked
                        )
                      }
                    />

                    Sensor recently replaced

                  </label>

                </div>

              </div>


              <button
                className="analyze-button"
                onClick={analyzeAnomaly}
                disabled={loading}
              >

                {loading
                  ? "RUNNING ECOOPS AGENTS..."
                  : "ANALYZE ANOMALY →"}

              </button>


              {error && (
                <div className="error">
                  {error}
                </div>
              )}

            </section>


            {/* RESULT */}

            {result && (

              <section className="dashboard-panel result-panel">

                <div className="result-header">

                  <div>

                    <p className="eyebrow">
                      ANALYSIS COMPLETE
                    </p>

                    <h2>
                      {result.location}
                    </h2>

                    <p>
                      {result.metric.toUpperCase()}
                      {" "}RESOURCE ANALYSIS
                    </p>

                  </div>


                  <div
                    className={`decision ${result.decision.toLowerCase()}`}
                  >
                    {result.decision}
                  </div>

                </div>


                {/* METRICS */}

                <div className="metrics">

                  <div className="metric-card">

                    <span>
                      CHANGE
                    </span>

                    <strong>
                      {result.change_percent > 0
                        ? "+"
                        : ""}

                      {result.change_percent}%

                    </strong>

                  </div>


                  <div className="metric-card">

                    <span>
                      SEVERITY
                    </span>

                    <strong>
                      {result.severity}
                    </strong>

                  </div>


                  <div className="metric-card">

                    <span>
                      CONFIDENCE
                    </span>

                    <strong>
                      {confidencePercent}%
                    </strong>


                    <div className="confidence-bar">

                      <div
                        style={{
                          width: `${confidencePercent}%`,
                        }}
                      />

                    </div>

                  </div>

                </div>


                {/* CAUSE + POLICY */}

                <div className="result-grid">

                  <div className="info-card">

                    <p className="eyebrow">
                      POSSIBLE CAUSE
                    </p>

                    <h3>
                      {result.historical
                        ?.possible_cause ||
                        "No cause identified"}
                    </h3>


                    <div className="detail">

                      Historical similarity:{" "}

                      {result.historical
                        ?.historical_similarity ??
                        "N/A"}

                    </div>

                  </div>


                  <div className="info-card">

                    <p className="eyebrow">
                      GROUNDED POLICY
                    </p>

                    <h3>
                      {result.policy?.source ||
                        "Campus Sustainability Guidelines"}
                    </h3>


                    <ul>

                      {(result.policy?.guidance ||
                        []).map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}

                    </ul>

                  </div>

                </div>


                {/* RECOMMENDATION */}

                <div className="recommendation">

                  <div>

                    <p className="eyebrow">
                      RECOMMENDED ACTION
                    </p>

                    <h3>
                      {result.recommendations
                        ?. [0]?.action ||
                        "No recommendation available"}
                    </h3>

                  </div>


                  <div className="human-review">

                    ⚠ HUMAN APPROVAL REQUIRED

                  </div>

                </div>


                {/* AUDIT */}

                <div className="audit">

                  <p className="eyebrow">
                    DECISION AUDIT TRAIL
                  </p>


                  <div className="audit-list">

                    {(result.audit_trail || [])
                      .map((event, index) => (

                        <div
                          className="audit-item"
                          key={index}
                        >

                          <span>
                            {index + 1}
                          </span>


                          <div>

                            <strong>
                              {event.event}
                            </strong>

                            <small>
                              {event.tool ||
                                "EcoOps Decision Engine"}
                            </small>

                          </div>

                        </div>

                      ))}

                  </div>

                </div>

              </section>

            )}

          </main>

        )}


        {/* =====================================================
            ALERTS
        ===================================================== */}

        {page === "alerts" && (

          <main className="content">

            <section className="page-intro">

              <p className="eyebrow">
                SAFETY CENTER
              </p>

              <h1>
                Human Review Queue
              </h1>

              <p>
                EcoOps blocks automatic intervention when
                confidence or operational risk requires
                human judgment.
              </p>

            </section>


            <section className="dashboard-panel">

              {history.filter(
                (item) =>
                  item.decision === "ESCALATE"
              ).length === 0 ? (

                <div className="empty-state">

                  <div className="empty-icon">
                    ✓
                  </div>

                  <h3>
                    No active escalations
                  </h3>

                  <p>
                    High-risk anomalies requiring human
                    investigation will appear here.
                  </p>

                </div>

              ) : (

                history
                  .filter(
                    (item) =>
                      item.decision === "ESCALATE"
                  )
                  .map((item) => (

                    <div
                      className="alert-card"
                      key={item.id}
                    >

                      <div>

                        <p className="eyebrow">
                          EXTREME ANOMALY
                        </p>

                        <h3>
                          {item.location}
                        </h3>

                        <p>
                          {item.metric} ·{" "}
                          {item.change}% increase
                        </p>

                      </div>


                      <div>

                        <strong>
                          {Math.round(
                            item.confidence * 100
                          )}
                          %
                        </strong>

                        <span>
                          confidence
                        </span>

                      </div>


                      <div className="decision escalate">
                        ESCALATE
                      </div>

                    </div>

                  ))

              )}

            </section>

          </main>

        )}


        {/* =====================================================
            AUDIT TRAIL
        ===================================================== */}

        {page === "audit" && (

          <main className="content">

            <section className="page-intro">

              <p className="eyebrow">
                OBSERVABILITY
              </p>

              <h1>
                Decision Audit Trail
              </h1>

              <p>
                Every EcoOps decision can be traced through
                detection, grounding, confidence scoring,
                MCP tool usage, and safety routing.
              </p>

            </section>


            <section className="dashboard-panel">

              {result?.audit_trail?.length ? (

                <div className="full-audit">

                  {result.audit_trail.map(
                    (event, index) => (

                      <div
                        className="full-audit-item"
                        key={index}
                      >

                        <div className="audit-number">
                          {String(index + 1).padStart(
                            2,
                            "0"
                          )}
                        </div>


                        <div>

                          <strong>
                            {event.event}
                          </strong>

                          <p>
                            {event.tool ||
                              "EcoOps Decision Engine"}
                          </p>

                        </div>

                      </div>

                    )
                  )}

                </div>

              ) : (

                <div className="empty-state">

                  <div className="empty-icon">
                    ≡
                  </div>

                  <h3>
                    No analysis trace yet
                  </h3>

                  <p>
                    Run an analysis to generate the
                    complete agent decision trail.
                  </p>

                </div>

              )}

            </section>

          </main>

        )}

      </div>


      <footer>
        ECOOPS 2.0 · HUMAN-IN-THE-LOOP BY DESIGN
      </footer>

    </div>
  );
}


// ============================================================
// SCENARIO COMPONENT
// ============================================================

function Scenario({
  location,
  metric,
  change,
  severity,
  confidence,
  decision,
  onClick,
}) {
  return (
    <button
      className="scenario"
      onClick={onClick}
    >

      <div className="scenario-main">

        <strong>
          {location}
        </strong>

        <span>
          {metric}
        </span>

      </div>


      <div className="scenario-change">
        {change}
      </div>


      <div className="scenario-severity">
        {severity}
      </div>


      <div className="scenario-confidence">
        {confidence}
      </div>


      <div
        className={`decision ${decision.toLowerCase()}`}
      >
        {decision}
      </div>


      <span className="arrow">
        →
      </span>

    </button>
  );
}


export default App;