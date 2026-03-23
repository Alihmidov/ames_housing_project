from pydantic import BaseModel, Field

class HouseInput(BaseModel):
    total_living_area: float
    overall_qual: int
    gr_liv_area: float
    exter_qual: float
    kitchen_qual: float
    total_bathrooms: float
    year_built: int
    bsmt_qual: float
    house_age: int
    fireplace_qu: float
    fireplaces: int
    overall_cond: int
    garage_cars: float
    lot_area: float
    garage_cond: float
    garage_area: float

    # We use aliases here to match the specific column names used during model training
    # This allows the API to accept lowercase but handle uppercase internally
    central_air_n: str = Field(alias="central_air_N")
    bsmt_fin_sf_1: float
    heating_qc: float
    central_air_y: str = Field(alias="central_air_Y")

    class Config:
        # This setting allows the model to be populated using both the field names and aliases
        populate_by_name = True

class PredictionOutput(BaseModel):
    # Standard output format for the price prediction
    estimated_price: float
    currency: str = "USD"
    message: str = "Prediction successful"