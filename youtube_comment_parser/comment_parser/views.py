from django.shortcuts import render
from .script_parse.parse_comments import parse_comment
from .script_parse.processing_comments import result_classifity

def index(request):
    if request.method == 'POST':
        url = request.POST['url']
        error = parse_comment(url)
        result = result_classifity(error)
        context = {'angry': result[0], 'good': result[1], 'bad': result[2], 'neutral': result[3], 'error': error}
        return render(request, 'index.html', context=context)
    return render(request, 'index.html')
