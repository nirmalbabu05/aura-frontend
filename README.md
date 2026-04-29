# ✈️ Aura Holidays | Premium World Travel
**Redefining Luxury Travel with AI-Powered Experiences**

## 🚀 Overview

**Aura Holidays** is a modern, premium travel booking and itinerary management web application. Designed for a seamless and luxurious user experience, the platform allows users to explore global destinations, view meticulously curated travel packages, and manage their personal wishlists. 

Taking travel planning to the next level, Aura Holidays integrates an intelligent **AI Travel Assistant** and a dynamic **AI Itinerary Builder** powered by Google Gemini. Users can instantly generate custom trip plans based on their budget, vibe, and duration, and even download them as beautifully formatted PDFs. 

## ✨ Key Features

* 🤖 **AI Trip Builder:** Generates highly customized day-by-day itineraries based on user inputs (Destination, Duration, Budget, and Travel Vibe) with instant PDF download capabilities.
* 💬 **Smart AI Travel Assistant:** An integrated floating chat interface powered by data science that answers user queries and helps with real-time travel recommendations.
* ❤️ **Cloud-Synced Wishlist:** Secure Google Sign-In via Firebase Authentication allows users to save and manage their favorite premium packages across sessions.
* 🌍 **Dynamic Package Filtering:** A robust vanilla JavaScript rendering engine that seamlessly filters and displays global packages, including a highly specific regional filter for India (North, South, West, Islands).
* 📱 **Premium UI/UX:** Built with Tailwind CSS and GSAP, featuring smooth page transitions, responsive glassmorphism elements, sticky navigation, and modal pop-ups for an app-like experience.
* 📩 **Instant Enquiry System:** Integrated contact and booking forms designed for quick lead generation without backend email setups.

## 🛠️ Tech Stack

**Frontend Architecture**
* HTML5 & Semantic Markup
* Tailwind CSS (Utility-first styling, Custom Themes, Responsive Design)
* Vanilla JavaScript (ES6+, DOM Manipulation, Dynamic Rendering)
* GSAP (GreenSock Animation Platform for fluid UI transitions)

**Backend & AI Integrations**
* **Python API Engine:** Hosted on Render (`aura-holidays-api.onrender.com`) to serve real-time package data and manage wishlist interactions.
* **Google Gemini AI Engine:** The core brain behind the dynamic itinerary generation and chatbot features.

**Authentication & Database**
* **Firebase Auth:** Handled via `firebase-auth-compat` for seamless Google OAuth Login.
* **Cloud Database:** Real-time storing and fetching of user-specific wishlist data securely via the custom backend API.

**External Libraries**
* `html2pdf.js`: Client-side rendering of AI itineraries into downloadable PDF documents.
* `Web3Forms`: Secure and simple form submission handling.

## 💻 Running the Project Locally

### 📦 Installation

Since the backend API is already hosted live on Render, setting up the frontend locally is incredibly fast. Follow these steps:

**1️⃣ Clone the repository**
```bash
git clone [https://github.com/nirmalbabu05/Aura-Holidays.git](https://github.com/nirmalbabu05/Aura-Holidays.git)
cd Aura-Holidays
```

**2️⃣ Open the project in your favorite editor**
```bash
code .
```

**3️⃣ Start a local development server**
If you are using VS Code, simply install the **Live Server** extension and click "Go Live" on `index.html`. Alternatively, you can use Python's built-in server:
```bash
python -m http.server 8000
```

**4️⃣ Open the project in your browser at:**
```text
http://localhost:8000/
```

*Note: The frontend will automatically connect to the live Render backend for package fetching, AI generation, and wishlist sync.*

## 🚀 Deployment

This project is optimized for modern edge networks and is instantly deployable. 
* **Frontend Hosting:** Vercel (Configured for continuous deployment from GitHub).
* **Backend Hosting:** Render (Python API).

## 📜 License

This project was built to showcase modern full-stack capabilities, AI integration, and premium UI/UX design.

Made with ❤️ by Nirmal Babu V M
