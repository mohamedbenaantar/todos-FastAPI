from fastapi import FastAPI, Body

app = FastAPI()

Books = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'Drama'},
    {'title': 'Title Four', 'author': 'Author Two', 'category': 'Action'},
]
@app.get("/books/")
async def get_books():
    return Books

@app.get("/books/mybook")
async def read_all_books():
    return {'title': 'My_fav_book'}


# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_params': dynamic_param}

### Path parameter
@app.get("/books/{book_title}")
async def read_book_title(book_title: str):
    for book in Books:
        if book_title.casefold() == book.get('title').casefold():
            return book
        
# @app.get("/books/")
# async def read_book_category(category: str):
#     books_to_return = []
#     for book in Books:
#         if book.get('category').casefold() == category.casefold():
#             books_to_return.append(book)
#     return books_to_return

        
@app.get("/books/{dynamic_author}/")
async def read_book_for_author(dynamic_author: str, category: str):
    books_to_return = []
    for book in Books:
        if book.get('author').casefold() == dynamic_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return
        

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    Books.append(new_book)
    
    
@app.put("/books/update_book")
async def update_book_one(updated_book=Body()):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == updated_book.get('title').casefold():
            Books[i] = updated_book
            
            
@app.delete("/books/delete_book/{book_title}")
async def delete_book_by_title(book_title: str):
    for i in range(len(Books)):
        if Books[i].get('title').casefold() == book_title.casefold():
            Books.pop(i)
            break
        
        
@app.get("/books/by_author/{specific_author}")
async def get_books_author(specific_author: str):
    books_author = []
    for i in range(len(Books)):
        if Books[i].get('author').casefold() == specific_author.casefold():
            books_author.append(Books[i])
        else:
            continue
    return books_author