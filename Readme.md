# 🛰️ AI Airspace Surveillance & Target Tracking System

## Overview

This project is a **real-time AI-based airspace monitoring system** designed to simulate a military-grade air defense command center.  

It **monitors aircraft movement**, detects anomalous behavior using AI, tracks high-risk targets, and provides **dynamic visualizations** and **real-time alerts**.

This system demonstrates expertise in:

- Artificial Intelligence & Machine Learning  
- Geospatial analysis & mapping  
- Real-time data simulation  
- Cyber-physical system simulation  
- Defense & aviation analytics  

---

## Features

### 🟢 Aircraft Monitoring
- Track multiple aircraft in real-time  
- Simulate flight paths with speed, heading, and altitude  
- Display trajectories dynamically on an interactive map  

### 🟠 AI Anomaly Detection
- Detect abnormal behavior (speed, altitude, flight path deviation)  
- Assign risk scores:  
  - **10** → Normal  
  - **60** → Suspicious  
  - **95** → High Threat  

### 🔴 Target Tracking System
- Automatically identifies highest-risk aircraft  
- Highlights target on map with yellow ring  
- Shows intelligence panel with speed, altitude, and risk score  

### 🚨 Alerts & Analytics
- Real-time alerts for anomalies and restricted zone violations  
- Metrics panel for total aircraft, anomalies, restricted aircraft  
- Dynamic charts: risk distribution, speed vs altitude  

### 🗺️ Map Interface
- Interactive PyDeck map  
- Flight trajectories  
- Restricted airspace zones highlighted  
- Color-coded aircraft markers  

---

## Demo

A live demo of the system can be deployed using **Streamlit Community Cloud**:

[https://airsapce-ai-gofq97zd5cqp8yjecvbpec.streamlit.app/]

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/bakarrsillah/airsapce-ai.git
cd airspace-ai
