from mus_inst_recognition.views import FromLocal, ByLink

routes = [
    ('*', '/', FromLocal, 'from_local'),
    ('*', '/by_link', ByLink, 'by_link'),
]