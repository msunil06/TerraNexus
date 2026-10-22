# TerraNexus Database Backup & Disaster Recovery Guide

---

## 1. Automated MySQL Backups

To perform an atomic, consistent backup of the `terranexus_db` database using `mysqldump`:

```bash
mysqldump -u terranexus_user -p \
  --single-transaction \
  --quick \
  --routines \
  --triggers \
  terranexus_db > backup_terranexus_$(date +%Y%m%d_%H%M%S).sql
```

Compress the backup:

```bash
gzip backup_terranexus_*.sql
```

### Automated Cron Job Example

Add to crontab (`crontab -e`) to perform daily backups at 02:00 UTC:

```cron
0 2 * * * /usr/bin/mysqldump -u terranexus_user -pStrongPassword123! --single-transaction terranexus_db | gzip > /var/backups/terranexus/db_$(date +\%F).sql.gz
```

---

## 2. Disaster Recovery & Restoration

To restore a database snapshot into a fresh or existing MySQL instance:

```bash
# Decompress if archived
gunzip backup_terranexus_2026-10-22.sql.gz

# Recreate database and import
mysql -u root -p -e "DROP DATABASE IF EXISTS terranexus_db; CREATE DATABASE terranexus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u terranexus_user -p terranexus_db < backup_terranexus_2026-10-22.sql
```
