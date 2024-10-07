import os
import requests
from fastapi import APIRouter, HTTPException
from requests.auth import HTTPBasicAuth
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import OnetIndustryAPISchema, OnetIndustryModel
from datetime import datetime

# Initialize the router
router = APIRouter(
    prefix="/v1/onetindustries", tags=["ONET", "ONET Industries", "Version 1"]
)

# ONET API credentials
API_USERNAME = os.getenv("ONET_USERNAME")
API_PASSWORD = os.getenv("ONET_PASSWORD")
ONET_API_BASE_URL = "https://services.onetcenter.org/ws/online"


# Prisma connection and disconnection lifecycle events
@router.on_event("startup")
async def startup():
    await connect_prisma()


@router.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()


# Helper function to fetch industries from ONET API and handle XML response
def fetch_all_industries():
    """Fetch all industries from ONET API."""
    url = f"{ONET_API_BASE_URL}/industries"

    try:
        response = requests.get(url, auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD))
        response.raise_for_status()

        industries = []
        if "xml" in response.headers.get("Content-Type", "").lower():
            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.content)
            for industry in root.findall(".//industry"):
                code = industry.find("code").text
                title = industry.find("title").text
                industries.append({"code": code, "title": title})
        else:
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from O*NET (expected XML)",
            )
        return industries

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching industries from ONET: {e}"
        )


# Endpoint to fetch industries from ONET API (doesn't save to database)
@router.get("/fetch", response_model=list[OnetIndustryAPISchema])
async def fetch_onet_industries():
    """Fetch industries from ONET API without saving to the database."""
    industries = fetch_all_industries()
    return industries


# Endpoint to save all industries from ONET API to the database
@router.post("/save")
async def save_onet_industries():
    """Fetch industries from ONET API and save them to the local database, associating them with a new import record."""
    try:
        industries = fetch_all_industries()

        # Create a new OnetImport record
        import_record = await prisma.onetimport.create(data={})

        for industry in industries:
            # Check if the industry already exists in the database by its unique code
            existing_industry = await prisma.onetindustry.find_unique(
                where={"code": industry["code"]}
            )

            if existing_industry:
                # Associate the existing industry with the new import
                await prisma.onetimport.update(
                    where={"id": import_record.id},
                    data={"industries": {"connect": [{"id": existing_industry.id}]}},
                )
            else:
                # Create a new industry entry and associate it with the new import
                new_industry = await prisma.onetindustry.create(
                    data={"title": industry["title"], "code": industry["code"]}
                )
                await prisma.onetimport.update(
                    where={"id": import_record.id},
                    data={"industries": {"connect": [{"id": new_industry.id}]}},
                )

        return {
            "message": f"Industries saved successfully and associated with import {import_record.id}",
            "import_id": import_record.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving industries: {str(e)}"
        )


# Endpoint to get all industries saved in the local database
@router.get("/", response_model=list[OnetIndustryModel])
async def get_saved_industries():
    """Fetch all industries that have been saved to the local database."""
    industries = await prisma.onetindustry.find_many()
    return industries


# Endpoint to get a specific ONET industry by ID
@router.get("/{industry_id}", response_model=OnetIndustryModel)
async def get_onet_industry(industry_id: str):
    """Fetch a specific ONET industry by its ID."""
    industry = await prisma.onetindustry.find_unique(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="ONET Industry not found")
    return industry


# Endpoint to delete a specific ONET industry by ID
@router.delete("/{industry_id}")
async def delete_onet_industry(industry_id: str):
    """Delete a specific ONET industry by its ID."""
    industry = await prisma.onetindustry.delete(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="ONET Industry not found")
    return {"message": f"Industry {industry_id} deleted successfully."}


# Endpoint to delete all ONET industries from the database
@router.delete("/")
async def delete_all_onet_industries():
    """Delete all ONET industries from the system."""
    await prisma.onetindustry.delete_many()
    return {"message": "All ONET industries deleted successfully."}
