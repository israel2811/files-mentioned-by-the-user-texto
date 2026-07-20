# Workspace-Scoped Customization Rules (NEXUS/CCA-AAV)

These rules apply automatically to all agentic sessions running within this workspace.

## 1. Safety and Data Custody
- **Never Delete**: Do not permanently delete or overwrite any files in this project.
- **Quarantine**: If any file or folder is redundant, move it to a backup directory prefixed with `99_` (e.g., `99_quarantine/`).
- **Exclusion Zones**: Never modify or alter directories related to backup tools or version control: `.git/`, `FileHistory/`, `USB_D_Migration/`, `OneDrive_backup/`, `RESPALDO_USB/`.
- **Incremental Saves**: Always save progress incremental logs or manifests when doing file processing.

## 2. Academic Rigor and Citations
- **Strict DOI Mapping**: Every academic or scientific claim must be immediately accompanied by its corresponding verified DOI citation in the same sentence.
- **Hypothesis Flagging**: Any technical, physical, or clinical assumption that has not been verified against a Peer-Reviewed publication in the core database must be explicitly marked with the tag `[POR-VALIDAR]`.
- **Segregation of Personal Evidence**: Maintain a strict separation between the academic body of the thesis (clinically defendable models like RDoC/continuum and telecom audio codecs PLC/CNG) and personal forensic evidence (stalkerware, logs, acoso). Forensic details should be kept in isolated technical annexes under ISO/IEC 27037 guidelines.

## 3. Host System Resource Optimization
- **Low CPU Priority**: Keep Google Drive, OneDrive, and Dropbox sync processes set to `BelowNormal` or `Idle` priority on the host machine to maximize RAM and CPU availability.
- **File Chunking**: Avoid reading raw JSON or HTML files larger than 600 KB in a single pass. Write a script to split them into small, manageable chunks before parsing.

## 4. Browser Control (Brave / CDP)
- **Persistent Remote Debugging**: Always assume Brave is launchable/listening on `--remote-debugging-port=50064`. The agent should connect via CDP to interact with the user's active profiles and active sessions for Google Drive, GitHub, and academic tools.
- **Session Reuse**: Avoid creating clean or sandboxed browser profiles whenever possible; instead, leverage active user profile sessions to bypass authentication requirements (OAuth, 2FA).

