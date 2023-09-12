from django.shortcuts import render
from myApp.models import Song


# Create your views here.
def index_search(request):
    if request.method == "GET":
        list = Song.objects.all()
        context = {"songs_list": list}
        return render(request, "myApp/1.html", context)
    else:
        list = []
        name_name = request.POST.get('dname')
        # 按照歌名匹配
        list_song_name = []  # 所有歌曲名（字符串列表）
        datalist = Song.objects.all()
        for obj in datalist:  # obj为所有对象
            list_song_name.append(obj.song_name)
            if name_name is not None and name_name in obj.song_name and obj not in list:
                list.append(obj)

        # 按歌手名匹配
        list_singer = []  # 所有歌曲名（字符串列表）
        datalist = Song.objects.all()
        for obj in datalist:  # obj为所有对象
            list_singer.append(obj.artist)
            if name_name is not None and name_name in obj.artist and obj not in list:
                list.append(obj)

        # 按照歌词匹配
        list_lyrics = []  # 所有歌词（字符串列表）
        datalist = Song.objects.all()
        for obj in datalist:  # obj为所有对象
            list_lyrics.append(obj.lyrics)
            if name_name is not None and name_name in obj.lyrics and obj not in list:
                list.append(obj)

        context = {"songs_list": list}
        return render(request, "myApp/1.html", context)


def index_song(request):
    list = []
    name_name = request.POST.get("1")
    datalist = Song.objects.all()
    for obj in datalist:
        if name_name == obj.song_name:
            return render(request, "myapp/index.html", locals())

    context = {"songs_list": list}
    return render(request, "myApp/index.html", context)
