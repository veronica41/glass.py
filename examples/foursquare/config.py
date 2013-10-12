# Application
HOST = "vm012.elijah.cs.cmu.edu"
PORT = 8080 

# Google
GOOGLE_CLIENT_ID = "345475634573-b5atfg97ucp9tt4t9qbn7atmm3ejn65t.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "_jLcnxY5opFt6br_bVHBrdfx"
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/glass.location',
    'https://www.googleapis.com/auth/glass.timeline',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Foursquare
FOURSQUARE_CLIENT_ID = "2RTUERQPW4YJBVWF4SF1Y3XBTAU2GN13AYDOYBYEDHYO2MWC"
FOURSQUARE_CLIENT_SECRET = "TWBJDKTLGZOFNSZJZZMNTVXDYFWXBCBSVZEOILPBYCKW2BEX"
FOURSQUARE_CLIENT_REDIRECT = "https://%s:%i/foursquare/callback" % (HOST, PORT)
