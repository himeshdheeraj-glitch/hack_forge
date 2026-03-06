# 🚀 Deployment Guide: AI Policy Navigator

Your project is now fully prepared for public deployment. Since you are using **Streamlit**, the most effective way to make it live for the hackathon is via **Streamlit Community Cloud** or **Hugging Face Spaces**.

---

## 🏗️ Option 1: Streamlit Community Cloud (Recommended)
This is the fastest way to get a public URL for your Streamlit app.

1.  **Code is Ready**: I have already pushed your latest code to GitHub:
    👉 **[https://github.com/himeshdheeraj-glitch/hack_forge.git](https://github.com/himeshdheeraj-glitch/hack_forge.git)**
2.  **Connect**: Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3.  **New App**: Click **"Create new app"**.
4.  **Configure**:
    - **Repository**: `himeshdheeraj-glitch/hack_forge`
    - **Branch**: `main`
    - **Main file path**: `app.py`
5.  **Deploy**: Click **"Deploy!"**. Your app will be live on a public URL within minutes.

---

## 🏛️ Option 2: Hugging Face Spaces
Ideal if you want to showcase the AI models as part of a larger ecosystem.

1.  **Create Space**: Go to [huggingface.co/spaces](https://huggingface.co/spaces) and create a new space.
2.  **Select SDK**: Choose **Streamlit** as the SDK.
3.  **Link GitHub**: Connect your GitHub repository `himeshdheeraj-glitch/hack_forge`.
4.  **Launch**: Hugging Face will automatically build and serve your app.

---

## 🐳 Option 3: Docker Deployment (Private Hosting)
If you want to host it on your own server (DigitalOcean, AWS, etc.), I have generated a `Dockerfile` for you below.

### 📄 Dockerfile
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

---

### 🛡️ Critical Reminder: Persistence
Since this app uses `users.json` for storage, note that on Streamlit Cloud, the file system is **ephemeral**. To save user data permanently in production:
- I recommend switching `load_users()` and `save_users()` to use a **Database** (like Supabase or MongoDB). 
- **Would you like me to help you set up a free database connection now?** 🏛️🦾🔭🏁
