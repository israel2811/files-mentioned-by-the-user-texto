Set WshShell = CreateObject("WScript.Shell")

' 1. Codex / Codex Beta
On Error Resume Next
WshShell.Run "cmd /c start """" ""C:\Users\Dell\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe""", 0, False
WshShell.Run "cmd /c start codex", 0, False

' 2. Chrome Default -> Google Drive
WshShell.Run "chrome.exe --profile-directory=""Default"" ""https://drive.google.com""", 1, False

' 3. Chrome Profile 2 -> ChatGPT
WshShell.Run "chrome.exe --profile-directory=""Profile 2"" ""https://chatgpt.com""", 1, False

' 4. Brave Default -> Claude AI
WshShell.Run "brave.exe --profile-directory=""Default"" ""https://claude.ai""", 1, False

' 5. Edge Default -> NotebookLM
WshShell.Run "msedge.exe --profile-directory=""Default"" ""https://notebooklm.google.com""", 1, False
