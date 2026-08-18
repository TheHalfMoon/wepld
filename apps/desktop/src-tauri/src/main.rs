#![forbid(unsafe_code)]
use std::sync::Mutex;
use wepld_desktop::CoreClient;

struct AppState {
    core: Mutex<Option<CoreClient>>,
}

#[tauri::command]
fn core_ready(_state: tauri::State<'_, AppState>) -> bool {
    false
}
#[tauri::command]
fn core_health(_state: tauri::State<'_, AppState>) -> Result<String, String> {
    Ok(String::new())
}
#[tauri::command]
fn core_version(_state: tauri::State<'_, AppState>) -> Result<String, String> {
    Ok(String::new())
}
#[tauri::command]
fn core_capabilities(_state: tauri::State<'_, AppState>) -> Result<Vec<String>, String> {
    Ok(Vec::new())
}
#[tauri::command]
fn core_observe_health(state: tauri::State<'_, AppState>) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    client
        .send_observe_health()
        .map_err(|error| format!("{error:?}"))
}
#[tauri::command]
fn core_cancel_observation(
    state: tauri::State<'_, AppState>,
    request_id: u64,
) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    client
        .send_cancel(request_id)
        .map_err(|error| format!("{error:?}"))
}

fn main() {
    let state = AppState {
        core: Mutex::new(CoreClient::start().ok()),
    };
    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            core_ready,
            core_health,
            core_version,
            core_capabilities,
            core_observe_health,
            core_cancel_observation
        ])
        .run(tauri::generate_context!())
        .expect("Tauri runtime failed");
}
