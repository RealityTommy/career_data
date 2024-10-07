import os
import requests
import xml.etree.ElementTree as ET
from fastapi import APIRouter, HTTPException
from requests.auth import HTTPBasicAuth
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import OnetIndustryModel, OnetIndustryCreate, OnetIndustryUpdate

# Initialize the router
router = APIRouter(
    prefix="/v1/onetindustries", tags=["ONET", "Industries", "Version 1"]
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
    """Fetch all industries from ONET API and handle the XML response."""
    url = f"{ONET_API_BASE_URL}/industries"

    try:
        response = requests.get(url, auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD))
        response.raise_for_status()

        # Check if response is XML
        if "xml" in response.headers.get("Content-Type", "").lower():
            return parse_xml_response(response.text)
        else:
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from O*NET (expected XML)",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching industries from O*NET: {e}"
        )


# Helper function to parse XML response from ONET API
def parse_xml_response(xml_content):
    """Parse the XML response and extract industries."""
    industries = []

    try:
        root = ET.fromstring(xml_content)

        for industry in root.findall(".//industry"):
            code = industry.find("code").text
            title = industry.find("title").text
            industries.append({"code": code, "title": title})

        return industries
    except ET.ParseError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to parse XML from O*NET: {e}"
        )


# Endpoint to fetch all industries from ONET API (doesn't save to database)
@router.get("/fetch-onet", response_model=list[OnetIndustryModel])
async def fetch_onet_industries():
    """Fetch all industries from ONET API without saving to the database."""
    industries = fetch_all_industries()
    return industries


# Endpoint to save all industries from ONET API and associate them with the import
@router.post("/save")
async def save_onet_industries():
    """Save all industries from ONET API to the database and associate them with the import."""
    try:
        industries = fetch_all_industries()

        # Create a new entry in the OnetImport table
        import_record = await prisma.onetimport.create(data={})

        for industry in industries:
            industry_data = {
                "title": industry.get("title"),
                "code": industry.get("code"),
            }

            # Check if the industry already exists in the database by its unique code
            existing_industry = await prisma.onetindustry.find_unique(
                where={"code": industry_data["code"]}
            )

            if existing_industry:
                # Associate the existing industry with the current import
                await prisma.onetimport.update(
                    where={
                        "id": import_record.id
                    },  # Corrected: `where` keyword is now properly defined
                    data={"industries": {"connect": [{"id": existing_industry.id}]}},
                )
            else:
                # Create a new industry and associate it with the current import
                new_industry = await prisma.onetindustry.create(data=industry_data)
                await prisma.onetimport.update(
                    where={
                        "id": import_record.id
                    },  # Corrected: `where` keyword is now properly defined
                    data={"industries": {"connect": [{"id": new_industry.id}]}},
                )

        return {
            "message": f"Industries saved and associated with import {import_record.id}."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving industries: {str(e)}"
        )


# New Endpoint to get all industries saved in the local database
@router.get("/", response_model=list[OnetIndustryModel])
async def get_saved_industries():
    """Fetch all industries that have been saved to the local database."""
    industries = await prisma.onetindustry.find_many()
    return industries


# Get a specific ONET industry by ID
@router.get("/{industry_id}", response_model=OnetIndustryModel)
async def get_onet_industry(industry_id: str):
    """Fetch a specific ONET industry by its ID."""
    industry = await prisma.onetindustry.find_unique(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="ONET Industry not found")
    return industry


# Update an industry by ID
@router.put("/{industry_id}", response_model=OnetIndustryModel)
async def update_onet_industry(industry_id: str, industry_data: OnetIndustryUpdate):
    """Update an existing ONET industry record."""
    industry = await prisma.onetindustry.update(
        where={"id": industry_id},
        data=industry_data.dict(exclude_unset=True),
    )
    if not industry:
        raise HTTPException(status_code=404, detail="ONET Industry not found")
    return industry


# Delete a specific ONET industry by ID
@router.delete("/{industry_id}")
async def delete_onet_industry(industry_id: str):
    """Delete an ONET industry record by its ID."""
    industry = await prisma.onetindustry.delete(where={"id": industry_id})
    if not industry:
        raise HTTPException(status_code=404, detail="ONET Industry not found")
    return {"message": f"Industry {industry_id} deleted successfully."}


# Delete all ONET industries
@router.delete("/")
async def delete_all_onet_industries():
    """Delete all ONET industries from the system."""
    await prisma.onetindustry.delete_many()
    return {"message": "All ONET industries deleted successfully."}
