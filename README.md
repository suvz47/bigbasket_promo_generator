# 🌟 BigBasket Banner Generator 🌟

### **🚀 Create stunning banners for your products, effortlessly! Powered by cutting-edge AI technology.**

---

## Table of Contents
- [✨ Introduction](#-introduction)
- [⚙️ Features](#%EF%B8%8F-features)
- [🛠️ Installation](#%EF%B8%8F-installation)
- [🎮 Usage](#-usage)
  - [🔹 Using the Frontend](#-using-the-frontend)
  - [🔹 Backend API](#-backend-api)
- [📸 Demo](#-demo)
- [⚡ Technologies Used](#-technologies-used)
- [📜 License](#-license)

---

## ✨ Introduction
Welcome to **BigBasket Banner Generator**, a simple yet powerful tool for creating visually appealing banners for your products. This tool leverages **Generative AI models** like **Google Gemini and Google Imagen**, making the banner creation process both smart and efficient!

> 📌 **Note:** This project is built for educational and creative purposes, aimed at designers and marketers looking to generate eye-catching banners effortlessly.

---

## ⚙️ Features
- **🖼️ Image Uploads**: Upload 0, 1 or more images to include in your banner.
- **📝 Smart Content Generation**: Uses generative AI to create banners based on input topic and style.
- **📐 Customizable Aspect Ratios**: Supports multiple aspect ratios (1:1, 16:9, etc.).
- **🖍️ Auto Image Editing**: The AI tool automatically detects anomalies in the image and fixes them.
- **🔍 Preview in Real-Time**: See your uploaded images and the final generated banner, and make modifications or download it.

---

## 🛠️ Installation

### Prerequisites
- Python 3.11
- Access to Gemini API
- Access to Google Cloud Platform and Vertex AI
- Access to Google Imagen
- Huggingface Account

### Steps
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/username/bigbasket-banner-generator.git
    cd bigbasket-banner-generator
    ```

2. **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Backend (FastAPI)**:
    ```bash
    uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
    ```

5. **Run the Frontend (Gradio)**:
    ```bash
    python frontend.py
    ```

---

## 🎮 Usage

<details>
  <summary><b>🔹 Using the Frontend</b></summary>
  
  1. **Access the UI**: Open your browser and go to `http://localhost:8000`.
  2. **Enter Topic**: Provide the topic for your banner, including details like product, theme, and colors.
  3. **Upload Images**: Click on the "📸 Upload Images" button to upload images.
  4. **Select Aspect Ratio**: Choose from the dropdown (e.g., `1:1`, `9:16`).
  5. **Generate**: Click on "✨ Generate Banner". Your banner will be generated in less than 50 seconds!

  ![frontend-screenshot](https://via.placeholder.com/800x400?text=Frontend+Screenshot)
  
</details>

<details>
  <summary><b>🔹 Backend API</b></summary>
  
  The backend exposes a RESTful API for generating banners.
  
  - **Endpoint**: `/generate_banner`
  - **Method**: `POST`
  - **Parameters**:
    - `topic`: Banner topic (string)
    - `images`: List of images to include (file upload)
    - `aspect_ratio`: Optional aspect ratio (`1:1`, `9:16`, etc.)
    
  Example cURL command:
  ```bash
  curl -X POST -F "topic=Summer Sale" -F "images=@path/to/image1.jpg" -F "aspect_ratio=16:9" http://localhost:8000/generate_banner
  ```
</details>

---

## 📸 Demo

![banner-demo](https://via.placeholder.com/1200x400?text=Banner+Generator+Demo)

> 🎥 **Watch the Full Demo on [YouTube](https://youtu.be/FRH5ro5l8lQ)**.

---

## ⚡ Technologies Used
- **🖥️ Backend**: FastAPI - Lightning-fast Python web framework.
- **🤖 AI Models**: Google Gemini, Google Imagen via Google Vertex AI.
- **🎨 UI**: Gradio - Easy to use UI for interacting with machine learning models.
- **💾 Storage**: Local storage for saving generated images. (alternate - GCP buckets)

---

## 💡 How It Works

1. **User Input**: The user provides details about the banner through a Gradio UI.
2. **Backend Processing**: The backend (FastAPI) receives the user inputs and images, then calls the `BannerGenerator` class to process.
3. **Banner Generation**: The AI models analyze the inputs to generate relevant text and banners.
4. **Refinement**: The banner undergoes a refinement stage to ensure quality and consistency.
5. **Result Display**: The final banner is displayed on the UI for the user.

<details>
  <summary><b>🌍 Architecture Overview</b></summary>
  
  ![architecture-diagram](https://via.placeholder.com/800x400?text=Architecture+Diagram)
  
  **Components**:
  - **Frontend**: User interaction layer.
  - **Backend**: Handles business logic and processing.
  - **AI Models**: Google Gemini & Imagen for text and image generation.
</details>

---


## 🤝 Contact Us
For any questions or inquiries:

📧 **Email**: suvojithore.dev@gmail.com

👥 **Contributors**: [Suvojit](https://www.linkedin.com/in/suvojith/), Gayathri, Varen, Payal.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

> 🔔 **Stay Connected**: Follow us for updates, news, and new features. Don’t forget to give a ⭐ if you like this project!

---

### ⚡ Powered by Gemini AI 🧠 | Built for Designers 🎨 | Made with ❤️ by [Suvojit](https://www.linkedin.com/in/suvojith/), Gayathri, Varen and Payel.