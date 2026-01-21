import requests
import sqlite3
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"
CACHE_DURATION_HOURS = 24
DB_PATH = "kernel_secmon.db"


def extract_ips_from_details(details: str) -> List[str]:
    """
    Extract IP addresses from event details string.
    Supports both IPv4 and basic IPv6 patterns.
    """
    # IPv4 pattern
    ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    # Find all IPv4 addresses
    ips = re.findall(ipv4_pattern, details)
    
    # Filter out invalid IPs (e.g., 999.999.999.999)
    valid_ips = []
    for ip in ips:
        parts = ip.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            # Skip private/local IPs
            if not (parts[0] in ['10', '127'] or 
                   (parts[0] == '172' and 16 <= int(parts[1]) <= 31) or
                   (parts[0] == '192' and parts[1] == '168')):
                valid_ips.append(ip)
    
    return valid_ips


def init_threat_intel_db():
    """Initialize threat intelligence cache table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threat_intel_cache (
            ip TEXT PRIMARY KEY,
            threat_score INTEGER,
            is_malicious BOOLEAN,
            abuse_count INTEGER,
            country_code TEXT,
            isp TEXT,
            domain TEXT,
            report_url TEXT,
            cached_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def get_cached_threat_intel(ip: str) -> Optional[Dict]:
    """Retrieve cached threat intelligence if not expired."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM threat_intel_cache WHERE ip = ?',
        (ip,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # Check if cache is still valid
    cached_at = datetime.fromisoformat(row['cached_at'])
    if datetime.now() - cached_at > timedelta(hours=CACHE_DURATION_HOURS):
        return None
    
    return dict(row)


def save_threat_intel(ip: str, data: Dict):
    """Save threat intelligence data to cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO threat_intel_cache 
        (ip, threat_score, is_malicious, abuse_count, country_code, isp, domain, report_url, cached_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ip,
        data.get('abuseConfidenceScore', 0),
        data.get('abuseConfidenceScore', 0) > 50,
        data.get('totalReports', 0),
        data.get('countryCode', 'Unknown'),
        data.get('isp', 'Unknown'),
        data.get('domain', 'Unknown'),
        f"https://www.abuseipdb.com/check/{ip}",
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()


def check_ip_reputation(ip: str) -> Dict:
    """
    Check IP reputation using AbuseIPDB API.
    Returns cached data if available, otherwise makes API call.
    """
    # Check cache first
    cached = get_cached_threat_intel(ip)
    if cached:
        return {
            'ip': ip,
            'threat_score': cached['threat_score'],
            'is_malicious': bool(cached['is_malicious']),
            'abuse_count': cached['abuse_count'],
            'country_code': cached['country_code'],
            'isp': cached['isp'],
            'domain': cached['domain'],
            'report_url': cached['report_url'],
            'cached': True
        }
    
    # If no API key, return placeholder data
    if not ABUSEIPDB_API_KEY:
        return {
            'ip': ip,
            'threat_score': 0,
            'is_malicious': False,
            'abuse_count': 0,
            'country_code': 'Unknown',
            'isp': 'Unknown',
            'domain': 'Unknown',
            'report_url': f"https://www.abuseipdb.com/check/{ip}",
            'cached': False,
            'error': 'No API key configured'
        }
    
    try:
        # Make API request
        headers = {
            'Accept': 'application/json',
            'Key': ABUSEIPDB_API_KEY
        }
        params = {
            'ipAddress': ip,
            'maxAgeInDays': '90',
            'verbose': ''
        }
        
        response = requests.get(
            ABUSEIPDB_API_URL,
            headers=headers,
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            # Save to cache
            save_threat_intel(ip, data)
            
            return {
                'ip': ip,
                'threat_score': data.get('abuseConfidenceScore', 0),
                'is_malicious': data.get('abuseConfidenceScore', 0) > 50,
                'abuse_count': data.get('totalReports', 0),
                'country_code': data.get('countryCode', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'domain': data.get('domain', 'Unknown'),
                'report_url': f"https://www.abuseipdb.com/check/{ip}",
                'cached': False
            }
        else:
            return {
                'ip': ip,
                'threat_score': 0,
                'is_malicious': False,
                'abuse_count': 0,
                'country_code': 'Unknown',
                'isp': 'Unknown',
                'domain': 'Unknown',
                'report_url': f"https://www.abuseipdb.com/check/{ip}",
                'cached': False,
                'error': f'API error: {response.status_code}'
            }
    except Exception as e:
        return {
            'ip': ip,
            'threat_score': 0,
            'is_malicious': False,
            'abuse_count': 0,
            'country_code': 'Unknown',
            'isp': 'Unknown',
            'domain': 'Unknown',
            'report_url': f"https://www.abuseipdb.com/check/{ip}",
            'cached': False,
            'error': str(e)
        }


def enrich_event_with_threat_intel(event_details: str) -> Dict:
    """
    Main function to enrich event with threat intelligence.
    Extracts IPs from event details and checks their reputation.
    """
    ips = extract_ips_from_details(event_details)
    
    if not ips:
        return {
            'has_network_activity': False,
            'checked_ips': [],
            'malicious_ips': [],
            'max_threat_score': 0
        }
    
    results = []
    malicious_ips = []
    max_score = 0
    
    for ip in ips[:5]:  # Limit to first 5 IPs to avoid rate limits
        intel = check_ip_reputation(ip)
        results.append(intel)
        
        if intel['is_malicious']:
            malicious_ips.append(intel)
        
        max_score = max(max_score, intel['threat_score'])
    
    return {
        'has_network_activity': True,
        'checked_ips': results,
        'malicious_ips': malicious_ips,
        'max_threat_score': max_score,
        'total_ips_found': len(ips)
    }


# Initialize the threat intel cache table
init_threat_intel_db()
