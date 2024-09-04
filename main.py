from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO)

def convert_object_ids(data):
    if isinstance(data, dict):
        return {key: convert_object_ids(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PipelineRequest(BaseModel):
    pipeline: list

client = MongoClient('mongodb://localhost:27017/')
db = client['docs']
collection = db['collection']

@app.get("/")
async def root():
    return {"message": "MongoDB connected"}

@app.post("/docs/")
async def execute_pipeline(request: PipelineRequest):
    try:
        pipeline = request.pipeline
        result = list(collection.aggregate(pipeline))
        result = convert_object_ids(result) 
        return {"result": result}
    except Exception as e:
        logging.error(f"Error executing pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-pipeline/")
async def test_pipeline():
    try:
        pipeline = [
            { "$project": { "data.category": 1, "data.time_created": 1 } }
        ]
        result = list(collection.aggregate(pipeline))
        result = convert_object_ids(result)
        return {"result": result}
    except Exception as e:
        logging.error(f"Error testing pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/aggregate/")
async def aggregate_data(pipeline: PipelineRequest):
    try:
        stages = pipeline.pipeline
        result = list(collection.aggregate(stages))
        result = convert_object_ids(result)
        return {"result": result}
    except Exception as e:
        logging.error(f"Error executing aggregation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
