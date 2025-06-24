# deadline_sheepit_submitter
## Overview

This repository provides a custom plugin and submitter for Thinkbox Deadline 10.3, allowing you to run the [SheepIt render farm client](https://www.sheepit-renderfarm.com/) directly from your render nodes managed by Deadline.

---

## Installation

1. **Copy the plugin files**
    - Place the entire `SheepIt` plugin folder in:
      ```
      [Deadline Repository]/custom/plugins/SheepIt/
      ```

2. **Place the SheepIt Java client**
    - Download `sheepit-client.jar` from [sheepit-renderfarm.com](https://www.sheepit-renderfarm.com/media/applet/client/sheepit-client.jar)
    - Place it in:
      ```
      [Deadline Repository]/custom/plugins/SheepIt/client/sheepit-client.jar
      ```

3. **Copy the submission script**
    - Place `SubmitSheepItJob.py` in:
      ```
      [Deadline Repository]/custom/scripts/Submission/
      ```

4. **Restart Deadline Monitor and all Workers** to ensure the plugin and submitter are loaded.

---

## Usage

1. In Deadline Monitor, go to `Submit > SheepIt Job`.
2. Fill in your SheepIt login, password, number of machines, and machine list if needed.
3. Submit the job. Each Deadline task will launch a SheepIt client instance on the assigned Worker.

---

## Important

- The file `sheepit-client.jar` **must** be present at: [Deadline Repository]/custom/plugins/SheepIt/client/sheepit-client.jar

- Java must be available on each Worker, either in the system PATH or in the location configured in the plugin (normally, it's integrated with sheepit so if you keep the original path, it will work on all your machines).
- No login/password is stored in the repository; they are provided at job submission.

---

## Support

For issues with this plugin or script, open an issue in this repository or contact your pipeline technical director.
For SheepIt client questions, visit [SheepIt FAQ](https://www.sheepit-renderfarm.com/faq).

---



