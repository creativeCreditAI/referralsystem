import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "creativecreditai@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_welcome_email(user_email: str, user_name: str, referral_token: str):
    """Send a welcome email to newly registered user."""
    if not GMAIL_APP_PASSWORD:
        print(f"⚠️  Email service not configured. Would send to: {user_email}")
        return

    referral_link = f"{FRONTEND_URL}/signup?ref={referral_token}"

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: 'Inter', sans-serif; color: #2c2140; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4b2f69, #ff8a1f); padding: 20px; border-radius: 8px; color: white; }}
                .content {{ padding: 20px 0; line-height: 1.6; }}
                .referral-box {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff8a1f; }}
                .link {{ color: #ff8a1f; text-decoration: none; font-weight: bold; }}
                .button {{ display: inline-block; background: #4b2f69; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin: 10px 0; }}
                .footer {{ border-top: 1px solid #ddd; padding-top: 20px; font-size: 0.9rem; color: #999; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Korva! 🎉</h1>
                </div>
                
                <div class="content">
                    <p>Hi {user_name},</p>
                    
                    <p>Thank you for registering with <strong>Korva</strong>! You're now part of our growing community.</p>
                    
                    <p>Start building your network and earning rewards by sharing your referral link with friends and colleagues:</p>
                    
                    <div class="referral-box">
                        <p><strong>Your Referral Link:</strong></p>
                        <p><code>{referral_link}</code></p>
                        <p>Share this link to invite others and earn rewards for every successful signup!</p>
                    </div>
                    
                    <p><a href="{FRONTEND_URL}" class="button">Visit Korva</a></p>
                    
                    <p>Questions? Learn more at <a href="https://bunifucapital.com" class="link">bunifucapital.com</a></p>
                </div>
                
                <div class="footer">
                    <p>© 2026 Korva. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Welcome to Korva, {user_name}! 🚀"
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = user_email
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, user_email, msg.as_string())

        print(f"✓ Welcome email sent to {user_email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send email to {user_email}: {str(e)}")
        return None


def send_referral_bonus_email(user_email: str, user_name: str, referrer_name: str, reward_points: int):
    """Send email to user when they earn rewards through a referral."""
    if not GMAIL_APP_PASSWORD:
        print(f"⚠️  Email service not configured. Would send to: {user_email}")
        return

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: 'Inter', sans-serif; color: #2c2140; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4b2f69, #ff8a1f); padding: 20px; border-radius: 8px; color: white; }}
                .content {{ padding: 20px 0; line-height: 1.6; }}
                .badge {{ display: inline-block; background: #ff8a1f; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; }}
                .footer {{ border-top: 1px solid #ddd; padding-top: 20px; font-size: 0.9rem; color: #999; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>You've Earned Rewards! 🏆</h1>
                </div>
                
                <div class="content">
                    <p>Hi {user_name},</p>
                    
                    <p>Great news! <strong>{referrer_name}</strong> referred you to Korva, and you've both earned rewards!</p>
                    
                    <p>Your reward: <span class="badge">{reward_points} Points</span></p>
                    
                    <p>Keep growing your network and earn even more rewards!</p>
                </div>
                
                <div class="footer">
                    <p>© 2026 Korva. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎉 You earned {reward_points} points!"
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = user_email
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, user_email, msg.as_string())

        print(f"✓ Reward email sent to {user_email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send reward email to {user_email}: {str(e)}")
        return None
