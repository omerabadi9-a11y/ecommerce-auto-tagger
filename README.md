# 🏷️ E-Commerce Auto-Tagger

Smart inventory management system for e-commerce stores - AWS Final Project

## 📋 Project Description

An automated system that analyzes product images using AI and generates marketing descriptions. Built on AWS Serverless architecture (Event-Driven).

## 🏗️ Architecture

User uploads image → S3 → Lambda → Rekognition → Bedrock → DynamoDB → API Gateway → Frontend

## ☁️ AWS Services Used

### Required Services
- **Amazon S3** - Image storage + Static website hosting
- **AWS Lambda** - Business logic (3 functions)
- **Amazon API Gateway** - REST API exposure
- **Amazon DynamoDB** - Product catalog database
- **AWS IAM** - Permissions management (Least Privilege)

### Additional Services
- **Amazon Rekognition** - AI image analysis and object detection
- **Amazon Bedrock (Nova Lite)** - Marketing description generation in Hebrew
- **Amazon CloudWatch** - Monitoring and logs

## 🚀 How It Works

1. User uploads a product image via the web interface
2. Image is stored in S3
3. S3 Trigger activates the `AnalyzeVisionImage` Lambda function
4. Rekognition detects objects in the image
5. Bedrock generates a marketing description in Hebrew
6. Results are saved to DynamoDB
7. Frontend displays the tagged product catalog

## 📁 Project Structure

ecommerce-auto-tagger/

├── lambda/

│   ├── analyze_vision_image.py   # Main function - Rekognition + Bedrock

│   ├── get_products.py           # Returns product catalog from DynamoDB

│   └── generate_upload_url.py    # Generates secure S3 upload URL

├── frontend/

│   └── index.html                # Web interface

└── README.md

## 🌐 Live Demo

Website URL: `http://ecommerce-autotagger-website.s3-website-us-east-1.amazonaws.com`

API URL: `https://urhnwa221c.execute-api.us-east-1.amazonaws.com/prod`

## 👥 Team

- **Taima** - Infrastructure, Lambda, Rekognition, API Gateway
- **Omer** - Bedrock integration, Frontend, GitHub
- **Lial & Alinor** - Documentation, Presentation
