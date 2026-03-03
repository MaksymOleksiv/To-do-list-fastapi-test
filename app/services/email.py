import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from app.core.celery_app import celery_app

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email_async(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject, recipients=[email_to], body=body, subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@celery_app.task
def send_email_task(subject: str, email_to: str, body: str):
    asyncio.run(send_email_async(subject, email_to, body))
