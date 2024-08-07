from app.models import Domain
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from datetime import datetime

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Domain.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_domain_model(test_db):
    domain = Domain(
        domain_name='test.dk',
        is_available=True,
        last_checked=datetime.now()
    )
    test_db.add(domain)
    test_db.commit()

    retrieved = test_db.query(Domain).filter_by(domain_name='test.dk').first()
    assert retrieved is not None
    assert retrieved.domain_name == 'test.dk'
    assert retrieved.is_available == True