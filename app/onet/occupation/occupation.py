import os
import requests
from fastapi import APIRouter, HTTPException
from requests.auth import HTTPBasicAuth
from app.prisma import prisma, connect_prisma, disconnect_prisma
from .schema import OnetOccupationAPISchema, OnetOccupationModel

# Initialize the router
router = APIRouter(
    prefix="/v1/onetoccupations", tags=["ONET", "Occupations", "Version 1"]
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


# Helper function to fetch occupations from ONET API and handle pagination
def fetch_all_occupations():
    """Fetch all occupations from ONET API with pagination."""
    url = f"{ONET_API_BASE_URL}/occupations"
    occupations = []
    page = 1
    page_size = 20  # ONET returns 20 results by default

    try:
        while True:
            # Add pagination parameters to the request
            response = requests.get(
                url,
                params={"start": (page - 1) * page_size + 1, "end": page * page_size},
                auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
            )
            response.raise_for_status()

            if "xml" in response.headers.get("Content-Type", "").lower():
                import xml.etree.ElementTree as ET

                root = ET.fromstring(response.content)

                # Extract occupations
                occupations_on_page = []
                for occupation in root.findall(".//occupation"):
                    code = occupation.find("code").text
                    title = occupation.find("title").text
                    occupations_on_page.append({"code": code, "title": title})

                # If no more occupations are returned, break the loop
                if not occupations_on_page:
                    break

                occupations.extend(occupations_on_page)

                # Check if fewer occupations were returned than the page size, indicating the last page
                if len(occupations_on_page) < page_size:
                    break

                page += 1  # Move to the next page

            else:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid response format from O*NET (expected XML)",
                )

        return occupations

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching occupations from ONET: {e}"
        )


# Endpoint to fetch occupations from ONET API (doesn't save to database)
@router.get("/fetch", response_model=list[OnetOccupationAPISchema])
async def fetch_onet_occupations():
    """Fetch occupations from ONET API without saving to the database."""
    occupations = fetch_all_occupations()
    return occupations


@router.post("/save")
async def save_onet_occupations():
    """Fetch all occupations from ONET API and save them to the local database, associating them with a new import record."""
    try:
        occupations = fetch_all_occupations()

        # Create a new OnetImport record
        import_record = await prisma.onetimport.create(data={})

        for occupation in occupations:
            # Check if the occupation already exists in the database by its unique code
            existing_occupation = await prisma.onetoccupation.find_unique(
                where={"code": occupation["code"]}
            )

            if existing_occupation:
                # Associate the existing occupation with the new import
                await prisma.onetimport.update(
                    where={"id": import_record.id},
                    data={"occupations": {"connect": [{"id": existing_occupation.id}]}},
                )
            else:
                # Create a new occupation entry and associate it with the new import
                new_occupation = await prisma.onetoccupation.create(
                    data={"title": occupation["title"], "code": occupation["code"]}
                )
                await prisma.onetimport.update(
                    where={"id": import_record.id},
                    data={"occupations": {"connect": [{"id": new_occupation.id}]}},
                )

        return {
            "message": f"Occupations saved successfully and associated with import {import_record.id}",
            "import_id": import_record.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving occupations: {str(e)}"
        )


# Endpoint to get all occupations saved in the local database
@router.get("/", response_model=list[OnetOccupationModel])
async def get_saved_occupations():
    """Fetch all occupations that have been saved to the local database."""
    occupations = await prisma.onetoccupation.find_many()
    return occupations


# Endpoint to get a specific ONET occupation by ID
@router.get("/{occupation_id}", response_model=OnetOccupationModel)
async def get_onet_occupation(occupation_id: str):
    """Fetch a specific ONET occupation by its ID."""
    occupation = await prisma.onetoccupation.find_unique(where={"id": occupation_id})
    if not occupation:
        raise HTTPException(status_code=404, detail="ONET Occupation not found")
    return occupation


# Endpoint to delete a specific ONET occupation by ID
@router.delete("/{occupation_id}")
async def delete_onet_occupation(occupation_id: str):
    """Delete a specific ONET occupation by its ID."""
    occupation = await prisma.onetoccupation.delete(where={"id": occupation_id})
    if not occupation:
        raise HTTPException(status_code=404, detail="ONET Occupation not found")
    return {"message": f"Occupation {occupation_id} deleted successfully."}


# Endpoint to delete all ONET occupations from the database
@router.delete("/")
async def delete_all_onet_occupations():
    """Delete all ONET occupations from the system."""
    await prisma.onetoccupation.delete_many()
    return {"message": "All ONET occupations deleted successfully."}
