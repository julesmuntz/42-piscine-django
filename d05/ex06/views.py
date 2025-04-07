from django.shortcuts import render
from ex00.views import get_db_connection


def update(request, table_name, page_title):
    messages = []
    titles = []
    current_opening_crawl = ""
    selected_title = ""
    created = ""
    updated = ""

    try:
        if request.method == "POST":
            title_to_update = request.POST.get("title")
            new_opening_crawl = request.POST.get("opening_crawl")

            if title_to_update and new_opening_crawl is not None:
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
                selected_title = title_to_update

        # Get list of all titles
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT title FROM {table_name} ORDER BY episode_nb;")
            titles = [row[0] for row in cur.fetchall()]

            # Get current opening crawl if a title is selected
            if request.method == "GET" and titles:
                selected_title = request.GET.get("title", titles[0])

            if selected_title:
                if table_name == "ex06_movies":
                    cur.execute(
                        f"SELECT opening_crawl, created, updated FROM {table_name} WHERE title = %s;",
                        [selected_title],
                    )
                    result = cur.fetchone()
                    if result:
                        current_opening_crawl = result[0] or ""
                        created = result[1]
                        updated = result[2]
                else:
                    cur.execute(
                        f"SELECT opening_crawl FROM {table_name} WHERE title = %s;",
                        [selected_title],
                    )
                    result = cur.fetchone()
                    if result and result[0]:
                        current_opening_crawl = result[0]

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
            "selected_title": selected_title,
            "current_opening_crawl": current_opening_crawl,
            "created": created,
            "updated": updated,
            "table_name": table_name,
        },
    )
