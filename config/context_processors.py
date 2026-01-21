def query_params(request):
    return {"q": (request.GET.get("q") or "").strip()}
