# 🤖 LinkedIn Job Automation using Selenium

This project automates the process of searching and applying for jobs on **LinkedIn** using **Python** and **Selenium WebDriver**.  
It automatically logs in, searches for jobs with given keywords & location, applies to **Easy Apply** jobs, and navigates across multiple pages until all listings are processed.

⚠️ **Disclaimer**: This project is for **educational purposes only**. Automating job applications may violate LinkedIn’s Terms of Service. Use responsibly on test accounts.

---

## 📌 Features
- 🔑 **Login automation** with LinkedIn credentials  
- 🔍 **Job search automation** by keyword & location  
- 🖱️ **Easy Apply** button detection  
- ✅ Automatically **submits applications** if possible  
- 🗑️ **Discards multi-step applications** safely  
- 🔄 Scrolls & loads more job cards on each page  
- ⏭️ Navigates to the **next job page** until the last one  
- 📝 Clear **console logs** showing each step  

---

## 🛠️ Tech Stack
- [Python 3.9+](https://www.python.org/downloads/)  
- [Selenium](https://selenium-python.readthedocs.io/)  
- Chrome WebDriver / Edge WebDriver  
- Virtual Environment (`venv`)  

---

## 📂 Project Structure


JOB AUTOMATION/
│── drivers/                # ChromeDriver & EdgeDriver executables
│── selenium\_py/            # Python virtual environment
│── src/
│   ├── **init**.py
│   ├── main.py             # Main entry point (run this)
│── config.json             # Config file (optional for credentials)
│── requirements.txt        # Python dependencies
│── setup.py                # Setup script
│── README.md               # Project guide

````

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/mudhay027/LinkedIn-Job-Automation-Using-Selenium.git
cd LinkedIn-Job-Automation-Using-Selenium
````

### 2. Create & activate virtual environment

```bash
# Windows
python -m venv selenium_py
selenium_py\Scripts\activate

# Linux / Mac
python3 -m venv selenium_py
source selenium_py/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download WebDriver

* Chrome users: [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)
* Edge users: [Download EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Place the `.exe` file inside the **drivers/** folder.

---

## ▶️ Usage

### 1. Update credentials in `main.py`

```python
USERNAME = "your_email@example.com"
PASSWORD = "your_password"
```

### 2. Run the script

```bash
python src/main.py
```

### 3. Example Output

```
🚀 Starting LinkedIn Job Automation Script...
🔑 Logging into LinkedIn...
✅ Logged in successfully!
🔍 Searching jobs: Data scientist in Chennai, India
✅ Jobs listing loaded.

=== 📄 Processing Page 1 ===
Found 25 jobs on page
[1] ✅ Application submitted
[2] ❌ Not direct submit, discarding.
...
🏁 All pages processed. Job automation finished.
🛑 Browser closed. Program finished.
```

---

## 🎥 Demo Video

Include your walkthrough video here (show setup + running + results).
Example:

```
[![Watch the video](https://img.youtube.com/vi/<VIDEO_ID>/0.jpg)](https://youtu.be/<VIDEO_ID>)
```

---

## 📌 Notes

* Script only applies to **Easy Apply** jobs.
* If LinkedIn shows a **captcha or 2FA**, the script pauses until you solve it.
* Use headless mode if you don’t want browser UI:

  ```python
  driver = init_driver(headless=True)
  ```

---

## 🤝 Contribution

Feel free to fork, improve, and raise pull requests.

---

## ⚠️ Disclaimer

This project is **for educational purposes only**.
The author is **not responsible** for any misuse or violation of LinkedIn’s policies.

```

---

Do you want me to **add badges (Python, Selenium, GitHub stars, MIT License)** at the top of this README to make your repo more professional-looking?
```
