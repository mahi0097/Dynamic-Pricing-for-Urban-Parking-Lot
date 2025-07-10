# 🚗 Real-Time Dynamic Pricing for Urban Parking Lots

> **Final Submission — Summer Analytics 2025**  
> Hosted by: Consulting & Analytics Club × Pathway

---

## 📝 Project Overview

Parking prices that remain static often lead to overcrowding or underutilization.  
To tackle this problem, this project simulates an **intelligent real-time pricing system** for urban parking lots based on **demand, traffic, queue length, and competition**.

We developed a **streaming pipeline using Pathway** that dynamically updates parking lot prices every few seconds using real-time data and core economic principles.

---

## 🧰 Tech Stack Used

| Purpose               | Tool / Library                       |
|-----------------------|--------------------------------------|
| Programming Language  | Python 3                             |
| Real-Time Engine      | [Pathway](https://pathway.com)       |
| Data Processing       | Pandas, NumPy                        |
| Visualization         | Bokeh (for real-time live charts)    |
| Notebook Environment  | Google Colab                         |
| Version Control       | Git + GitHub                         |

---

## 🔧 Project Architecture & Workflow

```mermaid
flowchart TD
    A[CSV Input Data (14 Lots)] --> B[Pathway Streaming Engine]
    B --> C[Real-Time Feature Processor]
    C --> D[Dynamic Pricing Engine]
    D --> E[Bokeh Visualization + Console Output]
🧩 Modules:
Ingestion: Stream 14-lot data (8 AM to 4:30 PM daily) into a real-time processor

Feature Engine: Extracts occupancy rate, queue, traffic, etc. from each row

Pricing Engine:

✅ Model 1: Linear occupancy pricing

✅ Model 2: Multi-feature demand pricing

✅ Model 3: Competition-aware logic using geo-coordinates

Streaming Output: Pushes predicted prices to terminal & plots
Pricing Models Explained
🔹 Model 1 – Baseline Linear
Price = Base + α × (Occupancy / Capacity)

Simple occupancy-based pricing

🔹 Model 2 – Demand-Based Dynamic
Price = Base × (1 + λ × Demand Score)
Demand score calculated from:

Occupancy

Queue length

Traffic condition

Vehicle type

Special day indicator

🔹 Model 3 – Competition-Aware Pricing (Bonus)
Calculates geographic proximity using Haversine distance

Adjusts pricing based on competitor prices and lot saturation

📂 Repository Structure
graphql
Copy
Edit
📦 RealTime-Parking-Pricing/
├── cleaned_dataset.csv           # Cleaned CSV used for streaming
├── dataset.csv                   # Raw CSV file (original format)
├── notebook.ipynb                # Final Google Colab notebook
├── utils.py                      # Optional helper code (Haversine, demand)
├── README.md                     # This documentation
├── architecture.png              # Optional PNG architecture diagram
└── report.pdf                    # (Optional) Final PDF Report
▶️ How to Run
Upload cleaned_dataset.csv in Google Colab

Run notebook.ipynb

Watch live terminal output and pricing stream

View real-time visualization (if Bokeh enabled)

📝 Optional Report
Includes:

Feature engineering

Model comparison

Visualization snapshots

Observations + business impact
Submission Checklist
 Public GitHub Repository

 Cleaned and working code

 Well-commented notebook

 This README with architecture diagram

 (Optional) Report in PDF

🙌 Acknowledgments
Summer Analytics 2025

Consulting & Analytics Club, IIT Guwahati

The Pathway team for the real-time computation engine

📫 Contact
👤 Name: Your Name

📧 Email: yourname@example.com

🌐 GitHub: github.com/yourusername
