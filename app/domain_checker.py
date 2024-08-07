# app/domain_checker.py
import asyncio
import aiohttp
import whois
from sqlalchemy import update
from app.models import Domain
from app.database import get_db
from app.config import Config
import string
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_domains():
    characters = string.ascii_lowercase + string.digits
    return [f"{char}.dk" for char in characters] + [f"{char1}{char2}.dk" for char1 in characters for char2 in characters]

async def check_domain(session, domain):
    try:
        whois_info = whois.whois(domain)
        is_available = not bool(whois_info.domain_name)
    except whois.parser.PywhoisError:
        is_available = True
    except Exception as e:
        logger.error(f"Error checking domain {domain}: {str(e)}")
        is_available = None
    return domain, is_available

async def check_domains():
    domains = generate_domains()
    logger.info(f"Checking {len(domains)} .dk domains")
    
    queries_per_hour = 0
    hour_start = time.time()
    
    async with aiohttp.ClientSession() as session:
        while True:
            for i in range(0, len(domains), Config.BATCH_SIZE):
                batch = domains[i:i+Config.BATCH_SIZE]
                tasks = [check_domain(session, domain) for domain in batch]
                results = await asyncio.gather(*tasks)
                
                db = next(get_db())
                for domain, is_available in results:
                    if is_available is not None:
                        stmt = update(Domain).where(Domain.domain_name == domain).values(
                            is_available=is_available,
                            last_checked=datetime.now()
                        ).returning(Domain.id)
                        
                        result = db.execute(stmt)
                        if result.rowcount == 0:
                            new_domain = Domain(domain_name=domain, is_available=is_available, last_checked=datetime.now())
                            db.add(new_domain)
                        
                        logger.info(f"Checked domain: {domain}, Available: {is_available}")
                
                db.commit()
                
                queries_per_hour += Config.BATCH_SIZE
                if queries_per_hour >= Config.HOURLY_LIMIT:
                    time_elapsed = time.time() - hour_start
                    if time_elapsed < 3600:
                        sleep_time = 3600 - time_elapsed
                        logger.info(f"Reached query limit. Sleeping for {sleep_time:.2f} seconds")
                        await asyncio.sleep(sleep_time)
                    queries_per_hour = 0
                    hour_start = time.time()
                
                await asyncio.sleep(Config.QUERY_DELAY)
            
            logger.info("Completed checking all domains. Starting over.")

if __name__ == "__main__":
    asyncio.run(check_domains())