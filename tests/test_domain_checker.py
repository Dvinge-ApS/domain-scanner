import pytest
from app.domain_checker import generate_domains, check_domain
from unittest.mock import patch, MagicMock
import whois  # Add this import

def test_generate_domains():
    domains = generate_domains()
    assert len(domains) == 1296 + 36  # 36^2 + 36
    assert all(domain.endswith('.dk') for domain in domains)
    assert 'a.dk' in domains
    assert 'zz.dk' in domains

@pytest.mark.asyncio
async def test_check_domain():
    mock_session = MagicMock()
    
    with patch('app.domain_checker.whois.whois') as mock_whois:
        # Test for an unavailable domain
        mock_whois.return_value.domain_name = 'example.dk'
        domain, is_available = await check_domain(mock_session, 'example.dk')
        assert domain == 'example.dk'
        assert is_available == False

        # Test for an available domain
        mock_whois.side_effect = whois.parser.PywhoisError('Domain not found')
        domain, is_available = await check_domain(mock_session, 'available.dk')
        assert domain == 'available.dk'
        assert is_available == True

        # Test for an error case
        mock_whois.side_effect = Exception('Unexpected error')
        domain, is_available = await check_domain(mock_session, 'error.dk')
        assert domain == 'error.dk'
        assert is_available is None