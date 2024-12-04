from django.http import HttpRequest, JsonResponse

#-Function to get routes-#
def get_route(request: HttpRequest):

    #-List of API routes-#
    routes = [
        "GET /api",
        "GET /api/threads",
        "GET /api/thread/:id"]

    #-Returning a JSON Response-#
    return JsonResponse(routes, safe = False)
