"""
Mock veri üretimi modülü
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime
import random

def generate_mock_data(user_count=10, log_per_user=3, seed=42, save_path=None):
    """
    Gerçekçi mock login verisi üretir.
    """
    fake = Faker()
    np.random.seed(seed)
    random.seed(seed)
    users = [f"U{10000+i}" for i in range(user_count)]
    mfa_methods = ["SMS", "OTP", "Mail"]
    applications = ["CRM", "HR System"]
    browsers = ["Chrome", "Firefox", "Edge", "Safari"]
    oses = ["Windows 10", "macOS", "Linux"]
    units = ["Bilgi İşlem", "Satış", "Finans", "İK"]
    titles = ["Takım Lideri", "Uzman", "Yönetici", "Stajyer"]

    def generate_login_time(is_normal):
        # İş saatleri: 08:00-18:00
        if is_normal:
            hour = random.randint(8, 18)
        else:
            hour = random.choice(list(range(0, 8)) + list(range(19, 24)))
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        day = random.randint(1, 28)
        return datetime(2025, 5, day, hour, minute, second)

    data = []
    for user in users:
        base_ip = fake.ipv4_private()
        unit = random.choice(units)
        title = random.choice(titles)
        for _ in range(log_per_user):
            is_normal = np.random.rand() > 0.08  # %8 rastgelelik
            created_at = generate_login_time(is_normal)
            client_ip = base_ip if is_normal else fake.ipv4_private()
            mfa = random.choices(mfa_methods, weights=[0.7, 0.2, 0.1])[0] if is_normal else random.choice(mfa_methods)
            app = random.choice(applications)
            browser = random.choices(browsers, weights=[0.6, 0.2, 0.1, 0.1])[0] if is_normal else random.choice(browsers)
            os = random.choices(oses, weights=[0.7, 0.2, 0.1])[0] if is_normal else random.choice(oses)
            data.append([
                user, mfa, created_at, client_ip, app, browser, os, unit, title
            ])
    df = pd.DataFrame(data, columns=[
        "UserId", "MFAMethod", "CreatedAt", "ClientIP", "Application", "Browser", "OS", "Unit", "Title"
    ])
    if save_path:
        df.to_csv(save_path, index=False)
    return df