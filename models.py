from pydantic import BaseModel, ValidationError, validator

BEELINE = "BEELINE"
RTK = "ROSTELECOM"

PROVIDERS = [BEELINE, RTK]


# TODO Validation to provider
class Mapping(BaseModel):
    phone: str
    iccid: str
    provider: str

    @validator('phone')
    def valid_phone(cls, phone: str) -> str:
        if not phone.isdigit():
            raise ValueError(
                f'{phone} - Contains more than not numbers or empty field.')
        if 9 < len(phone) > 11:
            raise ValueError(f'{phone} - Incorrect length phone.')
        if len(phone) == 11 and phone[0] != '7':
            raise ValueError(f'{phone} - The phone should start at 7.')
        if len(phone) == 10:
            return '7' + phone
        return phone

    @validator('iccid')
    def valid_iccid(cls, iccid: str) -> str:
        if not iccid.isdigit():
            raise ValueError(
                f'{iccid} - Contains more than not numbers or empty field.')
        if 18 < len(iccid) > 20:
            raise ValueError(f'{iccid} - Incorrect length iccid')
        return iccid

    @validator('provider')
    def valid_provider(cls, provider: str) -> str:
        if provider not in PROVIDERS:
            raise ValueError(f'{provider} - Incorrect provider')
        return provider
