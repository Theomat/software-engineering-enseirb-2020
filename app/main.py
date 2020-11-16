from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse

import spacy


app = FastAPI()
model = spacy.load('/app/model')


class IntentProbs(BaseModel):
    find_train: float = Field(..., alias='find-train')
    irrelevant: float = Field(..., alias='irrelevant')
    find_flight: float = Field(..., alias='find-flight')
    find_restaurant: float = Field(..., alias='find-restaurant')
    purchase: float = Field(..., alias='purchase')
    find_around_me: float = Field(..., alias='find-around-me')
    provide_showtimes: float = Field(..., alias='provide-showtimes')
    find_hotel: float = Field(..., alias='find-hotel')

    class Config:
        schema_extra = {
            "example": {
                "find-train": 0.06405537575483322,
                "irrelevant": 0.2867065966129303,
                "find-flight": 0.05505348742008209,
                "find-restaurant": 0.12349507212638855,
                "purchase": 0.18044070899486542,
                "find-around-me": 0.1441631019115448,
                "provide-showtimes": 0.05473391339182854,
                "find-hotel": 0.09135178476572037
            }
        }


@app.get("/")
def root():
    return RedirectResponse(url='/docs')


@app.get("/api/intent", response_model=IntentProbs)
def get_intent(sentence: str = None):
    if sentence is None or sentence == '':
        raise HTTPException(status_code=422,
                            detail="Please use a non empty sentence using the 'sentence' query. use /docs for help")
    return model(sentence).cats
