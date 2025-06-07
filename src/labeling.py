"""
Risk skoru etiketleme modülü
"""
import pandas as pd

def calculate_risk(row, user_stats):
    risk = 0
    hour = pd.to_datetime(row['CreatedAt']).hour
    if hour < 8 or hour > 18:
        risk += 30
    if row['ClientIP'] != user_stats[row['UserId']]['base_ip']:
        risk += 20
    if row['MFAMethod'] != user_stats[row['UserId']]['base_mfa']:
        risk += 10
    if row['Browser'] != user_stats[row['UserId']]['base_browser']:
        risk += 10
    if row['OS'] != user_stats[row['UserId']]['base_os']:
        risk += 10
    if row['Application'] != user_stats[row['UserId']]['base_app']:
        risk += 5
    if row['Unit'] != user_stats[row['UserId']]['base_unit']:
        risk += 5
    if row['Title'] != user_stats[row['UserId']]['base_title']:
        risk += 5
    return min(risk, 100)

def label_risk_scores(df):
    user_stats = {}
    for user in df['UserId'].unique():
        user_logs = df[df['UserId'] == user]
        user_stats[user] = {
            'base_ip': user_logs['ClientIP'].mode()[0],
            'base_mfa': user_logs['MFAMethod'].mode()[0],
            'base_browser': user_logs['Browser'].mode()[0],
            'base_os': user_logs['OS'].mode()[0],
            'base_app': user_logs['Application'].mode()[0],
            'base_unit': user_logs['Unit'].mode()[0],
            'base_title': user_logs['Title'].mode()[0],
        }
    df['RiskScore'] = df.apply(lambda row: calculate_risk(row, user_stats), axis=1)
    return df