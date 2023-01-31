from fastapi import FastAPI
from schemas.students import Student
from config.db import con
from models.index import students
import pandas as pd
from fastapi.responses import StreamingResponse

tags_metadata = [
    {
        "name": "Insert",
        "description": "Funkce pro uložení dat do databáze.",
    },
    {
        "name": "CSV",
        "description": "Funcke pro stažení všeho z databáze a vytvoření z csv souboru.",
    },
    {
        "name": "Student_delete",
        "description": "Mazání studenta dle jeho id v záznamu.",
    },
    {
        "name": "Student_search",
        "description": "Hledání studenta dle jména. Pomocí klíčových charakterů."
    },
    {
        "name": "Student_id",
        "description": "Vyhledávání studenta dle id ze záznamu."
    }

]
app = FastAPI(openapi_tags=tags_metadata)


@app.get("/csv", tags=["CSV"])
def get_csv_data():
    """
    Práce s csv souborem. Pomocí selectu vemu všechna data z tabulky students.
    Vytvořím DataFrame, kam tyto data vložím pod atributy tabulky se data naskládají a zapíší do csv souboru.
    :return csv:
    """
    context = {
        'data': False
    }
    data = con.execute(students.select())
    context['data'] = data
    df = pd.DataFrame(data)
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )


# insert data
@app.post('/api/students', tags=["Insert"])
async def store(student: Student):
    """
    Jako parametr je Student. Dle schéma vím, co musím přijat, abych mohl zapsat do databáze.
    Získaná data vložím z parametru do dalšího parametru funkce.
    :param student:
    :return success nebo some problem:
    """
    data = con.execute(students.insert().values(
        name=student.name,
        email=student.email,
        age=student.age,
        country=student.country,
    ))
    if data.is_insert:
        return {
            "success": True,
            "msg": "Student Store Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "Some Problem"
        }


# delete data
@app.delete('/api/students/{id}', tags=["Student_delete"])
async def delete(id: int):
    """
    Pomocí id, které dostanu z paramtru se provede select, který dle získaného id smaže záznam z tabulky.
    :param id:
    :return succes nebo problem:
    """
    data = con.execute(students.delete().where(students.c.id == id))
    if data:
        return {
            "success": True,
            "msg": "Student Delete Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "Some Problem"
        }


@app.get('/api/students/{search}', tags=["Student_search"])
async def search(search):
    """
    Pomocí parametru získám klíčové charaktery. Pomocí nich vykonám select.
    Ten pomocí charakterů najde vše, co to obsahuje.
    :param search:
    :return data:
    """
    data = con.execute(students.select().where(students.c.name.like('%' + search + '%'))).fetchall()
    return {
        "success": True,
        "data": data
    }


@app.get('/api/student/{id}', tags=["Student_id"])
async def search(id):
    """
    Dle získaného id provedu select, který získu všechna data za pomocí id a vrátí daný záznam.
    :param id:
    :return data:
    """
    data = con.execute(students.select().where(students.c.id == id)).fetchall()
    return {
        "success": True,
        "data": data
    }
