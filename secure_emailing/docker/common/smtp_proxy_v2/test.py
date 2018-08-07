from credentials_emailing import StoreCredentials

st = StoreCredentials()

print st.validate_mailfrom("foo@demo1.com", "demo" ,"demo")