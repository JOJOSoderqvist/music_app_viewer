from django.shortcuts import render
from django.db import connection


# Create your views here.
def index(request):
    query_result = None
    if request.method == "POST":
        query = request.POST.get("query", "")
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                query_result = cursor.fetchall()
                column_headers = [col[0] for col in cursor.description]
        except Exception as e:  # Handle exceptions for errors in SQL or connection issues
            query_result = []
            column_headers = []
            print("Error executing query:", e)

    return render(request, 'index.html', {'query_result': query_result, 'column_headers': column_headers})
