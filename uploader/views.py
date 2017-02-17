from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    context = {
        "subtitle": {},
        "text": ""
    }
    if request.method == "GET":
        return render(request, 'uploader/index.html', context)
    if request.method == "POST":
        srt_file = request.FILES['srt_file']
        context["subtitle"], context["text"] = handle_uploaded_file(srt_file, srt_file.name)
        return render(request, 'uploader/index.html', context)


def handle_uploaded_file(file, name):
    print(file)
    with open('temp', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    name = name.replace(".srt", ".js")
    new_file = open("uploader/static/"+name, "w+")
    original_file = open('temp')

    # modify uploaded file
    result = '[\n'
    result_array = []
    count = 0
    line = original_file.readline()
    print(line)
    while line is not '':
        duration = original_file.readline().strip()
        result += '{\n'
        result_array.append({"duration": duration})
        result += f'"duration": "{duration}",\n'

        line1 = original_file.readline().strip()
        line1 = line1.replace("\"", "\\\"")
        result += f'"line1": "{line1}",\n'
        result_array[count][line1] = line1

        line2 = original_file.readline().strip()
        line2 = line2.replace("\"", "\\\"")
        if line2 is not '':
            result += f'"line2": "{line2}"\n'
            result_array[count][line2] = line2
            result += '},\n'
            original_file.readline()
            line = original_file.readline()
            count +=1
        else:
            result += f'"line2": ""\n'
            result += ('},\n')
            line = original_file.readline()
            count +=1
    result += ']\n'
    # print(result)
    print(result_array)
    original_file.close()

    new_file.write(result);
    new_file.close()

    return result_array, result
