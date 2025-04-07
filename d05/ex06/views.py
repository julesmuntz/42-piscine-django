from django.shortcuts import render
from ex00.views import get_db_connection
from importlib import import_module
from django.utils import timezone


def update(request, table_name, page_title):
    messages = []
    titles = []
    opening_crawl = ""

    try:
        if request.method == "POST":
            title_to_update = request.POST.get("title")
            new_opening_crawl = request.POST.get("opening_crawl")
            if title_to_update and new_opening_crawl is not None:
                if page_title[:3] == "SQL":
                    with get_db_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            f"UPDATE {table_name} SET opening_crawl = %s WHERE title = %s;",
                            [new_opening_crawl, title_to_update],
                        )
                        conn.commit()
                        if cur.rowcount <= 0:
                            messages = ["No data available"]
                        else:
                            messages = ["OK"]
                elif page_title[:3] == "ORM":
                    module = import_module(f"ex{int(table_name[2:4]):02d}.models")
                    Movies = module.Movies
                    try:
                        movie = Movies.objects.get(title=title_to_update)
                        movie.opening_crawl = new_opening_crawl
                        if table_name == "ex07_movies":
                            movie.updated = timezone.now()
                        movie.save()
                        messages = ["OK"]
                    except Movies.DoesNotExist:
                        messages = ["No data available"]

        if page_title[:3] == "SQL":
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT title, opening_crawl FROM {table_name} ORDER BY episode_nb;")
                rows = cur.fetchall()
                titles = [row[0] for row in rows]
                selected_title = request.GET.get("title")
                if selected_title and selected_title in titles:
                    for row in rows:
                        if row[0] == selected_title:
                            opening_crawl = row[1] or ""
                            break
                elif titles:
                    opening_crawl = rows[0][1] or ""

        elif page_title[:3] == "ORM":
            module = import_module(f"ex{int(table_name[2:4]):02d}.models")
            Movies = module.Movies
            movies = Movies.objects.all().order_by("episode_nb")
            titles = [movie.title for movie in movies]

            selected_title = request.GET.get("title")
            if selected_title and selected_title in titles:
                movie = Movies.objects.filter(title=selected_title).first()
                if movie:
                    opening_crawl = movie.opening_crawl or ""
            elif titles:
                opening_crawl = movies.first().opening_crawl or ""

        if not titles:
            messages = ["No data available"]

    except Exception:
        messages = ["No data available"]

    return render(
        request,
        "d05/templates/update.html",
        {
            "title": page_title,
            "label": "update",
            "messages": messages,
            "titles": titles,
            "opening_crawl": opening_crawl,
        },
    )
