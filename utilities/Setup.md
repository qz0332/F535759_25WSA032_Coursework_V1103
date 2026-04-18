
# 🐍 **Project Setup Instructions (Windows + VS Code)**

Welcome! Follow these steps to set up your Python project correctly on your computer.  
You only need to do this **once per project**.

---

## ✅ 1. Open the Project in VS Code

1. Download and unzip the project folder  
2. Open VS Code  
3. Go to **File → Open Folder**  
4. Select the **project folder** (the folder containing this README)

You should now see the project files in the VS Code Explorer.

---

## ✅ 2. Run the Setup Script

This project includes a PowerShell script that will:

- create a Python virtual environment in your **Local AppData**  
- configure VS Code to use that environment  
- activate it for you automatically  

### 👉 Steps

1. Open the **VS Code terminal**  
   ```
   Terminal → New Terminal
   ```

2. Run this command (exactly as written):

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\powershell\setup-venv.ps1
   ```

3. Wait for the script to finish.  
   It will show messages like:

   - *Creating virtual environment…*  
   - *VS Code configured to use: …*  
   - *Your virtual environment is now active!*

---

## ✅ 3. Confirm the Environment Is Active

After the script completes, the terminal prompt should show something like:

```
(venv) C:\path	o\project>
```

To test it, run:

```powershell
python --version
```

If you see a version number (e.g., `Python 3.12.1`), all is good.

---

## 📦 4. Installing Project Dependencies

If the project contains a `requirements.txt`, install everything with:

```powershell
pip install -r requirements.txt
```

---

## 🎉 You're Done!

Your project is now correctly configured.  
Any time you come back to work:

1. Open the project in VS Code  
2. Open a terminal  
3. If the venv is not active, run:

   ```powershell
   & "$env:LOCALAPPDATAenvs\<project-name>\Scripts\Activate.ps1"
   ```

VS Code will automatically use the correct Python interpreter because the script created a `.vscode/settings.json` file for you.

---

## ❓ Need help?

Ask your instructor if:

- the script produced an error  
- Python is not recognised  
- you are unsure which folder to open  

Happy coding! 🧑‍💻🐍

