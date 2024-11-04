from google_images_search import GoogleImagesSearch
import creds

gis = GoogleImagesSearch(creds.api, creds.cx)

def get_img(query):
    gis.search(search_params= {
        'q': query,
        'safe': 'active',
        'num': 1,
    })
    return gis.results()[0].url