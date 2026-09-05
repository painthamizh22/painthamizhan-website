const skills = ['Financial Analysis','Investment Analysis','Budgeting','Forecasting','Valuation'];
const tools = ['Microsoft Excel','Microsoft Word','Microsoft PowerPoint','Google Workspace'];
const strengths = ['Analytical Thinking','Strong Learning Agility','Effective Communication','Problem Solving','Teamwork','Time Management','Presentation Skills'];

export default function Home() {
  return (
    <main>
      <nav className="nav"><div className="logo">PS.</div><div className="links"><a href="#about">About</a><a href="#education">Education</a><a href="#skills">Skills</a><a href="#interests">Interests</a><a href="#contact">Contact</a></div></nav>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">B.COM FINANCE & INVESTMENT • CHRIST UNIVERSITY</p>
          <h1>Painthamizhan <span>S.</span></h1>
          <h2>Building a career around <em>finance, markets & investment.</em></h2>
          <p className="intro">First-year Finance & Investment student focused on financial analysis, investment research and understanding how capital creates long-term value.</p>
          <div className="buttons"><a className="primary" href="#contact">Let’s connect ↗</a><a className="secondary" href="#about">Explore my profile ↓</a></div>
        </div>
        <div className="hero-card"><div className="orb">PS</div><p>FINANCE<br/><strong>& INVESTMENT</strong></p><div className="line"/><small>Bengaluru, India</small></div>
      </section>

      <section id="about" className="section split"><div><p className="label">01 / ABOUT</p><h2>Curious about<br/><em>how money moves.</em></h2></div><div className="body-copy"><p>I’m a motivated B.Com Finance & Investment student at Christ University, Yeshwanthpur Campus, with a strong interest in financial markets and investment analysis.</p><p>I enjoy developing my analytical thinking, communication and presentation skills while turning classroom concepts into practical understanding.</p></div></section>

      <section id="education" className="section"><p className="label">02 / EDUCATION</p><div className="edu"><div><span>2025 — 2029</span><h3>Bachelor of Commerce</h3><p>Finance & Investment</p></div><div><h4>Christ University</h4><p>Yeshwanthpur Campus · 1st Semester</p></div></div><div className="edu"><div><span>COMPLETED</span><h3>Higher Secondary Education</h3><p>Class XII</p></div><div><h4>89%</h4><p>Academic Score</p></div></div></section>

      <section id="skills" className="section skills-section"><p className="label">03 / SKILLS</p><div className="skill-grid"><div><h3>Finance & Domain</h3>{skills.map(x=><div className="skill" key={x}>{x}<span>↗</span></div>)}</div><div><h3>Technical</h3>{tools.map(x=><div className="skill" key={x}>{x}<span>↗</span></div>)}</div><div><h3>Core Strengths</h3>{strengths.map(x=><div className="skill" key={x}>{x}<span>↗</span></div>)}</div></div></section>

      <section id="interests" className="section dark"><p className="label">04 / AREAS OF INTEREST</p><h2>Where I want to<br/><em>go deeper.</em></h2><div className="interest-grid">{['Financial Analysis','Investment Research','Financial Markets','Investment Analysis','Equity & Stock Market Analysis'].map((x,i)=><div className="interest" key={x}><b>0{i+1}</b><span>{x}</span><span>↗</span></div>)}</div></section>

      <section className="section objective"><p className="label">05 / CAREER OBJECTIVE</p><h2>Learn. Analyze. <em>Invest.</em></h2><p>Seeking opportunities in Financial Analysis where I can apply my academic knowledge and analytical abilities, gain practical experience, and develop professionally in the finance and investment industry.</p></section>

      <footer id="contact"><div><p className="label">LET’S CONNECT</p><h2>Have an opportunity?<br/><em>Let’s talk.</em></h2></div><a href="mailto:painthamizhan22@gmail.com">painthamizhan22@gmail.com ↗</a><small>© 2026 Painthamizhan S. · Bengaluru, India</small></footer>
    </main>
  );
}
