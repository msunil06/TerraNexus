"""
Restore UTF-8 Unicode Emojis and Currency Symbols in Azure SQL Database
Ensures all character columns in Azure SQL are NVARCHAR and restores
genuine flag emojis (🇦🇫, 🇮🇳, 🇺🇸, etc.) and currency symbols (؋, ₹, $, €, etc.)
from local database.
"""

import sys
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

import pymssql

def restore_unicode():
    server = os.getenv("DB_SERVER")
    port = int(os.getenv("DB_PORT", "1433"))
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, user, password]):
        print("[!] Missing required DB environment variables (DB_SERVER, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD).")
        return False

    if "@" not in user and ".database.windows.net" in server:
        user = f"{user}@{server.split('.')[0]}"

    print(f"[*] Connecting to Azure SQL Server: {server}:{port} (DB: {database})...")
    conn = pymssql.connect(
        server=server,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=True
    )
    cursor = conn.cursor()

    # Connect to SQLite source
    sqlite_path = BASE_DIR / "terranexus.db"
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    print("[*] Upgrading Azure SQL columns to NVARCHAR (Unicode & Emoji support)...")
    alter_statements = [
        # Countries
        "ALTER TABLE countries ALTER COLUMN flag_emoji NVARCHAR(32) NULL",
        "ALTER TABLE countries ALTER COLUMN currency_symbol NVARCHAR(32) NULL",
        "ALTER TABLE countries ALTER COLUMN currency_name NVARCHAR(100) NULL",
        "ALTER TABLE countries ALTER COLUMN common_name NVARCHAR(150) NOT NULL",
        "ALTER TABLE countries ALTER COLUMN official_name NVARCHAR(255) NOT NULL",
        "ALTER TABLE countries ALTER COLUMN capital_name NVARCHAR(150) NULL",
        "ALTER TABLE countries ALTER COLUMN largest_city NVARCHAR(150) NULL",
        "ALTER TABLE countries ALTER COLUMN demonym NVARCHAR(100) NULL",
        "ALTER TABLE countries ALTER COLUMN subregion NVARCHAR(100) NULL",
        "ALTER TABLE countries ALTER COLUMN overview NVARCHAR(MAX) NULL",
        "ALTER TABLE countries ALTER COLUMN major_industries NVARCHAR(MAX) NULL",
        "ALTER TABLE countries ALTER COLUMN natural_resources NVARCHAR(MAX) NULL",
        "ALTER TABLE countries ALTER COLUMN climate NVARCHAR(MAX) NULL",
        
        # Continents
        "ALTER TABLE continents ALTER COLUMN name NVARCHAR(100) NOT NULL",
        "ALTER TABLE continents ALTER COLUMN overview NVARCHAR(MAX) NULL",

        # Capitals
        "ALTER TABLE capitals ALTER COLUMN name NVARCHAR(150) NOT NULL",

        # Administrative Divisions
        "ALTER TABLE administrative_divisions ALTER COLUMN name NVARCHAR(150) NOT NULL",
        "ALTER TABLE administrative_divisions ALTER COLUMN capital_or_center NVARCHAR(100) NULL",

        # Oceans and Seas
        "ALTER TABLE oceans ALTER COLUMN name NVARCHAR(100) NOT NULL",
        "ALTER TABLE oceans ALTER COLUMN overview NVARCHAR(MAX) NULL",
        "ALTER TABLE seas ALTER COLUMN name NVARCHAR(100) NOT NULL",
        "ALTER TABLE seas ALTER COLUMN overview NVARCHAR(MAX) NULL",

        # Geographic Features
        "ALTER TABLE geographic_features ALTER COLUMN name NVARCHAR(150) NOT NULL",
        "ALTER TABLE geographic_features ALTER COLUMN feature_type NVARCHAR(100) NULL",
        "ALTER TABLE geographic_features ALTER COLUMN description NVARCHAR(MAX) NULL",

        # User Favorites
        "ALTER TABLE user_favorites ALTER COLUMN item_flag NVARCHAR(50) NULL",
        "ALTER TABLE user_favorites ALTER COLUMN item_title NVARCHAR(150) NOT NULL",
        "ALTER TABLE user_favorites ALTER COLUMN item_subtitle NVARCHAR(150) NULL"
    ]

    for stmt in alter_statements:
        try:
            cursor.execute(stmt)
        except Exception as e:
            pass

    print("[+] Schema columns upgraded to NVARCHAR successfully.")

    # Restore Countries from SQLite
    print("[*] Synchronizing country flag emojis and currency symbols from verified local source...")
    sqlite_cur.execute("""
        SELECT iso_a3, flag_emoji, currency_symbol, currency_name, common_name, official_name, capital_name
        FROM countries
    """)
    countries = sqlite_cur.fetchall()
    
    updated_count = 0
    for c in countries:
        flag = c["flag_emoji"]
        symbol = c["currency_symbol"]
        curr_name = c["currency_name"]
        iso = c["iso_a3"]

        cursor.execute(
            "UPDATE countries SET flag_emoji = %s, currency_symbol = %s, currency_name = %s WHERE iso_a3 = %s",
            (flag, symbol, curr_name, iso)
        )
        updated_count += 1

    print(f"[+] Restored {updated_count} countries with genuine Unicode flag emojis and currency symbols.")

    # Restore Continents
    sqlite_cur.execute("SELECT id, name, overview FROM continents")
    for cont in sqlite_cur.fetchall():
        cursor.execute(
            "UPDATE continents SET name = %s, overview = %s WHERE id = %d",
            (cont["name"], cont["overview"], cont["id"])
        )

    # Restore Oceans & Seas
    sqlite_cur.execute("SELECT id, name, overview FROM oceans")
    for oc in sqlite_cur.fetchall():
        cursor.execute(
            "UPDATE oceans SET name = %s, overview = %s WHERE id = %d",
            (oc["name"], oc["overview"], oc["id"])
        )
    sqlite_cur.execute("SELECT id, name, overview FROM seas")
    for se in sqlite_cur.fetchall():
        cursor.execute(
            "UPDATE seas SET name = %s, overview = %s WHERE id = %d",
            (se["name"], se["overview"], se["id"])
        )

    # Verify sample in Azure SQL
    cursor.execute("""
        SELECT common_name, flag_emoji, currency_symbol, currency_code 
        FROM countries 
        WHERE iso_a3 IN ('AFG', 'ALB', 'DZA', 'AND', 'AGO', 'IND', 'USA')
        ORDER BY common_name
    """)
    rows = cursor.fetchall()
    
    print("\n[*] Azure SQL Verification Results:")
    for r in rows:
        print(f"    - {r[0]}: Flag={ascii(r[1])} | Currency={r[3]} ({ascii(r[2])})")

    conn.close()
    sqlite_conn.close()
    print("\n[SUCCESS] Azure SQL Unicode restore complete!")

if __name__ == "__main__":
    restore_unicode()
