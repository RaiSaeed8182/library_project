from datetime import datetime


def log_user_signup(user_email: str, user_id: int):
    """
    Yeh function background mein chalega.
    User signup ka record file mein save karta hai.
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] New signup: id={user_id}, email={user_email}\n"
    
    with open("audit_log.txt", "a") as f:
        f.write(log_entry)
    
    print(f"✅ Audit logged: {user_email}")