# Personal Portfolio Website - Streamlit

A modern, interactive personal portfolio website built with Streamlit to showcase your projects, skills, and professional information.

## 🚀 Features

- **Responsive Design**: Modern UI with custom CSS styling
- **Project Showcase**: Display your projects with filtering by category
- **Skills Analytics**: Interactive charts showing your technical skills
- **Contact Form**: Easy way for visitors to get in touch
- **Blog Section**: Share your thoughts and articles
- **Navigation**: Clean sidebar navigation between sections

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd personal-website-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
personal-website-streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── assets/               # Images, icons, and other static files
│   ├── profile.jpg
│   └── project_images/
├── data/                 # Data files (if needed)
│   └── projects.json
└── .gitignore           # Git ignore file
```

## 🎨 Customization

### Personal Information
Edit the following sections in `app.py`:
- Your name and title
- About me section
- Contact information
- Skills and technologies

### Projects
Update the `projects_data` list in `app.py` with your actual projects:
```python
projects_data = [
    {
        "name": "Your Project Name",
        "description": "Project description",
        "technologies": ["Tech1", "Tech2"],
        "github": "https://github.com/yourusername/project",
        "demo": "https://demo-link.com",
        "image": "🛒",
        "category": "Web Development"
    }
]
```

### Skills
Modify the `skills_data` dictionary to reflect your actual skills:
```python
skills_data = {
    "Programming Languages": ["Python", "JavaScript", "Java"],
    "Web Technologies": ["React", "Node.js", "HTML/CSS"],
    # Add more categories as needed
}
```

### Styling
Customize the CSS in the `st.markdown()` section to match your preferred color scheme and styling.

## 📊 Available Pages

1. **🏠 Home**: Introduction, about me, and quick stats
2. **💼 Projects**: Showcase of your projects with filtering
3. **📊 Skills & Analytics**: Interactive charts and skill breakdown
4. **📞 Contact**: Contact form and information
5. **📝 Blog**: Blog posts and articles

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy using Heroku CLI or GitHub integration

### Other Platforms
- **Vercel**: Use the Streamlit adapter
- **Railway**: Direct deployment from GitHub
- **DigitalOcean**: Deploy on App Platform

## ⏱️ IRAN Watch (static + hourly updater)

This repo includes a simple static page in `static-site/` that reads `static-site/data.json` and shows:
- The **most recent post mentioning** the keyword (default: **IRAN**)
- A **countdown** to the next top-of-hour refresh

### How it updates hourly

This project can update `static-site/data.json` two ways:
- **Local scheduled (recommended)**: Twitter API v2 (reads the last \(\sim\)1 hour of tweets)
- **GitHub scheduled (fallback)**: RSS/Atom feed URL

### Option A: Local scheduled updater (Twitter API v2)

1. Copy `.env.example` → `.env`
2. Fill in:
   - `TWITTER_BEARER_TOKEN`
   - `TWITTER_USERNAME` (e.g. `realDonaldTrump`)
   - optional: `OPENAI_API_KEY` if you want the LLM to filter “actually about IRAN” vs a stray mention
3. Run once:
   - `powershell -ExecutionPolicy Bypass -File scripts/run_update.ps1`
4. Schedule it hourly using **Windows Task Scheduler**:
   - Action: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\personal-website-streamlit\scripts\run_update.ps1"`
   - Trigger: “Daily” → “Repeat task every: 1 hour”

### Option B: GitHub scheduled updater (Twitter API or RSS)

If you host this repo on GitHub, the workflow `Update IRAN timer` runs **every 5 minutes (best-effort)** and rewrites `static-site/data.json`.

- **Twitter API mode**:
  - Repo Secret: `TWITTER_BEARER_TOKEN`
  - Repo Variable: `TWITTER_USERNAME`
  - Optional Secret: `OPENAI_API_KEY`
  - Optional Variable: `OPENAI_MODEL`

- **RSS/Atom fallback mode**:
  - Repo Variable: `TRUMP_FEED_URL` (RSS/Atom URL)

### Hosting the static page

You can deploy `static-site/` to any static host.

- **GitHub Pages**: configure Pages to serve from the `static-site/` folder (or move/copy it to the publishing root, depending on your Pages setup).

## 🔧 Configuration

### Environment Variables
Create a `.env` file for sensitive information:
```
EMAIL_PASSWORD=your_email_password
GITHUB_TOKEN=your_github_token
```

### Streamlit Configuration
Create `.streamlit/config.toml` for custom configuration:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 📝 Adding New Features

### New Page
1. Add the page to the navigation selectbox
2. Create the page content in the main if-elif structure
3. Add any necessary data or functions

### New Project
1. Add project data to `projects_data` list
2. Update categories if needed
3. Add project images to `assets/project_images/`

### Contact Form Integration
1. Set up email service (SendGrid, SMTP, etc.)
2. Add form processing logic
3. Handle form submissions securely

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Icons from [Emoji](https://emojipedia.org/)
- Charts powered by [Plotly](https://plotly.com/)

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Contact: your.email@example.com
- LinkedIn: linkedin.com/in/yourprofile

---

**Happy coding! 🚀** 