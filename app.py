import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Akshay Sharma | Software Engineer",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #f8f6f1;
    --paper: #fffdf8;
    --ink: #16202a;
    --muted: #4d5a67;
    --primary: #0f766e;
    --secondary: #dc4f3d;
    --line: #d8d0c4;
    --glow: rgba(15, 118, 110, 0.15);
}

* { box-sizing: border-box; }

html, body, [class*="css"]  {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink);
}

body, .stApp {
    background:
        radial-gradient(circle at 90% 10%, rgba(220, 79, 61, 0.14), transparent 42%),
        radial-gradient(circle at 10% 20%, rgba(15, 118, 110, 0.15), transparent 40%),
        var(--bg);
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0;
    max-width: 1080px;
}

.section {
    margin: 2.25rem 0;
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 2.25rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
    animation: rise 700ms ease both;
}

@keyframes rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 1.8rem;
    align-items: stretch;
}

.name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: clamp(2.1rem, 4vw, 3.3rem);
    line-height: 1.1;
    margin: 0 0 0.75rem;
}

.role {
    display: inline-block;
    background: rgba(15, 118, 110, 0.1);
    color: var(--primary);
    border: 1px solid rgba(15, 118, 110, 0.25);
    border-radius: 999px;
    padding: 0.4rem 0.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.lead {
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.75;
}

.badge-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
}

.badge {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.9rem;
    background: #fff;
}

.badge strong {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    color: var(--primary);
    display: block;
}

h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    margin: 0 0 1rem;
}

.subtitle {
    color: var(--muted);
    margin-bottom: 1rem;
}

.card {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem;
    background: #fff;
    margin-bottom: 0.8rem;
}

.card h3 {
    margin: 0 0 0.35rem;
    font-size: 1.05rem;
}

.muted {
    color: var(--muted);
    font-size: 0.95rem;
}

.tagwrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.7rem;
}

.tag {
    font-size: 0.78rem;
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0.25rem 0.6rem;
    background: #fffcf5;
}

.links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-top: 1rem;
}

.links a {
    text-decoration: none;
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 0.5rem 0.8rem;
    background: #fff;
    transition: 180ms ease;
}

.links a:hover {
    transform: translateY(-2px);
    border-color: var(--primary);
    box-shadow: 0 6px 20px var(--glow);
}

.site-footer {
    text-align: center;
    color: var(--muted);
    margin: 2rem 0 1rem;
}

@media (max-width: 900px) {
    .hero { grid-template-columns: 1fr; }
    .section { padding: 1.3rem; border-radius: 18px; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section hero">
  <div>
    <div class="role">Software Development Engineer II @ Amazon</div>
    <h1 class="name">Akshay Sharma</h1>
    <p class="lead">
      I build scalable backend systems, ML-powered products, and clean user-facing experiences.
      My work has supported hundreds of thousands of sellers and high-volume event workflows.
    </p>
    <div class="links">
      <a href="#projects">View Projects</a>
      <a href="#experience">Experience</a>
      <a href="mailto:akshay.3.1999@gmail.com">Email</a>
      <a href="https://linkedin.com/in/akshay399/" target="_blank">LinkedIn</a>
    </div>
  </div>
  <div class="badge-grid">
    <div class="badge"><strong>3+</strong> Years Experience</div>
    <div class="badge"><strong>300K+</strong> Sellers Impacted</div>
    <div class="badge"><strong>1M+</strong> Shipment drops/month</div>
    <div class="badge"><strong>15+</strong> Technologies</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section" id="about">
  <h2>About</h2>
  <p class="subtitle">
    Backend-first engineer with full-stack delivery experience across data platforms, LLM systems, and seller-facing products.
  </p>
  <div class="card">
    I enjoy owning projects end-to-end: architecture, APIs, data pipelines, and product launch.
    My core stack includes Scala, Java/Spring, React, Spark, and AWS services.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section" id="experience">
  <h2>Experience</h2>
  <div class="card">
    <h3>Software Development Engineer II - Amazon</h3>
    <div class="muted">February 2021 - Present | Bengaluru, India</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section" id="projects">
  <h2>Featured Projects</h2>

  <div class="card">
    <h3>SahAI - LLM Chatbot for Sellers</h3>
    <p class="muted">
      Built key systems in an LLM + RAG assistant serving 300K+ active sellers in India,
      including a modular tool management layer and production prompt templates.
    </p>
    <div class="tagwrap">
      <span class="tag">LLM</span><span class="tag">RAG</span><span class="tag">Scala</span>
      <span class="tag">Spring</span><span class="tag">Prompt Engineering</span>
    </div>
  </div>

  <div class="card">
    <h3>Nostradamus - ML Insights Dashboard</h3>
    <p class="muted">
      Led dashboard development with a Scala Spark pipeline on EMR, backend APIs in Spring,
      and a React frontend with Elasticsearch-backed search.
    </p>
    <div class="tagwrap">
      <span class="tag">Spark</span><span class="tag">EMR</span><span class="tag">React</span>
      <span class="tag">Elasticsearch</span><span class="tag">Kinesis</span>
    </div>
  </div>

  <div class="card">
    <h3>Sale Events Planner</h3>
    <p class="muted">
      Delivered a seller recommendation platform for major sales events and simplified data architecture,
      reducing recurring infrastructure costs.
    </p>
    <div class="tagwrap">
      <span class="tag">Spring</span><span class="tag">React</span><span class="tag">DynamoDB</span>
      <span class="tag">Scalable Architecture</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section" id="skills">
  <h2>Skills</h2>
  <div class="card"><strong>Languages:</strong> C++, Java, Scala, JavaScript, TypeScript, Python</div>
  <div class="card"><strong>Web:</strong> Spring, React, Redux, HTML, CSS</div>
  <div class="card"><strong>Data/ML:</strong> Spark, EMR, SageMaker, Elasticsearch</div>
  <div class="card"><strong>Cloud:</strong> AWS, Lambda, Kinesis, SQS, SNS, S3, DynamoDB</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section" id="contact">
  <h2>Contact</h2>
  <div class="card"><strong>Email:</strong> akshay.3.1999@gmail.com</div>
  <div class="card"><strong>LinkedIn:</strong> linkedin.com/in/akshay399/</div>
  <div class="card"><strong>Phone:</strong> +91 9582312294</div>
  <div class="card"><strong>Location:</strong> Bengaluru, India</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="site-footer">
  <p>(c) {datetime.now().year} Akshay Sharma</p>
  <p>Built with Streamlit</p>
</div>
""",
    unsafe_allow_html=True,
)
