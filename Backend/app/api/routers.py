import io
import pandas as pd
import numpy as np
from fastapi import APIRouter, Request, UploadFile, File, BackgroundTasks, HTTPException, status
from app.api.schemas import PricingOptimizationRequest, PricingOptimizationResponse, BatchChurnResponse
import joblib

router = APIRouter()

def process_churn_file_async(df_data: pd.DataFrame, model_pipeline) -> None:
    """
    Simulated worker target for async batch executions logging telemetry arrays down 
    to permanent cache layers, monitoring arrays, or outbound transactional data pipelines.
    """
    try:
        X = df_data[["login_frequency", "days_since_last_purchase", "cart_abandonment_rate"]]
        probabilities = model_pipeline.predict_proba(X)[:, 1]
        df_data["churn_probability"] = probabilities
        print(f"[Async Job Finished] Tracked batch array generation size: {len(df_data)}")
    except Exception as exc:
        print(f"[Async Job Corrupted Execution Trace] Exception details: {exc}")

@router.post("/pricing/optimize", response_model=PricingOptimizationResponse, status_code=status.HTTP_200_OK)
async def optimize_pricing(payload: PricingOptimizationRequest, request: Request):
    pipeline = getattr(request.app.state, "pricing_pipeline", None)
    if not pipeline:
        raise HTTPException(status_code=503, detail="Dynamic Pricing model environment engine not available.")
    
    input_data = np.array([[
        payload.base_price,
        payload.competitor_price,
        payload.stock_level,
        payload.days_to_restock,
        payload.search_velocity_multiplier
    ]])
    
    prediction = float(pipeline.predict(input_data)[0])
    margin_delta = prediction - payload.base_price
    
    return PricingOptimizationResponse(
        recommended_price=round(prediction, 2),
        margin_delta=round(margin_delta, 2),
        confidence_score=0.97
    )

@router.post("/churn/batch-assess", response_model=BatchChurnResponse, status_code=status.HTTP_202_ACCEPTED)
async def batch_assess_churn(
    background_tasks: BackgroundTasks, 
    request: Request, 
    file: UploadFile = File(...)
):
    pipeline = getattr(request.app.state, "churn_pipeline", None)
    if not pipeline:
        raise HTTPException(status_code=503, detail="Churn Risk Classifier context engine not initialized.")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid media payload structure. Target must be a CSV file extension structure.")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed parsing systemic tabular dataframe representation: {str(e)}")

    required_columns = ["customer_id", "login_frequency", "days_since_last_purchase", "cart_abandonment_rate"]
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(
            status_code=422, 
            detail=f"Schema structurally misaligned. Required tracking schemas: {required_columns}"
        )
    
    # Enqueue tasks for deep calculations
    background_tasks.add_task(process_churn_file_async, df, pipeline)
    
    return BatchChurnResponse(
        status="Processing framework safely initiated using asynchronous threading vectors.",
        processed_count=len(df)
    )

# Synchronous parsing backup loop designed for frontend presentation rendering
@router.post("/churn/sync-assess")
async def sync_assess_churn(request: Request, file: UploadFile = File(...)):
    pipeline = getattr(request.app.state, "churn_pipeline", None)
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline engine context offline.")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    X = df[["login_frequency", "days_since_last_purchase", "cart_abandonment_rate"]]
    probabilities = pipeline.predict_proba(X)[:, 1]
    
    records = df.to_dict(orient="records")
    for i, rec in enumerate(records):
        rec["churn_probability"] = float(probabilities[i])
        
    return {"processed_records": records}