# 📱 Android WMS Mobile Automation Framework

### Selenium + Appium Based Enterprise Automation Project

---

## 📌 Project Overview

This project is an **Android Mobile Automation Framework** developed for automating Warehouse Management System (WMS) applications using **Python, Selenium, and Appium**.

The framework is designed to execute mobile-based warehouse workflows such as:

* Direct Loading Cycle
* Normal Shipping Cycle
* Silo Loading & Repacking
* Inbound & Outbound Operations
* Inventory Handling

It supports **Excel-driven Data Testing** and is specially designed for **offline enterprise environments** where internet access is restricted (e.g., Windows Server / Jenkins-based infrastructure).

---

## 🎯 Project Objective

To automate real-time Android-based WMS mobile workflows in enterprise warehouse environments using:

* Data Driven Testing
* Offline Package Installation
* Batch Execution Support
* Configurable Test Modules

This framework helps reduce manual testing effort and improves execution speed and accuracy for operational warehouse processes.

---

## 🛠️ Tech Stack Used

| Technology          | Usage                      |
| ------------------- | -------------------------- |
| Python 3.11         | Automation Scripting       |
| Selenium            | Web Automation Integration |
| Appium              | Android Mobile Automation  |
| Pandas              | Excel Data Handling        |
| OpenPyXL            | Excel File Processing      |
| Android SDK         | Device Communication       |
| Appium Server       | Test Execution Engine      |
| Jenkins             | CI/CD Execution            |
| Windows Server 2016 | Enterprise Offline Infra   |

---

## 📂 Project Structure

```
main/
│
├── common_controllers/
├── selenium_wms/
├── DirectLoadingCycle/
├── DirectLoadingCycleMB/
├── NormalShippingCycle/
├── NormalShippingCycleMB/
├── SiloLoadingAndRepacking/
├── reports/
│
├── requirements.txt
├── requirements_android.txt
├── requirements_offline.txt
├── test_app.py
```

---

## 🔐 Offline Installation Support

This project supports execution in environments where internet access is restricted.

Offline Python dependencies can be installed using locally stored wheel packages:

```
pip install --no-index --find-links=android_offline_packages -r requirements_offline.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/itssameerkhaan/selenium-wms-android-automation.git
cd selenium-wms-android-automation
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv android_venv
android_venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

Online Installation:

```
pip install -r requirements.txt
```

Offline Installation:

```
pip install --no-index --find-links=android_offline_packages -r requirements_offline.txt
```

---

### 4️⃣ Start Appium Server

```
appium
```

---

### 5️⃣ Run Automation Script

```
python test_app.py
```

---

## 📊 Automation Coverage

The framework is capable of automating:

* Warehouse Loading Operations
* Shipping Workflows
* Inventory Scanning
* Mobile Picking / Packing
* Repacking Activities
* Enterprise Warehouse Mobility Flows

---

## 🚀 Enterprise Use Case

This framework is built for enterprise warehouse systems where:

* Mobile WMS Applications are used
* Execution happens on Offline Infrastructure
* Automation runs through Jenkins Pipelines
* Deployment is done on Windows Server Environments

---

## 👨‍💻 Author

**Sameer Khan**
Automation Engineer | AI Integration Developer
Working on WMS Automation & AI-Based Bond Platform Integration

---

## 📜 License

This project is licensed under the MIT License.
