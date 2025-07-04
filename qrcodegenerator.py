import segno

def get_qrcode(url):
# output = io.BytesIO()

# qr.to_artistic(
#     background='',
#     target=output,
#     scale=4,
#     kind='gif'
# )
    return segno.make(url).svg_data_uri()
