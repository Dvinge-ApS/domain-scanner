# main.py
import asyncio
from app.domain_checker import check_domains
from app.db_init import init_db

if __name__ == "__main__":
    init_db()
    asyncio.run(check_domains())