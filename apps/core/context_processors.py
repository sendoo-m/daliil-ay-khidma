# apps/core/context_processors.py
def language_context(request):
    """Add language info to all templates"""
    lang = request.session.get('django_language', 'ar')
    return {
        'CURRENT_LANGUAGE': lang,
        'IS_ARABIC': lang == 'ar',
        'IS_ENGLISH': lang == 'en',
    }
