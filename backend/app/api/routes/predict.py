"""
POST /predict: fraud detection inference.
Request: transaction features (V1..V28, Amount).
Response: fraud_probability, is_fraud.
"""
from __future__ import annotations

from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import get_model
from app.core.config import settings

FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)] + ["Amount"]

router = APIRouter(prefix="/predict", tags=["predict"])


# Schema matches Credit Card Fraud dataset features (V1-V28, Amount)
class PredictRequest(BaseModel):
    """Transaction features for fraud prediction."""

    V1: float = Field(..., description="PCA component 1")
    V2: float = Field(..., description="PCA component 2")
    V3: float = Field(..., description="PCA component 3")
    V4: float = Field(..., description="PCA component 4")
    V5: float = Field(..., description="PCA component 5")
    V6: float = Field(..., description="PCA component 6")
    V7: float = Field(..., description="PCA component 7")
    V8: float = Field(..., description="PCA component 8")
    V9: float = Field(..., description="PCA component 9")
    V10: float = Field(..., description="PCA component 10")
    V11: float = Field(..., description="PCA component 11")
    V12: float = Field(..., description="PCA component 12")
    V13: float = Field(..., description="PCA component 13")
    V14: float = Field(..., description="PCA component 14")
    V15: float = Field(..., description="PCA component 15")
    V16: float = Field(..., description="PCA component 16")
    V17: float = Field(..., description="PCA component 17")
    V18: float = Field(..., description="PCA component 18")
    V19: float = Field(..., description="PCA component 19")
    V20: float = Field(..., description="PCA component 20")
    V21: float = Field(..., description="PCA component 21")
    V22: float = Field(..., description="PCA component 22")
    V23: float = Field(..., description="PCA component 23")
    V24: float = Field(..., description="PCA component 24")
    V25: float = Field(..., description="PCA component 25")
    V26: float = Field(..., description="PCA component 26")
    V27: float = Field(..., description="PCA component 27")
    V28: float = Field(..., description="PCA component 28")
    Amount: float = Field(..., ge=0, description="Transaction amount")

    def to_feature_vector(self) -> list[float]:
        """Ordered list of features for the model."""
        return [
            self.V1, self.V2, self.V3, self.V4, self.V5, self.V6, self.V7, self.V8,
            self.V9, self.V10, self.V11, self.V12, self.V13, self.V14, self.V15, self.V16,
            self.V17, self.V18, self.V19, self.V20, self.V21, self.V22, self.V23, self.V24,
            self.V25, self.V26, self.V27, self.V28, self.Amount,
        ]


class PredictResponse(BaseModel):
    """Fraud prediction result."""

    fraud_probability: float = Field(..., ge=0, le=1, description="Probability of fraud (0-1)")
    is_fraud: bool = Field(..., description="True if predicted as fraud (threshold 0.5)")


@router.post(
    "",
    response_model=PredictResponse,
    summary="Predict fraud probability",
    description="Run inference on transaction features (V1-V28, Amount). Returns fraud probability and binary label.",
)
def predict(body: PredictRequest) -> PredictResponse:
    model = get_model()
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Ensure model exists at " + settings.MODEL_PATH,
        )
    try:
        X = pd.DataFrame([body.to_feature_vector()], columns=FEATURE_COLUMNS)
        proba = model.predict_proba(X)[0]
        # Class 1 = fraud
        fraud_prob = float(proba[1]) if proba.shape[0] > 1 else 0.0
        return PredictResponse(
            fraud_probability=round(fraud_prob, 6),
            is_fraud=fraud_prob >= 0.5,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Inference error: {e!s}") from e
