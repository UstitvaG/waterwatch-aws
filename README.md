# WaterWatch 💧

A crowd-reporting tool for flooded and waterlogged streets, built for the **Environmental Hacks hackathon (Heat and Water track)** — part of the **Bharat Builds Tour** by WeMakeDevs × AWS.

## 📌 The Problem
Every monsoon, streets across Indian cities flood or waterlog — but there is no easy, real-time way for citizens to know which streets are affected before they leave home or pick a route. **WaterWatch** lets anyone mark a flooded location on a map in a few taps, allowing others nearby to see live updates and avoid dangerous routes.

## 🔗 Project Links
*   **Live Site:** [Launch WaterWatch App](YOUR_S3_WEBSITE_URL_HERE)
*   **Demo Video:** [Watch the Video Walkthrough](YOUR_VIDEO_LINK_HERE)

## 🚀 How It Works
1.  **View the Map:** A user opens the site and sees a live map of existing reports, color-coded by severity (Low / Medium / High).
2.  **Pin a Location:** They pin a new location (by clicking on the map or using their current GPS location).
3.  **Submit Report:** They pick a severity level, optionally attach a photo, and hit submit.
4.  **Live Sync:** The report is saved instantly and appears on the map for all other users in real time.

## 🏗️ Architecture & Tech Stack

```text
Browser (S3 Static Site)
      │
      │  POST /reports  (new report)
      │  GET  /reports  (list reports)
      ▼
API Gateway (HTTP API)
      │
      ▼
AWS Lambda (Python)
      │
      ▼
DynamoDB (WaterReports table)
```

### AWS Services Used
*   **Amazon S3:** Static website hosting for the frontend.
*   **Amazon API Gateway:** HTTP API exposing the `POST /reports` and `GET /reports` routes.
*   **AWS Lambda:** Serverless backend (Python) handling data storage and retrieval.
*   **Amazon DynamoDB:** NoSQL database storing report data (`reportID`, location, severity, timestamp, photo).

## 📂 Repository Structure
*   `index.html` - Frontend codebase containing the interactive map, reporting form, and client-side application logic.
*   `lambda_function.py` - Backend serverless code handling the `GET` and `POST` requests for `/reports`.

## 🛠️ Deployment & Local Setup

Follow these steps to deploy your own instance of WaterWatch:

### 1. Database Setup
*   Create an **Amazon DynamoDB** table named `WaterReports`.
*   Set the Partition Key to `reportID` (Type: **String**).

### 2. Backend Deployment
*   Create an **AWS Lambda** function using the **Python 3.12** runtime.
*   Paste the contents of `lambda_function.py` into the code editor.
*   Attach an IAM execution role to the Lambda function that grants read/write permissions to your DynamoDB table.

### 3. API Configuration
*   Create an **Amazon API Gateway** (HTTP API).
*   Configure two routes pointing to your Lambda function:
    *   `POST /reports`
    *   `GET /reports`
*   **Crucial:** Enable **CORS** on your API Gateway. Set Allow Origin to `*`, Methods to `GET, POST, OPTIONS`, and Headers to `Content-Type`.

### 4. Frontend Deployment
*   Open `index.html` and locate the `API_ENDPOINT` constant near the top of the `<script>` tag.
*   Update it with your unique API Gateway invoke URL (e.g., `https://amazonaws.com`).
*   Create an **Amazon S3** bucket, enable **Static Website Hosting**, and upload your updated `index.html` file.

## 🔮 What's Next
*   **Automated Authority Alerts:** Routing high-severity reports directly to relevant local municipal corporations or PWD divisions via Amazon SNS/Email based on geo-coordinates.
*   **Map Clustering:** Grouping nearby pins dynamically so the map interface stays clean and highly readable at scale.
*   **Spam Moderation:** Implementing a lightweight verification or community upvote system to filter duplicate or spam reports.

---
Built with 💙 for the **Environmental Hacks (Heat and Water track)** during the **Bharat Builds Tour** by WeMakeDevs × AWS.
