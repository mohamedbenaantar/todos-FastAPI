from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(title="Id is not needed!")
    title: str = Field(min_length=3)
    author: str = Field(min_length=2, max_length=100)
    # description: str = Field(gt=0, lt=12) Unsupported for str
    description: str = Field(min_length=10)
    rating: int = Field(gt=0, lt=5)
    published_date: int = Field(gt=1999, lt=2030)
    
    class Config: ## Example Values
        json_schema_extra = {
            'example': {
                "title": "BOOK-A",
                "author": "Smith",
                "description": "A new description of a Book A",
                "rating": 1,
                "published_date": 2029
            }            
        }     
        
Books = [
    Book(1, "Mystery Box", "John Week", "This is all about John",4, 2029),
    Book(2, "WWE Event", "John Cena", "This is from mbc action",3, 2028),
    Book(3, "Driver", "Jemmy Orteta", "This is a funny movie",5, 2025)
]


    
# @app.post("/books/create_book")
# async def create_book(new_book=Body()): ## no validation
#     Books.append(new_book)
    

@app.get("/books/",  tags=["All Books"], operation_id="read_all_books")
async def read_all_books():
    return Books

########################

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_a_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(404, "Book cannot be found")
        
##########################

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(404, "Cannot delete unexisting book")

##########################
      
@app.get("/books/",  tags=["All Books"], operation_id="read_all_books_rating")
async def read_book_by_rating(book_rating: int):
    books_return = []
    for book in Books:
        if book.rating == book_rating:
            books_return.append(book)
    return books_return
 
############################

   
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_publish(published_date: int = Query(gt=1999, lt=2030)):
    books_to_return = []
    for book in Books:
        if book.published_date == published_date:
            books_to_return.append(book)
    books_to_return
    
#############################


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest): ## no validation
     ## Object from class BookRequest
    book_convert = Book(**new_book.model_dump())
    
    Books.append(find_book_id(book_convert))
    
def find_book_id(book: Book):
    if len(Books) > 0:
        book.id =Books[-1].id + 1
    else:
        book.id = 1
    return book
      
###########################


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(404, "Cannot updated unexisting Item")
            
############################
         
