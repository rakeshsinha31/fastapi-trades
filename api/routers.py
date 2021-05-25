from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from .models import Trade, TradeDetails

router = APIRouter()


@router.post("/tradeDetails", response_description="Add new trade details")
def create_trade_details(request: Request, tradeDetails: TradeDetails = Body(...)):
    trade_details = jsonable_encoder(tradeDetails)
    details = request.app.mongodb["tradedetails"].insert_one(trade_details)
    created_trade_details = request.app.mongodb["tradedetails"].find_one(
        {"_id": details.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_trade_details)


@router.post("/", response_description="Add new trade")
def create_trade(request: Request, trade: Trade = Body(...)):
    trade_json = jsonable_encoder(trade)
    new_trade = request.app.mongodb["trade"].insert_one(trade_json)
    created_trade = request.app.mongodb["trade"].find_one(
        {"_id": new_trade.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_trade)


@router.get("/", response_description="List all trades")
def trades(
    request: Request,
    assetClass: str,
    end: str,
    start: str,
    maxPrice: str,
    minPrice: str,
    tradeType: str
) -> list:
    trade_details_list = []
    trade_list = []
    for trade in request.app.mongodb["trade"].find({
        "assetClass": {"eq": assetClass},
        "tradeDateTime": {"lte": datetime.strptime(end)},
        "tradeDateTime": {"gte": datetime.strptime(start)},
    }):

        trade_list.append(trade)
    print(trade_list)

    for trade_details in request.app.mongodb["tradedetails"].find({
        "price": {"gte": minPrice, "lte": maxPrice},
        "buySellIndicator": {"eq": tradeType},
    }):
        trade_details_list.append(trade_details)

    print(trade_details_list)

    trades = request.app.mongodb["trade"].find({
        {"_id": {"in": trade_details_list}}
    })

    print(trades)

    return trade_list


@router.get("/{id}", response_description="Get a single trade")
def get_trade(request: Request, id: str):
    if (trade := request.app.mongodb["trade"].find_one({"_id": id})) is not None:
        return trade
