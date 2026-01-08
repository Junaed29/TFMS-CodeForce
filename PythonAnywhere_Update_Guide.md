# How to Update Your Live Site 🚀

This is your cheat sheet for moving new code from your computer to PythonAnywhere.

## Step 1: On Your Computer (VS Code)

1.  **Code & Save**: Make your changes to the code.
2.  **Push to GitHub**:
    Open your terminal in VS Code and run:
    ```bash
    git add .
    git commit -m "Describe your update here"
    git push
    ```

## Step 2: On PythonAnywhere (Bash Console)

1.  **Open the Console**: Go to **Consoles** -> **Bash console**.
2.  **Go to your project**:
    ```bash
    cd ~/TFMS-CodeForce
    ```
3.  **Pull the changes**:
    ```bash
    git pull
    ```

## Step 3: Run Maintenance (Only if needed)

**How do I know if I need this?**

*   **Did you change `models.py`?** (Added a field, created a table?)
    *   👉 **YES**: Run these:
        ```bash
        workon myenv
        python manage.py migrate
        ```

*   **Did you change `style.css` or add Images?** (Any file in `static/`)
    *   👉 **YES**: Run these:
        ```bash
        workon myenv
        python manage.py collectstatic
        ```
        *(Type `yes` if asked)*

*   **If you only changed HTML or Views (`views.py`)**:
    *   👉 **NO**: Skip this step. Just Reload.

> **Pro Tip**: Nothing bad happens if you run these commands when you don't need to. It just takes a few extra seconds. If you are ever unsure, **run them anyway**! Better safe than sorry.

## Step 4: Reload (The most important step!)

1.  Go to the **Web** tab.
2.  Click the Green **Reload** button.
3.  **Done!** Check your site.
