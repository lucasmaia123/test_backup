from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import psycopg2
import datetime

conn = psycopg2.connect(database='postgres', user='postgres', 
                        host='localhost',
                        port='5432', password='282904')
cursor = conn.cursor()

def index(request):
    try:
        user = request.session['user']
        return render(request, 'user.html', {'user': user})
    except:
        pass
    return render(request, 'index.html')

def signup(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    query = '''SELECT login FROM users;'''
    cursor.execute(query)
    res = cursor.fetchall()
    if user in [res[i][0] for i in range(len(res))]:
        return render(request, 'index.html', {'msg': 'Usuário já existe!'})
    query = f'''INSERT INTO users VALUES ('{user}', '{password}');'''
    cursor.execute(query)
    conn.commit()
    return render(request, 'index.html', {'msg': 'Novo usuário criado com êxito!'})
    
def login(request):
    user = request.POST.get('login')
    password = request.POST.get('password')
    query = f'''SELECT password FROM users WHERE login = '{user}';'''
    cursor.execute(query)
    res = cursor.fetchall()
    try:
        if password == res[0][0]:
            request.session['user'] = user
            return render(request, 'user.html', {'user': user})
    except:
        pass
    return render(request, 'index.html', {'msg': 'Credenciais inválidas!'})

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return HttpResponseRedirect(reverse('myapp:homepage'))

def new_post(request):
    desc = request.POST.get('desc')
    message = request.POST.get('message')
    try:
        user = request.session['user']
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f'''INSERT INTO posts VALUES (DEFAULT, '{user}', '{desc}', '{date}', '{message}');'''
        cursor.execute(query)
        conn.commit()
    except:
        return render(request, 'user.html', context={'user': user, 'msg': 'Algo deu errado!'})
    return render(request, 'user.html', context={'user': user, 'msg': 'Novo post criado com sucesso!'})

def list_posts(request):
    try:
        user = request.session['user']
        query = f'''SELECT id, date, description FROM posts WHERE user_login = '{user}';'''
        cursor.execute(query)
        res = cursor.fetchall()
        posts = []
        for post in res:
            post = list(post)
            post[1] = post[1].strftime('%Y-%m-%d %H:%M:%S')
            posts.append(post)
    except:
        return render(request, 'user.html', context={'user': user, 'msg': f'usuário: {user}'})
    return render(request, 'list_posts.html', context={'user': user, 'posts': posts})

def check_post(request, key):
    try:
        query = f'''SELECT description, date, load FROM posts WHERE id={key};'''
        cursor.execute(query)
        res = cursor.fetchall()
        res = list(res[0])
        user = request.session['user']
    except:
        return render(request, 'user.html', context={'user': user, 'msg': 'Out of bounds!'})
    return render(request, 'check_post.html', context={'user': user, 'id': key, 'desc': res[0], 'date': res[1], 'load': res[2]})

def delete_post(request, key):
    try:
        query = f'''DELETE FROM posts WHERE id={key};'''
        cursor.execute(query)
        conn.commit()
    except:
        return render(request, 'list_posts.html', {'msg': 'Algo deu errado!'})
    return HttpResponseRedirect(reverse('myapp:list_posts'))
