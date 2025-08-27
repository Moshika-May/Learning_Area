urls = [
    "https://example.com",
    "http://example.org",
    "https://secure-site.net",
    "ftp://fileserver.com",
    "http://insecure.net"
]
secure_urls = [] 

# Iterate over each URL in the list
for url in urls:
    # Check if the URL starts with 'https://'
    if url.startswith("https://"):
        secure_urls.append(url)

print("Secure URLs:", secure_urls)  
