const { invoke } = window.__TAURI__.core;
const readinessStatus = document.getElementById("core-readiness");
const healthStatus = document.getElementById("core-health");
const versionStatus = document.getElementById("core-version");
const capabilitiesStatus = document.getElementById("core-capabilities");
const observationStatus = document.getElementById("observation-status");
let observationRequestId = null;
let observationBusy = false;

async function refresh() {
  try {
    readinessStatus.textContent = `Ready: ${String(await invoke("core_ready"))}`;
    healthStatus.textContent = `Health: ${String(await invoke("core_health"))}`;
    versionStatus.textContent = `Version: ${String(await invoke("core_version"))}`;
    const capabilities = await invoke("core_capabilities");
    capabilitiesStatus.textContent = `Capabilities: ${Array.isArray(capabilities) ? capabilities.join(", ") : String(capabilities)}`;
  } catch (_error) {
    readinessStatus.textContent = "Ready: unavailable";
    healthStatus.textContent = "Health: unavailable";
    versionStatus.textContent = "Version: unavailable";
    capabilitiesStatus.textContent = "Capabilities: unavailable";
  }
}

document.getElementById("observation-start").addEventListener("click", async () => {
  if (observationBusy || observationRequestId !== null) return;
  observationBusy = true;
  try {
    observationRequestId = await invoke("core_observe_health");
    observationStatus.textContent = "Observation active";
  } catch (_error) {
    observationRequestId = null;
    observationStatus.textContent = "Observation unavailable";
  } finally {
    observationBusy = false;
  }
});

document.getElementById("observation-cancel").addEventListener("click", async () => {
  if (observationBusy || observationRequestId === null) return;
  const requestId = observationRequestId;
  observationBusy = true;
  try {
    await invoke("core_cancel_observation", { requestId });
    if (observationRequestId === requestId) observationRequestId = null;
    observationStatus.textContent = "Observation cancelled";
  } catch (_error) {
    observationStatus.textContent = "Cancellation failed";
  } finally {
    observationBusy = false;
  }
});

refresh();
