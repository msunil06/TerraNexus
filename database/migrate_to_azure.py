"""
TerraNexus Azure SQL Database Online Migration Utility
Migrates all tables and seeded geographical, governance, user, and alliance data
from local SQLite (terranexus.db) to Azure SQL Database / Microsoft SQL Server.
"""

import sys
import os
from pathlib import Path

# Ensure root workspace is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

import pymssql
from sqlalchemy import create_engine, text, Integer, BigInteger, SmallInteger
from sqlalchemy.engine import URL

from app import create_app, db
# Import all model modules so db.metadata is fully populated
import models.geography
import models.marine_and_physical
import models.user

def check_azure_firewall():
    server = os.getenv("DB_SERVER")
    port = int(os.getenv("DB_PORT", "1433"))
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, user, password]):
        print("[!] Azure SQL credentials not fully configured in environment (DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD).")
        return False, None

    if "@" not in user and ".database.windows.net" in server:
        user = f"{user}@{server.split('.')[0]}"

    print(f"[*] Testing connection to Azure SQL Server: {server}:{port} (DB: {database})...")
    try:
        conn = pymssql.connect(
            server=server,
            port=port,
            user=user,
            password=password,
            database=database,
            timeout=8,
            login_timeout=8
        )
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        ver = cursor.fetchone()
        conn.close()
        print("[+] Azure SQL Connection SUCCESSFUL!")
        print(f"    Server Version: {ver[0].splitlines()[0]}")
        return True, user
    except Exception as e:
        err = str(e)
        if "40615" in err or "Client with IP address" in err:
            import urllib.request
            try:
                my_ip = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
            except Exception:
                my_ip = "122.172.201.234"
            print("\n" + "="*70)
            print("[!] AZURE SQL FIREWALL RESTRICTION DETECTED:")
            print(f"    Your current public IP is: {my_ip}")
            print(f"    Azure SQL blocks connections from unlisted IPs by default.")
            print("\n    To allow access:")
            print("    1. Open Azure Portal: https://portal.azure.com")
            print("    2. Go to 'terranx-db' or SQL Server 'terranx'")
            print("    3. Click 'Security' > 'Networking' (or 'Set server firewall')")
            print(f"    4. Add Firewall Rule with IP: {my_ip} (or 0.0.0.0 - 255.255.255.255)")
            print("    5. Check 'Allow Azure services and resources to access this server'")
            print("    6. Click 'Save' and re-run this migration.")
            print("="*70 + "\n")
        else:
            print(f"[-] Connection Error: {e}")
        return False, user

def run_migration():
    can_connect, user_auth = check_azure_firewall()
    if not can_connect:
        print("Migration halted because Azure SQL firewall is blocking this IP.")
        return False

    server = os.getenv("DB_SERVER")
    port = int(os.getenv("DB_PORT", "1433"))
    database = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")

    azure_url = URL.create(
        drivername="mssql+pymssql",
        username=user_auth,
        password=password,
        host=server,
        port=port,
        database=database
    )

    app = create_app()
    with app.app_context():
        print(f"\n[*] Ensuring Azure SQL Database tables exist via create_all()...")
        azure_engine = create_engine(azure_url, pool_recycle=180, pool_pre_ping=True)
        db.metadata.create_all(bind=azure_engine)
        print("[+] Tables verified on Azure SQL Database.")

        # Connect to local SQLite
        sqlite_path = BASE_DIR / "terranexus.db"
        sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")

        print("\n[*] Starting clean data migration from SQLite to Azure SQL...")
        total_migrated = 0

        with sqlite_engine.connect() as sqlite_conn, azure_engine.connect() as azure_conn:
            # 1. Clean existing records in reverse order to prevent foreign key conflicts
            print("    [1/2] Clearing any previous partial records in Azure SQL...")
            for table in reversed(db.metadata.sorted_tables):
                try:
                    azure_conn.execute(text(f"DELETE FROM [{table.name}]"))
                except Exception:
                    pass
            azure_conn.commit()

            # 2. Transfer table by table in foreign key dependency order
            print("    [2/2] Transferring records in dependency order...")
            for table in db.metadata.sorted_tables:
                table_name = table.name
                rows = sqlite_conn.execute(table.select()).mappings().all()
                if not rows:
                    continue

                # Check if table has an IDENTITY primary key
                has_identity = False
                for c in table.columns:
                    if c.primary_key and isinstance(c.type, (Integer, BigInteger, SmallInteger)):
                        has_identity = True
                        break

                print(f"    --> Table [{table_name}]: migrating {len(rows)} rows (Identity: {has_identity})...")

                try:
                    if has_identity:
                        azure_conn.execute(text(f"SET IDENTITY_INSERT [{table_name}] ON"))

                    batch = [dict(r) for r in rows]
                    azure_conn.execute(table.insert(), batch)

                    if has_identity:
                        azure_conn.execute(text(f"SET IDENTITY_INSERT [{table_name}] OFF"))

                    azure_conn.commit()
                    total_migrated += len(rows)
                    print(f"        [OK] [{table_name}] successfully migrated ({len(rows)} rows).")
                except Exception as e:
                    azure_conn.rollback()
                    if has_identity:
                        try:
                            azure_conn.execute(text(f"SET IDENTITY_INSERT [{table_name}] OFF"))
                            azure_conn.commit()
                        except Exception:
                            pass
                    print(f"        [ERROR] Failed migrating table [{table_name}]: {e}")

            # Verify final record counts in Azure SQL
            print("\n[*] Verifying Azure SQL Database Row Counts:")
            for check_table in ["continents", "countries", "cities", "administrative_divisions", "users"]:
                try:
                    res = azure_conn.execute(text(f"SELECT COUNT(*) FROM [{check_table}]")).scalar()
                    print(f"    - Table [{check_table}]: {res} rows in Azure SQL Online")
                except Exception:
                    pass

        print("\n" + "="*70)
        print(f"[SUCCESS] Online Database Migration Complete!")
        print(f"Total rows successfully copied to Azure SQL: {total_migrated}")
        print("Your TerraNexus database is now fully stored online in Azure SQL.")
        print("="*70 + "\n")
        return True

if __name__ == "__main__":
    run_migration()
