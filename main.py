from fastapi import FastAPI, Query, Body
import uvicorn



app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
     {"id": 2, "title": "Дубай", 'name': "dubai"}
]


@app.get("/")
def home():
    return "Helloo"


@app.post("/hotels/")
def create_hotel(
    title: str = Body(embed=True),
):
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
        }
    )
    return hotels

@app.get('/hotels')
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля")
):  
    hotels_ = []
    
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        
        hotels_.append(hotel)
        
    return hotels_

def from_tuple_to_str(tup: tuple) -> str:
    return str(tup)

@app.put("/hotels/{hotel_id}")
def put_hotels(
    hotel_id: int,
    title: str = Body(),
    name: str = Body(),
):
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        hotel["title"] = from_tuple_to_str(title)
        hotel['name'] = name
    return {"message": "Изменения применены"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    name: str | None = Body(None),
):
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        for k,v in hotel.items(): 
            if k == "title" and title is not None:
                hotel["title"] = title
            if k == "name" and name is not None:
                hotel["name"] = name
            
    return hotels   
        
        
    


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Ok"}
        
        


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)