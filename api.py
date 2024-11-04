from google_images_search import GoogleImagesSearch
import creds

gis = GoogleImagesSearch(creds.api, creds.cx)

def get_img(query, count):
    gis.search(search_params= {
        'q': query,
        'safe': 'active',
        'num': count,
    })
    if count == 1:
        return gis.results()[0].url
    else:
        results = ""
        response = gis.results()
        for result in response:
            results += f"{result.url}\n"
        return results