import { useEffect, useMemo, useState } from 'react';
import { createReferral, signupWithReferral, getStats } from './api';

function getSearchParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function buildReferralUrl(token) {
  const baseUrl = window.location.origin;
  return `${baseUrl}/signup?ref=${token}`;
}

function isSignupRoute() {
  return window.location.pathname === '/signup' || window.location.pathname.startsWith('/signup');
}

export default function App() {
  const signupMode = isSignupRoute();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [position, setPosition] = useState('');
  const [refToken, setRefToken] = useState(getSearchParam('ref') || '');
  const [referralLink, setReferralLink] = useState('');
  const [copied, setCopied] = useState(false);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ total_users: 0, total_referrals: 0, total_rewards: 0 });

  useEffect(() => {
    const token = getSearchParam('ref');
    if (token) setRefToken(token);

    getStats()
      .then(data => setStats(data))
      .catch(err => console.error('Failed to fetch stats:', err));
  }, []);

  const previewLink = useMemo(() => {
    if (referralLink) return referralLink;
    return refToken ? buildReferralUrl(refToken) : buildReferralUrl('your-token');
  }, [refToken, referralLink]);

  async function handleGenerate(event) {
    event.preventDefault();
    setLoading(true);
    setStatus('');

    try {
      const data = await createReferral({ name, email, position: 'User' });
      setReferralLink(data.referral_link || '');
      setRefToken(data.referral_token || '');
      setStatus('✓ Referral created successfully! Share your link.');
      setName('');
      setEmail('');
      setPosition('');
    } catch (error) {
      setStatus(`✗ ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleSignup(event) {
    event.preventDefault();
    setLoading(true);
    setStatus('');

    try {
      await signupWithReferral({ name, email, position }, refToken);
      setStatus('✓ Signup completed! Welcome aboard.');
      setName('');
      setEmail('');
      setPosition('');
    } catch (error) {
      setStatus(`✗ ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    const text = previewLink;
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1200);
    } catch (err) {
      setStatus('Failed to copy to clipboard');
    }
  }

  return (
    <div className="page">
      <header className="app-header">
        <img src="/krova-logo.svg" alt="Korva" className="logo" />
      </header>
      <section className="hero">
        <div className="brand-block">
          <div className="brand-mark">K</div>
          <div>
            <p className="eyebrow">Referral Dashboard</p>
            <h1>Grow your network with unique referral links.</h1>
            <p className="hero-copy">
              {signupMode
                ? 'Join through a referral and earn rewards.'
                : 'Generate a unique link, share it, and track successful signups.'}
            </p>
          </div>
        </div>

        <div className="hero-art" aria-hidden="true">
          <div className="orb orb-one" />
          <div className="orb orb-two" />
          <div className="brand-shape">
            <span className="shape-a" />
            <span className="shape-b" />
            <span className="shape-c" />
            <span className="shape-d" />
          </div>
        </div>
      </section>

      <main className="grid">
        <section className="card accent-card">
          <h2>{signupMode ? 'Join with a referral' : 'Create a referral link'}</h2>
          <form className="form" onSubmit={signupMode ? handleSignup : handleGenerate}>
            <label>
              Full Name
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Jane Doe"
                required
              />
            </label>

            <label>
              Email
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jane@example.com"
                type="email"
                required
              />
            </label>

            {signupMode && (
              <label>
                Position / Industry
                <select
                  value={position}
                  onChange={(e) => setPosition(e.target.value)}
                  required
                >
                  <option value="">-- Select one --</option>
                  <option value="Creative">Creative</option>
                  <option value="Financial Institution">Financial Institution</option>
                </select>
              </label>
            )}

            {signupMode && refToken ? (
              <div className="ref-display">
                <label>Referral Token</label>
                <code>{refToken}</code>
              </div>
            ) : null}

            <button type="submit" disabled={loading}>
              {loading ? 'Processing...' : signupMode ? 'Complete signup' : 'Generate referral'}
            </button>
          </form>

          {status ? <p className={`status ${status.startsWith('✓') ? 'success' : 'error'}`}>{status}</p> : null}
        </section>

        <section className="card">
          <h2>Referral link</h2>
          <p className="muted">
            {signupMode
              ? 'Share this with your friends to earn rewards.'
              : 'Share this unique link to start building your network.'}
          </p>
          <div className="link-box">
            <code>{previewLink}</code>
          </div>
          <div className="actions">
            <button type="button" onClick={handleCopy}>
              {copied ? '✓ Copied!' : 'Copy link'}
            </button>
          </div>
        </section>

        <section className="card stats-card">
          <h2>Community</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-icon">👥</div>
              <strong>{stats.total_users}</strong>
              <span>Registered Users</span>
            </div>
            <div className="stat-item">
              <div className="stat-icon">🎯</div>
              <strong>{stats.total_referrals}</strong>
              <span>Successful Referrals</span>
            </div>
            <div className="stat-item">
              <div className="stat-icon">🏆</div>
              <strong>{stats.total_rewards}</strong>
              <span>Total Rewards</span>
            </div>
          </div>
        </section>
      </main>
      <footer className="app-footer">
        <p>Learn more at <a href="https://bunifucapital.com" target="_blank" rel="noopener noreferrer">bunifucapital.com</a></p>
      </footer>
    </div>
  );
}
