#It should be registered after session middleware
from pet.main.models import PetPhoto


def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count = request.session.get('clicks_count', 0)
        clicks_count += 1
        request.session['clicks_count'] = clicks_count
        #in order to exist an easier path to click_count(not through session)
        request.clicks_count = clicks_count
        return get_response(request)
    return middleware

def last_viewed_pet_photos_middleware(get_response):
    def middleware(request):
        pet_photo_ids = request.session.get('last_viewed_pet_photo_ids', [])
        pets = PetPhoto.objects.filter(id__in=pet_photo_ids)
        request.last_viewed_pet_photos = pets
        return get_response(request)

    return middleware

